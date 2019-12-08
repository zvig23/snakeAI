import pygame

from a_star_path_finding import AStar


class autoPlayer(object):

    def __init__(self):
        self.board = [[]]
        self.bestPath=[]
        self.walls=[]
        self.head=self.walls[0]
        self.apple=()

    def initBoard(self,board,walls,target):
        self.board=board
        i=0
        j=0
        while i<20:
            while j<20:
                if board[i][j]==1:
                    self.walls.append((i,j))
                if board[i][j] == 2:
                    self.apple=(i, j)
        return

    def findBestPath(self):
        a = AStar()
        walls = self.walls
        # for i in range(1,20):
        #     for j in range(1,20):
        #         if j==1 or j==19:
        #             walls.append((i,j))
        #     if i == 1 or i == 19:
        #         walls.append((i, j))
        # # print (walls)
        a.init_grid(20, 20, walls, self.head, (5, 5))
        path = a.solve()
        self.bestPath= path

    def getNextDirection(self,headPos):
        nextStage=self.bestPath.pop()
        nextStape=\
            (self.head()[0]-nextStage()[0],
             self.head()[1]-nextStage()[1])

        if nextStape==(-1,0):
            return pygame.K_LEFT

        elif nextStape==(1,0):
            return pygame.K_RIGHT

        elif nextStape==(0,-1):
            return pygame.K_UP

        elif nextStape==(0,1):
            return pygame.K_DOWN

ai = autoPlayer()
print(ai.findBestPath())