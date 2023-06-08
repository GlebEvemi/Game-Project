import pygame
from sys import exit
import math
from GameSettings import *
from pygame.locals import *
import sys
import pyautogui
import random


pygame.init()

# Creating the window
screen = pygame.display.set_mode(pyautogui.size())
pygame.display.set_caption('Slime Arena')
# Setting the clock (FPS)
clock = pygame.time.Clock()

# Loads background
background = pygame.image.load("Other_pictures/nature.png").convert()

class Player(pygame.sprite.Sprite):
    """
    Represents the player character in the game.

    Attributes:
        Knight_idle (pygame.Surface): Image representing the idle state of the player character.
        image (pygame.Surface): Current image of the player character.
        Knight_Running_Frame1 (pygame.Surface): First frame of the running animation.
        Knight_Running_Frame2 (pygame.Surface): Second frame of the running animation.
        Knight_fight_Frame1 (pygame.Surface): First frame of the fighting animation.
        Knight_fight_Frame2 (pygame.Surface): Second frame of the fighting animation.
        player_walk (list): List of player walking frames.
        player_fight (list): List of player fighting frames.
        pos (pygame.Vector2): Current position of the player character.
        rect (pygame.Rect): Rectangle representing the player character's position and size.
        player_walk_index (float): Index of the current walking frame.
        player_fight_index (int): Index of the current fighting frame.
        score (int): Player's score.
        health (int): Player's health.
        speed (float): Player's movement speed.
        player_width (int): Width of the player character's image.
        player_height (int): Height of the player character's image.
        attacking (bool): Flag indicating if the player is currently attacking.
        attack_cooldown (int): Cooldown time between consecutive attacks.
        update_time (int): Time of the last update.
        animation_cooldown (int): Cooldown time between consecutive frame updates.
        damage (int): Amount of damage inflicted by the player's attacks.
        level (int): Player's current level.
    """

    def __init__(self):
        """
        Initializes a new instance of the Player class.
        """
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
        self.rect = self.image.get_rect(center=self.pos)
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
        self.animation_cooldown = 500
        self.damage = 15
        self.level = 1

    def draw(self, surface):
        """
        Draws the player character on the specified surface.

        Args:
            surface (pygame.Surface): Surface on which to draw the player character.
        """
        surface.blit(self.image, self.rect)
        draw_health_bar(surface, self.rect.x, self.rect.y - 10, self.rect.width, 10, self.health, GREEN)

    def player_animation_run(self):
        """
        Updates the player character's image for the running animation.
        """
        self.player_walk_index += 0.1
        if self.player_walk_index >= len(self.player_walk):
            self.player_walk_index = 0
        self.image = self.player_walk[int(self.player_walk_index)]

    def attack(self):
        """
        Performs the player character's attack action.
        """
        if self.attack_cooldown <= 0:
            self.attacking = True
            for _ in range(len(self.player_fight)):
                self.image = self.player_fight[self.player_fight_index]
                self.player_fight_index += 1
                if self.player_fight_index >= len(self.player_fight):
                    self.player_fight_index = 0
            attacking_rect = pygame.Rect(self.rect.x, self.rect.y, 1.5 * self.rect.width, self.rect.height)
            for slime in slimes:
                if attacking_rect.colliderect(slime.rect):
                    slime.health -= self.damage  # Reduce slime's health by self.damage upon hit
                    if slime.health <= 0:
                        slimes.remove(slime)

    def user_input(self):
        """
        Handles the user input for controlling the player character.
        """
        if self.attacking is False:
            self.velocity_x = 0
            self.velocity_y = 0
            keys = pygame.key.get_pressed()
            self.image = self.Knight_idle
            if keys[pygame.K_w]:
                self.velocity_y = -self.speed
                self.player_animation_run()
                # self.border_up()
            if keys[pygame.K_s]:
                self.velocity_y = self.speed
                self.player_animation_run()
                # self.border_down()
            if keys[pygame.K_d]:
                self.velocity_x = self.speed
                self.player_animation_run()
                # self.border_right()
            if keys[pygame.K_a]:
                self.velocity_x = -self.speed
                self.player_animation_run()
                # self.border_left()
            if keys[pygame.K_SPACE]:
                self.attack()
                self.attacking = False
                self.attack_cooldown = 50
            if keys[pygame.K_u]:
                self.level_up()

        if self.velocity_x != 0 and self.velocity_y != 0:  # moving diagonally
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

    def move(self):
        """
        Moves the player character based on the user input.
        """
        self.rect.centerx += self.velocity_x
        self.rect.centery += self.velocity_y
        # apply attack cooldown
        if player.attack_cooldown > 0:
            player.attack_cooldown -= 20
        self.borders()

    def borders(self):
        """
        Restricts the player character within the game window's borders.
        """
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WIDTH)
        self.rect.top = max(self.rect.top, 620)
        self.rect.bottom = min(self.rect.bottom, HEIGHT)

    def level_up(self):
        """
        Increases the player character's level and upgrades its attributes.
        """
        if self.score >= 10:
            self.level += 1
            self.score -= 10
            if self.level == 2:
                self.damage += 1
                self.speed += 0.1
            elif self.level == 3:
                self.damage += 2
                self.speed += 0.2
            elif self.level == 4:
                self.damage += 3
                self.speed += 0.3
            elif self.level >= 5:
                self.damage += 1
                self.speed += 0.1

    def update_score(self):
        """
        Updates and renders the player's score on the screen.
        """
        score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        screen.blit(score_text, (0, 10))

    def update_damage(self):
        """
        Updates and renders the player's damage on the screen.
        """
        damage_text = font.render(f"Damage: {self.damage}", True, (0, 0, 0))
        screen.blit(damage_text, (0, 40))

    def update_speed(self):
        """
        Updates and renders the player's speed on the screen.
        """
        speed_text = font.render(f"Speed: {self.speed:.2f}", True, (0, 0, 0))
        screen.blit(speed_text, (0, 70))

    def instruction(self):
        """
        Updates and renders the player's speed on the screen.
        """
        instruction_text = font.render(f"MOVING: W - UP, S - DOWN, A - LEFT, D - RIGHT, SPACE - ATTACK", True, (0, 0, 0))
        screen.blit(instruction_text, (0, 100))
        
    def user_info(self):
        """
        Renders the information about score exchange for level upgrades on the screen.
        """
        if self.score >= 10:
            info_text = font.render(
                f"You have: {self.score} score. You can exchange 10 score on 1 level upgrade by pressing U key!",
                True, (0, 0, 0))
            screen.blit(info_text, (0, 130))

    def draw_level(self, surface):
        """
        Renders the player's level on the screen.
        """
        level_text = font.render(f"Level: {self.level}", True, (0, 0, 0))
        surface.blit(level_text, (self.rect.centerx - level_text.get_width() // 2, self.rect.top - 40))

    def update(self):
        """
        Updates the player character.
        """
        self.user_input()
        self.move()
        self.draw(screen)
        self.update_score()
        self.update_damage()
        self.user_info()
        self.update_speed()
        self.instruction()
        self.draw_level(screen)

player = Player()

class Slime(pygame.sprite.Sprite):
    """
    Represents a slime enemy in the game.

    Attributes:
        alive (bool): Flag indicating if the slime is alive.
        image (pygame.Surface): The image representing the slime.
        pos (pygame.Vector2): The position of the slime.
        rect (pygame.Rect): The rectangle used for collision detection and positioning.
        speed (int): The speed of the slime.
        health (int): The health of the slime.
        damage (int): The damage the slime can inflict on the player.

    Methods:
        __init__(): Initializes a new instance of the Slime class.
        draw(surface): Draws the slime's health bar on the specified surface.
        movement(): Controls the slime's movement towards the player.
        borders(): Restricts the slime's movement within the game window's borders.
        update(): Updates the slime's state and position.

    """

    def __init__(self):
        """
        Initializes a new instance of the Slime class.
        Randomly assigns attributes such as speed, health, and damage.
        """
        super().__init__()
        self.alive = True
        self.image = pygame.image.load("Other_pictures/red_slime.png").convert_alpha()
        self.pos = pygame.Vector2(SLIME_START_X, SLIME_START_Y)
        self.rect = self.image.get_rect(center=self.pos)
        self.speed = random.choice(SLIME_SPEED)
        self.health = random.choice(slime_health_list)
        if self.speed >= 4:
            self.health = 1
        elif self.speed == 3:
            self.health = 50
        elif self.speed == 2:
            self.health = 100
        elif self.speed == 1:
            self.health = 150
        self.damage = (10 * self.speed) + (10 * player.level)

    def draw(self, surface):
        """
        Draws the slime's health bar on the specified surface.

        Args:
            surface (pygame.Surface): The surface on which to draw the health bar.
        """
        draw_health_bar(surface, self.rect.x, self.rect.y - 10, self.rect.width, 10, self.health, GREEN)

    def movement(self):
        """
        Controls the slime's movement towards the player.
        """
        distance_x = player.rect.x - self.rect.x
        distance_y = player.rect.y - self.rect.y
        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
        if distance != 0:
            self.rect.x += self.speed * distance_x / distance
            self.rect.y += self.speed * distance_y / distance

    def borders(self):
        """
        Restricts the slime's movement within the game window's borders.
        """
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WIDTH)
        self.rect.top = max(self.rect.top, 700)
        self.rect.bottom = min(self.rect.bottom, HEIGHT)

    def update(self):
        """
        Updates the slime's state and position.
        Handles the slime's movement, drawing the health bar, and checking for death.
        """
        self.movement()
        self.draw(screen)
        if self.health <= 0:
            self.last_x, self.last_y = self.rect.centerx, self.rect.centery
            self.kill()
            diamond = Diamond()
            diamond.rect.center = self.last_x, self.last_y
            all_sprites_group.add(diamond)
        self.borders()
        
slime = Slime()

class Diamond(pygame.sprite.Sprite):
    """
    Represents a diamond object in the game.

    Attributes:
        cost (int): The cost of the diamond (blue = 2, red = 5).
        alive (bool): Flag indicating if the diamond is alive.
        cure (int): The amount of health the diamond can restore to the player.
        image_list (list): The list of image paths for different diamond types.
        image (pygame.Surface): The image representing the diamond.
        pos (pygame.Vector2): The position of the diamond.
        rect (pygame.Rect): The rectangle used for collision detection and positioning.

    Methods:
        __init__(): Initializes a new instance of the Diamond class.
        update(): Updates the state of the diamond.

    """

    def __init__(self):
        """
        Initializes a new instance of the Diamond class.
        Randomly assigns attributes such as cost, cure, and image based on chance.
        """
        super().__init__()
        self.cost = None
        self.alive = True
        self.cure = None
        self.image_list = ["Other_pictures/blue_diamond.png", "Other_pictures/purple_diamond.png"]
        if random.randint(0, 100) < Purple_chance:
            self.image = pygame.image.load(self.image_list[1])
            self.cost = 5
            self.cure = 10 + player.level
        else:
            self.image = pygame.image.load(self.image_list[0])
            self.cost = 2
            self.cure = 5 + player.level
        self.pos = pygame.Vector2(DIAMOND_START_X, DIAMOND_START_Y)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        """
        Updates the state of the diamond.
        This method is empty as there is no specific update  for the diamond.
        """
        pass

        
diamond = Diamond()

def game_over():
    """
    Displays the game over screen and handles user input for restarting or exiting the game.

    Returns:
        bool: True if the user chooses to restart the game.

    """
    click = False

    background = pygame.image.load("Other_pictures/nature.png").convert()

    restart_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 100, 150, 50)
    restart_font = pygame.font.Font(None, 40)
    restart_text = restart_font.render("Restart", True, (255, 255, 255))
    restart_text_rect = restart_text.get_rect(center=restart_button.center)

    exit_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 200, 150, 50)
    exit_text = restart_font.render("Exit", True, (255, 255, 255))
    exit_text_rect = exit_text.get_rect(center=exit_button.center)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mouse_x, mouse_y = pygame.mouse.get_pos()

        if restart_button.collidepoint((mouse_x, mouse_y)):
            if click:
                return True

        if exit_button.collidepoint((mouse_x, mouse_y)):
            if click:
                pygame.quit()
                sys.exit()

        screen.blit(background, (0, 0))

        font = pygame.font.Font(None, 36)
        text = font.render('Game Over', True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, (225, 193, 110), restart_button)
        pygame.draw.rect(screen, (225, 193, 110), exit_button)
        screen.blit(restart_text, restart_text_rect)
        screen.blit(exit_text, exit_text_rect)

        pygame.display.update()
        clock.tick(FPS)
    
def reset_game():
    """
    Resets the game state to the initial values.
    - Resets the player's score, health, level, damage, and speed.
    - Moves the player's sprite to the starting position.
    - Removes all Diamond sprites from the game.

    """
    player.score = 0
    player.health = 100
    player.level = 1
    player.damage = 15
    player.speed = 6
    player.rect.center = (PLAYER_START_X, PLAYER_START_Y)
    for sprite in all_sprites_group:
        if isinstance(sprite, Diamond):
            sprite.kill()

# Set up health bar font
font = pygame.font.SysFont("Times New Roman", 24)

def draw_text(text, font, color, surface, x, y):
    """
    Draws text on the given surface at the specified coordinates.

    Args:
        text (str): The text to be drawn.
        font (pygame.font.Font): The font to be used for the text.
        color (tuple): The RGB color value of the text.
        surface (pygame.Surface): The surface on which the text will be drawn.
        x (int): The x-coordinate of the top-left corner of the text.
        y (int): The y-coordinate of the top-left corner of the text.

    """
    text = font.render(text, font, color)
    text_rect = text.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text, text_rect)


def main_menu():
    """
    Displays the main menu screen and handles user input for starting or quitting the game.
    
    """
    
    click = False

    background = pygame.image.load("Other_pictures/nature.png").convert()

    title_font = pygame.font.Font(None, 80)
    title_text = title_font.render("Slime Arena", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

    start_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2, 150, 50)
    start_font = pygame.font.Font(None, 40)
    start_text = start_font.render("Start", True, (255, 255, 255))
    start_text_rect = start_text.get_rect(center=start_button.center)

    exit_button = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 100, 150, 50)
    exit_text = start_font.render("Exit", True, (255, 255, 255))
    exit_text_rect = exit_text.get_rect(center=exit_button.center)
    
    click = False
    
    running = True
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if start_button.collidepoint((mouse_x, mouse_y)):
            if click:
                game()
        elif exit_button.collidepoint((mouse_x, mouse_y)):
            if click:
                pygame.quit()
                exit()
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
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            game()

        screen.blit(background, (0, 0))
        screen.blit(title_text, title_rect)
        pygame.draw.rect(screen, (225, 193, 110), start_button)
        pygame.draw.rect(screen, (225, 193, 110), exit_button)
        screen.blit(start_text, start_text_rect)
        screen.blit(exit_text, exit_text_rect)

        pygame.display.flip()
        clock.tick(FPS)
        
def draw_health_bar(surface, x, y, width, height, health, color):
    """
    Draws a health bar on the given surface at the specified position.

    Args:
        surface (pygame.Surface): The surface on which to draw the health bar.
        x (int): The x-coordinate of the top-left corner of the health bar.
        y (int): The y-coordinate of the top-left corner of the health bar.
        width (int): The width of the health bar.
        height (int): The height of the health bar.
        health (int): The current health value.
        color (tuple): The RGB color value of the health bar.

    """
    # Limit the maximum health value to 100
    health = min(health, 100)
    
    # Calculate the width of the health bar based on the health percentage
    red_width = int((health / 100) * width)

    # Create the health bar rect and background rect
    green_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(surface, RED, green_rect)

    # Draw the red portion of the health bar
    red_rect = pygame.Rect(x, y, red_width, height)
    pygame.draw.rect(surface, GREEN, red_rect)


slimes = [Slime()]
all_sprites_group = pygame.sprite.Group()

def game():
    """
    The main game loop that handles gameplay mechanics, sprite interactions, and screen updates.

    """
    game_active = True
    restart_requested = False
    start_game_sound.play()
    # Set the initial game state

    # Adding sprites to group
    all_sprites_group.add(player)
    all_sprites_group.add(slimes)

    spawn_timer = 0
    slime_spawn_timer = 5   # Spawn a slime every 5 seconds
    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        if game_active:
            for slime in slimes:
                slime.movement()
            #Screen blit
            screen.blit(background, (0,0))
            if len(slimes) == 0:
                spawn_timer += clock.get_time() / 1000 # Convert clock time to seconds

                if spawn_timer >= slime_spawn_timer:
                    slime = Slime()
                    slime.rect.center = (WIDTH - slime.rect.width, random.randint(750, 1000))#HEIGHT - slime.rect.height
                    slimes.append(slime)
                    all_sprites_group.add(slime)
                    spawn_timer = 0
 
            for sprite in all_sprites_group:
                
                if isinstance(sprite, Diamond):
                    if sprite.rect.colliderect(player.rect):
                        player.score += sprite.cost
                        player.health += sprite.cure
                        all_sprites_group.remove(sprite)
                if isinstance(sprite, Slime):
                    sprites_to_remove = []
                    for sprite in slimes:
                        if sprite.rect.colliderect(player.rect):
                            sprites_to_remove.append(sprite)
                            player.health -= sprite.damage
                            if player.health <= 0:
                                game_active = False

                    for sprite in sprites_to_remove:
                        slimes.remove(sprite)
                        all_sprites_group.remove(sprite)

 
            all_sprites_group.draw(screen)
            all_sprites_group.update()
            pygame.display.update()
            
            for slime in slimes:
                slime.movement() 
                
            clock.tick(FPS)
            
        else:  # Game is over
            if not restart_requested:
                game_over()
                restart_requested = True

            if restart_requested:  # Reset game upon restart
                reset_game()
                start_game_sound.play()
                game_active = True
                restart_requested = False
main_menu()
