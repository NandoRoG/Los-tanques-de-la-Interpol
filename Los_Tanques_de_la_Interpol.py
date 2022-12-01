import tkinter as tk
from tkinter import messagebox
import numpy as np
from numpy import random 
import pygame
from pygame import MOUSEBUTTONUP, MOUSEBUTTONDOWN
from pygame.locals import( RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,) 

pygame.init()
def goodShotPrint(screen,rect):
     arr =[]
     arr.append("Ay mi madre el bicho!!!")
     arr.append("Sera o no sera")
     arr.append("Si fallo le puedo echar la culpa a la aritmetica")
     rand = random.random_integers(0,len(arr)-1)
     fuente = pygame.font.Font(None,24)
     msg = fuente.render(arr[rand],1,(0,0,0))
     screen.blit(msg,rect)
def printPregunta():
    res = messagebox.askquestion("El flotante de x es x(1+e)?")
    if res == "yes": return True 
    else: return False 

class Player(pygame.sprite.Sprite):
    
    def __init__(self, x,y,z):
        super(Player, self).__init__()
        self.pos = [x,y]
        self.x_points = [x]
        self.y_points = [y]
        self.surf = pygame.image.load(f"Pictures/{z}.jpg")
        self.rect = (x,y)
        
    
    def fire(self, screen):
        
        if len(self.x_points) != 3 or len(self.y_points) !=3:
            screen.fill((255,255,255))
            fuente = pygame.font.Font(None,72)
            msg = fuente.render("Son dos puntos, vuelva a intentarlo",1,(255,0,0))
            screen.blit(msg,(350,50))
            self.x_points = [self.x_points[0]]
            self.y_points = [self.y_points[0]]
            return False;
        pol = np.polyfit(self.x_points,self.y_points,2)
        if np.abs(pol[0]) < 0.0003 or pol[0] < 0:
               screen.fill((255,255,255))
               fuente = pygame.font.Font(None,72)
               msg = fuente.render("Tiro imposible, vuelva a intentarlo",1,(255,0,0))
               screen.blit(msg,(350,50))
               
               self.x_points = [self.x_points[0]]
               self.y_points = [self.y_points[0]]
               return False
        bullet = pygame.image.load("Pictures/images (2).jpg")
        bullet = pygame.transform.scale(bullet,(50,25))
        trace = []
        
        correct = printPregunta()
        a = 1
        if correct: a = 3
        audio = pygame.mixer.Sound("Pictures/Cymatics - Gunshot Beefy.wav")
        audio.play()
        for i in range(self.x_points[0],screen.get_width(),a):
               y =  pol[0]*(i**2)+pol[1]*i + pol[2]
               if y > screen.get_height() or i == screen.get_width():
                   screen.fill((255, 255, 255))
                   PrintGame()
                   pygame.display.flip()
                   
                   
               yder = 2*pol[0]*(i)+pol[1]
               

               if y < screen.get_height() and y>0:
                   screen.fill((255, 255, 255))
                   PrintGame()
                   for j in range (len(trace)):
                       if j > 60:
                           pygame.draw.circle(screen,(110,110,110),trace[j],4)
                       if j > 30:
                           pygame.draw.circle(screen,(170,170,170),trace[j],3)
                       else:
                           pygame.draw.circle(screen,(200,200,200),trace[j],3)
                   screen.blit(bullet,(i,y))
                   goodShotPrint(screen,(i -40,y -25))
                   trace.append((i,y))
                   if len(trace) > 100:
                       trace.pop(0)
                   pygame.display.flip()
                   

               
        return True
class FireButton(pygame.sprite.Sprite):
    def __init__(self):
        super(FireButton, self).__init__()
        image = pygame.image.load("Pictures/images (1).jpg")
        self.rect = (600,600)
        self.surf = pygame.transform.scale(image,(100,40))
        
class Turn():
    def __init__(self,x):
        super(Turn, self).__init__()
        self.ActualPlayer = x[0]
        self.num =0
        self.Players = x
    def change(self):
        if self.ActualPlayer == self.Players[len(self.Players)-1]:
            self.ActualPlayer = self.Players[0]
            self.num = 0
        else:
            self.num = self.num + 1
            self.ActualPlayer = self.Players[self.num]

# Set up the drawing window
screen = pygame.display.set_mode([1500, 780])
pygame.display.set_caption("Los Tanques de la Interpol...")
screen.fill((255, 255, 255))

x1 = [20]
y1 = [400]
x2 = [1250]
y2 = [400]
a = Player(x1[0],y1[0],"images")
b = Player(x2[0],y2[0],"images2")
c = FireButton()
def PrintGame():
    screen.blit(a.surf,a.rect)
    screen.blit(b.surf,b.rect)
    screen.blit(c.surf,c.rect) 
    

turn = Turn([a,b])

# Run until the user asks to quit
running = True
on_click = False
while running:
    
    PrintGame()
    
       
        

    
    
    
    but =  pygame.mouse.get_pressed(3)
    if but[0] and not on_click:
        on_click = True
        if x_mouse > c.rect[0] and x_mouse < c.rect[0] + c.surf.get_width() and y_mouse > c.rect[1] and y_mouse < c.rect[1] + c.surf.get_height():
                   if turn.ActualPlayer.fire(screen):
                       turn.change()
                   
        else:
                    turn.ActualPlayer.x_points.append(x_mouse)
                    turn.ActualPlayer.y_points.append(y_mouse)
                    pygame.draw.circle(screen, (255, 0, 0), (x_mouse,y_mouse), 4)
    for event in pygame.event.get():
        x_mouse, y_mouse = pygame.mouse.get_pos()
        if x_mouse > c.rect[0] and x_mouse < c.rect[0] + c.surf.get_width() and y_mouse > c.rect[1] and y_mouse < c.rect[1] + c.surf.get_height() and on_click:
               c.surf = pygame.image.load("Pictures/images (2).jpg")
               c.surf = pygame.transform.scale(c.surf,(100,40))
               screen.blit(c.surf,c.rect)
        if event.type == MOUSEBUTTONUP:
            
            on_click = False
        
        #Did the user click the window close button? If so, stop the loop.
        if event.type == QUIT:
            running = False
        
          # Did the user click the window close button?
        if event.type == pygame.QUIT:
            running = False
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
        # Flip the display
   
        pygame.display.flip()


