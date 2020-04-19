import sys
import random
import math
import pygame
import pygame as pg
import tkinter as tk
from tkinter import messagebox


# Colors
red = pg.Color(255, 0, 0)
green = pg.Color(0, 255, 0)
black = pg.Color(0, 0, 0)
white = pg.Color(255, 255, 255)
brown = pg.Color(165, 42, 42)

global score

#Show Score
def showScore(choice=1):
    SFont = pygame.font.SysFont('times', 28)
    Ssurf = SFont.render("Score  :  {0}".format(score), True, black)
    Srect = Ssurf.get_rect()
    if choice == 1:
        Srect.midtop = (200, 100)
    else:
        Srect.midtop = (400, 200)
    playSurface.blit(Ssurf, Srect)


class cube(object):
    rows = 20
    w = 500
    def __init__(self, start, cordx=1, cordy=0, color=(255, 0, 0)):
        self.pos = start
        self.cordx = 1
        self.cordy = 0
        self.color = color
 
       
    def move(self, cordx, cordy):
        self.cordx = cordx
        self.cordy = cordy
        self.pos = (self.pos[0] + self.cordx, self.pos[1] + self.cordy)
 
    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
 
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
       
 
 
 
class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.cordx = 0
        self.cordy = 1
 
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
 
            keys = pygame.key.get_pressed()
 
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.cordx = -1
                    self.cordy = 0
                    self.turns[self.head.pos[:]] = [self.cordx, self.cordy]
 
                elif keys[pygame.K_RIGHT]:
                    self.cordx = 1
                    self.cordy = 0
                    self.turns[self.head.pos[:]] = [self.cordx, self.cordy]
 
                elif keys[pygame.K_UP]:
                    self.cordx = 0
                    self.cordy = -1
                    self.turns[self.head.pos[:]] = [self.cordx, self.cordy]
 
                elif keys[pygame.K_DOWN]:
                    self.cordx = 0
                    self.cordy = 1
                    self.turns[self.head.pos[:]] = [self.cordx, self.cordy]
 
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.cordx == -1 and c.pos[0] <= 0: c.pos = (c.rows - 1, c.pos[1])
                elif c.cordx == 1 and c.pos[0] >= c.rows-1: c.pos = (0, c.pos[1])
                elif c.cordy == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                elif c.cordy == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], c.rows - 1)
                else: c.move(c.cordx, c.cordy)


            #if s.body[0] in s.body[1:]: break
            # Self hit
            for block in s.body[1:]:
                if c.pos == block:
                    content = "GAME OVER!!"
                    message_box("\'You Lost!' '\', '\'Play again...' '\'", content)
                    #s.reset((10, 10))
                    #break
                    pygame.quit()
                    sys.exit()
                    # gameOver()
       
 
    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.cordx = 0
        self.cordy = 1
 
 
    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.cordx, tail.cordy
 
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))
 
        self.body[-1].cordx = dx
        self.body[-1].cordy = dy
       
 
    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)
 
 
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
 
    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn
 
        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))
       
 
def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,255))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width,rows, surface)
    pygame.display.update()
 
 
def randomSnack(rows, item):
 
    positions = item.body
 
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break
       
    return (x,y)
 
 
def message_box(subject, content):
    window = tk.Tk()
    window.attributes("-topmost", True)
    window.withdraw()
    messagebox.showinfo(subject, content)
    try:
        window.destroy()
    except:
        pass

 
def main():
    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    pg.display.set_caption('Python Snake_Game')
    s = snake((255,0,0), (10,10))
    snack = cube(randomSnack(rows, s), color=(0,255,0))
    flag = True
    score = 0
 
    clock = pygame.time.Clock()
   
    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            score += 1
            snack = cube(randomSnack(rows, s), color=(0,255,0))
        # else:
        #     s.body.pop()
 
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                print("\'Score: \', len(s.body)")
                content = "GAME OVER!!"
                message_box("\'You Lost!' '\', '\'Play again...' '\'", content)
                s.reset((10,10))
                #break
                showScore()
                pygame.quit()
                sys.exit()

        redrawWindow(win)
    pass

if __name__ == '__main__':
    main()
