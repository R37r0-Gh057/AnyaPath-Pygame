import pygame

from constants import SOUNDS_DIR


class AudioManager:
    def __init__(self) -> None:
        pygame.mixer.init()

        self.background_music = pygame.mixer.Sound(
            SOUNDS_DIR / "bg_music.mp3"
        )

        self.dialogues = {
            "welcome": SOUNDS_DIR / "welcome_to_anya_house.mp3",
            "waku": SOUNDS_DIR / "waku_waku.mp3",
            "gwah": SOUNDS_DIR / "gwah.mp3",
        }

        self.channel_music = pygame.mixer.Channel(0)
        self.channel_sfx = pygame.mixer.Channel(1)

    def play_background_music(self) -> None:
        self.channel_music.set_volume(0.2)
        self.channel_music.play(
            self.background_music,
            loops=-1,
        )

    def play_dialogue(self, key: str) -> None:
        sound_path = self.dialogues.get(key)

        if sound_path:
            sound = pygame.mixer.Sound(sound_path)
            self.channel_sfx.play(sound)
