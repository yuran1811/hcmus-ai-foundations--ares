import logging

import pygame as pg


class Audio:
    """
    Audio class for loading and playing sounds
    """

    def __init__(self):
        self.sounds: dict[str, pg.mixer.Sound] = {}

    def load_sound(self, name: str, path: str):
        """
        Load a sound file
        """

        if name in self.sounds:
            logging.warning("Sound %s already loaded", name)
            return

        self.sounds[name] = pg.mixer.Sound(path)

    def load_sounds(self, sounds: dict[str, str]):
        """
        Load multiple sounds

        sounds: dictionary of sounds
                    key: name of the sound;
                    value: path to the sound file
        """

        for name in sounds:
            self.load_sound(name, sounds[name])

    def play(self, name: str, loops=0, maxtime=0, fade_ms=0):
        if name in self.sounds:
            self.sounds[name].play(loops, maxtime, fade_ms)

    def stop(self, name=None):
        if name is None:
            for sound_name in self.sounds:
                self.sounds[sound_name].stop()
        else:
            if name in self.sounds:
                self.sounds[name].stop()
