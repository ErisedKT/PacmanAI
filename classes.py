class Cell(object):
    h = 0
    def __init__(self, x, y, maze_txt):
        self._x = x
        self._y = y
        Cell.h += 1
        
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
        return Cell.h

    def __repr__(self):
        return '<' + str(self._x) + ', ' + str(self._y) + '>'

class Maze(object):
    def __init__(self, maze_txt):
        """Create maze"""
        self.rows = len(maze_txt)
        self.cols = len(maze_txt[0])
        self._maze = []
        
        # Create maze array with Cell objects.
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                row.append(Cell(c, r, maze_txt))
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
