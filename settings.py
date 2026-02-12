import pygame
#settings for game window size
#be aware, a smaller screen makes the game harder, and a bigger easier
window_x, window_y = 1920, 1080 



game_state = "start"
kills = 0
fire_rate = 20
last_shot_time = 0
enemy_type = "ghost"
shooting = False
