from a_star_path_finding import AStar
from bfs import BFS
from qLearning import QLearning

'''
AutoPlayer class that choose wich algorithm to choose from
'''


class AutoPlayer:

    def __init__(self):
        self.bestPath = []
        self.walls = None
        self.apple = None
        self.start = None
        self.expnaded = 0
        self.generated = 0
        self.bfs = BFS()

    def init_board(self, walls, target, start):
        self.apple = target
        self.start = start
        self.walls = walls
        return


    '''
    connect to A star Ai , and recive path 
    '''

    def connect_a_star(self):
        a_star = AStar()
        a_star.init_grid(20, 20, self.walls, self.start, self.apple)
        path_a_star = a_star.solve()
        self.bestPath = path_a_star
        self.expnaded = len(a_star.total_expended)
        self.generated = a_star.total_generated

        return path_a_star
    '''
    connect to A star Ai , and recive path 
    '''

    def connect_bfs(self):
        self.bfs.init_grid(20, 20, self.walls, self.start, self.apple)
        path_bfs = self.bfs.solve()
        self.bestPath = path_bfs
        self.expnaded = len(self.bfs.total_expended)
        self.generated = self.bfs.total_generated

        return path_bfs

    '''
    connect to q_learning , and recive path 
    '''

    def connect_q_learning(self):
        q_learning = QLearning(20, self.walls, self.start, self.apple)
        path_q_learning = q_learning.get_path()
        self.bestPath = path_q_learning

    '''
    function to get the next step from the q_learning result 
    '''

    def find_next_step(self):
        path = None
        if len(self.bestPath) != 0:
            path = self.bestPath[0]
            self.bestPath = self.bestPath[1:]
        if path is not None and len(path) != 0:
            if path[0] < self.start[0]:
                self.start = path
                return 1
            if path[0] > self.start[0]:
                self.start = path
                return 2
            if path[1] < self.start[1]:
                self.start = path
                return 3
            if path[1] > self.start[1]:
                self.start = path
                return 4
        else:
            return None

    def find_next_move_a_star(self):
        path = self.connect_a_star()
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


    def find_next_move_bfs(self):
        path = self.connect_bfs()
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
