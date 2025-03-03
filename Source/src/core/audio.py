import logging

import pygame as pg


class Audio:
    """
    Audio class for loading and playing sounds
    """

    def __init__(self):
        self.sounds: dict[str, dict[str, bool | pg.mixer.Sound]] = {}

    def load_sound(self, name: str, path: str):
        """
        Load a sound file
        """

        if name in self.sounds:
            logging.warning("Sound %s already loaded", name)
            return

        self.sounds[name] = {
            "src": pg.mixer.Sound(path),
            "playing": False,
        }

    def load_sounds(self, sounds: dict[str, str]):
        """
        Load multiple sounds

        sounds: dictionary of sounds
                    key: name of the sound;
                    value: path to the sound file
        """

        for name in sounds:
            self.load_sound(name, sounds[name])

    def set_volume(self, name: str, volume: float):
        if name not in self.sounds or not (0.0 <= volume <= 1.0):
            return

        self.sounds[name]["src"].set_volume(volume)  # type: ignore

    def is_muted(self, name: str):
        if name not in self.sounds:
            return False

        return self.sounds[name]["src"].get_volume() == 0.0  # type: ignore

    def mute(self, name: str, mute: bool = True):
        if name not in self.sounds:
            return

        self.set_volume(name, 0.0 if mute else 1.0)

    def is_playing(self, name: str):
        if name not in self.sounds:
            return False

        return self.sounds[name]["playing"]

    def play(self, name: str, loops=0, maxtime=0, fade_ms=0):
        if name in self.sounds and not self.sounds[name]["playing"]:
            self.sounds[name]["src"].play(loops, maxtime, fade_ms)  # type: ignore
            self.sounds[name]["playing"] = True

    def stop(self, name=None):
        if name is None:
            for name in self.sounds:
                self.sounds[name]["src"].stop()  # type: ignore
                self.sounds[name]["playing"] = False
        else:
            if name in self.sounds:
                self.sounds[name]["src"].stop()  # type: ignore
                self.sounds[name]["playing"] = False
