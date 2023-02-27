import numpy as np


def is_valid_move(x, y):
    if x < 1 or y < 1:
        return False
    if x > 19 or y > 19:
        return False
    return True


class QLearning:
    def __init__(self, size, walls, headLoc, rewardLoc):
        np.random.seed(1)
        self.F = np.zeros(shape=[size, size], dtype=np.float)
        self.R = np.zeros(shape=[size, size], dtype=np.float)
        self.Q = np.zeros(shape=[size, size], dtype=np.float)
        self.start = headLoc
        self.goal = rewardLoc
        self.gamma = 0.95
        self.lrn_rate = 0.35
        self.max_epochs = 150
        self.walls = walls
        self.expanded = 0
        self.generated = 0

    def init_board(self):
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
            while x < 18 * 18:
                next_s = self.get_rnd_next_state(curr_s)
                poss_next_next_states = self.get_poss_next_states(next_s)

                max_q = -9999.99
                for j in range(len(poss_next_next_states)):
                    next_next_stage = poss_next_next_states[j]
                    q = self.Q[next_next_stage[0]][next_next_stage[1]]
                    if q > max_q:
                        max_q = q
                # Q = [(1-a) * Q]  +  [a * (rt + (g * maxQ))]
                self.Q[curr_s[0]][curr_s[1]] = ((1 - self.lrn_rate) * self.Q[curr_s[0]][curr_s[1]]) + (
                        self.lrn_rate * (self.R[next_s[0]][next_s[1]] + (self.gamma * max_q)))

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
        if is_valid_move(x + 1, y) and self.F[x + 1][y] != -1:
            ans.append((x + 1, y))
        # left
        if is_valid_move(x - 1, y) and self.F[x - 1][y] != -1:
            ans.append((x - 1, y))
        # up
        if is_valid_move(x, y + 1) and self.F[x][y + 1] != -1:
            ans.append((x, y + 1))
        # down
        if is_valid_move(x, y - 1) and self.F[x][y - 1] != - 1:
            ans.append((x, y - 1))

        return ans

    def get_next_move(self, state, path):
        x = state[0]
        y = state[1]
        ans = state
        max_utility = -1

        # right
        if is_valid_move(x + 1, y) and (x + 1, y) not in self.walls and self.Q[x + 1][y] > max_utility and (
        x + 1, y) not in path:
            self.expanded += 1
            ans = (x + 1, y)
            max_utility = self.Q[x + 1][y]
        # left
        if is_valid_move(x - 1, y) and (x - 1, y) not in self.walls and self.Q[x - 1][y] > max_utility and (
        x - 1, y) not in path:
            self.expanded += 1
            ans = (x - 1, y)
            max_utility = self.Q[x - 1][y]
        # up
        if is_valid_move(x, y + 1) and (x, y + 1) not in self.walls and self.Q[x][y + 1] > max_utility and (
        x, y + 1) not in path:
            self.expanded += 1
            ans = (x, y + 1)
            max_utility = self.Q[x][y + 1]
        # down
        if is_valid_move(x, y - 1) and (x, y - 1) not in self.walls and self.Q[x][y - 1] > max_utility and (
        x, y - 1) not in path:
            self.expanded += 1
            ans = (x, y - 1)

        self.generated += 1

        if ans == state:
            if (x + 1, y) not in self.walls and (x + 1, y) not in path:
                ans = (x + 1, y)
            elif (x - 1, y) not in self.walls and (x - 1, y) not in path:
                ans = (x - 1, y)
            elif (x, y + 1) not in self.walls and (x, y + 1) not in path:
                ans = (x + 1, y + 1)
            elif (x, y - 1) not in self.walls and (x, y - 1) not in path:
                ans = (x, y - 1)
        return ans

    def get_path(self):
        path = []
        curr_state = self.start
        self.init_board()
        while curr_state != self.goal and curr_state:
            next_state = self.get_next_move(curr_state, path)
            if next_state not in path:
                path.append(next_state)
                curr_state = next_state
            else:
                break

        return path

    def walk(self):
        path = []
        curr = self.start
        while curr != self.goal:
            next = np.argmax(self.Q[curr])
            path.append(next)
            curr = next
        return path


if __name__ == '__main__':
    walls = ()
    a = QLearning(6, walls, (0, 0), (5, 5))
    path = a.get_path()
    print(path)
