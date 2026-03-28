from pygame import mixer

from ui.background import handle_assets_path


class AudioManager:
    def __init__(self):
        mixer.init()

        self.sounds = {
            "peg_click": mixer.Sound(
                handle_assets_path(relative_path="assets/peg_click.wav")
            ),
            "color_select": mixer.Sound(
                handle_assets_path(relative_path="assets/color_select.wav")
            ),
            "feedback": mixer.Sound(
                handle_assets_path(relative_path="assets/feedback.wav")
            ),
            "button_click": mixer.Sound(
                handle_assets_path(relative_path="assets/button_click.wav")
            ),
            "game_lose": mixer.Sound(
                handle_assets_path(relative_path="assets/game_lose.wav")
            ),
            "game_win": mixer.Sound(
                handle_assets_path(relative_path="assets/game_win.wav")
            ),
            "solved": mixer.Sound(
                handle_assets_path(relative_path="assets/solved.wav")
            ),
            "unsolved": mixer.Sound(
                handle_assets_path(relative_path="assets/unsolved.wav")
            ),
        }

        for sound in self.sounds.values():
            sound.set_volume(1.0)

    def play(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
