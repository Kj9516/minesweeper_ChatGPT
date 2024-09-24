# language_selector.py

import pygame
import sys

class LanguageSelector:
    def __init__(self, screen, localization):
        self.screen = screen
        self.localization = localization
        self.active = True
        self.selected_language = None
        self.font = pygame.font.Font(None, 36)
        self.languages = self.localization['languages']
        self.buttons = self.create_buttons()

    def create_buttons(self):
        buttons = []
        button_width = 200
        button_height = 50
        total_height = len(self.languages) * (button_height + 20)
        start_y = (self.screen.get_height() - total_height) // 2
        for i, lang in enumerate(self.languages):
            rect = pygame.Rect(
                (self.screen.get_width() - button_width) // 2,
                start_y + i * (button_height + 20),
                button_width,
                button_height
            )
            buttons.append((rect, lang))
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
                for rect, lang in self.buttons:
                    if rect.collidepoint(event.pos):
                        self.selected_language = lang

    def draw(self):
        self.screen.fill((200, 200, 200))
        title_text = self.font.render(self.localization['ru']['select_language'], True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_text, title_rect)

        mouse_pos = pygame.mouse.get_pos()
        for rect, lang in self.buttons:
            if rect.collidepoint(mouse_pos):
                color = (150, 150, 150)
            else:
                color = (100, 100, 100)
            pygame.draw.rect(self.screen, color, rect)

            # Отображаем название языка (можно улучшить отображение)
            lang_text = self.font.render(lang.upper(), True, (255, 255, 255))
            lang_rect = lang_text.get_rect(center=rect.center)
            self.screen.blit(lang_text, lang_rect)

        pygame.display.flip()
