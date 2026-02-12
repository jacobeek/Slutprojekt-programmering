import pygame
from random import randint
from settings import window_x, window_y
from game import GameStats

class Enemy(pygame.sprite.Sprite):
    kills = 0
    def __init__(self, player_sprite, bullets):
        super().__init__()
        
        self.player_sprite = player_sprite

        #images and sounds
        self.hit_sound = pygame.mixer.Sound("sounds/bullet_hit_sound.mp3")
        self.hit_sound.set_volume(0.1)

        #settings
        self.time = 0
        self.bullet = bullets
        
        #enemy spawn position
    
    def spawn(self):
        self.player = self.player_sprite
        self.player_pos = pygame.Vector2(self.player.rect.center)
        
        #randomize where the ghost should spawn
        if randint(0,1) == 0:
            if self.player_pos.x < window_x/2:
                self.spawn_x = window_x + 80
                self.spawn_y = randint(0,window_y) 

            else:
                self.spawn_x = -80
                self.spawn_y = randint(0,window_y)
        else:
            if self.player_pos.y > window_y/2:
                self.spawn_x = randint(0,window_x) 
                self.spawn_y = -80

            else:
                self.spawn_x = randint(0,window_x) 
                self.spawn_y = window_y + 80

        self.rect = self.image.get_rect(center=(self.spawn_x, self.spawn_y))    


    def pathing(self):
        #pathing for the enemies
        enemy_pos = pygame.Vector2(self.rect.center)
        player_pos = pygame.Vector2(self.player.rect.center)

        direction = player_pos - enemy_pos
        if direction.length() > 0:
            direction = direction.normalize()

        self.rect.x += direction.x * self.speed
        self.rect.y += direction.y * self.speed

    def hp(self, bullets):
        #health points
        if pygame.sprite.spritecollide(self, bullets, True): 
            self.health -= 1
            self.hit_sound.play()
        if self.health <= 0:
            GameStats.kills += 1
            self.kill()
              
            

    def update(self, bullets):
        #update all the methods every tick
        self.pathing()
        return self.hp(bullets)

class Ghost(Enemy):
    def __init__(self, player_sprite, bullets):
        super().__init__(player_sprite, bullets)
        
        self.image = pygame.image.load("images/ghost.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80,120))
        
        self.speed = 3
        self.health = 3
        self.spawn()

        self.player_sprite = player_sprite

    def pathing(self):
        return super().pathing()
    def hp(self, bullets):
        return super().hp(bullets)
    def spawn(self):
        return super().spawn()
    def update(self, bullets):
        return super().update(bullets)
    
class Fireball(Enemy):
    def __init__(self, player_sprite, bullets):
        super().__init__(player_sprite, bullets)

        self.image = pygame.image.load("images/fire_ball.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150,150))
        self.speed = 2
        self.health = 5
        self.spawn()

        self.player_sprite = player_sprite

    def pathing(self):
        return super().pathing()
    def hp(self, bullets):
        return super().hp(bullets)
    def spawn(self):
        return super().spawn()
    def update(self, bullets):
        return super().update(bullets)
    