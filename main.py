# main.py
import os

import pygame
import sys
import json
from menu import Menu
from game import Game
from scores_screen import ScoresScreen
from language_selector import LanguageSelector

def resource_path(relative_path):
    """ Получает абсолютный путь к ресурсам, независимо от того, запущен ли файл напрямую или как исполняемый файл. """
    try:
        # PyInstaller создает временную папку и сохраняет пути к файлам в `sys._MEIPASS`
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_config():
    config_path = resource_path("config.json")
    # Загрузка конфигурации из файла
    with open(config_path, 'r') as f:
        return json.load(f)

def load_localization():
    localization_path = resource_path("localization.json")
    # Загрузка конфигурации из файла
    with open(localization_path, 'r') as f:
        return json.load(f)

def main():
    pygame.init()
    config = load_config()
    localization = load_localization()
    language = 'en'  # Язык по умолчанию

    screen = pygame.display.set_mode((800, 600))  # Изначальный размер для меню
    pygame.display.set_caption('Сапёр')
    clock = pygame.time.Clock()

    # Добавляем выбор языка
    language_selector = LanguageSelector(screen, localization)
    menu = None
    game = None
    scores_screen = None

    while True:
        if language_selector.active:
            language_selector.run()
            if language_selector.selected_language:
                language = language_selector.selected_language
                menu = Menu(screen, config, localization, language)
                language_selector.active = False
        elif menu and menu.active:
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
                game = Game(screen, level_config, menu.selected_level, localization, language)
                menu.active = False
            elif menu.show_scores:
                scores_screen = ScoresScreen(screen, localization, language)
                menu.active = False
        elif scores_screen and scores_screen.active:
            scores_screen.run()
        elif scores_screen and not scores_screen.active:
            # Возвращаемся в меню
            menu.active = True
            menu.show_scores = False
            scores_screen = None
            screen = pygame.display.set_mode((800, 600))  # Размер для меню
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
