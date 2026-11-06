# Kandy For Scale Captions – updates

Automatic updates for the Kandy For Scale Captions panel in Premiere Pro.
Editors' panels read `latest.json` when they open and install new versions on their own.

- `latest.json` – the current version, signed with the Kandy For Scale update key.
- `updates/` – the update packages (caption engine + panel code only).
- `tools/publish.py` – prepares a new version (needs the private signing key, which is never stored here).
