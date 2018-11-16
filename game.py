import pygame
import json

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


# parse color read from json to RGB tuple
def parse_color_from_json(color):
    if color == "RED":
        return 211, 47, 47
    elif color == "GREEN":
        return 76, 175, 80
    elif color == "BLUE":
        return 0, 145, 234
    elif color == "YELLOW":
        return 255, 234, 0
    elif color == "PURPLE":
        return 103, 58, 183


# load levels data from json file
def load_level(loaded_level):
    with open('assets/levels.json') as levels_file:
        levels_file = json.load(levels_file)
        level_one = levels_file["levels"][loaded_level]

        print(loaded_level)

        for dot in level_one["dots"]:
            pygame.draw.circle(grid_surface, parse_color_from_json(dot["color"]), (dot["x"], dot["y"]), 25)


# displays new level
def generate_new_level():
    global current_level

    if current_level < 2:
        current_level += 1
    else:
        current_level = 0

    load_level(current_level)


# handles click events on button
def handle_click_buttons():
    mouse_position = pygame.mouse.get_pos()

    # restart button click handling
    if 550 > mouse_position[0] > 400 and 320 > mouse_position[1] > 290:
        load_level(current_level)

    # new level button click handling
    elif 550 > mouse_position[0] > 400 and 370 > mouse_position[1] > 340:
        generate_new_level()


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
    text_font = pygame.font.SysFont("comicsansms", 24)
    text_flows_label = text_font.render("Flows", False, WHITE)
    text_flows_value = text_font.render("0/6", False, PURPLE)
    text_pipes_label = text_font.render("Pipe", False, WHITE)
    text_pipes_value = text_font.render("0 %", False, PURPLE)
    text_moves_label = text_font.render("Moves", False, WHITE)
    text_moves_value = text_font.render("0", False, PURPLE)

    main_surface.blit(grid_surface, (10, 10))
    main_surface.blit(text_flows_label, (400, 30))
    main_surface.blit(text_flows_value, (490, 30))
    main_surface.blit(text_pipes_label, (400, 70))
    main_surface.blit(text_pipes_value, (490, 70))
    main_surface.blit(text_moves_label, (400, 110))
    main_surface.blit(text_moves_value, (490, 110))


# generate buttons
def generate_buttons():
    pygame.draw.rect(main_surface, WHITE, (400, 290, 150, 30))
    pygame.draw.rect(main_surface, WHITE, (400, 340, 150, 30))


init_game()
generate_surfaces()
load_level(current_level)
generate_fonts()
generate_buttons()

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            handle_click_buttons()

    pygame.display.flip()
