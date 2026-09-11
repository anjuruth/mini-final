# Scream Volume Manager

Minimal Windows desktop app for a Useless Projects event.

## What it does

- Detects the default microphone
- Records a ~2.5 second scream sample
- Measures loudness using RMS and peak amplitude
- Converts loudness to a 0–100 percentage
- Sets the **real Windows master system volume** to that percentage
- Displays the measured percentage in the app

## Tech stack

- Python
- PySide6 (desktop UI)
- sounddevice + numpy (audio capture + analysis)
- pycaw (Windows Core Audio volume control)

## Setup

> Windows is required for actual system volume control.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python scream_volume_manager.py
```

## Usage

1. Launch the app.
2. Confirm microphone is detected.
3. Click **SET VOLUME**.
4. Scream for about 2–3 seconds.
5. The app shows the measured percentage and sets Windows master volume to that value.

## Notes

- If you run this on non-Windows OS, audio capture can still work but Windows volume control will raise an error by design.
- For reliable input device selection, configure your default microphone in Windows Sound settings.
