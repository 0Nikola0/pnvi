from hooks import StaticHook
from .button import Button
from utils.decorators import on_collision_point


class CheckButton(Button):
    @on_collision_point
    def handle_click(self, mouse_pos: tuple[int, int]) -> None:
        self.hook.set_data(current_screen=StaticHook.read_data()["main_menu_screen"])
