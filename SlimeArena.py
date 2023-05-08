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

class Slime:
    def __init__(self, health = 100):
        self.health = health
        self.slime_surf = pygame.image.load('Test1.png').convert_alpha()
        self.slime_rect = self.slime_surf.get_rect(topleft = (random.randint(1930, 2100), random.randint(1080, 1200)))
    def movement(self):
        while Player.alive:
            distance_x = Player.player_rect(0) - self.slime_rect(0)
            distance_y = Player.player_rect(1) - self.slime_rect(1)
            distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

            # Move the enemy toward the player
            speed = 2
            if distance != 0:
                self.slime_rect[1] += speed * distance_x / distance
                self.slime_rect[2] += speed * distance_y / distance

Slimes = [Slime(), Slime(), Slime(), Slime(), Slime()]
                                                   

Player = Character()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        Player.player_rect.x -= 4
    if keys[pygame.K_d]:
        Player.player_rect.x += 4
    if keys[pygame.K_w]:
        Player.player_rect.y -= 4
    if keys[pygame.K_s]:
        Player.player_rect.y += 4
            
    
    screen.blit(bg_surf,(0,0))
    screen.blit(Player.player_surf, Player.player_rect)
    for slime in Slimes:
        screen.blit(slime.slime_surf, slime.slime_rect)
    slime.movement()



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