import pygame
from sys import exit
import random
import pyautogui




pygame.init()
screen = pygame.display.set_mode(pyautogui.size())
pygame.display.set_caption("SlimeArena")
clock = pygame.time.Clock()

bg_surf = pygame.image.load('nature.png').convert()

class Character:
    def __init__(self, health = 100):
        self.health = health
        self.alive = True
        self.player_surf = pygame.image.load('player_walk_1.png').convert_alpha()
        self.player_rect = self.player_surf.get_rect(topleft=(400, 200))
Player = Character()

class Slime:
    def __init__(self, health = 100):
        self.health = health
        self.slime_surf = pygame.image.load('Test1.png').convert_alpha()
        self.slime_rect = self.slime_surf.get_rect(topleft =(800, 800))
    def movement(self):
        distance_x = Player.player_rect.x - self.slime_rect.x
        distance_y = Player.player_rect.y - self.slime_rect.y
        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
        speed = 1
        if distance != 0:
            self.slime_rect.x += speed * distance_x / distance
            self.slime_rect.y += speed * distance_y / distance

slime1 = Slime()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(bg_surf,(0,0))
    slime1.movement()
    screen.blit(slime1.slime_surf, slime1.slime_rect)

    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
            Player.player_rect.x -= 4
    if keys[pygame.K_d]:
            Player.player_rect.x += 4
    if keys[pygame.K_w]:
            Player.player_rect.y -= 4
    if keys[pygame.K_s]:
            Player.player_rect.y += 4
        
    screen.blit(Player.player_surf, Player.player_rect)



    """ screen.blit(ground_surface,(0,300))
    pygame.draw.rect(screen, '#c0e8ec', score_rect)
    
    screen.blit(score_surf,score_rect) """


    """ if snail_rect.x < -100:
        snail_rect.x = 800
    snail_rect.x -= 4 """
    #screen.blit(snail_surf, snail_rect)
    """ if player_rect.colliderect(snail_rect):
        print('collision') """
    """ mouse_pos = pygame.mouse.get_pos()
    if player_rect.collidepoint(mouse_pos):
        print(pygame.mouse.get_pressed()) """
    
    pygame.display.update()
    clock.tick(60)