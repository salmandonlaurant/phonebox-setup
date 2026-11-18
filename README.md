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

## Notes

- Settings are global on the PC (all paired devices share them).
- The Wi-Fi stream deliberately reconnects every 60 seconds (normal behaviour).
- No secrets (tokens, credentials, paired config) are stored in this repo.
