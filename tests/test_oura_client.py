"""Offline contract, HTTP, OAuth, and CLI tests; all credentials are synthetic."""

from contextlib import redirect_stderr, redirect_stdout
from datetime import date
import copy
import http.client
import io
import json
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
import urllib.parse
import urllib.request

from docs import oura_client as client

FIXTURES = Path(__file__).parent / "fixtures" / "oura"
START = date(2026, 8, 23)
END = date(2026, 9, 21)


class NormalizationTests(unittest.TestCase):
    def setUp(self):
        self.collections = client.load_fixtures(FIXTURES)

    def test_fixture_contract_sorted_join_and_main_sleep_selection(self):
        expected = client.read_json(FIXTURES / "expected_oura.json")
        self.assertEqual(client.normalize(self.collections, START, END), expected)

    def test_missing_today_is_not_yesterdays_recovery(self):
        result = client.normalize(self.collections, START, date(2026, 9, 22))
        self.assertTrue(all(value is None for value in result["today"].values()))
        self.assertEqual(len(result["trend"]), 3)

    def test_empty_collections_are_successful_but_unknown(self):
        result = client.normalize({key: [] for key in client.COLLECTIONS}, START, END)
        self.assertEqual(result["status"], "fresh")
        self.assertEqual(result["trend"], [])
        self.assertTrue(all(value is None for value in result["today"].values()))

    def test_date_window_and_local_day_not_utc_timestamp(self):
        self.collections["daily_readiness"][0]["timestamp"] = "2026-09-22T01:00:00Z"
        result = client.normalize(self.collections, END, END)
        self.assertEqual([row["date"] for row in result["trend"]], ["9/21"])
        self.assertEqual(result["today"]["readiness"], 82)

    def test_union_of_partial_endpoints_and_year_boundary(self):
        collections = {
            "daily_readiness": [{"day": "2025-12-31", "score": 0}],
            "daily_sleep": [{"day": "2026-01-01", "score": 90}], "sleep": [],
        }
        result = client.normalize(collections, date(2025, 12, 31), date(2026, 1, 1))
        self.assertEqual(result["trend"], [
            {"date": "12/31", "readiness": 0, "sleep_score": None, "hrv_ms": None},
            {"date": "1/1", "readiness": None, "sleep_score": 90, "hrv_ms": None},
        ])

    def test_naps_deleted_and_rest_do_not_supply_overnight_metrics(self):
        for kind in ("sleep", "late_nap", "deleted", "rest", None):
            with self.subTest(kind=kind):
                row = dict(self.collections["sleep"][0], type=kind)
                self.collections["sleep"] = [row]
                self.assertIsNone(client.normalize(self.collections, START, END)["today"]["hrv_ms"])

    def test_missing_duration_and_hrv_remain_null(self):
        row = dict(self.collections["sleep"][0], total_sleep_duration=None, average_hrv=None)
        self.collections["sleep"] = [row]
        today = client.normalize(self.collections, START, END)["today"]
        self.assertIsNone(today["sleep_hours"])
        self.assertIsNone(today["hrv_ms"])

    def test_invalid_values_fail_instead_of_becoming_health_scores(self):
        for value in (True, "82", -1, 101, float("nan"), float("inf")):
            with self.subTest(value=value):
                self.collections["daily_readiness"][0]["score"] = value
                with self.assertRaises(client.OuraError):
                    client.normalize(self.collections, START, END)

    def test_invalid_day_fails(self):
        self.collections["sleep"][0]["day"] = "not-a-day"
        with self.assertRaises(client.OuraError):
            client.normalize(self.collections, START, END)


class TransportTests(unittest.TestCase):
    def test_pagination_keeps_dates_and_sends_bearer_only_in_header(self):
        pages = [{"data": [{"day": "2026-09-20"}], "next_token": "opaque+/="},
                 {"data": [{"day": "2026-09-21"}], "next_token": None}]
        with patch.object(client, "request_json", side_effect=pages) as request:
            rows = client.fetch_collection("daily_readiness", "synthetic-token", START, END)
        self.assertEqual(len(rows), 2)
        for call in request.call_args_list:
            req = call.args[0]
            self.assertEqual(req.get_header("Authorization"), "Bearer synthetic-token")
            self.assertNotIn("synthetic-token", req.full_url)
            query = urllib.parse.parse_qs(urllib.parse.urlsplit(req.full_url).query)
            self.assertEqual(query["start_date"], ["2026-08-23"])
            self.assertEqual(query["end_date"], ["2026-09-21"])
        self.assertEqual(query["next_token"], ["opaque+/="])

    def test_repeated_cursor_and_malformed_pages_fail(self):
        pages = [{"data": [], "next_token": "same"}] * 2
        with patch.object(client, "request_json", side_effect=pages):
            with self.assertRaisesRegex(client.OuraError, "repeated pagination"):
                client.fetch_collection("sleep", "synthetic-token", START, END)
        for page in ({}, {"data": {}}, {"data": [None]}, {"data": [], "next_token": 3}):
            with self.subTest(page=page), self.assertRaises(client.OuraError):
                client.page_data(page)

    def test_http_errors_are_actionable_and_never_echo_secrets(self):
        for code, hint in ((401, "reconnect"), (403, "scope"), (429, "retry"), (500, "retry")):
            error = urllib.error.HTTPError("https://example.invalid/secret", code, "secret", {}, None)
            with self.subTest(code=code), patch.object(urllib.request, "build_opener") as opener:
                opener.return_value.open.side_effect = error
                with self.assertRaises(client.OuraError) as caught:
                    client.request_json(urllib.request.Request(client.API_URL + "sleep"))
                self.assertIn(hint, str(caught.exception))
                self.assertNotIn("secret", str(caught.exception))
                self.assertEqual(opener.return_value.open.call_args.kwargs["timeout"], 20)

    def test_network_and_json_errors_are_sanitized(self):
        for failure in (urllib.error.URLError("secret"), TimeoutError("secret"),
                        ValueError("secret"), http.client.IncompleteRead(b"secret")):
            with patch.object(urllib.request, "build_opener") as opener:
                opener.return_value.open.side_effect = failure
                with self.assertRaisesRegex(client.OuraError, "network failure") as caught:
                    client.request_json(urllib.request.Request(client.API_URL + "sleep"))
                self.assertNotIn("secret", str(caught.exception))

    def test_redirects_cannot_forward_credentials(self):
        request = urllib.request.Request(client.API_URL + "sleep", headers={"Authorization": "Bearer synthetic"})
        self.assertIsNone(client.NoRedirect().redirect_request(
            request, None, 302, "redirect", {}, "https://example.invalid/"
        ))


class CacheAndAuthTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.credentials = Path(self.tmp.name) / "credentials.json"
        self.output = Path(self.tmp.name) / "health-data.json"
        self.cache = {"fetched_at": "previous-success", "oura": {"connected": True, "status": "fresh",
                     "today": {"readiness": 77}, "trend": [{"date": "9/20", "readiness": 77}]},
                      "strava": {"connected": True, "days_since_workout": 2}, "shapedNote": "Keep this"}

    def test_offline_refresh_never_reads_credentials_or_calls_network(self):
        before = copy.deepcopy(self.cache)
        with patch.object(client, "ensure_access_token", side_effect=AssertionError("credentials read")), \
                patch.object(client, "request_json", side_effect=AssertionError("network used")):
            result, error = client.refresh(self.credentials, self.cache, START, END, FIXTURES)
        self.assertIsNone(error)
        self.assertEqual(result["oura"], client.read_json(FIXTURES / "expected_oura.json"))
        self.assertEqual(result["strava"], before["strava"])
        self.assertEqual(result["shapedNote"], "Keep this")
        self.assertNotEqual(result["fetched_at"], before["fetched_at"])
        self.assertEqual(self.cache, before)

    def test_partial_fetch_failure_keeps_last_good_data_and_timestamp(self):
        client.write_json(self.credentials, {"oura": {"access_token": "synthetic-token"}})
        with patch.object(client, "fetch_collection", side_effect=[[], client.OuraError("HTTP 429")]):
            result, error = client.refresh(self.credentials, self.cache, START, END)
        expected = copy.deepcopy(self.cache)
        expected["oura"]["status"] = "error"
        self.assertEqual(result, expected)
        self.assertEqual(error, "HTTP 429")

    def test_missing_credentials_fail_without_network(self):
        with patch.object(client, "request_json", side_effect=AssertionError("network used")):
            result, error = client.refresh(self.credentials, {}, START, END)
        self.assertIsNotNone(error)
        self.assertEqual(result, {"oura": {"connected": True, "status": "error"}})

    def test_bearer_only_credentials_are_used_without_refresh(self):
        client.write_json(self.credentials, {"oura": {"access_token": "synthetic-token"}})
        with patch.object(client, "request_json", side_effect=AssertionError("unexpected refresh")):
            self.assertEqual(client.ensure_access_token(self.credentials), "synthetic-token")

    def test_fresh_oauth_token_is_reused(self):
        client.write_json(self.credentials, {"oura": {"access_token": "synthetic-token", "access_token_expires_at": 2000}})
        with patch.object(client.time, "time", return_value=1000), \
                patch.object(client, "request_json", side_effect=AssertionError("unexpected refresh")):
            self.assertEqual(client.ensure_access_token(self.credentials), "synthetic-token")

    def test_refresh_rotates_and_persists_before_data_fetch(self):
        client.write_json(self.credentials, {"oura": {
            "access_token": "synthetic-old", "access_token_expires_at": 1100,
            "client_id": "synthetic-id", "client_secret": "synthetic-secret", "refresh_token": "synthetic-refresh",
        }, "strava": {"refresh_token": "synthetic-strava"}})
        response = {"access_token": "synthetic-new", "refresh_token": "synthetic-rotated", "expires_in": 86400}

        def fetch(name, token, start, end):
            stored = client.read_json(self.credentials)
            self.assertEqual(stored["oura"]["refresh_token"], "synthetic-rotated")
            self.assertEqual(stored["oura"]["access_token_expires_at"], 87400)
            self.assertEqual(stored["strava"]["refresh_token"], "synthetic-strava")
            self.assertEqual(token, "synthetic-new")
            return []

        with patch.object(client.time, "time", return_value=1000), \
                patch.object(client, "request_json", return_value=response) as request, \
                patch.object(client, "fetch_collection", side_effect=fetch):
            _, error = client.refresh(self.credentials, {}, START, END)
        self.assertIsNone(error)
        req = request.call_args.args[0]
        self.assertEqual(req.full_url, client.TOKEN_URL)
        self.assertEqual(req.get_method(), "POST")
        self.assertEqual(urllib.parse.parse_qs(req.data.decode())["grant_type"], ["refresh_token"])
        self.assertEqual(stat.S_IMODE(self.credentials.stat().st_mode), 0o600)

    def test_invalid_refresh_response_preserves_credentials_and_cache(self):
        credentials = {"oura": {"client_id": "synthetic-id", "client_secret": "synthetic-secret", "refresh_token": "synthetic-refresh"}}
        client.write_json(self.credentials, credentials)
        with patch.object(client, "request_json", return_value={"access_token": "synthetic-new"}):
            result, error = client.refresh(self.credentials, self.cache, START, END)
        self.assertIn("rotated refresh_token", error)
        self.assertEqual(client.read_json(self.credentials), credentials)
        self.assertEqual(result["oura"]["today"], self.cache["oura"]["today"])

    def test_dry_run_merges_but_leaves_files_unchanged(self):
        client.write_json(self.output, self.cache)
        original = self.output.read_bytes()
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            code = client.main(["--fixtures", str(FIXTURES), "--end-date", END.isoformat(),
                                "--output", str(self.output), "--dry-run"])
        self.assertEqual(code, 0)
        self.assertEqual(self.output.read_bytes(), original)
        self.assertEqual(json.loads(stdout.getvalue())["strava"], self.cache["strava"])

    def test_cli_writes_cache_and_preserves_strava(self):
        client.write_json(self.output, self.cache)
        command = [sys.executable, str(Path(client.__file__)), "--fixtures", str(FIXTURES),
                   "--end-date", END.isoformat(), "--output", str(self.output)]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")
        stored = client.read_json(self.output)
        self.assertEqual(stored["oura"], client.read_json(FIXTURES / "expected_oura.json"))
        self.assertEqual(stored["strava"], self.cache["strava"])

    def test_cli_missing_token_is_nonzero_and_preserves_good_cache(self):
        client.write_json(self.output, self.cache)
        with redirect_stderr(io.StringIO()):
            code = client.main(["--credentials", str(self.credentials), "--output", str(self.output)])
        self.assertEqual(code, 1)
        stored = client.read_json(self.output)
        self.assertEqual(stored["oura"]["status"], "error")
        self.assertEqual(stored["oura"]["today"], self.cache["oura"]["today"])
        self.assertEqual(stored["fetched_at"], "previous-success")

    def test_corrupt_cache_is_not_overwritten(self):
        self.output.write_text("not JSON")
        with redirect_stderr(io.StringIO()):
            code = client.main(["--fixtures", str(FIXTURES), "--output", str(self.output)])
        self.assertEqual(code, 1)
        self.assertEqual(self.output.read_text(), "not JSON")

    def test_cache_cannot_overwrite_credentials(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
            client.main(["--credentials", str(self.credentials), "--output", str(self.credentials)])
        self.assertEqual(caught.exception.code, 2)

    def test_atomic_write_failure_keeps_existing_file(self):
        client.write_json(self.output, self.cache)
        before = self.output.read_bytes()
        with patch.object(client.os, "replace", side_effect=OSError("synthetic failure")):
            with self.assertRaises(client.OuraError):
                client.write_json(self.output, {"new": True})
        self.assertEqual(self.output.read_bytes(), before)
        self.assertEqual(list(Path(self.tmp.name).iterdir()), [self.output])


if __name__ == "__main__":
    unittest.main()
