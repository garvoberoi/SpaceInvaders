import math
import pygame
import random
from pygame import mixer

# initialise the pygame
pygame.init()

# create a screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.jpg')

# Title and Icon
pygame.display.set_caption("Space Invaders")  # Setting the name of window
icon = pygame.image.load('icon.png')  # loading the image into variable icon
pygame.display.set_icon(icon)  # setting the icon of window

# player
playership = pygame.image.load('playership.png')  # loading the imgae of player ship in the variable
playerx = 380  # setting the position of the image
playery = 500
playerx_change = 0

# Alien
alienship = []
alienx = []
alieny = []
alienx_change = []
alieny_change = []
num_of_aliens = 10

for i in range(num_of_aliens):
    alienship.append(pygame.image.load('alien.png'))  # loading the imgae of alien ship in the variable
    alienx.append(random.randint(0, 736))  # setting random position of alien
    alieny.append(random.randint(10, 80))
    alienx_change.append(3)
    alieny_change.append(40)


# bullet
# Ready = bullet is ready to fire
# fire = bullet is moving
bullet = pygame.image.load('bullet.png')  # loading the imgae of bullet in the variable
bulletx = 380  # setting the position of the image
bullety = 500
bullety_change = 20
bullet_state = "ready"

playing = True

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textx = 0
texty = 0

# game over
over_text = pygame.font.Font('freesansbold.ttf', 70)

# background music
mixer.music.load('background.wav')
mixer.music.play(-1) # playing background music on the loop


def scores(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))   # rendering the text
    screen.blit(score, (x, y)) # displaying the text


def game_over_text():
    over = over_text.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (190, 250))
    f_score = font.render("Final Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(f_score, (290, 330))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 16, y + 10))


def player(x, y):
    screen.blit(playership, (x, y))  # Drawing the img on the screen


def alien(x, y, i):
    screen.blit(alienship[i], (x, y))



def iscollision(alienx, alieny, bulletx, bullety):
    distance = math.sqrt((math.pow(alienx - bulletx, 2)) + (math.pow(alieny - bullety, 2))) # calculating the distance between bullet and alien
    if distance < 40:
        return True
    else:
        return False


# Game loog
running = True
while running:

    # RGB = Red,Green,Blue(0-255)
    screen.fill((22, 22, 58))  # setting colour of backgroung
    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():  # for every event that happens in game
        if event.type == pygame.QUIT:  # if the cross button is pressed by the user
            running = False

        # if keystroke is pressed check whether its left or right
        if event.type == pygame.KEYDOWN:  # checking if any key is pressed down
            if event.key == pygame.K_LEFT:  # checking if LEFT key if pressed
                playerx_change = -7
            if event.key == pygame.K_RIGHT:  # checking if right key if pressed
                playerx_change = 7
            if event.key == pygame.K_SPACE:  # if space is pressed
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)
        if event.type == pygame.KEYUP:  # checking if any key is released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0

    # player movement
    playerx += playerx_change  # increment the value of position of ship
    if playerx <= 0:  # until a boundary
        playerx = 0
    elif playerx >= 736:
        playerx = 736


    for i in range(num_of_aliens):
        # alien movement
        if alieny[i] > 400:
            for j in range(num_of_aliens):
                alieny[j] = 2000
            game_over_text()
            playing = False
            break

        alienx[i] += alienx_change[i]
        if alienx[i] <= 0:
            alienx_change[i] = 4
            alieny[i] += alieny_change[i]
        elif alienx[i] >= 736:
            alienx_change[i] = -4
            alieny[i] += alieny_change[i]

        # Collision
        collision = iscollision(alienx[i], alieny[i], bulletx, bullety)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bullety = 480
            bullet_state = "ready"
            score_value += 1
            alienx[i] = random.randint(0, 736)
            alieny[i] = random.randint(10, 80)
        alien(alienx[i], alieny[i], i)


    # bullet movement
    if bullety <= 0:
        bullety = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletx, bullety)
        bullety -= bullety_change

    player(playerx, playery)
    if playing:
        scores(textx, texty)
    pygame.display.update()  # always updating the screen
