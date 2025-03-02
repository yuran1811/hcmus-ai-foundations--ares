import os
from pathlib import Path

from config import SUPPORTED_BGM_EXTENSIONS
from constants.paths import BGMS_PATH
from core.audio import Audio


class BGMController:
    def __init__(self):
        self.bgm_files = self._get_bgm_files()
        self.bgm_files_path = [os.path.join(BGMS_PATH, _) for _ in self.bgm_files]
        self.current_index = 0

        self.audio = Audio()
        self.audio.load_sounds(
            {name: path for name, path in zip(self.bgm_files, self.bgm_files_path)}
        )

    def _get_bgm_files(self):
        try:
            files = [
                f
                for f in os.listdir(BGMS_PATH)
                if Path(f).suffix.lower() in SUPPORTED_BGM_EXTENSIONS
            ]
            return sorted(files)
        except FileNotFoundError:
            return []

    def next_track(self):
        if not self.bgm_files:
            return

        self.stop()
        self.current_index = (self.current_index + 1) % len(self.bgm_files)
        self.play()

    def prev_track(self):
        if not self.bgm_files:
            return

        self.stop()
        self.current_index = (self.current_index - 1 + len(self.bgm_files)) % len(
            self.bgm_files
        )
        self.play()

    def set_current_track(self, index: int):
        if not self.bgm_files:
            return

        self.stop()
        self.current_index = index % len(self.bgm_files)
        self.play()

    def set_volume(self, volume: float):
        self.audio.set_volume(self.bgm_files[self.current_index], volume)

    def is_muted(self):
        return self.audio.is_muted(self.bgm_files[self.current_index])

    def mute(self, mute=False):
        self.audio.mute(self.bgm_files[self.current_index], mute)

    def is_playing(self):
        return self.audio.is_playing(self.bgm_files[self.current_index])

    def play(self):
        if self.audio.is_playing(self.bgm_files[self.current_index]):
            return

        self.audio.play(self.bgm_files[self.current_index], -1)

    def stop(self):
        self.audio.stop(self.bgm_files[self.current_index])
