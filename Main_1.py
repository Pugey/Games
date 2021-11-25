
#%%
import pygame
import random
import math
from pygame import mixer




#initialize the pygame
pygame.init()

#create the screen, width 800, height 600
screen = pygame.display.set_mode((800,600))

# background
background = pygame.image.load("Background.jpg")


#background song
mixer.music.load("time.mp3")
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("Alien.png")
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("ghost.png"))
    enemyX.append(random.randint(0,700))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(2)
    enemyY_change.append(20)

#bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)

textX = 10
testY = 10

#Game over text
over_font = pygame.font.Font("freesansbold.ttf",64)


def show_score(x, y):
    score = font.render("score : " +  str(score_value),True, (255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = font.render("GAME OVER", True, (255,0,0))
    screen.blit(over_text, (290, 265))


def player(x,y):
    screen.blit(playerImg, (x, y))


def enemy(x,y, i):
    screen.blit(enemyImg[i], (x,y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x + 16, y + 10))

def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + math.pow(enemyY-bulletY,2))
    if distance < 27:
        return True
    else:
        return False

# Game Loop
running = True
while running: 

    #RGB - Red, Green, Blue
    screen.fill((25,50,50))
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            # Write score to db
            ###################################################
            import sqlite3                          
            conn = sqlite3.connect('score.db')   
            c=conn.cursor()

            #c.execute("""CREATE TABLE scores (name text, score integer)""") 

            navn=input("Skriv inn navnet ditt:")
            # score_value må konverteres til string
            sqlite_insert_query = "INSERT INTO scores (name, score) VALUES ('" + navn + "'," + str(score_value) + ");" 
            c.execute(sqlite_insert_query)
            conn.commit()
            conn.close()
            pygame.quit()

    # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(playerX,bulletY)
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #Checkeing for boundaries of spaceship so it doesn't go out of bounds
    playerX += playerX_change      

    if playerX <=0:
        playerX = 0
    elif playerX >=670:
        playerX = 670

    #enemy movement
    for i in range(num_of_enemies):

        
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]    
        if enemyX[i] <=0:
            enemyX_change[i] = 7
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >=736:
            enemyX_change[i] = -7
            enemyY[i] += enemyY_change[i]

    # collison
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("bang.mp3")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 100
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i], enemyY[i], i)

    #bullet movement
    if bulletY <=0 :
        bulletY = 480
        bullet_state = "ready"

    if  bullet_state is "fire":
         fire_bullet(bulletX,bulletY)
         bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()

# %%
