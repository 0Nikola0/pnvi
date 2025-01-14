from screens import Screen
from .text_button import TextButton
from utils.decorators import on_collision_point


class ExitButton(TextButton):
    @on_collision_point
    def handle_click(self, mouse_pos: tuple[int, int]) -> None:
        Screen.exit()

