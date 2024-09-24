import pygame

def adjust_font_size(text, font_name, max_size, rect_width, rect_height):
    font_size = max_size
    font = pygame.font.Font(font_name, font_size)
    text_surface = font.render(text, True, (0, 0, 0))
    while (text_surface.get_width() > rect_width or text_surface.get_height() > rect_height) and font_size > 10:
        font_size -= 1
        font = pygame.font.Font(font_name, font_size)
        text_surface = font.render(text, True, (0, 0, 0))
    return font, text_surface