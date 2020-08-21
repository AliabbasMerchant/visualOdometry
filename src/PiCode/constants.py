# All measurements in cm

distance_between_cameras = 6.5
bf = 1300.0
# bf = distance between image plane and camera hole
perceived_focal_length = 631.578947368421  # 290
# f = perceived focal length of camera
# height_of_cameras = 10  # not used
# horizontal_distance_to_baseline = 10  # not used # distance from plane of camera to the lowermost line in the image

map_block = 30  # size of map block (in cm)
map_horizon = 500  # 5m

color_limit = 75


# properties of images
Height = 240
Width = 320
Area = Height * Width

primary_camera = 'right'  # PiCam

bot_height = 20  # not used
bot_width = 24  # along x-axis
bot_length = 26

effAngle = 90  # the angle in which the bot is facing, just like in graphs  # degrees
bot_x = 0  # from center of cameras
bot_y = 0  # from center of cameras

target_approximation = 20

destination_x = 0
destination_y = 1000

# avg_computation_time = 3
avg_100cm_movement_time = 1.9
avg_block_movement_time = map_block/100 * avg_100cm_movement_time


def get_eff_angle():
    ans = effAngle
    while ans < 0:
        ans += 360
    return ans % 360



# 4*60 - 6.8
# 8*60 - 13.5
