# scores_screen.py

import pygame
import sys
from scoreboard import Scoreboard
from utils import adjust_font_size


class ScoresScreen:
    def __init__(self, screen):
        self.screen = screen
        self.active = True
        self.font = pygame.font.Font(None, 24)
        self.button_font = pygame.font.Font(None, 28)  # Шрифт для кнопки
        self.scoreboard = Scoreboard()
        self.back_button = pygame.Rect(50, 500, 120, 40)  # Увеличиваем ширину кнопки

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

        mouse_pos = pygame.mouse.get_pos()
        if self.back_button.collidepoint(mouse_pos):
            color = (150, 150, 150)
        else:
            color = (100, 100, 100)
        pygame.draw.rect(self.screen, color, self.back_button)

        back_text = 'Назад'
        font, back_surface = adjust_font_size(
            back_text,
            None,
            28,
            self.back_button.width - 10,
            self.back_button.height - 10
        )
        back_text_rect = back_surface.get_rect(center=self.back_button.center)
        self.screen.blit(back_surface, back_text_rect)

        pygame.display.flip()

