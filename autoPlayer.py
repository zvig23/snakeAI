import pygame

from a_star_path_finding import AStar
from qLearning import qLearning
from hamilthon import hamilton_solver


class AutoPlayer:

    def __init__(self):
        self.bestPath = []
        self.walls = None
        self.apple = None
        self.start = None

    def initBoard(self, walls, target, start):
        self.apple = target
        self.start = start
        self.walls = walls
        return

    def connet_Astar(self):
        a_star = AStar()
        a_star.init_grid(20, 20, self.walls, self.start, self.apple)
        path_Astar = a_star.solve()
        self.bestPath = path_Astar
        return path_Astar

    def connect_Qlearning(self):
        q_learning = qLearning(20, self.walls, self.start, self.apple)
        path_qlearning = q_learning.getPath()
        print(path_qlearning)
        return path_qlearning

    def connect_Hamilton(self):
        hamilton = hamilton_solver(20, self.walls, self.start, self.apple)
        path_qlearning = hamilton.getPath()
        print(path_qlearning)
        return path_qlearning

    def find_next_step(self):
        path = self.connect_Hamilton()
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
