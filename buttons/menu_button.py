from hooks import StaticHook
from .text_button import TextButton
from utils.decorators import on_collision_point


class MenuButton(TextButton):
    @on_collision_point
    def handle_click(self, mouse_pos: tuple[int, int]) -> None:
        self.hook.set_data(current_screen=StaticHook.read_data()["main_menu_screen"])
