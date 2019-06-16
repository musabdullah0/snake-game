"""
    Simple snake game made with pygame
    by: Musab Abdullah in 2019
"""

import pygame
import sys
import random

# global constants
num_boxes = 20
margin = 2
box_size = 30
stats_size = 100
display_size = num_boxes * box_size + (num_boxes - 1) * margin
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
fruit_color = (255, 0, 0)

# initializing game
pygame.init()  # initializes all imported pygame modules
gameDisplay = pygame.display.set_mode((display_size, display_size + stats_size))
pygame.display.set_caption('snake game')
clock = pygame.time.Clock()

# while this is false, game keeps going on
crashed = False

# grid is one layer bigger than screen(0s around to symbolize wall)
grid = [[0 for i in range(num_boxes + 2)] for j in range(num_boxes + 2)]

# list of tuples with coordinates of snake body
snake_body = [(1, 1), (1, 2), (1, 3)]  # in rows, cols
fruit_location = (5, 5)
direction = 2  # moving right initially


def init_snake():
    """draws the snake at top-left moving right with length 3"""
    for i in range(1,4):
        grid[1][i] = 1


def update_grid(draw, erase=None, thing=1):
    """draw is coordinates of where to put a square
    erase is only there if snake is moving
    thing = 1 when snake moving and thing = 2 if placing fruit"""
    pygame.draw.rect(gameDisplay, black, (0, 0, display_size, display_size))
    # (condition_if_false, condition_if_true)[test]
    grid[draw[0]][draw[1]] = (2, 1)[thing == 1]
    if thing == 1:
        snake_body.append((draw[0], draw[1]))  # in r/c
    if erase:
        grid[erase[0]][erase[1]] = 0  # in r/c
        snake_body.pop(0)
    # color the screen based on grid
    for r in range(1,len(grid) - 1):
        for c in range(1, len(grid) - 1):
            if grid[r][c] != 0:
                drawing_color = (fruit_color, white)[grid[r][c] == 1]
                color(r, c, drawing_color)


def update_stats():
    pygame.draw.rect(gameDisplay, (211,211,211), (0, display_size, display_size, stats_size))
    my_font = pygame.font.SysFont("monospace", 45)
    label = "Score: " + str(len(snake_body) - 3)
    score = my_font.render(label, 1, (255, 0, 0))
    gameDisplay.blit(score, (display_size//2 - 50, display_size + stats_size//2))


def color(r, c, box_color):
    """colors a box on the grid white at row r and column c"""
    pygame.draw.rect(gameDisplay, box_color, (c * (box_size+margin) - box_size - 2 * margin,
                                              r * (box_size+margin) - box_size - 2 * margin,
                                              box_size, box_size), 0)


def move():
    """1 is up, 2 is right, 3 is down, 4 is left
    kinda trippy that x is the column and y is the row"""
    global direction
    head_r = snake_body[-1][0]
    head_c = snake_body[-1][1]
    tail_r = snake_body[0][0]
    tail_c = snake_body[0][1]
    if direction == 1:
        gonna_crash(head_r - 1, head_c)
        update_grid(draw=(head_r - 1, head_c), erase=(tail_r, tail_c))

    elif direction == 2:
        gonna_crash(head_r, head_c + 1)  # in r,c
        update_grid(draw=(head_r, head_c + 1), erase=(tail_r, tail_c))  # in x/y

    elif direction == 3:
        gonna_crash(head_r + 1, head_c)
        update_grid(draw=(head_r + 1, head_c), erase=(tail_r, tail_c))

    elif direction == 4:
        gonna_crash(head_r, head_c - 1)
        update_grid(draw=(head_r, head_c - 1), erase=(tail_r, tail_c))
    else:
        print("wyd, that's not a direction")


def gonna_crash(r, c):
    """checks if the snake is gonna crash into the wall or itself"""
    global fruit_location
    if r == 0 or r == len(grid) or c == 0 or c == len(grid) or grid[r][c] == 1:
        crash_message()
    elif grid[r][c] == 2:
        grid[r][c] = 0
        # print("got a fruit at", r, c)
        snake_body.append((r, c))
        fruit_location = fruit()


def fruit():
    """randomly places a fruit somewhere on the grid"""
    r = random.randrange(1, num_boxes + 1)
    c = random.randrange(1, num_boxes + 1)
    while (r, c) in snake_body:
        r = random.randrange(1, num_boxes + 1)
        c = random.randrange(1, num_boxes + 1)
    grid[r][c] = 2
    print('put fruit at ' + str(r) + ', ' + str(c))
    return r, c


def crash_message():
    """changes global crashed variable to True and exits game"""
    global crashed
    crashed = True
    print("you crashed! game over")
    pygame.quit()
    sys.exit()


def print_array(arr):
    """for testing use only"""
    f = 0
    print("printing grid")
    for row in arr:
        f += row.count(2)
        print(row, "\n")
    print(f, "fruit")


def make_text(font_size, label, text_color, background_color, x_offset=0, y_offset=0):
    text = pygame.font.SysFont('silomttf', font_size)
    text_surf = text.render(label, 1, text_color, background_color)
    x = (display_size-text_surf.get_width())//2 + x_offset
    y = (display_size-text_surf.get_height())//2 + y_offset
    return gameDisplay.blit(text_surf, (x, y))


def main():
    """main loop of game"""
    global crashed, direction
    while not crashed:
        # any checks if anything in the iterable is True and then returns True
        if any(event.type == pygame.QUIT for event in pygame.event.get()):
            crashed = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and (direction == 2 or direction == 4):
            direction = 1
        elif keys[pygame.K_RIGHT] and (direction == 1 or direction == 3):
            direction = 2
        elif keys[pygame.K_DOWN] and (direction == 2 or direction == 4):
            direction = 3
        elif keys[pygame.K_LEFT] and (direction == 1 or direction == 3):
            direction = 4
        move()
        update_stats()
        pygame.display.update()
        clock.tick(8)


def intro():
    """intro sequence of game"""
    intro_on = True
    while intro_on:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        make_text(100, 'snake.ai', red, None)
        b = make_text(50, 'start', red, green, x_offset=0, y_offset=150)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            if b.collidepoint(pos):
                break
        pygame.display.update()


intro()
fruit()
init_snake()
main()
pygame.quit()
sys.exit()
