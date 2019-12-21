import pygame

from a_star_path_finding import AStar


class AutoPlayer:

    def __init__(self):
        self.bestPath = []
        self.walls = None
        self.apple = None
        self.start = None
        self.path = None

    def initBoard(self, walls, target, start):
        self.apple = target
        self.start = start
        self.walls = walls
        return

    def find_next_step(self):
        a = AStar()
        a.init_grid(20, 20, self.walls, self.start, self.apple)
        path = a.solve()
        self.bestPath = path
        print(path)
        if path is not None:
            if path[1][0] < self.start[0]:
                return 1
            if path[1][0] > self.start[0]:
                return 2
            if path[1][1] < self.start[1]:
                return 3
            if path[1][1] > self.start[1]:
                return 4
        else:
            return None
