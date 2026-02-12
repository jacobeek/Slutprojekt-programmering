import pygame
from settings import window_x, window_y



class MenuItem:
    def __init__(self, text, font, center_pos):
        self.text = text
        self.font = font
        self.center_pos = center_pos
        self.selected = False
        self.default_color = (150, 150, 150)
        self.selected_color = (255, 255, 255)
        self.render()

    def select(self):
        """Select this item"""
        self.selected = True
        self.render()

    def deselect(self):
        """Deselect this item"""
        self.selected = False
        self.render()

    def render(self):
        color = self.selected_color if self.selected else self.default_color
        self.image = self.font.render(self.text, True, color)
        self.rect = self.image.get_rect(center=self.center_pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Menu:
    """Base menu class with selection management"""
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font("text/Pixeltype.ttf", 80)
        self.items = []
        self.selected_index = 0

    def move_selection(self, direction):
        """Move selection by direction (-1 up, 1 down)"""
        self.items[self.selected_index].deselect()
        self.selected_index = (self.selected_index + direction) % len(self.items)
        self.items[self.selected_index].select()

    def select(self):
        return self.selected_index

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, window_x, window_y))
        for item in self.items:
            item.draw(screen)


class MainMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        center_x = game.screen.get_width() // 2
        start_y = 400
        spacing = 90

        self.items = [
            MenuItem("Start Game", self.font, (center_x, start_y)),
            MenuItem("Load Game", self.font, (center_x, start_y + spacing)),
            MenuItem("Settings", self.font, (center_x, start_y + 2 * spacing)),
            MenuItem("Quit", self.font, (center_x, start_y + 3 * spacing)),
        ]

        self.selected_index = 0
        self.items[self.selected_index].select()

class PauseMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        center_x = game.screen.get_width() // 2
        start_y = 400
        spacing = 90

        self.items = [
            MenuItem("Resume", self.font, (center_x, start_y)),
            MenuItem("Main Menu", self.font, (center_x, start_y + spacing)),
            MenuItem("Save Game", self.font, (center_x, start_y + 2 * spacing)),
            MenuItem("Quit", self.font, (center_x, start_y + 3 * spacing)),
        ]
        self.selected_index = 0
        self.items[self.selected_index].select()
            

class SaveMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        center_x = game.screen.get_width() // 2
        start_y = 400
        spacing = 90

        self.items = [
            MenuItem("Save Slot 1", self.font, (center_x, start_y)),
            MenuItem("Save Slot 2", self.font, (center_x, start_y + spacing)),
            MenuItem("Save Slot 3", self.font, (center_x, start_y + 2 * spacing)),
            MenuItem("Back", self.font, (center_x, start_y + 3 * spacing)),
        ]
        self.selected_index = 0
        self.items[self.selected_index].select()