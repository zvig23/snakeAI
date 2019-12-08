import heapq


class Cell(object):
    def __init__(self, x, y, reachable):
        """Initialize new cell.

        @param reachable is cell reachable? not a wall?
        @param x cell x coordinate
        @param y cell y coordinate
        @param g cost to move from the starting cell to this cell.
        @param h estimation of the cost to move from this cell
                 to the ending cell.
        @param f f = g + h
        """
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0


class AStar(object):
    def __init__(self):
        # open list
        self.opened = []
        heapq.heapify(self.opened)
        # visited cells list
        self.closed = set()
        # grid cells
        self.cells = []
        self.grid_height = None
        self.grid_width = None

    def init_grid(self, width, height, walls, start, end):
        """Prepare grid cells, walls.

        @param width grid's width.
        @param height grid's height.
        @param walls list of wall x,y tuples.
        @param start grid starting point x,y tuple.
        @param end grid ending point x,y tuple.
        """
        self.grid_height = height
        self.grid_width = width
        walls.append([(0, 1), (0, 19), (1, 1), (1, 19), (1, 19), (2, 1), (2, 19), (3, 1), (3, 19), (4, 1), (4, 19), (5, 1), (5, 19), (6, 1), (6, 19), (7, 1), (7, 19), (8, 1), (8, 19), (9, 1), (9, 19), (10, 1), (10, 19), (11, 1), (11, 19), (12, 1), (12, 19), (13, 1), (13, 19), (14, 1), (14, 19), (15, 1), (15, 19), (16, 1), (16, 19), (17, 1), (17, 19), (18, 1), (18, 19), (19, 1), (19, 19), (19, 19)])
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in walls:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))
        self.start = self.get_cell(*start)
        self.end = self.get_cell(*end)

    def get_heuristic(self, cell):
        """Compute the heuristic value H for a cell.

        Distance between this cell and the ending cell multiply by 10.

        @returns heuristic value H
        """
        return 10 * (1/(abs(cell.x - self.end.x)+1) + 1/(abs(cell.y - self.end.y)+1))

    def get_cell(self, x, y):
        """Returns a cell from the cells list.

        @param x cell x coordinate
        @param y cell y coordinate
        @returns cell
        """
        return self.cells[x * self.grid_height + y]

    def get_adjacent_cells(self, cell):
        """Returns adjacent cells to a cell.

        Clockwise starting from the one on the right.

        @param cell get adjacent cells for this cell
        @returns adjacent cells list.
        """
        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells

    def get_path(self):
        cell = self.end
        path = [(cell.x, cell.y)]
        while cell.parent is not self.start:
            cell = cell.parent
            path.append((cell.x, cell.y))

        path.append((self.start.x, self.start.y))
        path.reverse()
        return path

    def update_cell(self, adj, cell):
        """Update adjacent cell.

        @param adj adjacent cell to current cell
        @param cell current cell being processed
        """
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def solve(self):
        """Solve maze, find path to ending cell.

        @returns path or None if not found.
        """
        # add starting cell to open heap queue
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # pop cell from heap queue
            f, cell = heapq.heappop(self.opened)
            # add cell to closed list so we don't process it twice
            self.closed.add(cell)
            # if ending cell, return found path
            if cell is self.end:
                return self.get_path()
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found
                        # for this adj cell.
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))


class Test():

    def __init__(self):
        pass

    def test_maze(self):
        a = AStar()
        walls =[]# [(0, 5), (1, 0), (1, 1), (1, 5), (2, 3),
                # (3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1)]
        for i in range(0,20):
            for j in range(0,20):
                if j==1 or j==19:
                    walls.append((i,j))
            if i == 1 or i == 19:
                walls.append((i, j))
        a.init_grid(20, 20, walls, (1, 1), (5, 5))
        path = a.solve()
        return path

    def test_maze_no_walls(self):
        a = AStar()
        walls = ()
        a.init_grid(6, 6, walls, (0, 0), (5, 5))
        path = a.solve()
        return (len(path)== 11)

    def test_maze_no_solution(self):
        a = AStar()
        walls = ((0, 5), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                 (2, 3), (3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1))
        a.init_grid(6, 6, walls, (0, 0), (5, 5))
        return (a.solve())

if __name__ == '__main__':
    test = Test()
    print (test.test_maze())
