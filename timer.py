import pygame
import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.running = False
        self.font = pygame.font.Font(None, 36)

    def start(self):
        self.start_time = time.time()
        self.running = True

    def stop(self):
        if self.running:
            self.elapsed_time = int(time.time() - self.start_time)
            self.running = False

    def update(self):
        if self.running:
            self.elapsed_time = int(time.time() - self.start_time)

    def draw(self, screen, x, y):
        timer_text = self.font.render(f'Время: {self.elapsed_time}s', True, (0, 0, 0))
        screen.blit(timer_text, (x, y))
