import pygame
import json
import numpy
import time

# game constants
FPS = 30
WIDTH = 600
HEIGHT = 400

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (38, 50, 56)
GREEN_CYAN = (0, 230, 118)
GREEN = (76, 175, 80)
PURPLE = (103, 58, 183)
RED = (211, 47, 47)
BLUE = (0, 145, 234)
YELLOW = (255, 234, 0)

# global variables
current_level = 0
running = True
game_array = numpy.empty((6, 6), dtype="U10")
available_colors = ["RED", "BLUE", "GREEN", "PURPLE", "YELLOW"]
connected_colors = []
visited_cells = {}


# parse color read from json to RGB tuple
def parse_color_from_json(color):
    if color == "RED":
        return RED
    elif color == "GREEN":
        return GREEN
    elif color == "BLUE":
        return BLUE
    elif color == "YELLOW":
        return YELLOW
    elif color == "PURPLE":
        return PURPLE


# load levels data from json file
def load_level(loaded_level):
    text_font_big = pygame.font.SysFont("comicsansms", 28)

    generate_surfaces()
    generate_buttons()

    with open('assets/levels.json') as levels_file:
        levels_file = json.load(levels_file)
        level_one = levels_file["levels"][loaded_level]

        for dot in level_one["dots"]:
            pygame.draw.circle(grid_surface, parse_color_from_json(dot["color"]), (dot["x"], dot["y"]), 25)
            game_array[dot["index_y"]][dot["index_x"]] = dot["color"]

        text_level_indicator = text_font_big.render("LEVEL {id}".format(id=level_one["id"]), False, GREEN_CYAN)
        main_surface.blit(text_level_indicator, (430, 0))


# displays new level
def generate_new_level():
    global current_level

    if current_level < 2:
        current_level += 1
    else:
        current_level = 0

    load_level(current_level)


# find possible options:
def find_possible_options(position, color):
    options = []

    if 0 < position[0] < len(game_array) - 1:
        if not [position[0] + 1, position[1]] in visited_cells:
            options.append((position[0] + 1, position[1]))
        if not game_array[position[0] - 1, position[1]] in visited_cells:
            options.append((position[0] - 1, position[1]))

    elif position[0] == 0:
        if game_array[position[0] + 1, position[1]] == "" in visited_cells:
            options.append((position[0] + 1, position[1]))

    elif position[0] == len(game_array) - 1:
        if game_array[position[0] - 1, position[1]] == "" in visited_cells:
            options.append((position[0] - 1, position[1]))

    if 0 < position[1] < len(game_array) - 1:
        if game_array[position[0], position[1] + 1] == "" or game_array[position[0], position[1] + 1] == color:
            options.append((position[0], position[1] + 1))
        if game_array[position[0], position[1] - 1] == "" or game_array[position[0], position[1] - 1] == color:
            options.append((position[0], position[1] - 1))

    elif position[1] == 0:
        if game_array[position[0], position[1] + 1] == "" or game_array[position[0], position[1] + 1] == color:
            options.append((position[0], position[1] + 1))

    elif position[1] == len(game_array) - 1:
        if game_array[position[0], position[1] - 1] == "" or game_array[position[0], position[1] - 1] == color:
            options.append((position[0], position[1] - 1))

    print("POSSIBLE MOVES: {options}".format(options=options))

    return options


# backtrack implementation
def solve():
    solved = False
    actual_color = available_colors[0]
    current_position = numpy.argwhere(game_array == actual_color)[0]
    final_position = numpy.argwhere(game_array == actual_color)[1]

    while not solved:
        options = find_possible_options(current_position, actual_color)

        if current_position[0] == final_position[0] and current_position[1] == final_position[1]:
            available_colors.remove(actual_color)
            connected_colors.append(actual_color)
            solved = True
        for option in options:
            game_array[option[0]][option[1]] = actual_color
            pygame.draw.circle(grid_surface, parse_color_from_json(actual_color),
                               (option[1] * 60 + 30, option[0] * 60 + 30), 25)
            visited_cells[option] = actual_color
            break


# handles click events on button
def handle_click_buttons():
    mouse_position = pygame.mouse.get_pos()

    # restart button click handling
    if 550 > mouse_position[0] > 400 and 320 > mouse_position[1] > 290:
        load_level(current_level)

    # new level button click handling
    elif 550 > mouse_position[0] > 400 and 370 > mouse_position[1] > 340:
        generate_new_level()
    # solve level button click handling
    elif 550 > mouse_position[0] > 400 and 270 > mouse_position[1] > 240:
        solve()


# init game
def init_game():
    global clock

    pygame.init()
    clock = pygame.time.Clock()
    icon = pygame.image.load('assets\logo.jpg')
    pygame.display.set_icon(icon)
    pygame.display.set_caption("Flow free")


# generate surfaces
def generate_surfaces():
    global main_surface, grid_surface

    main_surface = pygame.display.set_mode((WIDTH, HEIGHT))
    main_surface.fill(GREY)
    grid_surface = pygame.Surface((360, 360))
    grid_surface.fill(GREY)

    for x in range(0, 6):
        for y in range(0, 6):
            pygame.draw.rect(grid_surface, GREEN_CYAN, [60 * y, 60 * x, 60, 60], 1)


# generate fonts
def generate_fonts():
    text_font_big = pygame.font.SysFont("comicsansms", 24)

    text_flows_label = text_font_big.render("Flows", False, WHITE)
    text_flows_value = text_font_big.render("0/6", False, PURPLE)
    text_pipes_label = text_font_big.render("Pipe", False, WHITE)
    text_pipes_value = text_font_big.render("0 %", False, PURPLE)
    text_moves_label = text_font_big.render("Moves", False, WHITE)
    text_moves_value = text_font_big.render("0", False, PURPLE)

    main_surface.blit(grid_surface, (10, 10))
    main_surface.blit(text_flows_label, (400, 50))
    main_surface.blit(text_flows_value, (500, 50))
    main_surface.blit(text_pipes_label, (400, 90))
    main_surface.blit(text_pipes_value, (500, 90))
    main_surface.blit(text_moves_label, (400, 130))
    main_surface.blit(text_moves_value, (500, 130))


# generate buttons
def generate_buttons():
    text_font_small = pygame.font.SysFont("comicsansms", 16)

    # solve button
    solve_button_text = text_font_small.render("Solve", False, PURPLE)
    pygame.draw.rect(main_surface, WHITE, (400, 240, 150, 30))
    main_surface.blit(solve_button_text, (453, 245))

    # restart button
    restart_button_text = text_font_small.render("Restart", False, WHITE)
    pygame.draw.rect(main_surface, PURPLE, (400, 290, 150, 30))
    main_surface.blit(restart_button_text, (445, 295))

    # new level button
    new_level_button_text = text_font_small.render("New level", False, PURPLE)
    pygame.draw.rect(main_surface, WHITE, (400, 340, 150, 30))
    main_surface.blit(new_level_button_text, (445, 345))


init_game()
load_level(current_level)

while running:

    generate_fonts()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_click_buttons()

    pygame.display.flip()
    clock.tick(FPS)
