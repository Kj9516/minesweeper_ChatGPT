# scores_screen.py

import pygame
import sys
from scoreboard import Scoreboard

class ScoresScreen:
    def __init__(self, screen):
        self.screen = screen
        self.active = True
        self.font = pygame.font.Font(None, 24)
        self.scoreboard = Scoreboard()
        self.back_button = pygame.Rect(50, 500, 100, 40)

    def run(self):
        self.handle_events()
        self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_button.collidepoint(event.pos):
                    self.active = False  # Возвращаемся в главное меню

    def draw(self):
        self.screen.fill((255, 255, 255))
        title = self.font.render('Лучшие результаты', True, (0, 0, 0))
        self.screen.blit(title, (50, 20))

        scores = self.scoreboard.load_scores()
        for idx, score in enumerate(scores):
            date_time = score['datetime']
            level = score['level']
            width = score['width']
            height = score['height']
            mines = score['mines']
            time_spent = score['time']
            score_text = f"{idx + 1}. {date_time} - Уровень: {level}, Поле: {width}x{height}, Мины: {mines}, Время: {time_spent}s"
            text_surface = self.font.render(score_text, True, (0, 0, 0))
            self.screen.blit(text_surface, (50, 60 + idx * 30))

        pygame.draw.rect(self.screen, (100, 100, 100), self.back_button)
        back_text = self.font.render('Назад', True, (255, 255, 255))
        self.screen.blit(back_text, (self.back_button.x + 10, self.back_button.y + 10))

        pygame.display.flip()
