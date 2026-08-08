# Connecting Oura + Strava

A one-time setup runbook for wiring your own Oura and Strava into your 1000-second-system install, so the Physical pillar uses your real recovery + training. Do this at your desktop in Claude Code -- it needs the local install files, `python3`, and `curl`, which a phone or iPad can't give the agent.

Total time: ~8 minutes. Oura is the easy one (~2 min); Strava's one-time app registration is the longer part (~5 min).

---

## Step 0 -- Prereqs (1 min)

1. Be at your desktop, in Claude Code, in your 1000-second-system workspace.
2. Be on **v2.4.0 or later**. If you installed earlier, run `/1000s-update` first -- that's the release that adds the health integration.
3. Sanity check the runtime:
   ```bash
   python3 --version && curl --version | head -1
   ```
   Both should print a version. (python3 powers the Strava token refresh; curl does the API reads.)

Your credentials will live in `1000-second-system/system/health/credentials.json` -- inside the gitignored install folder. They are never committed and never leave your machine. Nothing routes through a server the project controls.

---

## Step A -- Connect Oura (~2 min, easy)

1. Go to **https://cloud.ouraring.com/** and log in.
2. Create a token:
   - If your account offers **Personal Access Tokens**, create one. That's a single bearer token -- the simplest path.
   - If it only offers OAuth apps, create a **Personal** app and note `client_id` / `client_secret`. (`/sources` confirms the current method for you against https://cloud.ouraring.com/docs/authentication.)
   - Scopes you want: `daily`, `heartrate`, `workout`, `personal`.
3. Copy the token.
4. In Claude Code, run **`/sources`** -> **connect Oura** -> paste the token. It writes the `oura` block to `credentials.json` and adds the Oura entry to `system/sources.md`.

**Manual fallback** (if `/sources` isn't in your install yet): create `1000-second-system/system/health/credentials.json` with:
```json
{ "oura": { "access_token": "PASTE_TOKEN_HERE" } }
```

---

## Step B -- Connect Strava (~5 min, one-time app)

1. Go to **https://www.strava.com/settings/api** and create an API application:
   - Name: anything (e.g. "1000 Second Method").
   - **Authorization Callback Domain: `localhost`** (this must match the redirect below).
   - After creating, copy **Client ID** and **Client Secret**.
2. **Authorize** -- open this URL in your browser (paste your Client ID in place of `CLIENT_ID`):
   ```
   https://www.strava.com/oauth/authorize?client_id=CLIENT_ID&response_type=code&redirect_uri=http://localhost&approval_prompt=force&scope=activity:read_all
   ```
   Click **Authorize**. Your browser redirects to a `http://localhost/?state=&code=THE_CODE&scope=...` URL that **won't load** -- that's expected. Copy `THE_CODE` (the value between `code=` and `&scope`) straight from the address bar.
3. In Claude Code, run **`/sources`** -> **connect Strava** -> paste the **Client ID**, **Client Secret**, and the **code**. It exchanges the code once for a refresh token, writes the `strava` block to `credentials.json`, and fetches `strava_token.py` into `system/health/`.

**Manual fallback** (exchange the code yourself):
```bash
curl -X POST https://www.strava.com/oauth/token \
  -d client_id=YOUR_ID -d client_secret=YOUR_SECRET \
  -d code=THE_CODE -d grant_type=authorization_code
```
From the JSON response, save `refresh_token` (and `access_token`, `expires_at`) into `credentials.json` under `strava`, alongside `client_id` and `client_secret`. The code is single-use and expires fast -- if it fails, re-do step B2 for a fresh code.

---

## Step C -- Test + verify (~1 min)

1. **Test the connections:** run `/sources` -> **test** (or just run `/1000seconds`). It runs the Health fetch: `strava_token.py` mints a Strava token, the agent GETs Oura + Strava, and writes `system/health/health-data.json`. Each source should come back `fresh` with a one-line sample (today's readiness; days since last workout).
2. **See it in the page:** run `/1000seconds`, open the rendered page, click the **Health** tab. You should see your real readiness / sleep / HRV / resting HR, your two-week trend sparklines, and your recent workouts -- and on the Today tab, the Physical pick responding to your recovery (mobility on amber days, movement after a gap).

---

## Reference: `credentials.json` shape

```json
{
  "oura":   { "access_token": "..." },
  "strava": {
    "client_id": "...",
    "client_secret": "...",
    "refresh_token": "...",
    "access_token": "",
    "access_token_expires_at": 0
  }
}
```

## Notes

- `credentials.json` and `health-data.json` live in `1000-second-system/system/health/`, which is gitignored. Sovereign: nothing leaves your machine.
- To rotate or revoke: re-run `/sources` -> connect to refresh, or `/sources` -> remove (which clears the local block; revoke the app itself in Oura/Strava settings).
- Strava access tokens expire every 6 hours; `strava_token.py` re-mints them automatically on each run, so you only do the OAuth dance once.
