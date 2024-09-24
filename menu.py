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
        for i, level in enumerate(self.levels):
            rect = pygame.Rect(50, 100 + i * 70, 200, 50)
            buttons.append((rect, level))
        # Добавляем кнопку для просмотра таблицы результатов
        scores_rect = pygame.Rect(50, 100 + len(self.levels) * 70, 200, 50)
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
                text = self.font.render(action.capitalize(), True, (255, 255, 255))
            elif action == 'scores':
                text = self.font.render('Таблица результатов', True, (255, 255, 255))
            self.screen.blit(text, (rect.x + 10, rect.y + 10))
        self.screen.blit(self.logo, self.logo_rect)
        pygame.display.flip()
