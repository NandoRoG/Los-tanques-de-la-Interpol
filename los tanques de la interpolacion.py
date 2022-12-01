# %%
import numpy as np
import pygame
import math

pygame.init()

# %%
def dropLeft(x, last):
    return ((x - 650) ** 2) / 2 + last

# %%
def dropRight(x, last):
    return ((x - 850) ** 2) / 2 + last

# %%
def DrawLand(screen: pygame.Surface, func, width, height):
    last = 0
    for i in range(width // 2):
        if i < width / 2 - 100:
           last = func(i)
           pygame.draw.line(screen, (155,118,83), (i, last), (i, height))
        else:
           pygame.draw.line(screen, (155,118,83), (i, dropLeft(i, last)), (i, height))

    for i in range(width, width // 2, -1):
        if i > width / 2 + 100:
           last = func(i)
           pygame.draw.line(screen, (155,118,83), (i, last), (i, height))
        else:
           pygame.draw.line(screen, (155,118,83), (i, dropRight(i, last)), (i, height))

# %%
#Effects

def game_over(screen: pygame.Surface, x_player, func, turn):
    fuente = pygame.font.Font(None,30)
    msg = fuente.render("Congratulations " + ("Player 1" if turn == 0 else "Player 2") + " !!!!!!!!",1,(255,0,0))
    screen.blit(msg,(700,200))
    pygame.display.flip()
    pygame.time.delay(5000)

def hit(screen: pygame.Surface, x_player, func, turn):
    fuente = pygame.font.Font(None,30)
    msg = fuente.render("Good one " + ("Player 1" if turn == 0 else "Player 2"),1,(255,0,0))
    screen.blit(msg,(700,200))
    pygame.display.flip()
    pygame.time.delay(2000)

def miss(screen: pygame.Surface, x_player, func, turn):
    fuente = pygame.font.Font(None,30)
    msg = fuente.render("Vete pa la Cujae " + ("Player 1" if turn == 0 else "Player 2") + " :|",1,(255,0,0))
    screen.blit(msg,(700,200))
    pygame.display.flip()
    pygame.time.delay(2000)

# %%
# Set up the drawing window
screen = pygame.display.set_mode([1500, 780])
pygame.display.set_caption("Los Tanques de la Interpol...")
screen.fill((64, 207, 255))

effect_game_over = [game_over]
effect_hit = [hit]
effect_miss = [miss]

# def func(x):
#     return 0.2 * x + 400
# def derFunc(x):
#     return 0.2

def func(x):
    return 650
def derFunc(x):
    return 0

DrawLand(screen, func, 1500, 780)

screenLand = screen.convert()

# %%
def printPlayers(screen: pygame.Surface, player1: pygame.Surface, player2: pygame.Surface, x_player1, x_player2, life_player1, life_player2):
    new = screen.convert()

    derivate1 = derFunc(x_player1)
    derivate2 = derFunc(x_player2)

    angle1 = math.atan(derivate1)
    angle2 = math.atan(derivate2)

    if angle1 != 0:
        divisor1 = math.pi / angle1
        angle1 = 180 / divisor1

    if angle2 != 0:
        divisor2 = math.pi / angle2
        angle2 = 180 / divisor2
    
    newPlayer1 = pygame.transform.rotate(player1, -1 * angle1)
    newPlayer2 = pygame.transform.rotate(player2, -1 * angle2)

    new.blit(newPlayer1, (x_player1 - newPlayer1.get_width() / 2, func(x_player1) - newPlayer1.get_height() + 22))
    new.blit(newPlayer2, (x_player2 - newPlayer2.get_width() / 2, func(x_player2) - newPlayer2.get_height() + 20))

    pygame.draw.circle(new, (0, 0, 0), (750, 700), 40)

    fuente = pygame.font.Font(None,30)
    msg = fuente.render("Fire",1,(255,0,0))
    new.blit(msg,(732,692))

    msg = fuente.render("Life: " + str(life_player1),1,(0,0,255))
    new.blit(msg,(20,740))
    msg = fuente.render("Life: " + str(life_player2),1,(255,0,0))
    new.blit(msg,(1380,740))

    return new

# %%
player1 = pygame.transform.scale(pygame.image.load('player1.png'), (100, 100))
player2 = pygame.transform.scale(pygame.image.load('player2.png'), (100, 100))
bala = pygame.transform.scale(pygame.image.load('bala.png'), (64, 31))
flip_bala = pygame.transform.flip(bala, True, False)

life_player1 = 1000
life_player2 = 1000

x_player1 = 50
x_player2 = 1450

new = printPlayers(screen, player1, player2, x_player1, x_player2, life_player1, life_player2)
screen.blit(new, (0,0))

screenLandPlayer = screen.convert()

turn = 0

points_x = []
points_y = []

shadow_x1 = []
shadow_y1 = []
shadow_x2 = []
shadow_y2 = []

# %%
def clear():
    if turn == 0:
        shadow_x1.clear()
        shadow_y1.clear()

        shadow_x1.append(points_x[0])
        shadow_x1.append(points_x[1])

        shadow_y1.append(points_y[0])
        shadow_y1.append(points_y[1])

    else:
        shadow_x2.clear()
        shadow_y2.clear()

        shadow_x2.append(points_x[0])
        shadow_x2.append(points_x[1])

        shadow_y2.append(points_y[0])
        shadow_y2.append(points_y[1])

    points_x.clear()
    points_y.clear()

# %%
def changeTurn(turn):
    clear()

    if turn == 0:
        return 1
    else:
        return 0

# %%
def derivatePol(pol):
    derPol = [0] * (len(pol) - 1)

    for i in range(len(pol) - 1):
        derPol[i] = pol[i] * (len(pol) - 1 - i)

    return derPol

# %%
import random


def fire(turn, life_player1, life_player2):
    if turn == 0:
        points_x.append(x_player1)
        points_y.append(func(x_player1) - 50)

    else:
        points_x.append(x_player2)
        points_y.append(func(x_player2) - 50)

    pol = np.polyfit(points_x, points_y, 2)
    derPol = derivatePol(pol)
    
    if np.abs(pol[0]) < 0.0003:
        fuente = pygame.font.Font(None,72)
        msg = fuente.render("Tiro imposible, vuelva a intentarlo",1,(255,0,0))
        
        screen.blit(msg,(350,50))
        pygame.display.flip()
        pygame.time.wait(1000)
        
        clear()
        screen.blit(screenLandPlayer, (0,0))
        pygame.display.flip()
        
        return False, life_player1, life_player2

    if turn == 0:
        r = range(x_player1, 1500, 2)
    else:
        r = range(x_player2, -1, -2)

    screen_old = screen.convert()

    count = 0

    for i in r:
            count += 1

            y = pol[0]*(i**2) + pol[1] * i + pol[2]

            if turn == 1:
               distance_withObj = ((x_player1 - i)**2 + (func(x_player1) - y)**2) ** 0.5
            else:
               distance_withObj = ((x_player2 - i)**2 + (func(x_player2) - y)**2) ** 0.5

            if distance_withObj <= 70:
                if turn == 1:
                    life_player1 -= 500
                else:
                    life_player2 -= 500

                random.choice(effect_hit)(screen, x_player1 if turn == 0 else x_player2, func, turn)
                
                screenLandPlayer.blit(printPlayers(screenLand, player1, player2, x_player1, x_player2, life_player1, life_player2), (0,0))
                screen.blit(screenLandPlayer, (0,0))
                pygame.display.flip()
                break

            elif y < func(i):
                screen.blit(screen_old, (0,0))

                if count % 12 == 0:
                   pygame.draw.circle(screen, (255, 0, 0), (i, y), 4)
                   screen_old = screen.convert()
                
                derivate = derPol[0] * i + derPol[1]
                
                angle = math.atan(derivate)
                divisor = math.pi / angle
                angle = 180 / divisor
                
                if turn == 0:
                    newBala = pygame.transform.rotate(bala, -1 * angle)
                else:
                    newBala = pygame.transform.rotate(flip_bala, -1 * angle)
                    
                screen.blit(newBala, (i - newBala.get_width() / 2, y - newBala.get_height() / 2))
                pygame.display.flip()
            else:
                random.choice(effect_miss)(screen, x_player1 if turn == 0 else x_player2, func, turn)
                break

    if i == 1499 or i == 0:
        random.choice(effect_miss)(screen, x_player1 if turn == 0 else x_player2, func, turn)

    screen.blit(screenLandPlayer, (0,0))
    pygame.display.flip()

    return True, life_player1, life_player2

# %%
def printMove():
    screenLandPlayer.blit(printPlayers(screenLand, player1, player2, x_player1, x_player2, life_player1, life_player2), (0,0))
    screen.blit(screenLandPlayer, (0,0))
    
    points_x.clear()
    points_y.clear()

    pygame.display.flip()  

# %%
pygame.display.flip()
running = True

while running:

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        if turn == 0:
           x_player1 += 1
        else:
           x_player2 += 1

        printMove()

    if keys[pygame.K_LEFT]:
        if turn == 0:
           x_player1 -= 1
        else:
           x_player2 -= 1

        printMove()

    if keys[pygame.K_SPACE]:
        if len(points_x) >= 2:
            ok, life_player1, life_player2 = fire(turn, life_player1, life_player2)
            if ok:
               turn = changeTurn(turn)

            if turn == 0 and len(shadow_x1) > 1:
                pygame.draw.circle(screen, (128, 128, 128), (shadow_x1[0], shadow_y1[0]), 10)
                pygame.draw.circle(screen, (128, 128, 128), (shadow_x1[1], shadow_y1[1]), 10)
            elif len(shadow_x2) > 1:
                pygame.draw.circle(screen, (128, 128, 128), (shadow_x2[0], shadow_y2[0]), 10)
                pygame.draw.circle(screen, (128, 128, 128), (shadow_x2[1], shadow_y2[1]), 10)
            pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
           
            x_mouse, y_mouse = pygame.mouse.get_pos()
        
            if len(points_x) <= 1:
                if (turn == 0 and x_mouse > 750) or (turn == 1 and x_mouse < 750):
                    continue
        
                points_x.append(x_mouse)
                points_y.append(y_mouse)
                pygame.draw.circle(screen, (0, 0, 0), (x_mouse, y_mouse), 10)
                pygame.display.flip()

            elif ((x_mouse - 750)** 2 + (y_mouse - 700)** 2)**0.5 <= 40:
                ok, life_player1, life_player2 = fire(turn, life_player1, life_player2)

                if life_player1 <= 0 or life_player2 <= 0:
                    random.choice(effect_game_over)(screen, x_player1 if turn == 0 else x_player2, func, turn)
                    running = False

                if ok:
                   turn = changeTurn(turn)

                if turn == 0 and len(shadow_x1) > 1:
                    pygame.draw.circle(screen, (128, 128, 128), (shadow_x1[0], shadow_y1[0]), 10)
                    pygame.draw.circle(screen, (128, 128, 128), (shadow_x1[1], shadow_y1[1]), 10)
                elif len(shadow_x2) > 1:
                    pygame.draw.circle(screen, (128, 128, 128), (shadow_x2[0], shadow_y2[0]), 10)
                    pygame.draw.circle(screen, (128, 128, 128), (shadow_x2[1], shadow_y2[1]), 10)
                pygame.display.flip()

        if event.type == pygame.QUIT:
            running = False
            pygame.display.quit()

        


