#!/usr/bin/env python3
"""Fetch Oura v2 recovery into health-data.json using only the Python stdlib.

See docs/oura.md for authentication and offline examples. Without --output,
print normalized JSON. --fixtures never reads credentials or uses the network.
"""

import argparse
import copy
from datetime import date, datetime, timedelta, timezone
import http.client
import json
import math
import os
from pathlib import Path
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

API_URL = "https://api.ouraring.com/v2/usercollection/"
TOKEN_URL = "https://api.ouraring.com/oauth/token"
COLLECTIONS = ("daily_readiness", "daily_sleep", "sleep")
REFRESH_SKEW_SECONDS = 300


class OuraError(Exception):
    """A safe, operator-facing failure; never includes tokens or response bodies."""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Do not forward Authorization headers or token POSTs to another URL.
        return None


def request_json(request):
    try:
        with urllib.request.build_opener(NoRedirect).open(request, timeout=20) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        hints = {
            400: "request rejected; check OAuth credentials or date range",
            401: "token invalid or expired; reconnect with /sources",
            403: "check daily scope and active Oura membership",
            429: "rate limited; retry later",
        }
        raise OuraError("HTTP %s: %s" % (
            exc.code, hints.get(exc.code, "Oura request failed; retry later")
        )) from None
    except (OSError, ValueError, http.client.HTTPException):
        raise OuraError("network failure or invalid JSON response; retry later") from None


def read_json(path):
    try:
        with Path(path).open() as source:
            value = json.load(source)
    except (OSError, ValueError):
        raise OuraError("cannot read JSON file; check file permissions and JSON syntax") from None
    if not isinstance(value, dict):
        raise OuraError("JSON file must contain an object")
    return value


def write_json(path, value):
    """Replace a complete file atomically, with private permissions."""
    path = Path(path)
    temporary = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as out:
            temporary = out.name
            json.dump(value, out, indent=2, allow_nan=False)
            out.write("\n")
            out.flush()
            os.fsync(out.fileno())
        os.replace(temporary, path)
    except (OSError, ValueError):
        raise OuraError("cannot write JSON file; check destination permissions") from None
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)


def is_token(value):
    return isinstance(value, str) and bool(value.strip()) and not any(c.isspace() for c in value)


def number(value, field, maximum=None):
    if value is None:
        return None
    if (isinstance(value, bool) or not isinstance(value, (int, float))
            or not math.isfinite(value) or value < 0
            or (maximum is not None and value > maximum)):
        raise OuraError("invalid numeric field: " + field)
    return value


def ensure_access_token(path):
    try:
        credentials = read_json(path)
    except OuraError:
        raise OuraError("cannot read credentials JSON; configure oura.access_token via /sources") from None
    oura = credentials.get("oura")
    if not isinstance(oura, dict):
        raise OuraError("missing oura credentials; run /sources to connect")
    token = oura.get("access_token")
    expires_at = number(oura.get("access_token_expires_at"), "access_token_expires_at")
    # Accept an operator-supplied bearer token, including legacy stored tokens.
    # No promise that Oura still accepts a retired PAT; a 401 requires reconnecting.
    if is_token(token) and expires_at is None and not oura.get("refresh_token"):
        return token
    if is_token(token) and expires_at is not None and expires_at > time.time() + REFRESH_SKEW_SECONDS:
        return token
    keys = ("client_id", "client_secret", "refresh_token")
    if not all(is_token(oura.get(key)) for key in keys):
        raise OuraError("missing oura.access_token or OAuth refresh credentials; run /sources")
    data = {key: oura[key] for key in keys}
    data["grant_type"] = "refresh_token"
    response = request_json(urllib.request.Request(
        TOKEN_URL, data=urllib.parse.urlencode(data).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"}, method="POST",
    ))
    if not isinstance(response, dict) or not all(
        is_token(response.get(key)) for key in ("access_token", "refresh_token")
    ):
        raise OuraError("OAuth response missing access_token or rotated refresh_token; reconnect")
    expires_in = number(response.get("expires_in"), "expires_in")
    if not expires_in:
        raise OuraError("OAuth response missing positive expires_in; reconnect")
    oura.update(access_token=response["access_token"], refresh_token=response["refresh_token"],
                access_token_expires_at=int(time.time() + expires_in))
    # Oura refresh tokens are single-use. Persist rotation before any data GET.
    try:
        write_json(path, credentials)
    except OuraError:
        raise OuraError("cannot persist rotated OAuth credentials; reconnect with /sources") from None
    return oura["access_token"]


def page_data(page):
    if not isinstance(page, dict) or not isinstance(page.get("data"), list):
        raise OuraError("collection response must contain a data array")
    if not all(isinstance(row, dict) for row in page["data"]):
        raise OuraError("collection data must contain objects")
    cursor = page.get("next_token")
    if cursor is not None and not isinstance(cursor, str):
        raise OuraError("invalid pagination cursor")
    return page["data"], cursor


def fetch_collection(name, token, start, end):
    rows, seen = [], set()
    params = {"start_date": start.isoformat(), "end_date": end.isoformat()}
    for _ in range(100):
        request = urllib.request.Request(
            API_URL + name + "?" + urllib.parse.urlencode(params),
            headers={"Authorization": "Bearer " + token, "Accept": "application/json"},
        )
        data, cursor = page_data(request_json(request))
        rows.extend(data)
        if not cursor:
            return rows
        if cursor in seen:
            raise OuraError("repeated pagination cursor")
        seen.add(cursor)
        params["next_token"] = cursor
    raise OuraError("pagination limit exceeded")


def load_fixtures(directory):
    result = {}
    for name in COLLECTIONS:
        rows, cursor = page_data(read_json(Path(directory) / (name + ".json")))
        if cursor:
            raise OuraError("fixtures must contain complete collections (next_token: null)")
        result[name] = rows
    return result


def record_day(row):
    try:
        return date.fromisoformat(row["day"])
    except (KeyError, TypeError, ValueError):
        raise OuraError("collection record missing a valid ISO day") from None


def normalize(collections, start, end):
    """Join by Oura's local day, keeping today's missing measurements null."""
    daily = {}
    for collection in ("daily_readiness", "daily_sleep"):
        by_day = {}
        for row in collections[collection]:
            day = record_day(row)
            if start <= day <= end:
                by_day[day] = number(row.get("score"), collection + ".score", 100)
        daily[collection] = by_day

    nights = {}
    for row in collections["sleep"]:
        day = record_day(row)
        if not start <= day <= end or row.get("type") != "long_sleep":
            continue
        duration = number(row.get("total_sleep_duration"), "total_sleep_duration")
        # Longest main sleep wins; naps/deleted/rest records never replace it.
        rank = (duration or 0, str(row.get("bedtime_end") or ""), str(row.get("id") or ""))
        if day not in nights or rank > nights[day][0]:
            nights[day] = (rank, row)

    def metrics(day):
        sleep = nights.get(day, (None, {}))[1]
        seconds = number(sleep.get("total_sleep_duration"), "total_sleep_duration")
        return {
            "readiness": daily["daily_readiness"].get(day),
            "sleep_score": daily["daily_sleep"].get(day),
            "hrv_ms": number(sleep.get("average_hrv"), "average_hrv"),
            "resting_hr": number(sleep.get("lowest_heart_rate"), "lowest_heart_rate"),
            "sleep_hours": round(seconds / 3600, 2) if seconds is not None else None,
        }

    days = sorted(set(daily["daily_readiness"]) | set(daily["daily_sleep"]) | set(nights))
    trend = []
    for day in days:
        values = metrics(day)
        trend.append({"date": "%s/%s" % (day.month, day.day), **{
            key: values[key] for key in ("readiness", "sleep_score", "hrv_ms")
        }})
    return {"connected": True, "status": "fresh", "today": metrics(end), "trend": trend}


def refresh(credentials, cache, start, end, fixtures=None):
    """Return (merged cache, safe error or None), preserving last good data on failure."""
    result = copy.deepcopy(cache)
    try:
        if fixtures is not None:
            collections = load_fixtures(fixtures)
        else:
            token = ensure_access_token(credentials)
            collections = {name: fetch_collection(name, token, start, end) for name in COLLECTIONS}
        oura = normalize(collections, start, end)
    except OuraError as exc:
        oura = result.get("oura")
        if not isinstance(oura, dict):
            oura = {"connected": True}
            result["oura"] = oura
        oura["status"] = "error"
        return result, str(exc)
    result["oura"] = oura
    result["fetched_at"] = datetime.now(timezone.utc).isoformat()
    return result, None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--credentials", type=Path, default=Path(__file__).with_name("credentials.json"))
    parser.add_argument("--output", type=Path, help="merge into this cache; otherwise print JSON")
    parser.add_argument("--fixtures", type=Path, help="offline directory with three collection JSON files")
    parser.add_argument("--dry-run", action="store_true", help="print result without writing the cache")
    parser.add_argument("--end-date", type=date.fromisoformat, default=date.today(), help="local day YYYY-MM-DD")
    parser.add_argument("--days", type=int, default=30, help="inclusive window length (default: 30)")
    args = parser.parse_args(argv)
    if args.days < 1:
        parser.error("--days must be positive")
    if args.output and args.output.resolve() == args.credentials.resolve():
        parser.error("--output must not overwrite credentials")
    try:
        start = args.end_date - timedelta(days=args.days - 1)
    except (OverflowError, ValueError):
        parser.error("date window is out of range")
    try:
        cache = read_json(args.output) if args.output and args.output.exists() else {}
        result, error = refresh(args.credentials, cache, start, args.end_date, args.fixtures)
        if args.output and not args.dry_run:
            write_json(args.output, result)
        else:
            print(json.dumps(result, indent=2, allow_nan=False))
        if error:
            print("oura: " + error, file=sys.stderr)
            return 1
    except OuraError as exc:
        print("oura: " + str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
