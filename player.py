import pygame
from settings import *



class Player(pygame.sprite.Sprite):
    def __init__(self, enemy): 
        super().__init__()
        #images and sounds
        self.image_normal = pygame.image.load("images/player_walk_1.png").convert_alpha()
        self.image_hit = pygame.image.load("images/player_walk_1_hit.png").convert_alpha()
        self.image = self.image_normal 
        self.rect = self.image.get_rect(midbottom = (200,300))
        self.hit_sound = pygame.mixer.Sound("sounds/hit.mp3")
        self.hit_sound.set_volume(5)
        
        #settings for player
        self.x_vel = 0
        self.y_vel = 0
        self.speed = 5
        self.health = 5
        self.max_health = 5

        self.enemy = enemy 
        self.invis_frames = 0

    def player_input(self):
        #inputs
        self.x_vel = 0
        self.y_vel = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y_vel = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y_vel = self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x_vel = self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x_vel = -self.speed
    
    def collition(self):
        #prevent the character from going off screen
        if self.rect.bottom > window_y:
            self.rect.bottom = window_y
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > window_x:
            self.rect.right = window_x 
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

    def hp(self, enemy):
        #invincebility frames
        if self.invis_frames <= 0:
            if pygame.sprite.spritecollide(self, enemy, False): 
                self.health -= 1
                self.image = self.image_hit    
                self.hit_sound.play()
                
                self.invis_frames = 60
        
        #flashes an animation if the player is hit
        if self.invis_frames <= 45:
            self.image = self.image_normal
        if self.invis_frames <= 30:
            self.image = self.image_hit 
        if self.invis_frames <= 15:
            self.image = self.image_normal
        self.invis_frames -= 1
        
        #if the character runs out of hp
        if self.health <= 0:
            self.kill()

    def update(self, enemy):
        #updaes all the methods every tick
        self.player_input()
        self.collition()
        self.hp(enemy)