import pygame
from sys import exit
import math
from GameSettings import *
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
        self.Knight_fight_Frame1 = pygame.image.load('Knight_Frames/KNIGHT_FIGHT_FRAME.png').convert_alpha()
        self.player_walk = [self.Knight_Running_Frame1, self.Knight_Running_Frame2]
        self.pos = pygame.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.rect = self.image.get_rect(center = self.pos)
        self.player_index = 0
        self.score = 0
        self.health = 100
        self.speed = PLAYER_SPEED
        self.player_width = self.Knight_fight_Frame1.get_width()
        self.player_height = self.Knight_fight_Frame1.get_height()

    def player_animation_run(self):
        self.player_index += 0.1
        if self.player_index >= len(self.player_walk): self.player_index = 0
        self.image = self.player_walk[int(self.player_index)]
    
    """ def border_up(self):
        self.pos.y = max([self.pos.y - self.speed, 0])
        
    def border_down(self):
        self.pos.y = min([self.pos.y + self.speed, HEIGHT - self.player_height])
        
    def border_left(self):
        self.pos.x = max([self.pos.x - self.speed, 0])
        
    def border_right(self):
        self.pos.x = min([self.pos.x + self.speed, WIDTH - self.player_width]) """
    
    def user_input(self):
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
        
        if self.velocity_x != 0 and self.velocity_y != 0: #moving diagonally
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)


    def move(self):
        self.pos += (self.velocity_x, self.velocity_y)
        if self.pos.x <= 0: self.pos.x = 0
        if self.pos.x > WIDTH: 
            self.pos.x = WIDTH
        
        if self.pos.y <= 0: self.pos.y = 0
        if self.pos.y > HEIGHT:
            self.pos.y = HEIGHT
        self.rect.center = self.pos


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

# Set the initial game state
game_active = True
restart_requested = False
all_sprites_group = pygame.sprite.Group()


slimes = [Slime()]
# Adding sprites to group
all_sprites_group.add(player)
all_sprites_group.add(diamond)
all_sprites_group.add(slimes)

slime_spawn_timer = 0
slime_spawn_interval = 0  # Spawn a slime every 15 seconds
max_slimes = 2  # Maximum number of slimes allowed at a time
#Game loop
while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
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
                    player.health -= 5
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
    

