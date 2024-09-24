import pygame
import sys
from cell import Cell
from timer import Timer
from scoreboard import Scoreboard
import random

class Game:
    def __init__(self, screen, level_config):
        self.screen = screen
        self.width = level_config['width']
        self.height = level_config['height']
        self.mines_count = level_config['mines']
        self.cell_size = 30
        self.cells = []
        self.first_click = True
        self.game_over = False
        self.victory = False
        self.back_to_menu = False
        self.font = pygame.font.Font(None, 36)
        self.timer = Timer()
        self.scoreboard = Scoreboard()
        self.create_cells()

    def create_cells(self):
        for y in range(self.height):
            row = []
            for x in range(self.width):
                cell = Cell(x, y, self.cell_size)
                row.append(cell)
            self.cells.append(row)

    def run(self):
        self.handle_events()
        self.update()
        self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif not self.game_over and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                cell_x = x // self.cell_size
                cell_y = y // self.cell_size
                if cell_x < self.width and cell_y < self.height:
                    cell = self.cells[cell_y][cell_x]
                    if event.button == 1:
                        if self.first_click:
                            self.first_click = False
                            self.timer.start()
                            self.place_mines(cell_x, cell_y)
                            self.calculate_adjacent_mines()
                        if not cell.flagged:
                            self.open_cell(cell_x, cell_y)
                    elif event.button == 3:
                        if not cell.opened:
                            cell.flagged = not cell.flagged
            elif self.game_over and event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_again_rect.collidepoint(event.pos):
                    self.__init__(self.screen, {
                        'width': self.width,
                        'height': self.height,
                        'mines': self.mines_count
                    })
                elif self.menu_rect.collidepoint(event.pos):
                    self.back_to_menu = True

    def place_mines(self, exclude_x, exclude_y):
        positions = [(x, y) for x in range(self.width) for y in range(self.height)]
        positions.remove((exclude_x, exclude_y))
        mines = random.sample(positions, self.mines_count)
        for x, y in mines:
            self.cells[y][x].has_mine = True

    def calculate_adjacent_mines(self):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.cells[y][x]
                if not cell.has_mine:
                    mines = self.count_adjacent_mines(x, y)
                    cell.adjacent_mines = mines

    def count_adjacent_mines(self, x, y):
        mines = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if (dx != 0 or dy != 0) and 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.cells[ny][nx].has_mine:
                        mines += 1
        return mines

    def open_cell(self, x, y):
        cell = self.cells[y][x]
        if cell.opened or cell.flagged:
            return
        cell.opened = True
        if cell.has_mine:
            self.game_over = True
            self.timer.stop()
            self.reveal_mines()
        elif cell.adjacent_mines == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if (dx != 0 or dy != 0) and 0 <= nx < self.width and 0 <= ny < self.height:
                        self.open_cell(nx, ny)
        self.check_victory()

    def reveal_mines(self):
        for row in self.cells:
            for cell in row:
                if cell.has_mine:
                    cell.opened = True

    def check_victory(self):
        opened_cells = sum(cell.opened for row in self.cells for cell in row)
        if opened_cells == self.width * self.height - self.mines_count:
            self.victory = True
            self.game_over = True
            self.timer.stop()
            self.scoreboard.save_score(self.timer.elapsed_time)

    def update(self):
        if not self.game_over and not self.first_click:
            self.timer.update()

    def draw(self):
        self.screen.fill((255, 255, 255))
        for row in self.cells:
            for cell in row:
                cell.draw(self.screen)
        self.timer.draw(self.screen)
        if self.game_over:
            self.draw_game_over()
        pygame.display.flip()

    def draw_game_over(self):
        message = 'Победа!' if self.victory else 'Поражение!'
        text = self.font.render(message, True, (255, 0, 0))
        self.screen.blit(text, (self.width * self.cell_size + 20, 50))

        self.play_again_rect = pygame.Rect(self.width * self.cell_size + 20, 100, 150, 50)
        self.menu_rect = pygame.Rect(self.width * self.cell_size + 20, 160, 150, 50)

        pygame.draw.rect(self.screen, (0, 255, 0), self.play_again_rect)
        pygame.draw.rect(self.screen, (0, 0, 255), self.menu_rect)

        play_again_text = self.font.render('Играть заново', True, (255, 255, 255))
        menu_text = self.font.render('Выход в меню', True, (255, 255, 255))

        self.screen.blit(play_again_text, (self.play_again_rect.x + 10, self.play_again_rect.y + 10))
        self.screen.blit(menu_text, (self.menu_rect.x + 10, self.menu_rect.y + 10))
