import pygame
from sys import exit
import math
from GameSettings import *
from pygame.locals import *
import sys
import pyautogui
import random


pygame.init()

#Creating the window
screen = pygame.display.set_mode(pyautogui.size())
pygame.display.set_caption('Slime Arena')
clock = pygame.time.Clock()

#Loads images
background = pygame.image.load("nature.png").convert()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.Knight_idle = pygame.image.load('Knight_Frames/KNIGHT_IDLE.png').convert_alpha()
        self.image = self.Knight_idle
        self.Knight_Running_Frame1 = pygame.image.load('Knight_Frames/KNIGHT_Running_Frame1.png').convert_alpha()
        self.Knight_Running_Frame2 = pygame.image.load('Knight_Frames/KNIGHT_Running_Frame2.png').convert_alpha()
        self.Knight_fight_Frame1 = pygame.image.load('Knight_Frames/KNIGHT_FIGHT_FRAME1.png').convert_alpha()
        self.Knight_fight_Frame2 = pygame.image.load('Knight_Frames/KNIGHT_FIGHT_FRAME2.png').convert_alpha()
        self.player_walk = [self.Knight_Running_Frame1, self.Knight_Running_Frame2]
        self.player_fight = [self.Knight_fight_Frame1, self.Knight_fight_Frame2]
        self.pos = pygame.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.rect = self.image.get_rect(center = self.pos)
        self.player_walk_index = 0
        self.player_fight_index = 0
        self.score = 0
        self.health = 100
        self.speed = PLAYER_SPEED
        self.player_width = self.Knight_fight_Frame1.get_width()
        self.player_height = self.Knight_fight_Frame1.get_height()
        self.attacking = False 
        self.attack_cooldown = 0
        self.update_time = pygame.time.get_ticks()
        self.animation_cooldown = 200
    

    def player_animation_run(self):
        self.player_walk_index += 0.1
        if self.player_walk_index >= len(self.player_walk): self.player_walk_index = 0
        self.image = self.player_walk[int(self.player_walk_index)]

    def atack(self):
        if self.attack_cooldown <= 0:
            self.attacking = True
            for _ in range(len(self.player_fight)):
                self.image = self.player_fight[self.player_fight_index]
                self.player_fight_index += 1
                if self.player_fight_index >= len(self.player_fight): 
                    self.player_fight_index = 0
            attacking_rect = pygame.Rect(self.rect.centerx, self.rect.y, 1.5 *self.rect.width, self.rect.height)
            for slime in slimes:
                if attacking_rect.colliderect(slime.rect):
                    print("HIT")


    def user_input(self):
        if self.attacking == False:
            self.velocity_x = 0
            self.velocity_y = 0
            keys = pygame.key.get_pressed()
            self.image = self.Knight_idle
            if keys[pygame.K_w]:
                self.velocity_y = -self.speed
                self.player_animation_run()
                #self.border_up()
            if keys[pygame.K_s]:
                self.velocity_y = self.speed
                self.player_animation_run()
                #self.border_down()
            if keys[pygame.K_d]:
                self.velocity_x = self.speed
                self.player_animation_run()
                #self.border_right()
            if keys[pygame.K_a]:
                self.velocity_x = -self.speed
                self.player_animation_run()
                #self.border_left()
            if keys[pygame.K_SPACE]:
                self.atack()
                self.attacking = False
                self.attack_cooldown = 50
        
        if self.velocity_x != 0 and self.velocity_y != 0: #moving diagonally
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)


    def move(self):
        self.rect.centerx += self.velocity_x
        self.rect.centery += self.velocity_y
        #apply attack cooldown
        if player.attack_cooldown > 0:
            player.attack_cooldown -= 20
        self.borders()

    def borders(self):
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WIDTH)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, HEIGHT)

    def update(self):
        self.user_input()
        self.move()
        
player = Player()

class Slime(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.alive = True
        self.image = pygame.image.load("Test1.png").convert_alpha()
        self.pos = pygame.Vector2(SLIME_START_X, SLIME_START_Y)
        self.rect = self.image.get_rect(center = self.pos)
        self.speed = SLIME_SPEED

    def movement(self):
        distance_x = player.rect.x - self.rect.x
        distance_y = player.rect.y - self.rect.y
        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
        if distance != 0:
            self.rect.x += self.speed * distance_x / distance
            self.rect.y += self.speed * distance_y / distance
    
    def update(self):
        self.movement()

def spawn():
    slime_spawn_timer = 0
    slime_spawn_interval = 0  # Spawn a slime every 15 seconds
    max_slimes = 2  # Maximum number of slimes allowed at a time
    if slime_spawn_timer <= 0 and len(slimes) < max_slimes:
                slime = Slime()
                slime.rect.center = (WIDTH - slime.rect.width, random.randint(0, HEIGHT - slime.rect.height))
                slimes.append(slime)
                all_sprites_group.add(slimes)
                slime_spawn_timer = slime_spawn_interval
    else:
        slime_spawn_timer -= 1

class Diamond(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.cost = 5
        self.alive = True
        self.image = pygame.image.load("blue_diamond.png")
        self.pos = pygame.Vector2(DIAMOND_START_X, DIAMOND_START_Y)
        self.rect = self.image.get_rect(center = self.pos)
    def update(self):
        pass

        
diamond = Diamond()

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
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

        exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 100, 50)
        pygame.draw.rect(screen, (255, 255, 255), exit_button)
        font = pygame.font.Font(None, 24)
        text = font.render("Exit", True, (0, 0, 0))
        text_rect = text.get_rect(center=exit_button.center)
        screen.blit(text, text_rect)

        restart_button = pygame.Rect(WIDTH // 2 + 50, HEIGHT // 2 + 20, 100, 50)
        pygame.draw.rect(screen, (255, 255, 255), restart_button)
        text = font.render("Restart", True, (0, 0, 0))
        text_rect = text.get_rect(center=restart_button.center)
        screen.blit(text, text_rect)
        pygame.display.update()
    
def reset_game():
    player.score = 0
    player.health = 100
    player.rect.center = (PLAYER_START_X, PLAYER_START_Y)

#Set up health bar font
font = pygame.font.SysFont("Times New Roman", 24)

def draw_text(text, font, color, surface, x, y):
    text = font.render(text, font, color)
    text_rect = text.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text, text_rect)
 
# Main container function that holds the buttons and game functions
def main_menu():
    # A variable to check for the status later
    click = False
 
    while True:
 
        screen.fill((0,0,0))
 
        mouse_x, mouse_y = pygame.mouse.get_pos()

        #creating buttons
        play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
        #defining functions when a certain button is pressed
        if play_button.collidepoint((mouse_x, mouse_y)):
            if click:
                game()
        pygame.draw.rect(screen, (255, 0, 0), play_button)
 
        #writing text on top of button
        draw_text('PLAY', font, (255,255,255), screen, WIDTH // 2 - 30, HEIGHT // 2 - 10)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                    click = True
        pygame.display.update()
        clock.tick(60)
#Function to update the health bar
def update_health_bar():
    #Render the health bar text
    health_text = font.render(f"Health: {player.health}", True, (0, 0, 0))
    screen.blit(health_text, (1000, 10))

#Function to update the score
def update_score():
    #Render the score text
    score_text = font.render(f"Score: {player.score}", True, (0, 0, 0))
    screen.blit(score_text, (1000, 40))

slimes = [Slime()]
all_sprites_group = pygame.sprite.Group()
#Game loop
def game():
    game_active = True
    restart_requested = False
    # Set the initial game state

    # Adding sprites to group
    all_sprites_group.add(player)
    all_sprites_group.add(diamond)
    all_sprites_group.add(slimes)

    slime_spawn_timer = 0
    slime_spawn_interval = 0  # Spawn a slime every 15 seconds
    max_slimes = 3  # Maximum number of slimes allowed at a time
    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_clicked = True
                left_click, middle_click, right_click = pygame.mouse.get_pressed()
                if left_click and mouse_clicked:
                    mouse_clicked = False
        
        
        if game_active:
            #Screen blit
            screen.blit(background, (0,0))

            if slime_spawn_timer <= 0 and len(slimes) < max_slimes:
                    slime = Slime()
                    slimes.append(slime)
                    slime.rect.center = (WIDTH - slime.rect.width, random.randint(0, HEIGHT - slime.rect.height))
                    
                    all_sprites_group.add(slimes)
                    slime_spawn_timer = slime_spawn_interval
            else:
                slime_spawn_timer -= 1

            for sprite in all_sprites_group:


                if isinstance(sprite, Diamond):
                    if sprite.rect.colliderect(player.rect):
                        player.score += sprite.cost
                        all_sprites_group.remove(sprite)
                if isinstance(sprite, Slime):
                    if sprite.rect.colliderect(player.rect):
                        all_sprites_group.remove(sprite)
                        slimes.remove(sprite)
                        player.health -= 40
                        if player.health <= 0:
                            game_active = False

            all_sprites_group.draw(screen)
            all_sprites_group.update()

            update_health_bar()
            update_score()
            
            pygame.display.update()
            clock.tick(FPS)
            
        else:  # Game is over
            if not restart_requested:
                game_over()
                restart_requested = True

            if restart_requested:  # Reset game upon restart
                reset_game()
                game_active = True
                restart_requested = False
main_menu()
    
