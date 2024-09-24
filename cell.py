import pygame

class Cell:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(x * size, y * size, size, size)
        self.opened = False
        self.flagged = False
        self.has_mine = False
        self.adjacent_mines = 0
        self.font = pygame.font.Font(None, 24)

    def draw(self, screen):
        if self.opened:
            color = (200, 200, 200)
            if self.has_mine:
                color = (255, 0, 0)
            pygame.draw.rect(screen, color, self.rect)
            if self.adjacent_mines > 0 and not self.has_mine:
                text = self.font.render(str(self.adjacent_mines), True, (0, 0, 0))
                screen.blit(text, (self.rect.x + self.size / 4, self.rect.y + self.size / 4))
        else:
            pygame.draw.rect(screen, (100, 100, 100), self.rect)
            if self.flagged:
                pygame.draw.circle(screen, (255, 255, 0), self.rect.center, self.size / 4)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)
