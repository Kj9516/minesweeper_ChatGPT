import pygame
import sys
import json
from menu import Menu
from game import Game

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def main():
    pygame.init()
    config = load_config()
    screen = pygame.display.set_mode((800, 600))  # Изначальный размер для меню
    pygame.display.set_caption('Сапёр')
    clock = pygame.time.Clock()
    menu = Menu(screen, config)
    game = None

    while True:
        if menu.active:
            menu.run()
            if menu.selected_level:
                level_config = config['levels'][menu.selected_level]
                # Рассчитываем размеры экрана для выбранного уровня
                cell_size = 30
                field_width = level_config['width'] * cell_size
                field_height = level_config['height'] * cell_size
                side_panel_width = 200
                screen_width = field_width + side_panel_width
                screen_height = field_height
                screen = pygame.display.set_mode((screen_width, screen_height))
                game = Game(screen, level_config)
                menu.active = False
        elif game:
            game.run()
            if game.back_to_menu:
                menu.active = True
                menu.selected_level = None  # Сбрасываем выбранный уровень
                screen = pygame.display.set_mode((800, 600))  # Размер для меню
                game = None
        else:
            pygame.quit()
            sys.exit()
        clock.tick(60)

if __name__ == '__main__':
    main()