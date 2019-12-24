import numpy as np


class qLearning():
    def __init__(self, size, walls, headLoc, rewardLoc):
        np.random.seed(1)
        self.F = np.zeros(shape=[size, size], dtype=np.float)
        self.R = np.zeros(shape=[size, size], dtype=np.float)
        self.Q = np.zeros(shape=[size, size], dtype=np.float)
        self.start = headLoc
        self.goal = rewardLoc
        self.gamma = 0.95
        self.lrn_rate = 0.5
        self.max_epochs = 1
        self.walls = walls
        self.initilizeBoard()

    def initilizeBoard(self):
        # walls
        for wall in self.walls:
            self.F[wall[0], wall[1]] = -1
            self.R[wall[0], wall[1]] = -1
            self.Q[wall[0], wall[1]] = -1

        # apple
        self.F[self.goal[0], self.goal[1]] = 10
        self.R[self.goal[0], self.goal[1]] = 10
        self.Q[self.goal[0], self.goal[1]] = 10

        self.train()

    def train(self):
        # compute the Q matrix
        for i in range(0, self.max_epochs):
            curr_s = (
            np.random.randint(1, len(self.R) - 2), np.random.randint(1, len(self.R) - 2))  # random start state
            x = 0
            while (x < 18 * 18):
                next_s = self.get_rnd_next_state(curr_s)
                poss_next_next_states = self.get_poss_next_states(next_s)

                max_Q = -9999.99
                for j in range(len(poss_next_next_states)):
                    next_next_stage = poss_next_next_states[j]
                    q = self.Q[next_next_stage[0]][next_next_stage[1]]
                    if q > max_Q:
                        max_Q = q
                # Q = [(1-a) * Q]  +  [a * (rt + (g * maxQ))]
                self.Q[curr_s[0]][curr_s[1]] = ((1 - self.lrn_rate) * self.Q[curr_s[0]][curr_s[1]]) + (
                            self.lrn_rate * (self.R[next_s[0]][next_s[1]] + (self.gamma * max_Q)))

                next_s = self.get_rnd_next_state(curr_s)

                curr_s = next_s
                x += 1
                if curr_s[0] == self.goal[0] and curr_s[1] == self.goal[1]:
                    break

    def get_rnd_next_state(self, state):
        poss_next_states = self.get_poss_next_states(state)
        if len(poss_next_states) == 0:
            return state
        return poss_next_states[np.random.randint(0, len(poss_next_states))]

    def get_poss_next_states(self, state):
        x = state[0]
        y = state[1]
        ans = []
        # right
        if self.isVlidMove(x + 1, y) and self.F[x + 1][y] != -1:
            ans.append((x + 1, y))
        # left
        if self.isVlidMove(x - 1, y) and self.F[x - 1][y] != -1:
            ans.append((x - 1, y))
        # up
        if self.isVlidMove(x, y + 1) and self.F[x][y + 1] != -1:
            ans.append((x, y + 1))
        # down
        if self.isVlidMove(x, y - 1) and self.F[x][y - 1] != - 1:
            ans.append((x, y - 1))

        return ans

    def getNextMove(self, state):
        x = state[0]
        y = state[1]
        ans = state
        maxUtility = -9999
        # right
        if self.isVlidMove(x + 1, y) and self.F[x + 1][y] != -1 and self.Q[x + 1][y] > maxUtility:
            ans = (x + 1, y)
            maxUtility = self.Q[x + 1][y]
        # left
        if self.isVlidMove(x - 1, y) and self.F[x - 1][y] != -1 and self.Q[x - 1][y] > maxUtility:
            ans = (x - 1, y)
            maxUtility = self.F[x - 1][y]
        # up
        if self.isVlidMove(x, y + 1) and self.F[x][y + 1] != -1 and self.Q[x][y + 1] > maxUtility:
            ans = (x, y + 1)
            maxUtility = self.Q[x][y + 1]
        # down
        if self.isVlidMove(x, y - 1) and self.F[x][y - 1] != -1 and self.Q[x][y - 1] > maxUtility:
            ans = (x, y - 1)
            maxUtility = self.Q[x][y - 1]

        return ans

    def getPath(self):
        path = []
        curr_state = self.start
        path.append(curr_state)
        while curr_state != self.goal and curr_state:
            next_state = self.getNextMove(curr_state)
            path.append(next_state)
            curr_state = next_state
        # the apple
        return path

    def isVlidMove(self, x, y):
        try:
            if x < 0 or y < 0:
                return 1 == 3
            x = self.F[x][y]
            return 1 == 1
        except:
            return 1 == 12
        pass


# class Test():
#
#     def __init__(self):
#         pass
#
#     def test_maze(self):
#         walls =[(0, 5), (1, 0), (1, 5), (2, 3),(3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1)]
#         for i in range(0,20):
#             for j in range(0,20):
#                 if j==0 or j==19:
#                     walls.append((i,j))
#             if i == 0 or i == 19:
#                 walls.append((i, j))
#         a = qLearning(20, walls, (1, 1), (17, 5))
#
#         path = a.getPath()
#         maze = np.zeros(shape=[20, 20], dtype=np.int)
#         i=1
#         for step in path:
#             maze[step[0]][step[1]]=i
#             i+=1
#         for wall in walls:
#             maze[wall[0]][wall[1]]=30
#         print(maze)
#         return path
#
#     def test_maze_no_walls(self):
#         walls = ()
#         a=qLearning(6, walls, (0, 0), (5, 5))
#         path = a.getPath()
#         return path
#
#     def test_maze_no_solution(self):
#         walls = ((0, 5), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
#                  (2, 3), (3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1))
#         a=qLearning(6, walls, (0, 0), (5, 5))
#         return (a.solve())

if __name__ == '__main__':
    walls = ()
    a = qLearning(6, walls, (0, 0), (5, 5))
    path = a.getPath()
    print(path)
