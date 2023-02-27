import random
import time
from pathlib import Path

import pandas as pd
import pygame

from autoPlayer import AutoPlayer

from kivy.uix.label import Label
from kivy.uix.popup import Popup
from sys import exit


global results
global game_id
global curr_score

results = pd.DataFrame(columns=["timestamp", "time to calculate", "generated nodes", "expanded nodes", "score"])
game_id = time.time()
curr_score = 0


class Cube(object):
    rows = 20
    w = 500
    walls = []

    def __init__(self, start, color=(255, 0, 0)):
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
            circle_middle = (i * dis + centre - radius, j * dis + 8)
            circle_middle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circle_middle2, radius)


class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move_human(self):
        keys = pygame.key.get_pressed()
        for key in keys:
            if keys[pygame.K_LEFT]:
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif keys[pygame.K_RIGHT]:
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif keys[pygame.K_UP]:
                self.dirnx = 0
                self.dirny = -1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            elif keys[pygame.K_DOWN]:
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

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

    def move(self, direction):

        if direction == 1:
            self.dirnx = -1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif direction == 2:
            self.dirnx = 1
            self.dirny = 0
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif direction == 3:
            self.dirnx = 0
            self.dirny = -1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        elif direction == 4:
            self.dirnx = 0
            self.dirny = 1
            self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        else:
            print("Im gonna die")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

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
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def draw_grid(w, rows, surface):
    size_btwn = w // rows
    x = 0
    y = 0
    m = 0
    for i in range(rows):
        if i == 0:
            pygame.draw.rect(surface, (165, 42, 42), (x, y, size_btwn, size_btwn))
            for j in range(rows):
                x = x + size_btwn
                pygame.draw.rect(surface, (165, 42, 42), (x, y, size_btwn, size_btwn))
        elif i == 2:
            x = 0
            y = size_btwn * 19
            pygame.draw.rect(surface, (165, 42, 42), (x, y, size_btwn, size_btwn))
            for j in range(rows):
                x = x + size_btwn
                pygame.draw.rect(surface, (165, 42, 42), (x, y, size_btwn, size_btwn))
        else:
            x = 0
            m = m + size_btwn
            pygame.draw.rect(surface, (165, 42, 42), (x, m, size_btwn, size_btwn))
            x = size_btwn * 19
            pygame.draw.rect(surface, (165, 42, 42), (x, m, size_btwn, size_btwn))


def redraw_window(surface):
    global rows, width, s, apple
    surface.fill((0, 0, 0))
    s.draw(surface)
    apple.draw(surface)
    draw_grid(width, rows, surface)
    pygame.display.update()


def random_snack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(1, 18)
        y = random.randrange(1, 18)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break

    return (x, y)


def set_snake_body_as_walls():
    body_walls = []
    for a in s.body:
        body_walls.append((a.pos))
    return body_walls


def connect_ai_a_start():
    global curr_score
    global game_id
    global results
    body_walls = set_snake_body_as_walls()
    start = body_walls[0]
    target = apple.pos
    ap = AutoPlayer()
    body_walls = body_walls[1:]
    body_walls.extend(board_walls)
    ap.init_board(body_walls, target, start)
    calc_time = time.time()
    move_pos = ap.find_next_move_a_star()
    if (curr_score == 0) or (curr_score != len(body_walls)):
        if move_pos != None:
            curr_score = len(body_walls)
            row = ["Astar", time.time() - calc_time, ap.generated, ap.expnaded, curr_score-80]
            results.loc[len(results.index)] = row

    if move_pos is not None:
        return move_pos


'''
conncet to q_learning AI and get path 
'''


def connect_ai():
    move_pos = ap.find_next_step()
    if move_pos is not None:
        return move_pos


def set_board_walls():
    board_walls = []
    for i in range(0, 20):
        board_walls.append((0, i))
        board_walls.append((19, i))
        board_walls.append((i, 0))
        board_walls.append((i, 19))
    return board_walls


'''
run the game as BFS player 
'''
def run_bfs_game():
    global width, rows, s, apple, board_walls, ap
    width = 500
    rows = 20
    board_walls = set_board_walls()
    win = pygame.display.set_mode((width, width))
    s = Snake((255, 0, 0), (10, 10))
    s.reset((10, 10))

    apple = Cube(random_snack(rows, s), color=(0, 255, 0))
    flag = True
    clock = pygame.time.Clock()
    player = "A_star"
    while flag:
        pygame.time.delay(25)
        clock.tick(10)
        s.move(connect_bfs_start())

        if s.body[0].pos == apple.pos:
            s.add_cube()
            apple = Cube(random_snack(rows, s), color=(0, 255, 0))

        if check_for_end_game(s, player):
            break
        else:
            redraw_window(win)
    global results
    filepath = Path('C:/Users/dvirl/PycharmProjects/snakeAI/results BFS/BFS ' + str(time.time())[0:12] + ".csv")
    results.to_csv(filepath)
    pygame.quit()
    # exit()

def connect_bfs_start():
    global curr_score
    global game_id
    global results
    body_walls = set_snake_body_as_walls()
    start = body_walls[0]
    target = apple.pos
    ap = AutoPlayer()
    body_walls = body_walls[1:]
    body_walls.extend(board_walls)
    ap.init_board(body_walls, target, start)
    calc_time = time.time()
    move_pos = ap.find_next_move_bfs()
    if (curr_score == 0) or (curr_score != len(body_walls)):
        if move_pos != None:
            curr_score = len(body_walls)
            row = ["BFS", time.time() - calc_time, ap.generated, ap.expnaded, curr_score-80]
            results.loc[len(results.index)] = row

    if move_pos is not None:
        return move_pos



'''
run the game as A-star AI player 
'''


def run_a_star_game():
    global width, rows, s, apple, board_walls, ap
    width = 500
    rows = 20
    board_walls = set_board_walls()
    win = pygame.display.set_mode((width, width))
    s = Snake((255, 0, 0), (10, 10))
    s.reset((10, 10))

    apple = Cube(random_snack(rows, s), color=(0, 255, 0))
    flag = True
    clock = pygame.time.Clock()
    player = "A_star"
    while flag:
        pygame.time.delay(25)
        clock.tick(10)
        s.move(connect_ai_a_start())

        if s.body[0].pos == apple.pos:
            s.add_cube()
            apple = Cube(random_snack(rows, s), color=(0, 255, 0))

        if check_for_end_game(s, player):
            break
        else:
            redraw_window(win)
    global results
    filepath = Path('C:/Users/dvirl/PycharmProjects/snakeAI/results Astar/Astar ' + str(time.time())[0:12] + ".csv")
    results.to_csv(filepath)
    pygame.quit()
    # exit()


'''
run the game as q_learning AI machine
'''


def run_q_learning_game():
    global width, rows, s, apple, board_walls, ap
    global curr_score
    global game_id
    global results
    width = 500
    rows = 20
    board_walls = set_board_walls()
    win = pygame.display.set_mode((width, width))
    s = Snake((255, 0, 0), (10, 10))
    s.reset((10, 10))

    apple = Cube(random_snack(rows, s), color=(0, 255, 0))
    flag = True
    clock = pygame.time.Clock()

    body_walls = set_snake_body_as_walls()
    start = body_walls[0]
    target = apple.pos
    ap = AutoPlayer()
    body_walls = body_walls[1:]
    body_walls.extend(board_walls)
    ap.init_board(body_walls, target, start)
    calc_time = time.time()
    ap.connect_q_learning()
    player = "results Q_learning"
    if (curr_score == 0) or (curr_score != len(body_walls)):
        curr_score = len(body_walls)
        row = ["results Q_learning", time.time() - calc_time, 400, 400, curr_score]
        results.loc[len(results.index)] = row

    while flag:
        pygame.time.delay(25)
        clock.tick(10)
        s.move(connect_ai())

        if s.body[0].pos == apple.pos:
            s.add_cube()
            apple = Cube(random_snack(rows, s), color=(0, 255, 0))
            body_walls = set_snake_body_as_walls()
            start = body_walls[0]
            target = apple.pos
            ap = AutoPlayer()
            body_walls = body_walls[1:]
            body_walls.extend(board_walls)
            ap.init_board(body_walls, target, start)
            calc_time = time.time()
            ap.connect_q_learning()
            if (curr_score == 0) or (curr_score != len(body_walls)):
                curr_score = len(body_walls)
                row = ["results Q_learning", time.time() - calc_time, 400-len(s.body), len(ap.bestPath)*4, curr_score-80]
                results.loc[len(results.index)] = row

        if check_for_end_game(s, player):
            break
        else:
            redraw_window(win)
    filepath = Path('C:/Users/dvirl/PycharmProjects/snakeAI/results Q_learning/Q_learning ' + str(time.time())[0:12] + ".csv")
    results.to_csv(filepath)
    results.truncate()
    pygame.quit()
    # exit()


'''
run the game as human player 
'''


def run_human_game():
    global width, rows, s, apple, board_walls, ap
    width = 500
    rows = 20
    board_walls = set_board_walls()
    win = pygame.display.set_mode((width, width))
    s = Snake((255, 0, 0), (10, 10))
    s.reset((10, 10))
    apple = Cube(random_snack(rows, s), color=(0, 255, 0))
    flag = True
    clock = pygame.time.Clock()
    player = "human"
    while flag:
        pygame.time.delay(25)
        clock.tick(10)
        s.move_human()

        if s.body[0].pos == apple.pos:
            s.add_cube()
            apple = Cube(random_snack(rows, s), color=(0, 255, 0))

        if check_for_end_game(s, player):
            break
        else:
            redraw_window(win)
    pygame.quit()
    # exit()


'''
pop up windwos with the results
'''


def show_result(score, player):
    show_content = player + ' score :' + str(score)
    pop_win = Popup(title="score", size_hint=(None, None), size=(400, 400))
    pop_win.add_widget((Label(text=show_content)))
    pop_win.open()
    pass


'''
check if the game is ended 
and call the function that pop up windwos with the results
'''


def check_for_end_game(s, player):
    if s.body[0].pos[0] == 0 or s.body[0].pos[1] == 0:
        print('Score: ', len(s.body))
        show_result(len(s.body), player)
        # s.reset((10, 10))
        return True

    if s.body[0].pos[0] == 19 or s.body[0].pos[1] == 19:
        print('Score: ', len(s.body))
        show_result(len(s.body), player)
        # s.reset((10, 10))
        return True

    for x in range(len(s.body)):
        if s.body[x].pos in list(map(lambda z: z.pos, s.body[x + 1:])):
            print('Score: ', len(s.body))
            show_result(len(s.body), player)
            # s.reset((10, 10))
            print("---------------------")
            return True
    return False


'''
recive wich game to start 
and call the right function
'''


def start_game(game):
    if game == "a_star":
        run_a_star_game()
    elif game == "q_learning":
        run_q_learning_game()
    elif game == "bfs":
        run_bfs_game()
    elif game == "human":
        run_human_game()
