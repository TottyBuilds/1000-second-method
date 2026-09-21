# Oura recovery client

`oura_client.py` uses Python 3.9+ and the standard library to fetch Oura v2
`daily_readiness`, `daily_sleep`, and `sleep`. It writes the Oura block expected
by `system/health/health-data.json` and preserves Strava and other cache fields.
Workouts remain Strava's responsibility in the current health contract.

## Connect Oura (authoritative setup for INSTALL and `/sources`)

Use **OAuth2 authorization-code flow with the `daily` scope**. Oura's
[API specification](https://cloud.ouraring.com/v2/static/json/openapi-1.39.json)
states that personal access tokens were deprecated in December 2025 and are no
longer available for use (checked 2026-09-21). Do not send operators to create
a PAT. Follow Oura's [authentication documentation](https://cloud.ouraring.com/docs/authentication)
for the authorization and token exchanges below.

1. In the operator's install, create `1000-second-system/system/health/` and
   copy [oura_client.py](oura_client.py) there. For an install from GitHub, use
   `https://raw.githubusercontent.com/TottyBuilds/1000-second-method/main/docs/oura_client.py`.
   Keep this guide alongside it as `system/health/oura.md`. Verify the install
   directory and all `credentials.json` / `health-data.json` files are gitignored
   before storing credentials or live readings. Keep credentials out of chat,
   command history, logs, and PRs; enter them directly into the local file.
2. Open [Oura's application portal](https://cloud.ouraring.com/oauth/applications).
   Register the operator's application and an exact redirect URI under their
   control, then save its client ID and secret locally. Use the same redirect URI
   in both exchanges. The client handles subsequent refreshes; initial consent
   and code exchange are a one-time setup performed locally by the installing agent.
3. Generate an unpredictable `state` value locally (for example with Python's
   `secrets.token_urlsafe(32)`) and retain it for callback validation. Direct the
   operator to `https://cloud.ouraring.com/oauth/authorize` with URL-encoded query
   parameters `response_type=code`, `client_id`, `redirect_uri`, `scope=daily`,
   and `state`. On return, reject an error response or mismatched/missing state,
   and verify the returned granted scopes include `daily` before using `code`.
4. Exchange the code locally with a form-encoded POST to
   `https://api.ouraring.com/oauth/token`: `grant_type=authorization_code`, `code`,
   `redirect_uri`, `client_id`, and `client_secret`. Do not print the response.
   Store the returned tokens with the exact keys below, merging with any existing
   `strava` block. Compute `access_token_expires_at` as current Unix time in
   **seconds** plus the response's `expires_in`; do not store a relative expiry.

   ```json
   {
     "oura": {
       "client_id": "<Oura app client ID>",
       "client_secret": "<Oura app client secret>",
       "access_token": "<OAuth access_token>",
       "refresh_token": "<OAuth refresh_token>",
       "access_token_expires_at": 0
     }
   }
   ```

   Replace `0` with the computed absolute expiry. Save this as
   `1000-second-system/system/health/credentials.json` with mode `0600`.
   `redirect_uri`, `code`, and `state` are only needed during setup and are not
   runtime credential keys. `heartrate`, `workout`, and `personal` scopes are not
   required: overnight HRV and lowest heart rate come from `sleep` with `daily`.
5. From inside `1000-second-system/`, run:

   ```bash
   python3 system/health/oura_client.py \
     --credentials system/health/credentials.json \
     --output system/health/health-data.json
   ```

   On exit 0, add Oura to `system/sources.md`, recording its last successful read.
   Report `oura.status` and today's readiness/sleep score, or "not yet synced"
   for null readings. On failure, leave connection setup incomplete, report the
   short error, and continue the install. Missing live credentials do not prevent
   offline verification or installation of the rest of the method.

The client refreshes OAuth tokens when fewer than five minutes remain. Oura
refresh tokens are single-use: the helper atomically saves both new tokens and
their expiry before fetching data. Run one health refresh at a time so two
processes do not consume the same refresh token or overwrite each other's cache.

For compatibility with previously stored credentials, the client also accepts
an `oura.access_token` alone, without expiry or refresh fields. It sends that
bearer token as supplied; this does **not** establish that Oura accepts a retired
PAT. A 401 requires reconnecting through the OAuth setup above. There are no
alternate token environment variables or token CLI arguments.

## Offline dry run

From the repository root, no token, dependencies, or network are needed:

```bash
python3 -m unittest discover -s tests -v
python3 docs/oura_client.py --fixtures tests/fixtures/oura --end-date 2026-09-21 --dry-run
```

The synthetic fixtures represent September 19–21, 2026, with deliberately
unsorted records, null readings, a nap, and two main sleep periods on one day.
The September 21 result is readiness **82**, sleep score **86**, HRV **48 ms**,
lowest heart rate **51 bpm**, and **7.5 hours asleep**. The expected normalized
Oura block is committed as `tests/fixtures/oura/expected_oura.json`.

`--fixtures` bypasses credential reads and all HTTP, including OAuth. Without
`--output`, JSON goes to stdout and no files are written. To verify a merge into
a scratch cache, add `--output /tmp/1000sm-oura-fixture/health-data.json` and omit
`--dry-run`. Do not use an installed live cache as a fixture output.

`--dry-run` prints the merged result without modifying the output cache. In
**live mode**, OAuth credentials can still rotate and be saved; use `--fixtures`
for a completely offline run without credential writes.

## Cache contract and failure behavior

- The default window is 30 local calendar days, inclusive of `--end-date` (today
  by default). `--days` changes its length. Every collection follows `next_token`
  until exhausted; repeated cursors and malformed pages fail the whole refresh.
- Records join on Oura's `day`, preserving the operator's date rather than
  deriving it from UTC timestamps. Trend rows sort chronologically and display
  dates as `M/D`, matching the existing renderer.
- `today.readiness` uses `daily_readiness.score`; `today.sleep_score` uses
  `daily_sleep.score`. Neither borrows yesterday's score when today is missing.
- Overnight readings use the longest `long_sleep` on each day, measured by
  `total_sleep_duration`. Naps, deleted periods, and rejected rests do not replace
  it. `hrv_ms` is `average_hrv`; `resting_hr` is `lowest_heart_rate`; `sleep_hours`
  is `total_sleep_duration / 3600`, rounded to two decimals. This is time asleep,
  not time in bed. Oura documents that its API low heart rate can differ from
  the app's value because the sample aggregation differs.
- Missing measurements are JSON `null`, never zero. A successful empty response
  has `status: "fresh"`, empty trends, and null current readings: fresh means the
  fetch succeeded, not that the ring has synced. Recovery rules must use only
  available current scores from a source with `status: "fresh"`.
- Success atomically replaces only Oura's block and updates top-level `fetched_at`
  to the current UTC timestamp. An existing Strava block and unrelated fields
  survive. Without an existing Strava block, none is fabricated.
- HTTP/auth/network/response failures exit 1, retain Oura's last good readings,
  keep the previous `fetched_at`, and set `oura.status: "error"`. Other sources
  remain unchanged. A corrupt existing cache is left untouched. The agent must
  report the error and continue the punchlist without using stale recovery data.
- Errors omit response bodies and tokens. Requests have a 20-second timeout;
  redirects are rejected. A 429 asks the operator to retry later, without blocking
  the punchlist in a retry loop. A 403 requires checking the `daily` scope and
  applicable Oura membership; see [Oura's API reference](https://cloud.ouraring.com/v2/docs).

## Live smoke handoff

Only the operator's local credentials are missing from the offline path. Brent
can supply a valid `oura.access_token` privately to test an existing token, or
complete the OAuth setup above for ongoing refresh. Run the installed command
from step 5, then verify exit 0, `oura.status == "fresh"`, plausible current
readings (or a clear not-yet-synced result), and preservation of any Strava block.
Never commit the credential file or live cache. Live verification is optional
for landing the fixtures PR.
