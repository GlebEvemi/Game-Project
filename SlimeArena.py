import pygame
from sys import exit
from pygame.locals import *
import random
import pyautogui
import time
import math

pygame.init()
screen = pygame.display.set_mode(pyautogui.size())
screen_width, screen_height = pyautogui.size()
pygame.display.set_caption("SlimeArena")
clock = pygame.time.Clock()
#Чтобы растянуть маленькую картинку нужно -> pygame.transform.scale(pygame.image.load().convert(), (WIDTH, HEIGHT))
#Чтобы уменьшить Sprite нужно -> pygame.transform.rotozoom(surf, angle, scale)
bg_surf = pygame.image.load('nature.png').convert()
all_sprites_group = pygame.sprite.Group()

class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 100
        self.alive = True
        self.score = 0
        self.speed = 4
        self.KNIGHT_IDLE = pygame.image.load('KNIGHT_IDLE.png').convert_alpha()
        self.Knight_Running_Frame1 = pygame.image.load('KNIGHT_Running_Frame1.png').convert_alpha()
        self.Knight_Running_Frame2 = pygame.image.load('KNIGHT_Running_Frame2.png').convert_alpha()
        self.Knight_fight_Frame1 = pygame.image.load('KNIGHT_FIGHT_FRAME.png').convert_alpha()
        self.player_walk = [self.Knight_Running_Frame1, self.Knight_Running_Frame2]
        self.player_index = 0
        self.image = self.player_walk[self.player_index]
        
        self.pos = (400,200)
        self.hitbox_rect = self.image.get_rect(center = self.pos)

        self.player_width = self.Knight_fight_Frame1.get_width()
        self.player_height = self.Knight_fight_Frame1.get_height()
    def border_up(self):
        self.hitbox_rect.y = max([self.hitbox_rect.y - self.speed, 0])
        
    def border_down(self):
        self.hitbox_rect.y = min([self.hitbox_rect.y + self.speed, screen_height - self.player_height])
        
    def border_left(self):
        self.hitbox_rect.x = max([self.hitbox_rect.x - self.speed, 0])
        
    def border_right(self):
        self.hitbox_rect.x = min([self.hitbox_rect.x + self.speed, screen_width - self.player_width])



    def player_animation_run(self):
        self.player_index += 0.1
        if self.player_index >= len(self.player_walk): self.player_index = 0
        self.player_surf = self.player_walk[int(self.player_index)]

    def movement(self):
        keys = pygame.key.get_pressed()
        Player.image = Player.KNIGHT_IDLE
        if keys[pygame.K_a]:
                self.hitbox_rect.x -= self.speed
                self.player_animation_run()
                self.border_left()
        if keys[pygame.K_d]:
                self.hitbox_rect.x += self.speed
                self.player_animation_run()
                self.border_right()
        if keys[pygame.K_w]:
                self.hitbox_rect.y -= self.speed
                self.player_animation_run()
                self.border_up()
        if keys[pygame.K_s]:
                self.hitbox_rect.y += self.speed
                self.player_animation_run()
                self.border_down()
        if self.hitbox_rect.x != 0 and self.hitbox_rect.y != 0:
            self.hitbox_rect.x /= math.sqrt(2)
            self.hitbox_rect.y /= math.sqrt(2)
    
    def update(self):
        self.movement()
            
            
Player = Character()
#all_sprites_group.add(Player)

class Diamond(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.cost = 5
        self.image = pygame.image.load('purple_diamond.png').convert_alpha()
        self.pos = pygame.math.Vector2(900, 900)
        self.hitbox_rect = self.image.get_rect(center = self.pos)

    def diamond_kill(self):
        if Player.hitbox_rect.colliderect(Diamond1.hitbox_rect):
            Player.score += Diamond1.cost
            pass
    
    def update(self):
        self.diamond_kill()

Diamond1 = Diamond()
#all_sprites_group.add(Diamond1)


class Slime(pygame.sprite.Sprite):
    def __init__(self, health = 100):
        super().__init__()
        self.health = health
        self.pos = (800, 800)
        self.image = pygame.image.load('Test1.png').convert_alpha()
        self.hitbox_rect = self.image.get_rect(center = self.pos)
    def movement(self):
        distance_x = Player.hitbox_rect.x - self.hitbox_rect.x
        distance_y = Player.hitbox_rect.y - self.hitbox_rect.y
        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
        speed = 3
        if distance != 0:
            self.hitbox_rect.x += speed * distance_x / distance
            self.hitbox_rect.y += speed * distance_y / distance
    def update(self):
        self.movement()
Slime1 = Slime()
#all_sprites_group.add(Slime1)


def game_over():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()
                elif restart_button.collidepoint(mouse_pos):
                    return True

        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render('Game Over', True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(text, text_rect)

        exit_button = pygame.Rect(screen_width // 2 - 100, screen_height // 2 + 20, 100, 50)
        pygame.draw.rect(screen, (255, 255, 255), exit_button)
        font = pygame.font.Font(None, 24)
        text = font.render("Exit", True, (0, 0, 0))
        text_rect = text.get_rect(center=exit_button.center)
        screen.blit(text, text_rect)

        restart_button = pygame.Rect(screen_width // 2 + 50, screen_height // 2 + 20, 100, 50)
        pygame.draw.rect(screen, (255, 255, 255), restart_button)
        text = font.render("Restart", True, (0, 0, 0))
        text_rect = text.get_rect(center=restart_button.center)
        screen.blit(text, text_rect)
        pygame.display.update()

def reset_game():
    Player.score = 0
    Player.health = 100
    Player.hitbox_rect.topleft = (400, 200)
    Slime1.hitbox_rect.topleft = (800, 800)

#Set up health bar font
font = pygame.font.SysFont("Times New Roman", 24)

#Function to update the health bar
def update_health_bar():
    #Render the health bar text
    health_text = font.render(f"Health: {Player.health}", True, (0, 0, 0))
    screen.blit(health_text, (1000, 10))

#Function to update the score
def update_score():
    #Render the score text
    score_text = font.render(f"Score: {Player.score}", True, (0, 0, 0))
    screen.blit(score_text, (1000, 40))

# Set the initial game state
game_active = True
restart_requested = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if Player.hitbox_rect.colliderect(Slime1.hitbox_rect):
        game_active = False



    
    if game_active:
        screen.blit(bg_surf,(0,0))
        screen.blit(Slime1.image, Slime1.hitbox_rect)
        screen.blit(Player.image, Player.hitbox_rect)
        screen.blit(Diamond1.image, Diamond1.hitbox_rect)
        Player.update()
        Slime1.update()
        Diamond1.update()
        update_health_bar()
        update_score()
        pygame.display.update()
        clock.tick(60)
    else:  # Game is over
        if not restart_requested:
            game_over()
            restart_requested = True

        if restart_requested:  # Reset game upon restart
            reset_game()
            game_active = True
            restart_requested = False