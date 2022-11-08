import pygame as pg
import sys
import random

from pygame import draw

WHITE = (255, 255, 255)
BLACK = (40, 40, 40)
GREY = (100, 100, 100)
RED = (200, 50, 50)
GREEN = (100, 200, 100)
DARK_GREEN = (20, 90, 40)
BLUE = (100, 100, 200)
BROWN = (153, 77, 0)
ROWS = 10
COLUMNS = 10
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 650
SQUARE_DIM = 50
start_node = 0
rescue_node = 95

grid = [[1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 0, 3],
        [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [2, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0]]

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Dog Rescue')
screen.fill(WHITE)


# Converts the int based coordinates into their Cartesian counterpart.
def int_to_coord(node):
    node_x = 0
    node_y = 0
    if len(str(node)) == 1:
        node_y = int(str(node)[0])
    else:
        node_x = int(str(node)[0])
        node_y = int(str(node)[1])
    return [node_x, node_y]


# Checks whether the mouse cursor is inside a particular rectangular area.
def inside_rect(mouse_pos, rect_x, rect_y, width, height):
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]
    if mouse_x > rect_x and mouse_x < rect_x + width:
        if mouse_y > rect_y and mouse_y < rect_y + height:
            return True
    return False


# Given a node, find and return a list of all non-wall neighbours.
def find_neighbours(node):
    neighbours = []
    node_x, node_y = int_to_coord(node)
    for i in range(node_x - 1, node_x + 2):
        for j in range(node_y - 1, node_y + 2):
            if i >= 0 and i < COLUMNS and j >= 0 and j < ROWS and grid[j][i] != 1:
                if not (i == node_x and j == node_y):
                    neighbours.append(int(str(i) + str(j)))
    return neighbours


# Calculates the h_value between two nodes. Simply the sum of dx and dy.
def h_dist(node1, node2):
    node1_x, node1_y = int_to_coord(node1)
    node2_x, node2_y = int_to_coord(node2)
    dx = abs(node1_x - node2_x)
    dy = abs(node1_y - node2_y)
    h = dx + dy
    return h


# Given a list of nodes, find and return the first node with the lowest f_value.
def find_lowest_f(nodes, f_vals):
    lowest_f = nodes[0]
    for node in nodes:
        if f_vals[node] < f_vals[lowest_f]:
            lowest_f = node
    return lowest_f


def draw_dog(screen, coord):
    dog = pg.Rect(40 + coord[0] * 52, 40 + coord[1] * 52, 50, 50)
    pg.draw.rect(screen, WHITE, dog)
    pg.draw.circle(screen, GREEN, dog.center, dog.width / 2)
    pg.display.flip()


def draw_rescue(screen, coord):
    dog = pg.Rect(40 + coord[0] * 52, 40 + (coord[1] - 1) * 52, 50, 50)
    pg.draw.rect(screen, WHITE, dog)
    pg.draw.circle(screen, RED, dog.center, dog.width / 2)
    pg.display.flip()


def move(from_int, to_int):
    path = []
    from_coord = int_to_coord(from_int)
    to_coord = int_to_coord(to_int)
    while True:
        path.append(from_coord.copy())
        if from_coord[0] == to_coord[0]:
            break
        if from_coord[0] < to_coord[0]:
            from_coord[0] += 1
        else:
            from_coord[0] -= 1
    while True:
        path.append(from_coord.copy())
        if from_coord[1] == to_coord[1]:
            break
        if from_coord[1] < to_coord[1]:
            from_coord[1] += 1
        else:
            from_coord[1] -= 1

    return path


def main(start_node, clicked_go=False):
    screen.fill(BLACK)
    for row in range(ROWS):
        for column in range(COLUMNS):
            if grid[row][column] == 0 or grid[row][column] == 2:
                rect = pg.Rect(40 + column * 52, 40 + row * 52, 50, 50)
                pg.draw.rect(screen, WHITE, rect)
            elif grid[row][column] == 1:
                rect = pg.Rect(40 + column * 52, 40 + row * 52, 50, 50)
                pg.draw.rect(screen, GREY, rect)
            elif grid[row][column] == 3:
                rect = pg.Rect(40 + column * 52, 40 + row * 52, 50, 50)
                pg.draw.rect(screen, GREEN, rect)

    rect = pg.Rect(460, 580, 100, 50)
    pg.draw.rect(screen, DARK_GREEN, rect)
    f = pg.font.SysFont(None, 32)
    msg_image = f.render('SOLVE', True, WHITE, DARK_GREEN)
    msg_image_rect = msg_image.get_rect()
    msg_image_rect.center = rect.center
    screen.blit(msg_image, msg_image_rect)
    pg.display.flip()

    draw_dog(screen, int_to_coord(start_node))
    draw_rescue(screen, int_to_coord(rescue_node))

    while not clicked_go:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                if inside_rect(mouse_pos, 460, 580, 100, 50):
                    clicked_go = True
                    break

    # Initialising g_values to very high by default. And starting node's g_value is set to 0.
    g_vals = [100 for i in range(100)]
    g_vals[start_node] = 0

    # Initialising h_values and setting initial f_values.
    h_vals = [h_dist(i, end_node) for i in range(100)]
    f_vals = [g_vals[i] + h_vals[i] for i in range(100)]

    # Initialising lists containg open and close nodes as well as the parent nodes.
    open_nodes = []
    closed_nodes = []
    parents = [0 for i in range(100)]

    # Adding the start node into the open node list and also setting it as the current node.
    open_nodes.append(start_node)
    curr_node = start_node

    while curr_node != end_node:
        if len(open_nodes) == 0:  # If starting or ending node is entirely surrounded by walls.
            rand_list = [i for i in range(100)]
            while True:
                new_start = random.choice(rand_list)
                new_start_coord = int_to_coord(new_start)
                if grid[new_start_coord[1]][new_start_coord[0]] == 1:
                    rand_list.remove(new_start)
                    continue
                break

            rescue_path = move(rescue_node, start_node)
            for i in rescue_path:
                screen.fill(BLACK)
                for row in range(ROWS):
                    for column in range(COLUMNS):
                        if grid[row][column] == 0 or grid[row][column] == 2:
                            rect = pg.Rect(40 + column * 52, 40 + row * 52, 50, 50)
                            pg.draw.rect(screen, WHITE, rect)
                        elif grid[row][column] == 1:
                            rect = pg.Rect(40 + column * 52, 40 + row * 52, 50, 50)
                            pg.draw.rect(screen, GREY, rect)
                        elif grid[row][column] == 3:
                            rect = pg.Rect(40 + column * 52, 40 + row * 52, 50, 50)
                            pg.draw.rect(screen, GREEN, rect)
                draw_dog(screen, int_to_coord(start_node))
                draw_rescue(screen, i)
                pg.time.delay(200)

            start_path = move(start_node, new_start)
            for i in start_path:
                screen.fill(BLACK)
                for row in range(ROWS):
                    for column in range(COLUMNS):
                        if grid[row][column] == 0 or grid[row][column] == 2:
                            rect = pg.Rect(40 + column * 52, 40 + row * 52, 50, 50)
                            pg.draw.rect(screen, WHITE, rect)
                        elif grid[row][column] == 1:
                            rect = pg.Rect(40 + column * 52, 40 + row * 52, 50, 50)
                            pg.draw.rect(screen, GREY, rect)
                        elif grid[row][column] == 3:
                            rect = pg.Rect(40 + column * 52, 40 + row * 52, 50, 50)
                            pg.draw.rect(screen, GREEN, rect)
                draw_rescue(screen, i)
                draw_dog(screen, i)
                pg.time.delay(200)

            rescue_path = move(new_start, rescue_node)
            for i in rescue_path:
                screen.fill(BLACK)
                for row in range(ROWS):
                    for column in range(COLUMNS):
                        if grid[row][column] == 0 or grid[row][column] == 2:
                            rect = pg.Rect(40 + column * 52, 40 + row * 52, 50, 50)
                            pg.draw.rect(screen, WHITE, rect)
                        elif grid[row][column] == 1:
                            rect = pg.Rect(40 + column * 52, 40 + row * 52, 50, 50)
                            pg.draw.rect(screen, GREY, rect)
                        elif grid[row][column] == 3:
                            rect = pg.Rect(40 + column * 52, 40 + row * 52, 50, 50)
                            pg.draw.rect(screen, GREEN, rect)
                draw_rescue(screen, i)
                draw_dog(screen, int_to_coord(new_start))
                pg.time.delay(200)

            main(new_start, True)

        curr_node = find_lowest_f(open_nodes, f_vals)
        open_nodes.remove(curr_node)
        closed_nodes.append(curr_node)

        neighbours = find_neighbours(curr_node)
        for neighbour in neighbours:
            if neighbour == end_node:  # We've reached our destination.
                parents[neighbour] = curr_node
                curr_node = end_node
                break

            if neighbour in closed_nodes:
                continue

            cost = g_vals[curr_node] + 1
            if neighbour in open_nodes and cost < g_vals[neighbour]:
                open_nodes.remove(neighbour)
            elif neighbour in closed_nodes and cost < g_vals[neighbour]:
                closed_nodes.remove(neighbour)

            if neighbour not in open_nodes and neighbour not in closed_nodes:
                open_nodes.append(neighbour)
                g_vals[neighbour] = cost
                f_vals[neighbour] = g_vals[neighbour] + h_vals[neighbour]
                parents[neighbour] = curr_node

    path = [curr_node]

    while True:
        path.append(parents[curr_node])
        curr_node = parents[curr_node]
        if curr_node == start_node:
            break

    path = path[::-1]
    for i in range(len(path)):
        if i > 0:
            rect = pg.Rect(40 + int_to_coord(path[i - 1])[0] * 52, 40 + int_to_coord(path[i - 1])[1] * 52, 50, 50)
            pg.draw.rect(screen, WHITE, rect)
        draw_dog(screen, int_to_coord(path[i]))
        pg.time.delay(200)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

    pg.display.flip()


if __name__ == '__main__':
    start_node = 0
    end_node = 0
    for i in range(ROWS):
        for j in range(COLUMNS):
            if grid[i][j] == 2:
                start_node = int(str(j) + str(i))
            elif grid[i][j] == 3:
                end_node = int(str(j) + str(i))
    main(start_node)
