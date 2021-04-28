# A* pathfinding algorithm using pygame for visualization

import pygame as pg
from pygame.locals import *
import math
from queue import PriorityQueue
from time import sleep
import random 

width = 800
win = pg.display.set_mode((800, 800))
pg.display.set_caption("Pathfinder")


class Node:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = -1  # 1 start 2 end 3 barrier
        self.neighbor = []

    def get_pos(self):
        return self.x, self.y


def create_node(square_x, square_y, square_size, gap):

    grid = []
    for i in range(0, square_y*(square_size+gap), square_size+gap):
        grid.append([])
        for j in range(0, square_x*(square_size+gap), square_size+gap):
            node = Node(j, i)
            grid[i//(square_size+gap)].append(node)
            color = (0, 0, 0)
            pg.draw.rect(win, color, (j, i, square_size, square_size))

    pg.display.update()

    return grid


def update_node(pos, square_size, gap, start, end, n_init):

    y, x = pos

    y = y // (square_size+gap)
    x = x // (square_size+gap)

    if n_init == True:

        # node = grid[x][y]
        # n = len(node.neighbor)

        # for i in range(n):
        #     win_x = node.neighbor[i].x
        #     win_y = node.neighbor[i].y

        #     pg.draw.rect(win, (60,120,21), (win_x, win_y, square_size, square_size))
        #     pg.display.update()

        return start, end

    elif start == None:

        grid[x][y].type = 1
        win_x = grid[x][y].x
        win_y = grid[x][y].y
        start = grid[x][y]
        color = (255, 0, 0)
        pg.draw.rect(win, color, (win_x, win_y, square_size, square_size))

    elif end == None and grid[x][y].type != 1:
        grid[x][y].type = 2
        win_x = grid[x][y].x
        win_y = grid[x][y].y
        end = grid[x][y]
        color = (0, 0, 255)
        pg.draw.rect(win, color, (win_x, win_y, square_size, square_size))

    elif grid[x][y].type != 1 and grid[x][y].type != 2:
        grid[x][y].type = 3
        win_x = grid[x][y].x
        win_y = grid[x][y].y
        color = (0, 255, 0)
        pg.draw.rect(win, color, (win_x, win_y, square_size, square_size))

    pg.display.update()

    return start, end


def update_neighbors(grid, square_x, square_y, square_size, gap):

    for i in range(square_y):
        for j in range(square_x):

            grid[i][j].neighbor = []

            if i < (square_y - 1) and grid[i+1][j].type != 3:
                grid[i][j].neighbor.append(grid[i+1][j])

            if i > 0 and grid[i-1][j].type != 3:
                grid[i][j].neighbor.append(grid[i-1][j])

            if j > 0 and grid[i][j-1].type != 3:
                grid[i][j].neighbor.append(grid[i][j-1])

            if j < (square_x - 1) and grid[i][j+1].type != 3:
                grid[i][j].neighbor.append(grid[i][j+1])

            
            if j < (square_x - 1) and i > 0 and grid[i-1][j+1].type != 3:
                grid[i][j].neighbor.append(grid[i-1][j+1])

            if j < (square_x - 1) and i < (square_y - 1) and grid[i+1][j+1].type != 3:
                grid[i][j].neighbor.append(grid[i+1][j+1])
            
            if j > 0 and i > 0 and grid[i-1][j-1].type != 3:
                grid[i][j].neighbor.append(grid[i-1][j-1])
            
            if j > 0 and i < (square_y - 1) and grid[i+1][j-1].type != 3:
                grid[i][j].neighbor.append(grid[i+1][j-1])
            

            
            
            

    print("neighbors added")

    return grid


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return abs(x1-x2) + abs(y1-y2)

def h2(p1,p2): 
    x1, y1 = p1
    x2, y2 = p2

    return math.sqrt(abs(x1-x2) + abs(y1-y2))
    


def a_star(start, end, grid, square_size):

    tie_break = 0

    possible_path = PriorityQueue()
    possible_path.put((0, tie_break, start))
    shortest_path = {}

    # init g score for each spot in grid
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    # init f score for each spot in grid
    #fscore = gscore + hscore
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = 0 + h(start.get_pos(), end.get_pos())

    possible_path_tracker = {start}

    while not possible_path.empty():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        # checking for node with lowest f score, removes from queue
        current_node = possible_path.get()[2]
        possible_path_tracker.remove(current_node)

        if current_node != start and current_node != end:
            win_x = current_node.x
            win_y = current_node.y

            pg.draw.rect(win, (128, 0, 128), (win_x, win_y, square_size, square_size))
            pg.display.update()

            # slowed down for visual effect
            sleep(0.03)

        if current_node == end:
            draw_path(shortest_path, end, start, square_size)
            print("arrived at destination")
            break

        for neighbor in current_node.neighbor:

            new_g_score = g_score[current_node] + 1

            if new_g_score < g_score[neighbor]:

                shortest_path[neighbor] = current_node
                g_score[neighbor] = new_g_score
                f_score[neighbor] = new_g_score + \
                    h(neighbor.get_pos(), end.get_pos())

                if neighbor not in possible_path_tracker:
                    tie_break += 1
                    possible_path.put((f_score[neighbor], tie_break, neighbor))
                    possible_path_tracker.add(neighbor)


def draw_path(shortest_path, current, start, square_size):

    while current in shortest_path:
        current = shortest_path[current]

        if current != start:
            win_x = current.x
            win_y = current.y

            pg.draw.rect(win, (255, 192, 203), (win_x, win_y, square_size, square_size))
            pg.display.update()
            sleep(0.03)


if __name__ == '__main__':

    square_x = 70 #total squares in x direction
    square_y = 50 #total square in y direction
    square_size = 10  # pixel size
    gap = square_size//2  # gap between pixels
    w = square_x*(square_size+gap)-gap 
    l = square_y*(square_size+gap)-gap

    win = pg.display.set_mode((w, l)) # screen size
    pg.display.set_caption("Pathfinder")
    run = True
    win.fill((100, 100, 100))

    grid = create_node(square_x, square_y, square_size, gap)
    start = None
    end = None
    n_init = False

    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    run = False
                if event.key == pg.K_c:
                    start = None
                    end = None
                    n_init = False
                    grid = create_node(square_x, square_y, square_size, gap)

                if event.key == pg.K_SPACE and start and end:
                    n_init = True
                    update_neighbors(grid, square_x, square_y, square_size, gap)
                    a_star(start, end, grid, square_size)

            if pg.mouse.get_pressed()[0]:  # LEFT mouse click
                pos = pg.mouse.get_pos()
                start, end = update_node(pos, square_size, gap, start, end, n_init)

    pg.quit()
