import json
import os
from datetime import datetime


class SaveManager:
    """Handle game saving and loading"""
    
    def __init__(self):
        # Create saves directory relative to project folder
        project_dir = os.path.dirname(os.path.abspath(__file__))
        self.SAVE_DIR = os.path.join(project_dir, "saves")
        
        # Create saves directory if it doesn't exist
        if not os.path.exists(self.SAVE_DIR):
            os.makedirs(self.SAVE_DIR)
    
    def save_game(self, game):
        """Save game state to JSON file with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        game_data = {
            "timestamp": timestamp,
            "kills": game.game_stats.kills if hasattr(game, 'game_stats') else 0,
            "health": int(game.player_sprite.health),
            "max_health": int(game.player_sprite.max_health),
            "time": game.game_timer(),
            "player": {
                "x": int(game.player_sprite.rect.centerx),
                "y": int(game.player_sprite.rect.centery),
            },
            "enemies": [
                {
                    "type": enemy.__class__.__name__,
                    "x": int(enemy.rect.centerx),
                    "y": int(enemy.rect.centery),
                }
                for enemy in game.enemy_group
            ]
        }
        
        filepath = os.path.join(self.SAVE_DIR, f"save_{timestamp}.json")
        try:
            with open(filepath, 'w') as f:
                json.dump(game_data, f, indent=2)
            print(f"Game saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"Error saving game: {e}")
            return None
    
    def load_game(self, filepath):
        """Load game state from JSON file"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Save file not found: {filepath}")
            return None
        except Exception as e:
            print(f"Error loading game: {e}")
            return None
    
    def get_all_saves(self):
        """Get list of all save files"""
        if not os.path.exists(self.SAVE_DIR):
            return []
        
        saves = []
        for filename in os.listdir(self.SAVE_DIR):
            if filename.endswith('.json'):
                filepath = os.path.join(self.SAVE_DIR, filename)
                saves.append(filepath)
        
        # Sort by modification time (newest first)
        saves.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return saves
    
    def get_latest_save(self):
        """Get the most recent save file"""
        saves = self.get_all_saves()
        return saves[0] if saves else None
        return os.path.exists(filepath)
    

