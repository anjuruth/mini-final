import sys
from dataclasses import dataclass

import numpy as np
import sounddevice as sd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


@dataclass
class AudioMeasurement:
    rms: float
    peak: float
    percent: int


class ScreamVolumeManager(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Scream Volume Manager")
        self.resize(420, 220)

        self.status_label = QLabel("Checking microphone...", self)
        self.status_label.setWordWrap(True)

        self.result_label = QLabel("Measured Volume: --%", self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 22px; font-weight: bold;")

        self.button = QPushButton("SET VOLUME", self)
        self.button.clicked.connect(self.on_set_volume_clicked)

        layout = QVBoxLayout(self)
        layout.addWidget(self.status_label)
        layout.addWidget(self.result_label)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self._validate_microphone()

    def _validate_microphone(self) -> None:
        try:
            device = get_default_input_device()
            self.status_label.setText(
                f"Microphone detected: {device['name']}\n"
                "Press SET VOLUME, then scream for about 2–3 seconds."
            )
            self.button.setEnabled(True)
        except Exception as exc:
            self.status_label.setText(f"Microphone not available: {exc}")
            self.button.setEnabled(False)

    def on_set_volume_clicked(self) -> None:
        self.button.setEnabled(False)
        self.status_label.setText("Recording for 2.5 seconds... Scream now!")
        QApplication.processEvents()

        try:
            measurement = record_and_measure(duration_seconds=2.5)
            set_windows_master_volume(measurement.percent)
            self.result_label.setText(f"Measured Volume: {measurement.percent}%")
            self.status_label.setText(
                f"Done. RMS={measurement.rms:.4f}, Peak={measurement.peak:.4f}. "
                f"Windows master volume set to {measurement.percent}%."
            )
        except Exception as exc:
            self.status_label.setText(f"Error: {exc}")
        finally:
            self.button.setEnabled(True)


def get_default_input_device() -> dict:
    default_input_index = sd.default.device[0]
    if default_input_index is None or default_input_index < 0:
        raise RuntimeError("No default input device configured.")

    device_info = sd.query_devices(default_input_index, "input")
    if device_info["max_input_channels"] < 1:
        raise RuntimeError("Default input device has no input channels.")

    return device_info


def record_and_measure(duration_seconds: float = 2.5, sample_rate: int = 44100) -> AudioMeasurement:
    get_default_input_device()

    frames = int(duration_seconds * sample_rate)
    recording = sd.rec(frames, samplerate=sample_rate, channels=1, dtype="float32")
    sd.wait()

    samples = np.squeeze(recording)
    if samples.size == 0:
        raise RuntimeError("No audio data captured.")

    rms = float(np.sqrt(np.mean(np.square(samples))))
    peak = float(np.max(np.abs(samples)))

    loudness = max(peak, min(1.0, rms * 1.8))
    percent = int(round(np.clip(loudness, 0.0, 1.0) * 100))

    return AudioMeasurement(rms=rms, peak=peak, percent=percent)


def set_windows_master_volume(percent: int) -> None:
    if not (0 <= percent <= 100):
        raise ValueError("Volume percent must be in range 0-100.")

    if not sys.platform.startswith("win"):
        raise RuntimeError("Windows volume control is only supported on Windows.")

    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from ctypes import POINTER, cast
    from comtypes import CLSCTX_ALL

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    endpoint = cast(interface, POINTER(IAudioEndpointVolume))
    endpoint.SetMasterVolumeLevelScalar(percent / 100.0, None)


def main() -> int:
    app = QApplication(sys.argv)
    window = ScreamVolumeManager()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
