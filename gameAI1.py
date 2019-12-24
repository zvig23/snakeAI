import random
import pygame
import tkinter as tk
from tkinter import messagebox
import math
from random import randrange
from autoPlayer import AutoPlayer
import threading


class cube(object):
    rows = 20
    w = 500
    walls = []

    def __init__(self, start, dirnx=1, dirny=0, color=(255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)


class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self, direction):
        print("move", direction)

        # keys = pygame.key.get_pressed()
        # for key in keys:
        if direction == 1:  # keys[pygame.K_LEFT]:
            print("move left")
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif direction == 2:  # keys[pygame.K_RIGHT]:
            print("move right")
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif direction == 3:  # keys[pygame.K_UP]:
            print("move up")
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif direction == 4:  # keys[pygame.K_DOWN]:
            print("move down")
            self.dirnx = 0
            self.dirny = 1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        else:
            print("NONE")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    x = 0
    y = 0
    m = 0
    for i in range(rows):
        if (i == 0):
            pygame.draw.rect(surface, (165, 42, 42), (x, y, sizeBtwn, sizeBtwn))
            for j in range(rows):
                x = x + sizeBtwn
                pygame.draw.rect(surface, (165, 42, 42), (x, y, sizeBtwn, sizeBtwn))
        elif (i == 2):
            x = 0
            y = sizeBtwn * 19
            pygame.draw.rect(surface, (165, 42, 42), (x, y, sizeBtwn, sizeBtwn))
            for j in range(rows):
                x = x + sizeBtwn
                pygame.draw.rect(surface, (165, 42, 42), (x, y, sizeBtwn, sizeBtwn))
        else:
            x = 0
            m = m + sizeBtwn
            pygame.draw.rect(surface, (165, 42, 42), (x, m, sizeBtwn, sizeBtwn))
            x = sizeBtwn * 19
            pygame.draw.rect(surface, (165, 42, 42), (x, m, sizeBtwn, sizeBtwn))

    # x = x + sizeBtwn
    #  y = y + sizeBtwn

    # pygame.draw.rect(surface, (255, 0, 0), (x-1, y-1, sizeBtwn , sizeBtwn ))
    # pygame.draw.rect(surface, (255, 0, 0), (x * sizeBtwn, y * sizeBtwn, sizeBtwn, sizeBtwn))


def redrawWindow(surface):
    global rows, width, s, apple
    surface.fill((0, 0, 0))
    s.draw(surface)
    apple.draw(surface)
    drawGrid(width, rows, surface)
    pygame.display.update()


def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(1, 18)
        y = random.randrange(1, 18)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def set_snake_body_as_walls():
    body_walls = []
    for a in s.body:
        body_walls.append((a.pos))
    return body_walls


def connectAI():
    global s, apple, board_walls

    body_walls = set_snake_body_as_walls()
    start = body_walls[0]
    target = apple.pos
    ap = AutoPlayer()
    body_walls = body_walls[1:]
    body_walls.extend(board_walls)
    ap.initBoard(body_walls, target, start)
    #ap.connect_Qlearning()
    move_pos = ap.find_next_step()
    if move_pos != None:
        return move_pos


def set_board_walls():
    board_walls = []
    for i in range(0, 20):
        board_walls.append((0, i))
        board_walls.append((19, i))
        board_walls.append((i, 0))
        board_walls.append((i, 19))
    return board_walls


def main():
    global width, rows, s, apple, board_walls
    width = 500
    rows = 20
    board_walls = set_board_walls()
    win = pygame.display.set_mode((width, width))
    s = snake((255, 0, 0), (10, 10))
    apple = cube(randomSnack(rows, s), color=(0, 255, 0))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(25)
        clock.tick(10)
        s.move(connectAI())

        if s.body[0].pos == apple.pos:
            s.addCube()
            apple = cube(randomSnack(rows, s), color=(0, 255, 0))

        if s.body[0].pos[0] == 0 or s.body[0].pos[1] == 0:
            print('Score: ', len(s.body))
            # message_box('You Lost!', 'your score is '+str(len(s.body)))
            s.reset((10, 10))
            break

        if s.body[0].pos[0] == 19 or s.body[0].pos[1] == 19:
            print('Score: ', len(s.body))
            # message_box('You Lost!', 'your score is '+str(len(s.body)))
            s.reset((10, 10))
            break

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
                print('Score: ', len(s.body))
                # message_box('You Lost!', 'Play again...')
                s.reset((10, 10))
                print("---------------------")
                break

        redrawWindow(win)

    print()
    pass


main()
