# Set up your Oura connection

Connect Oura to bring readiness, sleep score, overnight HRV, lowest heart rate,
and hours asleep into your Daily Punchlist and its Health tab. The Physical
pillar uses those readings to help choose between training and recovery.
Workout history comes from Strava if you connect it separately.

You register an Oura application for your own use and approve access to your
account. Claude Code handles the local configuration and connection test.
Credentials and the downloaded health cache live in your workspace; this repo
does not run a service that receives them. Your agent reads the health data to
generate the punchlist, under your AI provider's data handling settings.

## Before you start

- Install the method using the [README instructions](https://github.com/TottyBuilds/1000-second-method#install), or
  connect Oura during the install's **Full wire-up** step.
- Have your Oura login ready. Open the Oura phone app and let your ring sync.
- **Gen3 and later rings require an active Oura membership for API access**, per
  [Oura's support guide](https://support.ouraring.com/hc/en-us/articles/4415266939155-The-Oura-API).
- Use Claude Code on the same computer as your browser for the local setup
  described here. The agent needs **Python 3.9+** (`python3 --version` checks it).
  No extra Python packages are required.

Oura is optional. If you want to skip this now, finish the install and return
with `/sources` later. You do not need to clone this repository to connect it.

## Connect Oura

### 1. Start in your installed workspace

In Claude Code, run `/sources`, then say **Connect Oura**. During a new install,
ask to connect Oura when the installer reaches physical tracking instead.
If an older install does not have these instructions, run `/1000s-update` first.

The agent prepares the local files and a one-time browser callback, then gives
you an exact **redirect URI**. That address sends the browser back to your own
computer after you approve access. Wait for the agent to supply it before
registering your application.

### 2. Register your own Oura application

Open the [Oura developer portal](https://developer.ouraring.com/) and sign in.
Create an application for your personal installation. Oura's
[support guide](https://support.ouraring.com/hc/en-us/articles/4415266939155-The-Oura-API)
directs new applications here; the
[previous portal](https://cloud.ouraring.com/oauth/applications) remains available
for editing existing applications.

Use these values where the form asks for them:

| Setting | What to enter |
|---|---|
| Application name | `1000 Second Method - Personal` (or your own name for it) |
| Description | `Read my Oura recovery data for my personal Daily Punchlist.` |
| Website | `https://github.com/TottyBuilds/1000-second-method` |
| Redirect URI | Copy the exact address supplied by your agent, including the port, path, and any trailing slash. |
| Permissions / scopes, if offered | `daily` only. This connection reads recovery data. |

Save the application and keep its **Client ID** and **Client Secret** available
for the next step. These identify your application; they are not your Oura
password. The agent will handle the access and refresh tokens after consent.

### 3. Save the application credentials locally

The agent should give you the full path to a prepared local file:

```text
1000-second-system/system/health/credentials.json
```

Open it in a local editor and fill in your application's `client_id` and
`client_secret` under `oura`. Preserve any existing `strava` entry. The agent
checks that this file is excluded from Git and readable only by your user.

**Do not paste the secret, tokens, or callback URL into chat, a terminal command,
or a GitHub issue.** Tell the agent when the file is saved. You should not have
to create or calculate tokens yourself.

### 4. Approve access in your browser

The agent supplies an Oura sign-in/consent link. Check that it is your
application, then approve the daily data permission. The browser returns to
the local callback; the agent validates the response and saves your tokens.
Keep the setup running until the agent confirms that this step completed.

The initial login is coordinated by the installing agent. The included
`oura_client.py` handles later data fetches and token refresh; running that
script alone does not start the initial login.

### 5. Confirm the connection worked

The agent runs a live read and confirms:

- **Oura is connected** in `1000-second-system/system/sources.md`.
- The latest fetch succeeded (`oura.status` is `fresh`).
- Today's readiness and sleep score are shown, or the agent reports
  **not yet synced** if today's readings are missing.

Run `/render`, then open **Health** in the generated page. `/1000seconds` also
refreshes connected health data when you use the daily command. There is no
separate always-on sync process installed by this connection.

A successful connection can have missing readings. Sync the ring in the Oura
app, then run `/sources` and ask to **test Oura** again. Missing readings stay
blank; the system does not substitute zero or yesterday's score.

## If something goes wrong

| What you see | What to do |
|---|---|
| `/sources` is unavailable | Open Claude Code in the workspace where you installed the method. If needed, install it from the README. For an older installation, run `/1000s-update`. |
| Python is missing or older than 3.9 | Ask the agent to help you install a supported Python version, then retry. You can finish the rest of the method first. |
| Oura rejects the redirect URI | Compare the application's saved URI with the agent's URI character for character. Host, port, path, and trailing slash must match. |
| The browser cannot open the callback page | Ask the agent to check that its local callback is running on the same computer and port, then restart authorization. Do not paste the callback URL into chat. |
| Authorization was denied, or the state check failed | Run `/sources` and ask to reconnect Oura. Start a new authorization attempt; do not reuse the old callback. |
| `401`, invalid token, or failed token refresh | Reconnect through `/sources`. An old token or a revoked connection may no longer work. |
| `403` / permission denied | Check your Oura membership and reconnect with the `daily` permission enabled. |
| Connected, but today's readings are blank | Sync your ring in the Oura app and test again later. A successful fetch does not guarantee today's data is available yet. |
| `429`, a network error, or an Oura service error | Retry later through `/sources`. The rest of the method still works; an error-status cache is not used as current recovery data. |

Oura documents authentication failures in its
[error guide](https://cloud.ouraring.com/docs/error-handling) and API response
codes in its [v2 reference](https://cloud.ouraring.com/v2/docs).

To disconnect, run `/sources` and ask to remove Oura. This removes the local
connection and credentials; revoke the application's access in Oura's settings
as well if you want to end its authorization. Previously downloaded health
files are local data and are not automatically erased by removing the source.

## Setup reference for the installing agent

This is the authoritative setup for both `INSTALL.md` and `/sources`. Walk the
operator through the steps above; implement the local authorization steps
below. Do not ask the operator to build OAuth requests or paste secrets into
the conversation. If the environment cannot complete local authorization,
explain the specific blocker and leave Oura setup incomplete.

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
   command history, logs, and PRs; enter them directly into the local file. Check
   `python3 --version` before beginning browser authorization.
2. Prepare a temporary callback listener bound only to loopback on an available
   port. For example, use `http://localhost:8765/callback/` if that port is free;
   give the operator the actual URI to register in the developer portal. The
   browser must be on the same machine. Suppress request logging because the
   callback contains a code. Keep the callback, state, and code in memory, use
   a bounded timeout, and close the listener after setup or cancellation.
   `oura_client.py` does not provide this listener or initial token exchange.
   Prepare `credentials.json` with mode `0600`, merging an `oura` object with
   empty `client_id` and `client_secret` fields only for a new connection.
   Give the operator the full file path to fill in locally. Do not overwrite
   existing credentials while preparing a reconnect.
3. Generate an unpredictable `state` value locally (for example with Python's
   `secrets.token_urlsafe(32)`) and retain it for callback validation. Direct the
   operator to `https://cloud.ouraring.com/oauth/authorize` with URL-encoded query
   parameters `response_type=code`, `client_id`, `redirect_uri`, `scope=daily`,
   and `state`. Start the listener before opening the consent link. On return,
   check the callback path, reject an error response or mismatched/missing state,
   require a nonempty `code`, and verify the returned granted scopes include
   `daily` before using the code. Use the registered redirect URI unchanged.
4. Exchange the code locally with a form-encoded POST to
   `https://api.ouraring.com/oauth/token`: `grant_type=authorization_code`, `code`,
   `redirect_uri`, `client_id`, and `client_secret`. Do not print the response.
   Validate nonempty access and refresh tokens and a positive `expires_in`
   before saving. Atomically store the returned tokens with the exact keys
   below, merging with any existing `strava` block. Compute
   `access_token_expires_at` as current Unix time in
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

The client uses Python 3.9+ and the standard library to fetch Oura v2
`daily_readiness`, `daily_sleep`, and `sleep`. It refreshes OAuth tokens when
fewer than five minutes remain. Oura refresh tokens are single-use: the helper
atomically saves both new tokens and
their expiry before fetching data. Run one health refresh at a time so two
processes do not consume the same refresh token or overwrite each other's cache.

For compatibility with previously stored credentials, the client also accepts
an `oura.access_token` alone, without expiry or refresh fields. It sends that
bearer token as supplied; this does **not** establish that Oura accepts a retired
PAT. A 401 requires reconnecting through the OAuth setup above. There are no
alternate token environment variables or token CLI arguments.

## Contributor reference: offline dry run

This checks the client with synthetic data. It does not connect an Oura account
and is not required for end-user setup.

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
