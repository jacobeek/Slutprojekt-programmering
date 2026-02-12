import pygame
import math


class Gun(pygame.sprite.Sprite):
    def __init__(self, player_sprite):
        super().__init__()
        #images and sounds
        self.original_image = pygame.image.load("images/gun.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image , (100, 85))
        
        self.image = self.original_image
        self.player = player_sprite
        self.offset = pygame.Vector2(0,20)
        self.rect = self.image.get_rect(center=self.player.rect.center + self.offset)
    
    def aim(self):
        gun_pos = self.player.rect.center + self.offset #get gun position
        mouse_pos = pygame.mouse.get_pos() #get mouse position
        
        #get the angle to the mouse (in degrees)
        dx = mouse_pos[0] - gun_pos[0]
        dy = mouse_pos[1] - gun_pos[1]
        angle = -math.degrees(math.atan2(dy, dx))
        self.image = pygame.transform.rotate(self.original_image, angle) #rotate the gun
        self.rect = self.image.get_rect(center=gun_pos) #update rect and keep center consistent
    
    def update(self):
    #update all methods every tick
        self.aim()