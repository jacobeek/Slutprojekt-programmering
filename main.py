import pygame
from sys import exit
from random import randint
import math
import csv


from settings import *
from player import Player
from gun import Gun
from bullet import Bullet
from enemy import Ghost, Fireball
from game import GameStats
from menu import MainMenu, PauseMenu


class Game:
    def __init__(self):
        # pygame core
        pygame.init()
        self.screen = pygame.display.set_mode((window_x, window_y))
        pygame.display.set_caption("Träskigt värre")
        self.clock = pygame.time.Clock()

        # state
        self.game_state = "menu"
        self.menu_state = "main_menu" 
        self.shooting = False
        self.last_shot_time = 0
        #menu timer
        self.action_locked = False
        self.last_action_time = 0
        self.action_cooldown = 500

        self.start_time = pygame.time.get_ticks()

        # groups
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        # player
        self.player_sprite = Player(self.enemy_group)
        self.player = pygame.sprite.GroupSingle(self.player_sprite)

        # gun
        self.gun_sprite = Gun(self.player_sprite)
        self.gun = pygame.sprite.GroupSingle(self.gun_sprite)

        # menu
        self.main_menu = MainMenu(self)
        self.pause_menu = PauseMenu(self)
        # sounds
        self.bullet_shot_sound = pygame.mixer.Sound("sounds/gun_shot.mp3")
        self.bullet_shot_sound.set_volume(0.2)

        # graphics
        self.background_surf = pygame.image.load("images/background.jpg").convert_alpha()

        self.text_font = pygame.font.Font("text/Pixeltype.ttf", 100)
        self.goal_text = self.text_font.render("Goal: 50 points", False, "White")
        self.goal_text_rect = self.goal_text.get_rect(center=(window_x - 300, 200))
        
        # game stats
        self.game_stats = GameStats()
        
    # -------------------- utility -------------------- #

    def draw_start_screen(self, screen):
        text = self.text_font.render("Welcome to Haunted Swamp", False, "White")
        subtext = self.text_font.render("Click to Start", False, "White")
        screen.blit(text, text.get_rect(center=(window_x // 2, 400)))
        screen.blit(subtext, subtext.get_rect(center=(window_x // 2, 500)))

    def draw_win_screen(self, screen):
        screen.fill((0, 0, 0))
        text = self.text_font.render("You Win!", False, "Green")
        subtext = self.text_font.render("Press R to Restart or ESC to Quit", False, "White")
        screen.blit(text, text.get_rect(center=(window_x // 2, 400)))
        screen.blit(subtext, subtext.get_rect(center=(window_x // 2, 500)))

    def draw_lose_screen(self, screen):
        screen.fill((0, 0, 0))
        text = self.text_font.render("Game Over", False, "Red")
        subtext = self.text_font.render("Press R to Retry or ESC to Quit", False, "White")
        screen.blit(text, text.get_rect(center=(window_x // 2, 400)))
        screen.blit(subtext, subtext.get_rect(center=(window_x // 2, 500)))

    def draw_menu_screen(self, screen):
        self.main_menu.draw(screen)
    
    def draw_pause_menu(self, screen):
        self.pause_menu.draw(screen)
    
    def render_kill_counter(self, kills):
        text_kills_surf = self.text_font.render(f"Points: {kills}", False, "White")
        text_kills_rect = text_kills_surf.get_rect(center=(window_x - 300, 100))
        return text_kills_surf, text_kills_rect
    
    def render_health_bar(self, screen, player_health, max_health=5):
        # Bar dimensions
        bar_width = 200
        bar_height = 30
        bar_x = 20
        bar_y = 20
        
        # Calculate health percentage and width
        health_percentage = max(0, min(100, (player_health / max_health) * 100))
        filled_width = int((health_percentage / 100) * bar_width)
        
        # Draw background (empty bar)
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
        
        # Draw filled health bar (green to red gradient based on health)
        if health_percentage > 50:
            color = (0, 255, 0)  # Green
        elif health_percentage > 25:
            color = (255, 255, 0)  # Yellow
        else:
            color = (255, 0, 0)  # Red
        
        pygame.draw.rect(screen, color, (bar_x, bar_y, filled_width, bar_height))
        
        # Draw border
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Draw health text
        font = pygame.font.Font("text/Pixeltype.ttf", 24)
        health_text = font.render(f"HP: {int(player_health)}/{max_health}", False, "White")
        screen.blit(health_text, (bar_x + 10, bar_y + 35))
    
    def game_timer(self):
        return (pygame.time.get_ticks() - self.start_time) // 1000

    def spawn_rate(self, kills):
        time = self.game_timer()
        if randint(0, 1000 + int(2 * math.sqrt(time))) > 990:

            if kills < 15:
                spawn_type = 0
            else:
                spawn_type = randint(0, 1)

            if spawn_type == 0:
                enemy = Ghost(self.player_sprite, self.gun_sprite)
            else:
                enemy = Fireball(self.player_sprite, self.gun_sprite)

            self.enemy_group.add(enemy)

    # -------------------- state resets --------------------

    def reset_game(self):
        GameStats.kills = 0
        self.player_sprite.max_health = 5
        self.player_sprite.health = 5
        self.enemy_group.empty()
        self.bullet_group.empty()
        self.start_time = pygame.time.get_ticks()
    # -------------------- main loop --------------------

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(60)

    #--------------------- handle actions ---------------------#
    
    def can_trigger_action(self):
        now = pygame.time.get_ticks()
        if now - 50 >= self.last_action_time:
            self.last_action_time = pygame.time.get_ticks()
            return True
        
    # -------------------- event handling --------------------

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            
            
            
            #pause menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.can_trigger_action():
                    if self.game_state == "playing": 
                        self.menu_state = "pause_menu"
                        self.game_state = "menu"
                    else: self.game_state = "playing"

            
            #main menu
            if self.menu_state == "main_menu" and event.type == pygame.KEYDOWN:
                if self.can_trigger_action():
                    self.main_menu.move_selection()
                    if event.key == pygame.K_RETURN:
                        if self.main_menu.selected_index == 0: 
                            self.game_state = "playing"
                            self.reset_game()
                        if self.main_menu.selected_index == 1:
                            pass # options menu not implemented 
                        if self.main_menu.selected_index == 2:
                            pass # credits menu not implemented
                        
                        if self.main_menu.selected_index == 3:
                            pygame.quit()
                            exit()
            
            
                        
            if self.menu_state == "pause_menu" and event.type == pygame.KEYDOWN:
                if self.can_trigger_action():
                    self.pause_menu.move_selection()
                    if event.key == pygame.K_RETURN:
                        if self.pause_menu.selected_index == 0: 
                            self.game_state = "playing"
                        if self.pause_menu.selected_index == 1:
                            self.game_state = "menu"
                        if self.pause_menu.selected_index == 2:
                            pass # save game not implemented
                        
                        if self.pause_menu.selected_index == 3:
                            pygame.quit()
                            exit()

                
            if self.game_state == "start":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.game_state = "playing"
                    self.reset_game()

            elif self.game_state == "playing":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.shooting = True
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.shooting = False

            elif self.game_state in ("win", "lose"):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.game_state = "playing"

                        # recreate player & gun
                        self.player_sprite = Player(self.enemy_group)
                        self.player = pygame.sprite.GroupSingle(self.player_sprite)

                        self.gun_sprite = Gun(self.player_sprite)
                        self.gun = pygame.sprite.GroupSingle(self.gun_sprite)

                        self.reset_game()

                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

    # -------------------- update --------------------

    def update(self):
        if self.game_state != "playing":
            return

        # shooting
        if self.shooting:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= fire_rate:
                bullet = Bullet(self.gun_sprite)
                self.bullet_group.add(bullet)
                self.bullet_shot_sound.play()
                self.last_shot_time = current_time

        # spawn enemies
        self.spawn_rate(GameStats.kills)

        # updates
        self.player.update(self.enemy_group)
        self.gun.update()
        self.bullet_group.update()
        self.enemy_group.update(self.bullet_group)
        
        # win / lose
        if GameStats.kills >= 50:
            self.game_state = "win"
        if self.player_sprite.health <= 0:
            self.game_state = "lose"

    # -------------------- draw --------------------

    def draw(self):
        

        if self.game_state == "playing":
            self.screen.blit(self.background_surf, (0, 0))

            self.render_health_bar(self.screen, self.player_sprite.health, self.player_sprite.max_health)

            kills_surf, kills_rect = self.render_kill_counter(GameStats.kills)
            self.screen.blit(kills_surf, kills_rect)
            self.screen.blit(self.goal_text, self.goal_text_rect)

            self.player.draw(self.screen)
            self.gun.draw(self.screen)
            self.bullet_group.draw(self.screen)
            self.enemy_group.draw(self.screen)

        elif self.game_state == "win":
            self.draw_win_screen(self.screen)

        elif self.game_state == "lose":
            self.draw_lose_screen(self.screen)

        elif self.game_state == "menu":
            self.draw_menu_screen(self.screen)

        elif self.game_state == "pause_menu":
            self.draw_pause_menu(self.screen)

if __name__ == "__main__":
    game = Game()
    game.run()