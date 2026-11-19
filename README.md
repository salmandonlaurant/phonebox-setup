# PhoneBox PC dashboard — setup & tuning scripts

Scripts used to tune a PhoneBox 0.9.19 dashboard for a Samsung Galaxy A32 5G
(1600x720 landscape) driving a Windows PC.

## Layout

- `scripts/` — one-off and reusable tuning scripts (glass rebuild, music picker,
  pairing QR, Discord panel, prayer widget, verification helpers).
- `helpers/` — files installed under `%LOCALAPPDATA%\PhoneBox` on the PC.
  `dc-ctl.py` + `dc-ctl-run.vbs` drive Discord voice actions through the agent.
  `dc-sfx.py` + `dc-sfx-run.vbs` play Discord soundboard sounds.
  `ytm-play.ps1` + `ytm-run.vbs` launch hidden YouTube Music videos.
  `pair-phone.py` + `pair-phone-run.vbs` generate a fresh pairing QR on demand.
  `pairweb.py` + `pairweb-run.vbs` serve the enhanced settings page on port 8770.
  `agent-post.py` + `agent-post-run.vbs` post to agent endpoints (media controls).
  `rebuild-glass.py` regenerates the AMOLED Liquid Glass overlays.

## Phonebox API used

- `GET/PUT http://127.0.0.1:8765/api/settings` (UTF-8 JSON,
  `Content-Type: application/json; charset=utf-8`)
- `POST http://127.0.0.1:8765/api/refresh?reload=true` after layout changes
- `POST http://127.0.0.1:8765/api/goto/{page}?countdown=0`
- `POST http://127.0.0.1:8765/api/pair/start` for QR pairing (5 minute expiry)

## Device tuning applied

`orientation=landscape`, `theme=amoled`, `keepAwake=true`, `idleDimMin=0`,
`artTint=false`, `pixelShift=false`; appearance `fontScale=105`, `gap=8`,
`padding=10`, `radius=22`, `pagePadding=8`, `shadow=false`, `border=false`.

## Enhanced settings page (Connect Device button)

The agent's `settings.html` is compiled into `PhoneBoxAgent.exe`, so the header
button is added by a tiny read-only proxy:

- Open **http://127.0.0.1:8770/** (desktop shortcut: `PhoneBox Settings`).
- A **📱 Connect Device** button sits immediately after the language selector.
  It opens a dialog with two QR codes: **1 · Pair this PC** (scan in PhoneBox →
  Pair / Add PC) and **2 · Add another device** (downloads the app on a new phone
  or tablet, then pair it with the first code).
- `pairweb.py` forwards all requests to the real agent on `127.0.0.1:8765` and
  strips browser origin headers so the agent's CSRF check still passes.
  `PhoneBox Pair Web.lnk` in Startup keeps it running after a PC restart.
- The original settings page remains at `http://127.0.0.1:8765/`.

## Pairing

The "Pair Phone (QR)" launcher on the dashboard runs `pair-phone-run.vbs`, which
asks the agent for a fresh code and opens the QR on the PC screen to scan.
`add_pair_button.py` adds that shortcut and launcher entry.

The phone only stores the PC's IP at pairing time and does not refresh it over
Wi-Fi, so a DHCP address change breaks the connection until you re-pair.
`set-static-ip.ps1` (run elevated) pins the PC to `192.168.1.102` so this does
not happen again. Adjust the address for your own network before using it.

## Notes

- Settings are global on the PC (all paired devices share them).
- The Wi-Fi stream deliberately reconnects every 60 seconds (normal behaviour).
- No secrets (tokens, credentials, paired config) are stored in this repo.
