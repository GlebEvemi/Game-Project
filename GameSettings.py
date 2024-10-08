import pyautogui
import pygame

pygame.init()

#Game setup
WIDTH, HEIGHT = pyautogui.size()
FPS = 60


#pLAYER SETTINGS
PLAYER_START_X = 400
PLAYER_START_Y = 200
PLAYER_SPEED = 6


#SLIME SETTINGS
SLIME_START_X = 1800
SLIME_START_Y = 800
SLIME_SPEED = [1, 2, 3, 4, 5]
slime_health_list = [100, 200]


#DIAMOND SETTINGS
DIAMOND_START_X = 900
DIAMOND_START_Y = 900
Purple_chance = 17
start_game_sound = pygame.mixer.Sound("sounds/start_game.wav")

#HEALTH_COLORS
GREEN = (0, 255, 0)
RED = (255, 0, 0)