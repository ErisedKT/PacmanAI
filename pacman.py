#! /usr/bin/python3
# pacman.py - Finds shortest past to food pellet in maze.

from queue import Queue, PriorityQueue
from classes import Cell, Maze, Pacman


def dfs(maze_obj, start, end, path):
    path = path + [start]
    if start == end:
        return path
    for node in start.accessible(maze_obj.maze):
        if node not in path:
            new_path = dfs(maze_obj, node, end, path)
            if new_path:
                return new_path


def bfs(maze_obj, start, end):
    frontier = Queue()
    frontier.put(start)
    parent = {start: None}

    while not frontier.empty():
        current = frontier.get()
        if current == end:
            return parent
        
        for next in current.accessible(maze_obj.maze):
            if next not in parent:
                parent[next] = current
                frontier.put(next)
        


def manhattan(c1, c2):
    return abs(c2.x - c1.x) + abs(c2.y - c1.y)


def greedy(maze_obj, start, end):
    frontier = PriorityQueue()
    count = 0
    frontier.put((0, count, start))
    count += 1
    parent = {start: None}
    
    while not frontier.empty():
        current = frontier.get()[2]

        if current == end:
            return parent

        for next in current.accessible(maze_obj.maze):
            if next not in parent:
                priority = manhattan(next, end)
                frontier.put((priority, count, next))
                count += 1
                parent[next] = current


def astar(maze_obj, start, end):
    frontier = PriorityQueue()
    count = 0
    frontier.put((0, count, start))
    parent = {start: None}
    cost = {start: 0}
    
    while not frontier.empty():
        current = frontier.get()[2]

        if current == end:
            return parent

        for next in current.accessible(maze_obj.maze):
            new_cost = cost[current] + 1
            if next not in cost or new_cost < cost[next]:
                cost[next] = new_cost
                priority = new_cost + manhattan(next, end)
                frontier.put((priority, count, next))
                count += 1
                parent[next] = current


def search_driver(maze_obj, search):
    start = maze_obj.pacman.get_cell(maze_obj.maze)
    end = maze_obj.food_cell()

    if search == dfs:
        path = dfs(maze_obj, start, end, [])
        return (len(path) - 1, path)
    
    parent = search(maze_obj, start, end)
    path = [end]
    node = end
    while node != start:
        path.append(parent[node])
        node = parent[node]
    return (len(path) - 1, path[::-1])


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


maze_file = 'bigMaze.txt'
maze_txt = open(maze_file).readlines()

big_maze = Maze(maze_txt)
steps, path = search_driver(big_maze, bfs)
print('Steps to food (BFS):', steps)
steps, path = search_driver(big_maze, dfs)
print('Steps to food (DFS):', steps)
steps, path = search_driver(big_maze, greedy)
print('Steps to food (Greedy):', steps)
steps, path = search_driver(big_maze, astar)
print('Steps to food (A*):', steps)
