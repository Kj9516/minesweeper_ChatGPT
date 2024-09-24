import sys

import pygame

class Menu:
    def __init__(self, screen, config):
        self.screen = screen
        self.config = config
        self.active = True
        self.selected_level = None
        self.font = pygame.font.Font(None, 36)
        self.levels = list(config['levels'].keys())
        self.logo = pygame.image.load('assets/logo.png')
        # Масштабируем логотип, если он слишком большой
        max_logo_size = (300, 300)
        self.logo = pygame.transform.scale(self.logo, max_logo_size)
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.topright = (self.screen.get_width() - 50, 50)
        self.buttons = self.create_buttons()

    def create_buttons(self):
        buttons = []
        for i, level in enumerate(self.levels):
            rect = pygame.Rect(50, 100 + i * 70, 200, 50)
            buttons.append((rect, level))
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
                for rect, level in self.buttons:
                    if rect.collidepoint(event.pos):
                        self.selected_level = level

    def draw(self):
        self.screen.fill((200, 200, 200))
        for rect, level in self.buttons:
            pygame.draw.rect(self.screen, (100, 100, 100), rect)
            text = self.font.render(level.capitalize(), True, (255, 255, 255))
            self.screen.blit(text, (rect.x + 50, rect.y + 10))
        self.screen.blit(self.logo, self.logo_rect)
        pygame.display.flip()
