import pygame
import BubblesGrid
import Bubble
import consts
import Screen
import Stack
import sound

sounds = {
    'pop': 'bubble_pop.mp3',
}

state = {
    "original_arrow": Screen.create_arrow(consts.ARROW_IMG),
    "rotated_arrow": None,
    "is_bubble_fired": False,
    "bubbles_popping": [],
    "turns_left_to_add_row": consts.NUM_OF_TURNS_TO_ADD_ROW,
    "is_window_open": True,
    "state": consts.RUNNING_STATE,
    "bullet_bubble": None,
    "bubble_direction": None,
    "mouse_angle": None
}

state["rotated_arrow"] = state["original_arrow"]


def main():
    global corrent_state
    corrent_state = state.copy()

    global score
    score = 0
    pygame.init()
    BubblesGrid.create()
    Stack.create(consts.STACK_SIZE)

    bubble_colors = consts.bubble_colors

    while corrent_state["is_window_open"]:

        handle_user_events()

        if corrent_state["is_bubble_fired"]:

            move_bubble()

            if Bubble.should_stop(BubblesGrid.bubbles_grid,
                                  corrent_state["bullet_bubble"]):
                corrent_state["is_bubble_fired"] = False
                new_bubble_location = BubblesGrid.find_bubble_location_in_grid(
                        corrent_state["bullet_bubble"])
                BubblesGrid.put_bubble_in_grid(corrent_state["bullet_bubble"],
                                               new_bubble_location)

                same_color_cluster = BubblesGrid.get_same_color_cluster(
                        new_bubble_location,
                        corrent_state["bullet_bubble"]["color"],
                        [])

                if BubblesGrid.should_bubbles_pop(same_color_cluster):

                    sound.Play(sounds['pop'],len(same_color_cluster)) #sound

                    score += 500 * len(same_color_cluster)

                    corrent_state["bubbles_popping"] = \
                        BubblesGrid.pop_bubbles(same_color_cluster)

                # The counter counts only if bubbles weren't popped
                else:
                    corrent_state["turns_left_to_add_row"] -= 1

                    if corrent_state["turns_left_to_add_row"] == 0:
                        BubblesGrid.add_new_line()

                        # Reseting the counter
                        corrent_state["turns_left_to_add_row"] = \
                            consts.NUM_OF_TURNS_TO_ADD_ROW

                remove_isolated_bubbles()
                BubblesGrid.set_one_empty_line()
                remove_extinct_colors(BubblesGrid.bubbles_grid,bubble_colors)
                Stack.add_bubble(Stack.get_length(),bubble_colors)

                if is_lose():
                    corrent_state["state"] = consts.LOSE_STATE

                    #penalty for loosing
                    score -= 1000
                    if score < 0:
                        score = 0

                elif is_win(BubblesGrid.bubbles_grid):
                    corrent_state["state"] = consts.WIN_STATE

        Screen.draw_game(corrent_state,score,highest_score)

    return score

def handle_user_events():
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            corrent_state["is_window_open"] = False

        elif corrent_state["state"] != consts.RUNNING_STATE:
            continue

        if event.type == pygame.MOUSEMOTION:
            rotate_arrow()

        elif event.type == pygame.MOUSEBUTTONDOWN and \
                not corrent_state["is_bubble_fired"] and \
                not corrent_state["bubbles_popping"]:
            fire_bubble()

def rotate_arrow():
    corrent_state["mouse_angle"] = Screen.calc_mouse_angle(pygame.mouse.get_pos())
    corrent_state["rotated_arrow"] = pygame.transform.rotate(corrent_state["original_arrow"],
                                                     corrent_state["mouse_angle"] - 90)

def fire_bubble():
    corrent_state["is_bubble_fired"] = True
    corrent_state["bubble_direction"] = \
        Bubble.calc_direction(corrent_state["mouse_angle"])
    corrent_state["bullet_bubble"] = Stack.remove_first()


def move_bubble():
    Bubble.move_in_direction(corrent_state["bullet_bubble"], corrent_state["bubble_direction"])

    if Bubble.is_colliding_with_wall(corrent_state["bullet_bubble"]):
        corrent_state["bubble_direction"] = (corrent_state["bubble_direction"][0] * (-1),
                                     corrent_state["bubble_direction"][1])


def remove_isolated_bubbles():
    global score
    isolated_bubbles_locations = BubblesGrid.find_isolated_bubbles()

    if len(isolated_bubbles_locations) > 0:
        corrent_state["bubbles_popping"] += \
            BubblesGrid.pop_bubbles(isolated_bubbles_locations)

        sound.Play(sounds['pop'],len(isolated_bubbles_locations)) #sound
        score += 100 * len(isolated_bubbles_locations)

# -----------------------------------------------------------------------------
# ---------------------------------your code-----------------------------------
# -----------------------------------------------------------------------------
def remove_extinct_colors(grid,bubble_colors):
    presented_colors = set()

    if len(bubble_colors)==1:
        return

    for row in grid:
        for coll in row:
            if coll['color'] in bubble_colors:
                presented_colors.add(coll['color'])

    for color in bubble_colors.copy():
        if color not in presented_colors:
            print(f"The color {color} has been removed")
            bubble_colors.remove(color)


def is_lose() -> bool:
    if BubblesGrid.get_length()>consts.NUM_OF_LINES_LOSE:
        return True
    return False

def is_win(bubble_grid) -> bool:
    for bubbles_row in bubble_grid:
        for bubble in bubbles_row:
            if bubble['color'] != 'EMPTY':
                return False
    else:
        return True

def load_highest_score(highest_score_file):
    highest_score = 0

    try:
        with open(highest_score_file, 'r') as file:
            highest_score = file.read()
    except:
        print(f"unable To load File : {highest_score_file}")

    return highest_score

def new_high_score(score,highest_score_file):
    with open(highest_score_file, 'w') as file:
        file.write(str(score))

# -----------------------------------------------------------------------------
# ------------------------------your code end----------------------------------
# -----------------------------------------------------------------------------

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    global score

    #loading Highest score
    highest_score_file = 'highest_score.text'
    highest_score = load_highest_score(highest_score_file)

    playing = False

    Screen.draw_menu()

    playing=True
    print(f"Highest Score Is : {highest_score}")
    while playing:
        current_score = main()
        print(f"Your Score Is : {current_score}")

        if current_score > int(highest_score):
            new_high_score(current_score,highest_score_file)
            print(f"New High Score({current_score})!")

        answer = input("would You Like To play Again(y/n)")

        if answer.lower() in ['n','no']:
            playing = False
            print("Bye Bye")