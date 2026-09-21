#!/usr/bin/env python3
"""Mint a valid Strava access token from the stored refresh token.

The Strava token helper in the 1000 Second Method health integration. Strava data
GETs and normalization are done by the agent inline; oura_client.py handles Oura.
This script exists because Strava access tokens expire every
6 hours and the OAuth refresh + token rotation is the one fiddly part worth making
deterministic.

Reads and writes `credentials.json` (default: alongside this script). Prints a
valid Strava access token to stdout. Exits non-zero with a one-line error on
failure so the caller can surface a clear status.

Usage:
    python3 strava_token.py [path/to/credentials.json]

credentials.json shape (the "strava" block):
    {
      "strava": {
        "client_id": "...",
        "client_secret": "...",
        "refresh_token": "...",
        "access_token": "",
        "access_token_expires_at": 0
      }
    }
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

TOKEN_URL = "https://www.strava.com/oauth/token"
# Refresh when the current token has under this many seconds of life left.
REFRESH_SKEW_SECONDS = 300


def _post_token(url, data):
    """POST form-encoded data, return the parsed JSON response."""
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)


def ensure_access_token(path):
    """Return a valid Strava access token, refreshing and persisting if needed."""
    with open(path) as fh:
        creds = json.load(fh)

    strava = creds.get("strava") or {}
    if not strava.get("client_id") or not strava.get("refresh_token"):
        raise SystemExit("strava: missing client_id/refresh_token -- run /sources to connect")

    # Reuse the cached token while it still has comfortable life left.
    expires_at = strava.get("access_token_expires_at", 0)
    if strava.get("access_token") and expires_at - time.time() > REFRESH_SKEW_SECONDS:
        return strava["access_token"]

    try:
        resp = _post_token(TOKEN_URL, {
            "client_id": strava["client_id"],
            "client_secret": strava["client_secret"],
            "grant_type": "refresh_token",
            "refresh_token": strava["refresh_token"],
        })
    except Exception as exc:  # network / auth failure -> clear, non-zero exit
        raise SystemExit("strava: token refresh failed: %s" % exc)

    if "access_token" not in resp:
        raise SystemExit("strava: refresh response missing access_token")

    strava["access_token"] = resp["access_token"]
    strava["access_token_expires_at"] = resp.get("expires_at", int(time.time()) + 21000)
    # Strava rotates refresh tokens -- persist the new one or the next refresh fails.
    if resp.get("refresh_token"):
        strava["refresh_token"] = resp["refresh_token"]

    creds["strava"] = strava
    with open(path, "w") as fh:
        json.dump(creds, fh, indent=2)

    return strava["access_token"]


if __name__ == "__main__":
    cred_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "credentials.json"
    )
    print(ensure_access_token(cred_path))
