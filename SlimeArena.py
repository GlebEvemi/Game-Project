import pygame
from sys import exit
import random
import pyautogui

pygame.init()
screen = pygame.display.set_mode(pyautogui.size())
screen_width, screen_height = pyautogui.size()
pygame.display.set_caption("SlimeArena")
clock = pygame.time.Clock()

bg_surf = pygame.image.load('nature.png').convert()
class Character:
    def __init__(self, health = 100,score = 0):
        self.health = health
        self.alive = True
        self.score = score
        self.speed = 4
        self.KNIGHT_IDLE = pygame.image.load('KNIGHT_IDLE.png').convert_alpha()
        self.Knight_Running_Frame1 = pygame.image.load('KNIGHT_Running_Frame1.png').convert_alpha()
        self.Knight_Running_Frame2 = pygame.image.load('KNIGHT_Running_Frame2.png').convert_alpha()
        self.player_walk = [self.Knight_Running_Frame1, self.Knight_Running_Frame2]
        self.player_index = 0
        self.player_surf = self.player_walk[self.player_index]
        self.player_rect = self.player_surf.get_rect(topleft=(400, 200))
        self.player_width = self.KNIGHT_IDLE.get_width()
        self.player_height = self.KNIGHT_IDLE.get_height()
    def border_up(self):
        self.player_rect.y = max([self.player_rect.y - self.speed, 0])
        
    def border_down(self):
        self.player_rect.y = min([self.player_rect.y + self.speed, screen_height - self.player_height])
        
    def border_left(self):
        self.player_rect.x = max([self.player_rect.x - self.speed, 0])
        
    def border_right(self):
        self.player_rect.x = min([self.player_rect.x + self.speed, screen_width - self.player_width])


    def player_animation_run(self):
        self.player_index += 0.1
        if self.player_index >= len(self.player_walk): self.player_index = 0
        self.player_surf = self.player_walk[int(self.player_index)]

    def movement(self):
        keys = pygame.key.get_pressed()
        self.player_surf = self.KNIGHT_IDLE
        if keys[pygame.K_a]:
            Player.player_rect.x -= self.speed
            Player.player_animation_run()
            Player.border_left()
        if keys[pygame.K_d]:
            Player.player_rect.x += self.speed
            Player.player_animation_run()
            Player.border_right()
        if keys[pygame.K_w]:
            Player.player_rect.y -= self.speed
            Player.player_animation_run()
            Player.border_up()
        if keys[pygame.K_s]:
            Player.player_rect.y += self.speed
            Player.player_animation_run()
            Player.border_down()
Player = Character()
class Diamond:
    def __init__(self, cost = 5):
        self.cost = cost
        self.diamond_surf = pygame.image.load('purple_diamond.png').convert_alpha()
        self.diamond_rect = self.diamond_surf.get_rect(topleft = (900, 900))

Diamond1 = Diamond()


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


def game_over():
    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                elif restart_button.collidepoint(mouse_pos):
                    pass
                    
                    

                    
                    
        screen.fill((0,0,0))
        font = pygame.font.Font(None, 36)
        text = font.render('Game Over', True, (255,255,255))
        text_rect = text.get_rect(center=(1920 // 2 + 20, 1080 // 2))
        screen.blit(text, text_rect)
        
        exit_button = pygame.Rect(1920 // 2 - 100, 1080 // 2 + 20, 100, 50)
        pygame.draw.rect(screen, (255,255,255), exit_button)
        font = pygame.font.Font(None, 24)
        text = font.render("Exit", True, (0,0,0))
        text_rect = text.get_rect(center = exit_button.center)
        screen.blit(text, text_rect)
        
        restart_button = pygame.Rect(1920 // 2 + 50,  1080 // 2 + 20, 100, 50)
        pygame.draw.rect(screen, (255,255,255), restart_button)
        text = font.render("Restart", True,(0,0,0))
        text_rect = text.get_rect(center = restart_button.center)
        screen.blit(text, text_rect)
        
            
        pygame.display.update()
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

Slime1 = Slime()
while True:
    game_active = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if Player.player_rect.colliderect(Slime1.slime_rect):
        pass
    if Player.player_rect.colliderect(Diamond1.diamond_rect):
        Player.score += Diamond1.cost



    
    if game_active:
        screen.blit(bg_surf,(0,0))
        Slime1.movement()
        screen.blit(Slime1.slime_surf, Slime1.slime_rect)
        Player.movement()
        screen.blit(Player.player_surf, Player.player_rect)
        screen.blit(Diamond1.diamond_surf, Diamond1.diamond_rect)
        update_health_bar()
        update_score()
        pygame.display.update()
        clock.tick(60)
    elif game_active == False:
        game_over()
        game_active = True
        continue