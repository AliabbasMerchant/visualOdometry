import constants
from helper_functions import get_img, get_object_contours, match_contours, get_commands, \
    calculate_height, calculate_dist_from_center_of_bot, calculate_distance, calculate_width, bot_rotate, bot_move, \
    release_cameras, move
import math
from Object import Object, create_object_map, objects
from test_help import tprint, show_bounding_box, plot_moves, save_obj_map

constants.destination_x = 0
constants.destination_y = 240

main = get_img()
other = get_img(main=False)
tprint("Images loaded")

main_contours = get_object_contours(main, cam='right')
other_contours = get_object_contours(other)
tprint("Contours found")

contours = match_contours(main_contours, other_contours)
tprint("Contours matched")

for index, contour_pair in enumerate(contours):
    print(contour_pair[0])
    print(contour_pair[1])
    if contour_pair[0][2] == constants.Width and contour_pair[1][2] == constants.Width:
        # Its a wall  # Wall may be wrongly detected as the horizon also
        distance = None
    elif contour_pair[0][0] == contour_pair[1][0] or \
            contour_pair[0][0] + contour_pair[0][2] == contour_pair[1][0] + contour_pair[1][2]:
        distance = 'inf'  # Object is at infinite distance
        # We don't consider it as an object worthy of being detected
    else:
        show_bounding_box(main, contour_pair[0], "right_"+str(index)+".png")
        show_bounding_box(other, contour_pair[1], "left_"+str(index)+".png")
        distance = calculate_distance(contour_pair[0], contour_pair[1])
        tprint("distance = ", distance)
        # distance of center of object from center of bot
        distance_from_cent = calculate_dist_from_center_of_bot(contour_pair[1], distance)
        tprint("distance_from_cent = ", distance_from_cent)
        colors = [contour_pair[0][4], contour_pair[1][4]]
        # considering left camera
        width = calculate_width(contour_pair[1], distance)
        tprint("width = ", width)
        # considering left camera
        height = calculate_height(contour_pair[1], distance)  # Not specifically needed
        tprint("height = ", height)
        # considering left camera
        angle = math.radians(constants.get_eff_angle())
        x = constants.bot_x + (distance * math.cos(angle) + distance_from_cent * math.sin(angle))
        y = constants.bot_y + (distance * math.sin(angle) - distance_from_cent * math.cos(angle))
        obj = Object(x, y, width, height, colors)
        objects.append(obj)

for obj in objects:
    tprint(obj)

object_map = create_object_map()
save_obj_map("map_test.txt", object_map)

moves = get_commands(object_map)
with open('map_test_path.txt', 'wt') as f:
    for move in moves:
        print(move)
        f.write(str(move))
        f.write('\n')
# plot_moves(object_map, moves, "plotted_map_test.txt")

release_cameras()
move(object_map, limit=10)
print("TARGET ACHIEVED!")