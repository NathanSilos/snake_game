import pygame as pg
from pygame.locals import *
import sys
from functions import *
import time
import random
import os
import pandas as pd

dir = os.path.dirname(os.path.abspath(__file__))
# Initializing pygame, music and font
pg.font.init()
pg.font.init()
pg.mixer.init()

# Start the music
music_player(dir + '\\Solomun-The-way-back.mp3')

# Create a screen
screen = pg.display.set_mode((600, 400))

# Import the screen image
background = pg.image.load( dir + '\\snake_game_home.jpg')

# Transform the image to the size of screen
background = pg.transform.scale(background, (600, 400)) 

# Defining colors
black = (0, 0, 0) # Black
grey = (105,105,105) # Grey
green = (34, 145, 43) # Green
red = (209, 58, 54) # Red
yellow = (255, 255, 0) # Yellow
white = (229, 229, 224) # White

# Defining positions variables
xfood = random.randrange(1, 600, 1)
yfood = random.randrange(1, 400, 1)

display_menu = True
xsnake = 300
ysnake = 200
xmove = 0
ymove = 0
speed = pg.time.Clock()
score = 0
movement = ''

snake_head = [xsnake, ysnake]
snake_body = [snake_head]
snake_counter = 0

# Keep the program open/working
while True:
    # Run for all the events happening inside of script
    for event in pg.event.get():
        # If the close buttom is pressed
        if event.type == pg.QUIT:
            sys.exit()
        # Movement of snake made by keyboard arrows
        if event.type == pg.KEYDOWN and display_menu == False:
            if event.key == pg.K_UP and ymove == 0:
                ymove = -10
                xmove = 0
            if event.key == pg.K_DOWN and ymove == 0:
                ymove = 10 
                xmove = 0
            if event.key == pg.K_LEFT and xmove == 0:
                ymove = 0
                xmove = -10
            if event.key == pg.K_RIGHT and xmove == 0: 
                ymove = 0
                xmove = 10

    if display_menu == True:

        # Insert background
        screen.blit(background,(0,0))

        # Insert PLAY button
        game_font = pg.font.Font( dir + '\\VCR_OSD_MONO_1.001.ttf', 40)
        play_button = pg.Rect((470, 300, 110, 60))
        play_button_font = game_font.render('PLAY', True, red)
        play_rect = play_button_font.get_rect()
        
        screen.blit(play_button_font, (480, 311))
        
        # Ler o histórico
        df = pd.read_csv(dir + '\\base_snake.csv')
        # Ordena
        df.sort_values(by=['pontos'], inplace=True, ascending=False)

        max_score = df.pontos.max()

        # Pontuacao máxima
        max_point = game_font.render(f'Max points: {max_score}', True, white)
        play_rect = max_point.get_rect()

        screen.blit(max_point, (20, 360))
        
        # Getting the mouse position
        mouse = pg.mouse.get_pos()

        # If the mouse pass under the PLAY button change the color ( x + width > mouse position x > position x)
        if 470 + 110 > mouse[0] > 470 and 300 + 60 > mouse[1] > 330:
            pg.draw.rect(background, yellow, (470, 300, 110, 60))
        else:
            pg.draw.rect(background, black, (470, 300, 110, 60))       

        # Check if PLAY button is clicked
        click = pg.mouse.get_pressed()
        
        # Starts the game if the PLAY button is clicked
        if click[0] == 1:
            mouse = pg.mouse.get_pos()
            if play_button.collidepoint(mouse):
                display_menu = False
                score = 0 
                snake_body = [snake_head]          

    else:
        # Starting the game
        screen.fill(grey)

        # Defining positions
        ysnake += ymove
        xsnake += xmove
        snake_head = [xsnake, ysnake]

        # Update the size of snake 
        if len(snake_body) > 1:
            snake_body.insert(0, snake_head)
            snake_body.pop(-1)
            # When the snake touchs it body
            for snake_position_body in snake_body[1:]:
                # print(snake_position_body[0], snake_head[0])
                if (snake_position_body[0] > snake_head[0] - 5 and  snake_position_body[0] < snake_head[0] + 5) and\
                (snake_position_body[1] > snake_head[1] - 5 and  snake_position_body[1] < snake_head[1] + 5):
                    # Returns to the initial page
                    display_menu = True 
        else:
            snake_body = [snake_head]

        # Draw a score in the left side of the screen
        score_font = pg.font.Font(dir + '\\VCR_OSD_MONO_1.001.ttf', 20)
        score_counter = score_font.render(f'Score:{score}', True, black)
        screen.blit(score_counter, (10, 10))

        # Drawing the snake
        for position in snake_body:
            pg.draw.rect(screen, black,(position[0], position[1], 10, 10))
        
        # Drawing the food 
        pg.draw.rect(screen, red,(xfood, yfood, 10, 10))
        
        # Setting the start speed
        snake_speed = 12 

        # Snake speed
        speed.tick(snake_speed + score)

        # When the snake touch the food
        if (xsnake > xfood - 10 and  xsnake < xfood + 10) and (ysnake > yfood - 10 and  ysnake < yfood + 10):
            # Redefining food variables of positions
            xfood = random.randrange(1, 600, 1)
            yfood = random.randrange(1, 400, 1)
            score += 1
            # Growing snake tail
            snake_body.append(snake_body[-1])
            snake_counter += 1
        
        # End the game if the snake touches the wall
        if (snake_head[0] < 0 or snake_head[0] > 600) or (snake_head[1] > 400 or snake_head[1] < 0):            
            xsnake = 300
            ysnake = 200

            # Cria um df com o valor dos pontos
            dfp = pd.DataFrame({'pontos': [score]})
            # Concatena o outro valor e exporta
            pd.concat([df, dfp]).to_csv(r'C:\Users\natha\Documents\01-Projetos\snake_game-main\base_snake.csv', index=False)

            # Returns to the initial page
            display_menu = True

        pg.display.update()
    pg.display.update()