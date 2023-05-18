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
#Set up health bar font
font = pygame.font.SysFont("Times New Roman", 24)

#Set up score
score = 0

#Function to update the health bar
def update_health_bar():
    #Render the health bar text
    health_text = font.render(f"Health: {Player.health}", True, (0, 0, 0))
    screen.blit(health_text, (1000, 10))

#Function to update the score
def update_score():
    #Render the score text
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (1000, 40))

slime1 = Slime()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if Player.player_rect.colliderect(slime1.slime_rect):
        score += 10

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
    update_health_bar()
    update_score()
    
    pygame.display.update()
    clock.tick(60)