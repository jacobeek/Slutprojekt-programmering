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
        self.background_color = (0, 0, 0)
        self.render()

    def render(self):
        
        color = self.selected_color if self.selected else self.default_color
        self.image = self.font.render(self.text, True, color)
        self.rect = self.image.get_rect(center=self.center_pos)

        
    def draw(self, screen):
        self.render()
        screen.blit(self.image, self.rect)




class MainMenu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font("text/Pixeltype.ttf", 80)

        center_x = game.screen.get_width() // 2
        start_y = 400
        spacing = 90
        self.direction = 0

        self.items = [
            MenuItem("Start Game", self.font, (center_x, start_y)),
            MenuItem("Load Game", self.font, (center_x, start_y + spacing)),
            MenuItem("Settings", self.font, (center_x, start_y + 2 * spacing)),
            MenuItem("Quit", self.font, (center_x, start_y + 3 * spacing)),
        ]

        self.selected_index = 0
        self.items[self.selected_index].selected = True

    def move_selection(self):
        keys = pygame.key.get_pressed()
        direction = 0
        if keys[pygame.K_UP]: direction = -1
        if keys[pygame.K_DOWN]: direction = 1
    
    
    
        self.items[self.selected_index].selected = False
        self.selected_index = (self.selected_index + direction) % len(self.items)
        self.items[self.selected_index].selected = True

    def select(self):
        return self.selected_index

    def draw(self, screen):
        # Draw black rectangle behind menu
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, window_x, window_y))
        
        for item in self.items:
            item.draw(screen)

class PauseMenu(MainMenu):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font("text/Pixeltype.ttf", 80)

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
        self.items[self.selected_index].selected = True

    def move_selection(self):
        super().move_selection()
        
    def select(self):
        return super().select()
    
    def draw(self, screen):
        for item in self.items:
            item.draw(screen)
            

class SaveMenu(MainMenu):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font("text/Pixeltype.ttf", 80)

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
        self.items[self.selected_index].selected = True

    def move_selection(self):
        super().move_selection()
        
    def select(self):
        return super().select()
    
    def draw(self, screen):
        for item in self.items:
            item.draw(screen)