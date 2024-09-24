# menu.py

import pygame
import sys
from scoreboard import Scoreboard

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, action in self.buttons:
                    if rect.collidepoint(event.pos):
                        if action in self.levels:
                            self.selected_level = action
                        elif action == 'scores':
                            self.show_scores = True  # Переходим к экрану результатов

    def draw(self):
        self.screen.fill((200, 200, 200))
        for rect, action in self.buttons:
            pygame.draw.rect(self.screen, (100, 100, 100), rect)
            if action in self.levels:
                text = self.button_font.render(action.capitalize(), True, (255, 255, 255))
            elif action == 'scores':
                text = self.button_font.render('Таблица результатов', True, (255, 255, 255))
            # Центрируем текст внутри кнопки
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
        self.screen.blit(self.logo, self.logo_rect)
        pygame.display.flip()
