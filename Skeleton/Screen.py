import Stack
from Skeleton import consts
import pygame
import math
import BubblesGrid

screen = pygame.display.set_mode(
        (consts.WINDOW_WIDTH, consts.WINDOW_HEIGHT))

red = pygame.image.load('images/00.png')
yellow = pygame.image.load('images/02.png')
blue = pygame.image.load('images/20.png')
green = pygame.image.load('images/22.png')
purple = pygame.image.load('images/10.png')

colors = {
    '(255, 89, 94)' : red,
    '(255, 202, 58)' : yellow,
    '(25, 130, 196)' : blue,
    '(138, 201, 38)' : green,
    '(106, 76, 147)' : purple
}

def draw_bubble(bubble):
    # pygame.draw.circle(screen, bubble["color"],
    #                    center=(bubble["center_x"], bubble["center_y"]),
    #                    radius=bubble["radius"])

    screen.blit(colors[f'{bubble["color"]}'],
                (bubble['center_x']-bubble['radius'],
                        bubble['center_y']-bubble['radius']))

def draw_bubbles_popping(bubbles_popping):
    for bubble in bubbles_popping:
        draw_bubble(bubble)

def calc_mouse_angle(mouse_pos):
    x_diff = mouse_pos[0] - consts.ARROW_MIDBOTTOM_X
    y_diff = consts.ARROW_MIDBOTTOM_Y - mouse_pos[1]
    angle = math.degrees(math.atan2(y_diff, x_diff))
    return angle

def create_arrow(arrow_img):
    arrow = pygame.image.load(arrow_img)
    sized_arrow = pygame.transform.scale(arrow, (
        consts.ARROW_WIDTH, consts.ARROW_HEIGHT))

    # Create a box to put the arrow in, so that the rotation will be around
    # it's bottom (the box's center)
    arrow_box = pygame.Surface(
            (consts.ARROW_WIDTH, consts.ARROW_HEIGHT * 2), )
    arrow_box.fill(consts.BACKGROUND_COLOR)
    arrow_box.blit(sized_arrow, (0, 0))

    return arrow_box


def draw_arrow(arrow):
    rotated_arrow_rect = arrow.get_rect(
            center=(consts.ARROW_MIDBOTTOM_X, consts.ARROW_MIDBOTTOM_Y))
    screen.blit(arrow, rotated_arrow_rect)


def draw_border():
    line_y = (consts.NUM_OF_LINES_LOSE - 1) * consts.BUBBLE_RADIUS * 2 - (
            consts.NUM_OF_LINES_LOSE - 2) * consts.ROWS_OVERLAP
    pygame.draw.line(screen, consts.BORDER_COLOR, start_pos=(0, line_y),
                     end_pos=(consts.WINDOW_WIDTH, line_y))


def draw_turns(num_of_turns):
    message = consts.TURNS_TEXT + str(num_of_turns)
    draw_message(message, consts.TURNS_FONT_SIZE, consts.TURNS_COLOR,
                 consts.TURNS_LOCATION)


def draw_lose_message():
    draw_message(consts.LOSE_MESSAGE, consts.LOSE_FONT_SIZE,
                 consts.LOSE_COLOR, consts.LOSE_LOCATION)


def draw_win_message():
    draw_message(consts.WIN_MESSAGE, consts.WIN_FONT_SIZE,
                 consts.WIN_COLOR, consts.WIN_LOCATION)


def draw_message(message, font_size, color, location):
    font = pygame.font.SysFont(consts.FONT_NAME, font_size)
    text_img = font.render(message, True, color)
    screen.blit(text_img, location)

def draw_scores(score,X,Y,msg):
    draw_message(msg, consts.TURNS_FONT_SIZE , consts.TURNS_COLOR,
                 (X,Y))

def draw_game(game_state,score,highest_score):
    screen.fill(consts.BACKGROUND_COLOR)
    draw_arrow(game_state["rotated_arrow"])

    if game_state["is_bubble_fired"]:
        draw_bubble(game_state["bullet_bubble"])

    BubblesGrid.draw()
    draw_border()
    draw_turns(game_state["turns_left_to_add_row"])
    Stack.draw()

    draw_scores(score,consts.WINDOW_WIDTH-200,consts.WINDOW_HEIGHT-40,f"SCORE : {score}")
    draw_scores(highest_score,consts.WINDOW_WIDTH-200,consts.WINDOW_HEIGHT-70,f"HIGHEST SCORE : {highest_score}")

    if len(game_state["bubbles_popping"]):
        BubblesGrid.animate_bubbles_pop(game_state["bubbles_popping"])
        draw_bubbles_popping(game_state["bubbles_popping"])

    elif game_state["state"] == consts.LOSE_STATE:
        draw_lose_message()

    elif game_state["state"] == consts.WIN_STATE:
        draw_win_message()

    pygame.display.flip()
