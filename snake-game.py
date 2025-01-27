import pygame
import time
from pygame.locals import *
from pygame import mixer
import random
import os
import sys

# Init Pygame
pygame.init()

# Init Pygame Mixer
mixer.init()

# Define Colors
white = (255, 255, 255) # Color of a snake
black = (0, 0, 0) # Background color
red = (255, 0, 0) # Game Over Message color
orange = (255, 165, 0) # Food color

width, height = 600, 400

game_display = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

pygame.display.set_caption("Snake Game in Python by @Bornunique911")

clock = pygame.time.Clock()

snake_size = 10
snake_speed = 10

brick_size = 10 # Size of the bricks
num_bricks = 15 # Number of bricks

# Mouse position initialized to 0, 0
mouse = [0, 0]

# Load snake images for each direction
snake_body = pygame.image.load('assets/images/body.png')
snake_head_up = pygame.image.load('assets/images/snake_head_up.png')
snake_head_down = pygame.image.load('assets/images/snake_head_down.png')
snake_head_left = pygame.image.load('assets/images/snake_head_left.png')
snake_head_right = pygame.image.load('assets/images/snake_head_right.png')

# Replay button image
replay_button_img = pygame.transform.scale(pygame.image.load('assets/images/game_close.png'), (width // 2, height // 2))

message_font = pygame.font.SysFont('ubuntu', 30)
score_font = pygame.font.SysFont('ubuntu', 25)

# Global variable for high score
high_score = 0

def load_high_score():
    global high_score
    if os.path.exists('high_score.txt'):
        with open('high_score.txt', 'r') as file:
            high_score = int(file.read())

def save_high_score():
    with open('high_score.txt', 'w') as file:
        file.write(str(high_score))

# Background music
def background_music():
    mixer.music.load('assets/audio_files/bensound-summer_ogg_music.ogg')
    mixer.music.play(-1)
#mixer.Channel(0).play(mixer.Sound('/home/born/Important_Stuff/Python_Projects/Snake_Game_in_Python/bensound-summer_ogg_music.ogg'))

# Background
def background():
    image = pygame.image.load('assets/images/background.jpg')
    game_display.blit(image, [0,0])

# Generate bricks
def generate_bricks(num_bricks, brick_size, width, height):
    bricks = []
    for _ in range(num_bricks):
        x = random.randrange(0, (width - brick_size) // brick_size) * brick_size
        y = random.randrange(0, (height - brick_size) // brick_size) * brick_size
        bricks.append([x, y])
    return bricks

# Generate a valid apple position
def generate_valid_apple_position(snake_pixels, bricks, snake_size, width, height):
    while True:
        x = round(random.randrange(0, width - snake_size) / 10.0) * 10.0
        y = round(random.randrange(0, height - snake_size) / 10.0) * 10.0
        if [x, y] not in snake_pixels and [x, y] not in bricks:
            return x, y

# Print score
def print_score(score):
    score_text = score_font.render("Score: " + str(score), True, orange)
    game_display.blit(score_text, [0,0])

def print_high_score(high_score):
    high_score_text = score_font.render("High Score: " + str(high_score), True, orange)
    game_display.blit(high_score_text, [0, 20])

# Draw snake
def draw_snake(snake_size, snake_pixels, direction, snake_head_up, snake_head_down, snake_head_left, snake_head_right, snake_body):
    for i, pixel in enumerate(snake_pixels):
        if i == len(snake_pixels) - 1:
            if direction == 'up':
                game_display.blit(pygame.transform.scale(snake_head_up, (snake_size, snake_size)), pixel)
            elif direction == 'down':
                game_display.blit(pygame.transform.scale(snake_head_down, (snake_size, snake_size)), pixel)
            elif direction == 'left':
                game_display.blit(pygame.transform.scale(snake_head_left,(snake_size, snake_size)), pixel)
            elif direction == 'right':
                game_display.blit(pygame.transform.scale(snake_head_right, (snake_size, snake_size)), pixel)
        else:
            game_display.blit(pygame.transform.scale(snake_body, (snake_size, snake_size)), pixel)

# Draw bricks
def draw_bricks(bricks, brick_size):
    for brick in bricks:
        pygame.draw.rect(game_display, red, [brick[0], brick[1], brick_size, brick_size])

# Main game loop
def run_game():
    global high_score
    background_music()
    collision_sound = mixer.Sound('assets/audio_files/crash.mp3')
    game_over = False
    game_close = False

    eat_sound = mixer.Sound('assets/audio_files/ding.mp3')

    game_over_sound = mixer.Sound('assets/audio_files/mixkit-sad-game-over-trombone-471.wav')

    x = width / 2
    y = height / 2

    x_speed = 0
    y_speed = 0

    snake_pixels = []
    snake_length = 1

    bricks = generate_bricks(num_bricks, brick_size, width, height)

    target_x, target_y = generate_valid_apple_position(snake_pixels, bricks, snake_size, width, height)

    direction = 'right'

    score = 0 # Initialize score

    # Replay button
    while not game_over:

        while game_close:
            game_display.fill(black)
            game_over_message = message_font.render("Game Over! Your score: " + str(score), True, red)
            game_display.blit(game_over_message, [width // 3, height // 3])
            high_score_message = message_font.render("High Score: " + str(high_score), True, red)
            game_display.blit(high_score_message, [width // 3, height // 2])
            # game_over_message = "Game Over! Your score: "
            # game_display.blit(game_over_message, [width // 3, height // 3])
            pygame.display.update()

            pygame.mixer.music.pause()
            game_over_sound.play()
            pygame.mixer.music.stop()

            # Replay button
            for event in pygame.event.get():
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_1:
                #         game_over = True
                #         game_close = False
                #     if event.key == pygame.K_2:
                #         run_game()
                if event.type == pygame.QUIT:
                    game_close = True
                else:
                    game_display.blit(replay_button_img, [width / 3, height / 2])
                    pygame.display.update()
                    time.sleep(2)
                    run_game()

            save_high_score()
        # Get mouse position
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                game_close = False
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    print(mouse)
                    if mouse[0] >= width / 2 and mouse[0] <= width / 2 + 100 and mouse[1] >= height / 2 and mouse[1] <= height / 2 + 100:
                        game_over = False
                        game_close = False
                        run_game()
                    else:
                        game_over = True
                        game_close = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_speed = -snake_size
                    y_speed = 0
                    direction = 'left'
                if event.key == pygame.K_RIGHT:
                    x_speed = snake_size
                    y_speed = 0
                    direction = 'right'
                if event.key == pygame.K_UP:
                    x_speed = 0
                    y_speed = -snake_size
                    direction = 'up'
                if event.key == pygame.K_DOWN:
                    x_speed = 0
                    y_speed = snake_size
                    direction = 'down'
        
        # Update snake position
        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True
            collision_sound.play()

        x += x_speed
        y += y_speed

        game_display.fill(black)
        background()
        game_display.blit(pygame.transform.scale(pygame.image.load('assets/images/apple.png'), (snake_size, snake_size)), (target_x, target_y))
        #pygame.draw.rect(game_display, orange, [target_x, target_y, snake_size, snake_size])

        snake_pixels.append([x,y])

        # Check if snake has eaten the apple
        if len(snake_pixels) > snake_length:
            del snake_pixels[0]

            #print_score += 10

        # Check for collision with itself
        for pixel in snake_pixels[:-1]:
            if pixel == [x,y]:
                game_close = True

        draw_snake(snake_size, snake_pixels, direction, snake_head_up, snake_head_down, snake_head_left, snake_head_right, snake_body)
        draw_bricks(bricks, brick_size)
        print_score(score=snake_length - 1)
        print_high_score(max(score, high_score))

        pygame.display.update()

        # Check if snake has eaten the apple
        if x == target_x and y == target_y:
            target_x, target_y = generate_valid_apple_position(snake_pixels, bricks, snake_size, width, height)
            snake_length += 1
            score += 10 # Increment score by 10
            high_score = max(score, high_score)
            eat_sound.play()

        # Update high score
        if score > high_score:
            high_score = score

        # Check for collision with bricks
        for brick in bricks:
            if x == brick[0] and y == brick[1]:
                collision_sound.play()
                game_close = True

        clock.tick(snake_speed)
    pygame.quit()
    sys.exit()

# Load high score when the game starts
load_high_score()

run_game()