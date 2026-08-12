import consts
import math
import BubblesGrid


def create(center_x, center_y, color):
    return {"color": color,
            "center_x": center_x,
            "center_y": center_y,
            "radius": consts.BUBBLE_RADIUS}


def calc_center_x(col, row, row_start):
    bubble_x = row_start + col * (
            consts.BUBBLE_RADIUS * 2 + consts.SPACE_BETWEEN_COLS) + consts.BUBBLE_RADIUS

    # Uneven rows has an offset
    if row % 2 != 0:
        bubble_x += consts.BUBBLE_RADIUS

    return bubble_x


def calc_center_y(row):
    return row * (consts.BUBBLE_RADIUS * 2 - consts.ROWS_OVERLAP) + \
           consts.BUBBLE_RADIUS


def move_in_direction(bubble, direction):
    bubble["center_x"] += direction[0]
    bubble["center_y"] += direction[1]


def is_colliding_with_wall(bullet_bubble):
    return bullet_bubble["center_x"] - consts.BUBBLE_RADIUS <= 0 or \
           bullet_bubble[
               "center_x"] + consts.BUBBLE_RADIUS >= consts.WINDOW_WIDTH


def calc_direction(angle):
    # y/x = tan(angle)
    y_movement = 10
    x_movement = y_movement / math.tan(math.radians(angle))
    return x_movement, -y_movement


def pop(bubbles_grid, bubble_location):
    bubble_popped = bubbles_grid[bubble_location[0]][bubble_location[1]].copy()
    bubbles_grid[bubble_location[0]][bubble_location[1]][
        "color"] = consts.NO_BUBBLE
    return bubble_popped


def is_isolated(bubbles_grid, bubble_location):
    return is_isolated_inner(bubbles_grid, bubble_location, [])


def is_isolated_inner(bubbles_grid, bubble_location, locations_checked):
    start_row, start_col = bubble_location
    locations_checked.append(bubble_location)

    # Bubbles on first row are considered not isolated
    if start_row == 0:
        return False

    neighbors_directions = BubblesGrid.get_neighbors_directions(start_row)

    for direction in neighbors_directions:
        new_row = start_row + direction[0]
        new_col = start_col + direction[1]
        new_location = (new_row, new_col)

        if 0 <= new_row < len(bubbles_grid) and \
                0 <= new_col < consts.BUBBLE_GRID_COLS and \
                new_location not in locations_checked and \
                bubbles_grid[new_row][new_col]["color"] != consts.NO_BUBBLE and \
                not is_isolated_inner(bubbles_grid, new_location,
                                      locations_checked):
            return False

    return True


# -----------------------------------------------------------------------------
# ---------------------------------your code-----------------------------------
# -----------------------------------------------------------------------------
def should_stop(bubbles_grid, bullet_bubble) -> bool:

    if bullet_bubble['center_y'] < bullet_bubble['radius']:
        return True

    for bubbles_row in bubbles_grid: #O(N^2)
        for bubble in bubbles_row:
            distance = ((( (bubble['center_x']-bullet_bubble['center_x'])**2 +
                  (bubble['center_y'] -bullet_bubble['center_y'])**2 )**0.5
                  -  (bubble['radius']+bullet_bubble['radius'])))

            if distance <= 0 and bubble['color'] != 'EMPTY':
                return True
    return False

#bullet_bubble > {'color' : (R,G,B),'center_x' : float, 'center_y' : float, 'radius': int}