# menu.py

import pygame
import sys
from scoreboard import Scoreboard
from utils import adjust_font_size


class Menu:
    def __init__(self, screen, config):
        self.screen = screen
        self.config = config
        self.active = True
        self.selected_level = None
        self.show_scores = False  # Новое состояние
        self.font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 32)  # Новый шрифт для кнопок
        self.levels = list(config['levels'].keys())
        self.logo = pygame.image.load('assets/logo.png')
        max_logo_size = (300, 300)
        self.logo = pygame.transform.scale(self.logo, max_logo_size)
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.topright = (self.screen.get_width() - 50, 50)
        self.buttons = self.create_buttons()
        self.scoreboard = Scoreboard()

    def create_buttons(self):
        buttons = []
        button_width = 250  # Увеличиваем ширину кнопок
        button_height = 50
        button_x = 50
        for i, level in enumerate(self.levels):
            rect = pygame.Rect(button_x, 100 + i * 70, button_width, button_height)
            buttons.append((rect, level))
        # Добавляем кнопку для просмотра таблицы результатов
        scores_rect = pygame.Rect(button_x, 100 + len(self.levels) * 70, button_width, button_height)
        buttons.append((scores_rect, 'scores'))
        return buttons

    def run(self):
        self.handle_events()
        self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, action in self.buttons:
                    if rect.collidepoint(event.pos):
                        if action in self.levels:
                            self.selected_level = action
                        elif action == 'scores':
                            self.show_scores = True  # Переходим к экрану результатов

    def draw(self):
        self.screen.fill((200, 200, 200))
        mouse_pos = pygame.mouse.get_pos()
        for rect, action in self.buttons:
            # Проверяем, находится ли курсор мыши над кнопкой
            if rect.collidepoint(mouse_pos):
                color = (150, 150, 150)  # Более светлый цвет при наведении
            else:
                color = (100, 100, 100)
            pygame.draw.rect(self.screen, color, rect)

            if action in self.levels:
                text = action.capitalize()
            elif action == 'scores':
                text = 'Таблица результатов'

            # Используем функцию для подбора размера шрифта
            font, text_surface = adjust_font_size(
                text,
                None,
                36,
                rect.width - 10,  # Учитываем отступы
                rect.height - 10
            )

            # Центрируем текст внутри кнопки
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)
        self.screen.blit(self.logo, self.logo_rect)
        pygame.display.flip()

