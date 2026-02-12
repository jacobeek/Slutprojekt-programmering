import pygame
from settings import window_x, window_y
import json
from save_manager import SaveManager
import os



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
            MenuItem("New Game", self.font, (center_x, start_y)),
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
            MenuItem("Save Game", self.font, (center_x, start_y + spacing)),
            MenuItem("Main Menu", self.font, (center_x, start_y + 2 * spacing)),
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
            MenuItem("Save Game", self.font, (center_x, start_y)),
            MenuItem("Back", self.font, (center_x, start_y + spacing)),
        ]
        self.selected_index = 0
        self.items[self.selected_index].select()
        
        
class LoadMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.save_manager = SaveManager()  # Create save manager FIRST
        self.items = []
        self.save_files = []
        self.refresh_saves()  # Then call refresh_saves
        
        if not self.items:
            # No saves, show empty state
            center_x = game.screen.get_width() // 2
            self.items = [MenuItem("No saves found", self.font, (center_x, 400))]
        
        self.selected_index = 0
        if self.items:
            self.items[self.selected_index].select()
    
    def refresh_saves(self):
        """Load available saves and populate menu items"""
        self.items = []
        self.save_files = []
        
        center_x = self.game.screen.get_width() // 2
        start_y = 300
        spacing = 80
        
        # Get all save files from save manager
        saves = self.save_manager.get_all_saves()
        
        for idx, save_path in enumerate(saves):
            try:
                with open(save_path, 'r') as f:
                    save_data = json.load(f)
                    
                # Create display text with save info
                timestamp = save_data.get("timestamp", "Unknown")
                kills = save_data.get("kills", 0)
                health = int(save_data.get("health", 0))
                game_time = save_data.get("time", 0)
                
                # Format: "2026-02-12_14:30:45 | Kills: 25 | Health: 4 | Time: 120s"
                display_text = f"{timestamp} | Kills: {kills} | HP: {health} | Time: {game_time}s"
                
                menu_item = MenuItem(display_text, self.font, (center_x, start_y + idx * spacing))
                self.items.append(menu_item)
                self.save_files.append(save_path)
            except Exception as e:
                print(f"Error loading save info: {e}")
        
        # Add "Back" option
        back_y = start_y + len(self.items) * spacing
        back_item = MenuItem("Back", self.font, (center_x, back_y))
        self.items.append(back_item)
        self.save_files.append(None)  # None indicates "Back" option
    
    def get_selected_save(self):
        """Get the filepath of the selected save, or None if 'Back' is selected"""
        if self.selected_index < len(self.save_files):
            return self.save_files[self.selected_index]
        return None
        
