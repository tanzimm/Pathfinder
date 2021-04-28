# A* pathfinding algorithm using pygame for visualization

import pygame as pg
from pygame.locals import *
import math
from queue import PriorityQueue
from time import sleep

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


def create_node(pixel_x, pixel_y, ps, gap):

    grid = []
    for i in range(0, pixel_x*(ps+gap), ps+gap):
        grid.append([])
        for j in range(0, pixel_y*(ps+gap), ps+gap):
            node = Node(j, i)
            grid[i//(ps+gap)].append(node)
            color = (0, 0, 0)
            pg.draw.rect(win, color, (i, j, ps, ps))

    pg.display.update()

    return grid


def update_node(pos, ps, gap, start, end, n_init):

    y, x = pos

    y = y // (ps+gap)
    x = x // (ps+gap)

    if n_init == True:

        # node = grid[x][y]
        # n = len(node.neighbor)

        # for i in range(n):
        #     win_x = node.neighbor[i].x
        #     win_y = node.neighbor[i].y

        #     pg.draw.rect(win, (60,120,21), (win_x, win_y, ps, ps))
        #     pg.display.update()

        return start, end

    elif start == None:

        grid[x][y].type = 1
        win_x = grid[x][y].x
        win_y = grid[x][y].y
        start = grid[x][y]
        color = (255, 0, 0)
        pg.draw.rect(win, color, (win_x, win_y, ps, ps))

    elif end == None and grid[x][y].type != 1:
        grid[x][y].type = 2
        win_x = grid[x][y].x
        win_y = grid[x][y].y
        end = grid[x][y]
        color = (0, 0, 255)
        pg.draw.rect(win, color, (win_x, win_y, ps, ps))

    elif grid[x][y].type != 1 and grid[x][y].type != 2:
        grid[x][y].type = 3
        win_x = grid[x][y].x
        win_y = grid[x][y].y
        color = (0, 255, 0)
        pg.draw.rect(win, color, (win_x, win_y, ps, ps))

    pg.display.update()

    return start, end


def update_neighbors(grid, pixel_x, pixel_y, ps, gap):

    for i in range(pixel_x):
        for j in range(pixel_y):

            grid[i][j].neighbor = []

            if i < (pixel_x - 1) and grid[i+1][j].type != 3:
                grid[i][j].neighbor.append(grid[i+1][j])

            if i > 0 and grid[i-1][j].type != 3:
                grid[i][j].neighbor.append(grid[i-1][j])

            if j > 0 and grid[i][j-1].type != 3:
                grid[i][j].neighbor.append(grid[i][j-1])

            if j < (pixel_y - 1) and grid[i][j+1].type != 3:
                grid[i][j].neighbor.append(grid[i][j+1])

    print("neighbors added")

    return grid


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2

    return abs(x1-x2) + abs(y1-y2)


def a_star(start, end, grid, ps):

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

            pg.draw.rect(win, (128, 0, 128), (win_x, win_y, ps, ps))
            pg.display.update()

            # slowed down for visual effect
            sleep(0.03)

        if current_node == end:
            draw_path(shortest_path, end, start, ps)
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


def draw_path(shortest_path, current, start, ps):

    while current in shortest_path:
        current = shortest_path[current]

        if current != start:
            win_x = current.x
            win_y = current.y

            pg.draw.rect(win, (255, 192, 203), (win_x, win_y, ps, ps))
            pg.display.update()
            sleep(0.03)


if __name__ == '__main__':

    pixel_x = 50
    pixel_y = 50
    ps = 10  # pixel size
    gap = ps//2  # gap between pixels
    w = pixel_x*(ps+gap)-gap
    l = pixel_y*(ps+gap)-gap

    win = pg.display.set_mode((w, l))
    pg.display.set_caption("Pathfinder")
    run = True
    win.fill((100, 100, 100))

    grid = create_node(pixel_x, pixel_y, ps, gap)
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
                    grid = create_node(pixel_x, pixel_y, ps, gap)

                if event.key == pg.K_SPACE and start and end:
                    n_init = True
                    update_neighbors(grid, pixel_x, pixel_y, ps, gap)
                    a_star(start, end, grid, ps)

            if pg.mouse.get_pressed()[0]:  # LEFT mouse click
                pos = pg.mouse.get_pos()
                start, end = update_node(pos, ps, gap, start, end, n_init)

    pg.quit()
