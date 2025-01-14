from hooks import StaticHook
from utils.decorators import on_collision_point
from .text_button import TextButton


class PlayButton(TextButton):
    @on_collision_point
    def handle_click(self, mouse_pos: tuple[int, int]) -> None:
        self.hook.set_data(current_screen=StaticHook.read_data()["play_screen"])
