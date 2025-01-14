import pygame


def on_collision_point(func):
    def wrapper(obj, point: tuple[int, int], *args, **kwargs):
        if obj.rect.collidepoint(point):
            return func(obj, point, *args, **kwargs)
    return wrapper


def on_collision_rect(func):
    def wrapper(obj, rect: pygame.Rect, *args, **kwargs):
        if obj.rect.colliderect(rect):
            return func(obj, rect, *args, **kwargs)
    return wrapper
