import pyautogui
import pygame
print(pyautogui.size())
pygame.init()

player_surf = pygame.image.load('player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(topleft=(400, 200))

print(player_rect(1))