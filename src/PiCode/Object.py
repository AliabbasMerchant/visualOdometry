import constants
import copy
import numpy as np
import math

objects = []


def logger(f):
    def log(*args, **kwargs):
        print("---Log--- {}".format(f.__name__))
        # print("{}, {}".format(*args, *kwargs))
        ret = f(*args, **kwargs)
        print(ret)
        return ret
    return log


class Object:
    def __init__(self, x, y, width, height, colors):
        self.x = x  # With regards to map  # center of bot
        self.y = y  # With regards to map  # center of bot
        self.width = width
        self.depth = None
        self.height = height
        if colors is not None:
            self.colors = copy.deepcopy(colors)  # 3 channel
        else:
            self.colors = []
        self.first_detect_angle = constants.get_eff_angle()
        # self.angle = self.calc_angle()  # angular position of the object wrt map origin

    # def calc_angle(self):
    #     return math.degrees(math.atan(self.y/self.x))

    def __str__(self):
        return "Object: x={}, y={}, width={}, height={}, colors={}, depth={}". \
            format(self.x, self.y, self.width, self.height, self.colors, self.depth)


@logger
def in_field_of_view(obj):
    # in degrees
    angle_range = 45  # TODO: Verify
    if constants.bot_x <= obj.x - obj.width / 2:
        if obj.depth is not None:
            if constants.bot_y <= obj.y - obj.depth / 2:
                return 45 - angle_range <= constants.get_eff_angle() <= 45 + angle_range
            elif constants.bot_y >= obj.y + obj.depth / 2:
                return 315 - angle_range <= constants.get_eff_angle() <= 315 + angle_range or constants.get_eff_angle() == 0
            else:
                return (315 <= constants.get_eff_angle() <= 315 + angle_range) or (
                            0 <= constants.get_eff_angle() <= 0 + angle_range)
        else:
            if constants.bot_y <= obj.y:
                return 45 - angle_range <= constants.get_eff_angle() <= 45 + angle_range
            else:
                return 315 - angle_range <= constants.get_eff_angle() <= 315 + angle_range or constants.get_eff_angle() == 0
    elif constants.bot_x >= obj.x + obj.width / 2:
        if obj.depth is not None:
            if constants.bot_y <= obj.y - obj.depth / 2:
                return 135 - angle_range <= constants.get_eff_angle() <= 135 + angle_range
            elif constants.bot_y >= obj.y + obj.depth / 2:
                return 225 - angle_range <= constants.get_eff_angle() <= 225 + angle_range
            else:
                return 180 - angle_range <= constants.get_eff_angle() <= 180 + angle_range
        else:
            if constants.bot_y <= obj.y:
                return 135 - angle_range <= constants.get_eff_angle() <= 135 + angle_range
            else:
                return 225 - angle_range <= constants.get_eff_angle() <= 225 + angle_range
    else:  # constants.bot_x within range of obj.width
        if obj.depth is not None:
            if constants.bot_y <= obj.y - obj.depth / 2:
                return 90 - angle_range <= constants.get_eff_angle() <= 90 + angle_range
            elif constants.bot_y >= obj.y + obj.depth / 2:
                return 270 - angle_range <= constants.get_eff_angle() <= 270 + angle_range
            else:
                return True  # should ideally not happen
        else:
            if constants.bot_y <= obj.y:
                return 90 - angle_range <= constants.get_eff_angle() <= 90 + angle_range
            else:
                return 270 - angle_range <= constants.get_eff_angle() <= 270 + angle_range


@logger
def get_color_deviation(color1, color2):
    # 3-channel colors
    return np.max(np.array([abs(color1[0] - color2[0]), abs(color1[1] - color2[1]), abs(color1[2] - color2[2])]))
    # TODO: Or should we take the average??


@logger
def match_to_objects(avg_color1, avg_color2, template=None):
    # template is an edged image
    threshold = 50  # TODO: Decide the threshold
    match_index = None
    deviation = 100000  # A sufficiently large number
    for i in range(len(objects)):
        if in_field_of_view(objects[i]):
            color_deviation = []
            for avg_color in objects[i].colors:
                color_dev = get_color_deviation(avg_color, avg_color1)
                color_dev += get_color_deviation(avg_color, avg_color2)
                color_dev /= 2
                color_deviation.append(color_dev)
            dev = np.average(color_deviation)
            if dev < deviation:
                deviation = dev
                match_index = i
    if deviation < threshold:
        return match_index
    else:
        return 'create_obj'


@logger
def round_off_to_num(no, num):
    quo = round(no // num)
    rem = no - (quo * num)
    if num >= 0:
        if rem < num / 2:
            return int(quo * num)
        else:
            return int(quo * num + num)
    else:
        if rem <= num / 2:
            return int(quo * num)
        else:
            return int(quo * num + num)


@logger
def create_object_map():
    # KEY:
    # 1 - Empty or Unknown(considered to be empty)
    # 9 - Occupied (-1)
    # 2 - Bot
    # 3 - Destination
    # 9 - Unknown (consider it occupied) # Due to unknown depths of objects
    std_depth = round((2 * constants.map_block) // constants.map_block)  # depth in cm of objects whose depth is unknown
    padding = round(constants.map_horizon // constants.map_block)  # Note: 16
    rows = round((abs(constants.destination_y) // constants.map_block) + 2 * padding)  # Note: 500/30 + 2*16 = 48
    cols = round((abs(constants.destination_x) // constants.map_block) + 2 * padding)  # Note: 400/30 + 2*16 = 45
    # print("Padding = ", padding)
    object_map = np.ones((rows, cols), np.float32)
    if constants.destination_x >= 0:
        origin_x = padding
    else:
        origin_x = cols - padding
    if constants.destination_y >= 0:
        origin_y = padding
    else:
        origin_y = rows - padding
    # print(origin_x, origin_y)  # Note: 16, 16
    bot_width = math.ceil(constants.bot_width / constants.map_block)
    bot_length = math.ceil(constants.bot_length / constants.map_block)
    # print(bot_width, bot_length)  # Note: 1, 1
    origin_x -= 1
    origin_y -= 1

    for obj in objects:
        # TODO: verify
        # print(obj.x, obj.y, obj.width)
        x = round(round_off_to_num(obj.x, constants.map_block) // constants.map_block)
        y = round(round_off_to_num(obj.y, constants.map_block) // constants.map_block)
        width = math.ceil(obj.width / constants.map_block)
        print(x, y, width)  # Note: 2, 2, 1
        if obj.depth is not None:
            depth = math.ceil(obj.depth / constants.map_block)
            # print(depth)
            object_map[
            math.ceil(origin_y + y):math.ceil(origin_y + y + math.ceil(depth)),
            math.ceil(origin_x + x - math.ceil(width / 2)):math.ceil(origin_x + x + math.ceil(width / 2))] = 9
            # object_map[math.ceil(origin_y + y - math.ceil(depth / 2)):math.ceil(origin_y + y + math.ceil(depth / 2)),
            #     math.ceil(origin_x + x - math.ceil(width / 2)):math.ceil(origin_x + x + math.ceil(width / 2))] = -1
        else:
            depth = obj.width if (obj.width / constants.map_block > std_depth) else std_depth
            object_map[
            math.ceil(origin_y + y):math.ceil(origin_y + y + math.ceil(depth)),
            math.ceil(origin_x + x - math.ceil(width / 2)):math.ceil(origin_x + x + math.ceil(width / 2))] = 9
            # object_map[
            # math.ceil(origin_y + y - math.ceil(std_depth / 2)):math.ceil(origin_y + y + math.ceil(std_depth / 2)),
            # math.ceil(origin_x + x - math.ceil(width / 2)):math.ceil(origin_x + x + math.ceil(width / 2))] = -1
            # object_map[
            # math.ceil(origin_y + y + math.ceil(std_depth)):,
            # math.ceil(origin_x + x - math.ceil(width / 2)):math.ceil(origin_x + x + math.ceil(width / 2))] = 9

    # d = math.ceil(origin_x + constants.bot_x - math.ceil(bot_width / 2))
    # f = math.ceil(origin_x + constants.bot_x + math.ceil(bot_width / 2))
    # g = math.ceil(origin_y - constants.bot_y - bot_length)
    # h = math.ceil(origin_y - constants.bot_y)
    # object_map[g:h, d:f] = 2
    # object_map[(g + h) // 2, (d + f) // 2] = 2
    # object_map[math.ceil(origin_y - constants.bot_y - bot_length / 2), math.ceil(origin_x + constants.bot_x)] = 2
    object_map[math.ceil(origin_y + constants.bot_y), math.ceil(origin_x + constants.bot_x)] = 2
    # print((g+h)//2, (d+f)//2)  # Note: 14, 15
    # print(math.ceil(origin_y - constants.bot_y - bot_length / 2), math.ceil(origin_x + constants.bot_x))  # Note: 15, 15
    __x = origin_x + round(constants.destination_x // constants.map_block)  # Note: 15 + 16
    __y = origin_y + round(constants.destination_y // constants.map_block)  # Note: 15 + 13
    # print(origin_x)
    # print(__y, __x)  # Note: 31, 28
    object_map[__y, __x] = 3

    object_map = np.flip(object_map, 0)
    return object_map
