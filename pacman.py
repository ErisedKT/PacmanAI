#! /usr/bin/python3
# pacman.py - Finds shortest past to food pellet in maze.

maze_file = 'bigMaze.txt'
maze_txt = open(maze_file).readlines()
h = 0

class Cell(object):
    def __init__(self, x, y, h):
        self._x = x
        self._y = y
        self.h = h
        h += 1
        
        if (maze_txt[y][x] == '%'):
            self._free = False
        else:
            self._free = True
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y

    @property
    def free(self):
        return self._free

    def accessible(self, maze):
        acc = []
        if (maze[self.y][self.x+1].free):
            acc.append(maze[self.y][self.x+1])
        if (maze[self.y][self.x-1].free):
            acc.append(maze[self.y][self.x-1])
        if (maze[self.y+1][self.x].free):
            acc.append(maze[self.y+1][self.x])
        if (maze[self.y-1][self.x].free):
            acc.append(maze[self.y-1][self.x])
        return acc

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return self.h

    def __repr__(self):
        return '<' + str(self._x) + ', ' + str(self._y) + '>'

class Maze(object):
    def __init__(self, maze_in):
        """Create maze"""
        self.rows = len(maze_in)
        self.cols = len(maze_in[0])
        self._maze = []
        
        # Create maze array with Cell objects.
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                row.append(Cell(c, r, h))
                if (maze_txt[r][c] == 'P'):
                    self._pacman = Pacman(c, r)
                elif (maze_txt[r][c] == '.'):
                    self.food_coords = (c, r)
            self.maze.append(row)

    @property
    def maze(self):
        return self._maze

    @property
    def pacman(self):
        return self._pacman

    def food_cell(self):
        return self._maze[self.food_coords[1]][self.food_coords[0]]
            

class Pacman(object):
    def __init__(self, x, y):
        """Create a pacman"""
        self.x = x
        self.y = y

    def move_r(self, maze):
        if (maze[self.y][self.x + 1].is_free()):
            self.x += 1

    def move_l(self, maze):
        if (maze[self.y][self.x - 1].is_free()):
            self.x -= 1

    def move_u(self, maze):
        if (maze[self.y - 1][self.x].is_free()):
            self.y -= 1

    def move_d(self, maze):
        if (maze[self.y + 1][self.x].is_free()):
            self.y += 1

    def get_cell(self, maze):
        return maze[self.y][self.x]

def bfs_driver(maze_obj):
    src = maze_obj.pacman.get_cell(maze_obj.maze)
    dest = maze_obj.food_cell()
    level = {src: 0}
    parent = {src: None}
    current = [src]
    i = 1
    while current:
        next = []
        for u in current:
            for v in u.accessible(maze_obj.maze):
                if v not in level:
                    next.append(v)
                    level[v] = i
                    parent[v] = u
                if v == dest:
                    path = [v]
                    node = v
                    while node != src:
                        path.append(parent[node])
                        node = parent[node]
                    return (level[v], path[::-1])
        current = next
        i += 1
        

def dfs(maze_obj, start, end, path):
    path = path + [start]
    if start == end:
        return path
    for node in start.accessible(maze_obj.maze):
        if node not in path:
            newPath = dfs(maze_obj, node, end, path)
            if newPath:
                return newPath

def dfs_driver(maze_obj):
    start = maze_obj.pacman.get_cell(maze_obj.maze)
    end = maze_obj.food_cell()
    shortest = dfs(maze_obj, start, end, [])
    return (len(shortest) - 1, shortest)


def display_path(maze_obj, path):
    res = []
    for r in range(len(maze_txt)):
        row = []
        for c in range(len(maze_txt[0])):
            if (maze_obj.maze[r][c] in path):
                row.append('.')
            else:
                row.append(maze_txt[r][c])
        res.append(''.join(row))
    maze_out = open('out.txt', 'w')
    for r in res:
        print(r, end='')
        maze_out.write(r)


def manhattan(c1, c2):
    return abs(c2.x - c1.x) + abs(c2.y - c1.y)


def greedy(maze_obj, start, end, path):
    path = path + [start]
    if start == end:
        return path
    children = sorted(start.accessible(maze_obj.maze),\
        key=(lambda c: manhattan(c, end)))
    for node in children:
        if node not in path:
            newPath = greedy(maze_obj, node, end, path)
            if newPath:
                return newPath
            

def greedy_driver(maze_obj):
    start = maze_obj.pacman.get_cell(maze_obj.maze)
    end = maze_obj.food_cell()
    shortest = greedy(maze_obj, start, end, [])
    return (len(shortest) - 1, shortest)

big_maze = Maze(maze_txt)
steps, shortest = bfs_driver(big_maze)
print('Steps to food (BFS):', steps)
steps, shortest = dfs_driver(big_maze)
print('Steps to food (DFS):', steps)
steps, shortest = greedy_driver(big_maze)
print('Steps to food (Greedy):', steps)