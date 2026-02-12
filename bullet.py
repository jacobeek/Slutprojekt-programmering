import pygame
from settings import window_x, window_y

class Bullet(pygame.sprite.Sprite):
    def __init__(self, gun_sprite):
        super().__init__()
        #images and sounds       
        self.image = pygame.image.load("images/ammo.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (12, 12))
    
        self.gun = gun_sprite 
        self.rect = self.image.get_rect(center=self.gun.rect.center)
        

        #informatiom for bullet direction

        self.speed = 40  # bullet speed
        self.direction = pygame.Vector2(0, 0)  # no movemnt
        mouse_pos = pygame.mouse.get_pos() #mouse position
        bullet_pos = pygame.Vector2(self.rect.center) # bullet position
        self.direction = pygame.Vector2(mouse_pos) - bullet_pos #calculate direction
        if self.direction.length() != 0: #ingen aning vad denna delen gör
            self.direction = self.direction.normalize()
    
    def shoot(self):
        # shoot in the direction
        if self.direction.length() != 0:
            self.rect.centerx += self.direction.x * self.speed
            self.rect.centery += self.direction.y * self.speed
        
        #remove the bullet if it goes off screen
        if self.rect.right < 0 or self.rect.left > window_x or self.rect.bottom < 0 or self.rect.top > window_y:
            self.kill()
    
    def update(self):
        self.shoot()