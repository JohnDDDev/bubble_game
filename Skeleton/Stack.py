import Bubble
import consts
import random
import Screen

stack = []


def create(stack_size):
    global stack
    stack = []
    for i in range(stack_size):
        add_bubble(i,consts.bubble_colors)
    return stack


def add_bubble(col,colors):
    bubble_x = Bubble.calc_center_x(col, row=0,
                                    row_start=consts.STACK_LOCATION[0])
    stack.append(Bubble.create(bubble_x,
                               consts.STACK_LOCATION[1],
                               random.choice(colors))) #consts.bubble_colors

def remove_first():
    bullet_bubble = stack.pop(0)

    for i in range(len(stack)):
        stack[i]["center_x"] = Bubble.calc_center_x(i, row=0,
                                                    row_start=
                                                    consts.STACK_LOCATION[0])
    return bullet_bubble


def get_length():
    return len(stack)


def draw():
    for bubble in stack:
        Screen.draw_bubble(bubble)

# -----------------------------------------------------------------------------
# ---------------------------------your code-----------------------------------
# -----------------------------------------------------------------------------
