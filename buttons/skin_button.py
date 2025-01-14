import pygame

from .button import Button
from hooks import EventHook, StaticHook
from game_objects import Coin
from utils.decorators import on_collision_point


class SkinButton(Button):
    skin_serial = 0

    def __init__(self, pos: tuple[int, int], size: tuple[int, int], hook: EventHook, name: str, price: int, sprite_path: str):
        super().__init__(pos, size, sprite_path, hook)

        self._id = SkinButton._set_id()
        
        self.sprite_path = sprite_path
        self.backup_sprite = self.sprite.copy()

        self.name = name
        self.price = price

        self.owned = self.get_ownership()
        self.available = self.get_availability()
        self.update_sprite()

        self.name_font = pygame.font.Font(pygame.font.get_default_font(), 24)
        self.price_font = pygame.font.Font(pygame.font.get_default_font(), 18)
        
        self.name_pos = pos[0] + size[0] / 2, (pos[1] + size[1])
        self.name_surface = self.name_font.render(str(self.name), True, (0, 0, 0))
        self.name_rect = self.name_surface.get_rect(centerx=self.name_pos[0], top=self.name_pos[1])

        self.price_pos = self.name_pos[0], self.name_pos[1] + self.name_rect.size[1] + 8
        self.price_surface = self.price_font.render(str(self.price), True, (0, 0, 0))
        self.price_rect = self.price_surface.get_rect(centerx=self.price_pos[0], top=self.price_pos[1])

        coin_icon_size = 20, 20
        self.coin_icon = Coin((self.price_rect.right + 2, self.price_rect.top - 2), coin_icon_size)

    
    @on_collision_point
    def handle_click(self, mouse_pos: tuple[int, int]) -> None:
        if not self.owned and self.available:
            self.hook.set_data(current_skin=self.sprite_path)
            
            owned_skins = StaticHook.read_data().get("owned_skins", set())
            owned_skins.add(self._id)
            StaticHook.add_data(owned_skins=owned_skins)
            StaticHook.add_data(coins=StaticHook.read_data()["coins"]-self.price)
            
            self.refresh()
            return True

    def draw(self, surface: pygame.Surface):
        surface.blit(self.sprite, self.rect.topleft)
        surface.blit(self.name_surface, self.name_rect)
        if not self.owned:
            surface.blit(self.price_surface, self.price_rect)
            self.coin_icon.draw(surface)

    @classmethod
    def _set_id(cls) -> int:
        SkinButton.skin_serial += 1
        return SkinButton.skin_serial
    
    def get_availability(self) -> bool:
        return StaticHook.read_data().get("coins", 0) >= self.price
    
    def get_ownership(self) -> bool:
        return self._id in StaticHook.read_data().get("owned_skins", set())
    
    def update_sprite(self) -> None:
        if not self.available and not self.owned:
            brighten = 140
            self.sprite.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_SUB)
        else:
            self.sprite = self.backup_sprite.copy()

    def refresh(self):
        self.owned = self.get_ownership()

        if self.available != self.get_availability():
            self.available = self.get_availability()
            self.update_sprite()
