import pygame
import sys
from cell import Cell
from timer import Timer
from scoreboard import Scoreboard
import random
from utils import adjust_font_size


class Game:
    def __init__(self, screen, level_config, level_name, localization, language):
        self.screen = screen
        self.width = level_config['width']
        self.height = level_config['height']
        self.mines_count = level_config['mines']
        self.level_name = level_name
        self.localization = localization
        self.language = language
        self.cell_size = 30
        self.cells = []
        self.first_click = True
        self.game_over = False
        self.victory = False
        self.back_to_menu = False
        self.font = pygame.font.Font(None, 36)
        self.timer = Timer(self.localization, self.language)
        self.scoreboard = Scoreboard()
        self.create_cells()
        self.field_width = self.width * self.cell_size
        self.field_height = self.height * self.cell_size
        self.side_panel_width = 200
        self.play_again_rect = None
        self.menu_rect = None

    def setup_game_over_buttons(self):
        button_width = 180
        button_height = 50
        button_x = self.field_width + 20
        self.play_again_rect = pygame.Rect(button_x, 100, button_width, button_height)
        self.menu_rect = pygame.Rect(button_x, 160, button_width, button_height)

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
                            # Открываем первую ячейку после установки мин
                            if not cell.flagged:
                                self.open_cell(cell_x, cell_y)
                        else:
                            if not cell.flagged:
                                self.open_cell(cell_x, cell_y)
                    elif event.button == 3:
                        if not cell.opened:
                            cell.flagged = not cell.flagged
            elif self.game_over and event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_again_rect and self.play_again_rect.collidepoint(event.pos):
                    self.__init__(self.screen, {
                        'width': self.width,
                        'height': self.height,
                        'mines': self.mines_count
                    }, self.level_name, self.localization, self.language)
                elif self.menu_rect and self.menu_rect.collidepoint(event.pos):
                    self.back_to_menu = True

    def place_mines(self, exclude_x, exclude_y):
        positions = [(x, y) for x in range(self.width) for y in range(self.height)]
        # Исключаем нажатую ячейку и её соседей
        excluded_positions = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = exclude_x + dx, exclude_y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    excluded_positions.append((nx, ny))
        positions = [pos for pos in positions if pos not in excluded_positions]
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
        self.game_over = True
        self.timer.stop()
        self.setup_game_over_buttons()

    def check_victory(self):
        opened_cells = sum(cell.opened for row in self.cells for cell in row)
        if opened_cells == self.width * self.height - self.mines_count:
            self.victory = True
            self.game_over = True
            self.timer.stop()
            # Сохраняем только победные результаты
            self.scoreboard.save_score(
                self.level_name,
                self.width,
                self.height,
                self.mines_count,
                self.timer.elapsed_time
            )
            self.setup_game_over_buttons()

    def update(self):
        if not self.game_over and not self.first_click:
            self.timer.update()

    def draw(self):
        self.screen.fill((255, 255, 255))
        # Рисуем игровое поле
        for row in self.cells:
            for cell in row:
                cell.draw(self.screen)
        # Рисуем таймер в боковой панели
        self.timer.draw(self.screen, self.field_width + 20, 10)
        if self.game_over:
            self.draw_game_over()
        pygame.display.flip()

    def draw_game_over(self):
        message_key = 'victory' if self.victory else 'defeat'
        message = self.localization[self.language][message_key]
        text = self.font.render(message, True, (255, 0, 0))
        self.screen.blit(text, (self.field_width + 20, 50))

        mouse_pos = pygame.mouse.get_pos()

        # Обработка кнопки "Играть заново"
        if self.play_again_rect.collidepoint(mouse_pos):
            color = (0, 200, 0)
        else:
            color = (0, 255, 0)
        pygame.draw.rect(self.screen, color, self.play_again_rect)

        # Обработка кнопки "Выход в меню"
        if self.menu_rect.collidepoint(mouse_pos):
            color = (0, 0, 200)
        else:
            color = (0, 0, 255)
        pygame.draw.rect(self.screen, color, self.menu_rect)

        # Текст кнопок
        play_again_text = self.localization[self.language]['play_again']
        menu_text = self.localization[self.language]['exit_to_menu']

        # Подбираем размер шрифта для текста кнопок
        font, play_again_surface = adjust_font_size(
            play_again_text,
            None,
            28,
            self.play_again_rect.width - 10,
            self.play_again_rect.height - 10
        )
        font, menu_surface = adjust_font_size(
            menu_text,
            None,
            28,
            self.menu_rect.width - 10,
            self.menu_rect.height - 10
        )

        # Центрируем текст внутри кнопок
        play_again_text_rect = play_again_surface.get_rect(center=self.play_again_rect.center)
        menu_text_rect = menu_surface.get_rect(center=self.menu_rect.center)

        self.screen.blit(play_again_surface, play_again_text_rect)
        self.screen.blit(menu_surface, menu_text_rect)

