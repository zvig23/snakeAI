import numpy as np
import random as rnd


class hamilton_solver():
    def __init__(self, size, walls, headLoc, rewardLoc):
        np.random.seed(1)
        self.size=size
        self.F = np.zeros(shape=[size, size], dtype=np.float)
        self.start = headLoc
        self.goal = rewardLoc
        self.walls = walls
        self.initilizeBoard()

    def initilizeBoard(self):
        # walls
        for wall in self.walls:
            self.F[wall[0], wall[1]] = 1

    def hamilton(self, G, size, pt, target, path=[]):
        #    print('hamilton called with pt={}, path={}'.format(pt, path))
        if pt not in set(path):
            path.append(pt)
            if len(path) == size:
                return path
            for pt_next in G.get(pt, []):
                res_path = [i for i in path]
                candidate = self.hamilton(G, size, pt_next, res_path)
                if candidate is not None:  # skip loop or dead end
                    return candidate

    def get_poss_next_states(self, state):
        x = state[0]
        y = state[1]
        ans = []
        # right
        if self.isVlidMove(x + 1, y) and self.F[x + 1][y] != 1:
            ans.append((x + 1, y))
        # left
        if self.isVlidMove(x - 1, y) and self.F[x - 1][y] != 1:
            ans.append((x - 1, y))
        # up
        if self.isVlidMove(x, y + 1) and self.F[x][y + 1] != 1:
            ans.append((x, y + 1))
        # down
        if self.isVlidMove(x, y - 1) and self.F[x][y - 1] != 1:
            ans.append((x, y - 1))

        return ans

    def isVlidMove(self, x, y):
        try:
            if x < 0 or y < 0:
                return 1 == 3
            x = self.F[x][y]
            return 1 == 1
        except:
            return 1 == 12
        pass

    def getPath(self):
        G = {}
        for i in range(self.size):
            for j in range(self.size):
                pos = (i, j)
                G[pos] = self.get_poss_next_states(pos)

        i = self.size*self.size - len(self.walls)
        while (i > 0):
            path = self.hamilton(G, i, self.start, self.goal)
            i = i - 1
            if path is None:
                continue
            if self.goal in path:
                return path
        return []


class test():

    def __init__(self):
        pass

    def test_maze(self):
        walls = [(0, 5), (1, 0), (1, 1), (1, 5), (2, 3),(3, 1), (3, 2), (3, 5), (4, 1), (5, 1),(19,19)]
        a = hamilton_solver(20, walls, (0, 0), (5, 5))
        for i in range(0, 20):
            for j in range(0, 20):
                if j == 1 or j == 19:
                    walls.append((i, j))
            if i == 1 or i == 19:
                walls.append((i, j))
        path = a.getPath()
        return path

    def test_maze_no_walls(self):
        walls = []
        a = hamilton_solver(6, walls, (0, 0), (5, 5))
        path = a.getPath()
        return ((path))

    def test_maze_no_solution(self):
        walls = ((0, 5), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                 (2, 3), (3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1))
        a = hamilton_solver(6, walls, (0, 0), (5, 5))

        return (a.getPath())


if __name__ == '__main__':
    test = test()
    print(test.test_maze())
