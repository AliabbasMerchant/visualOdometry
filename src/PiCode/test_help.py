import cv2
import copy


def tprint(*args, **kwargs):
    print("***", *args, **kwargs)


def show_bounding_box(img, contour, filename):
    height, width = img.shape[:2]
    image = img[0:height, 0:width].copy()
    x, y, w, h = contour[:4]
    image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow('image', image)
    cv2.imwrite(filename, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def save_obj_map(filename, object_map):
    with open(filename, 'wt') as f:
        for i in object_map:
            for j in i:
                if int(j) == 1:
                    f.write(" ")
                else:
                    f.write(str(int(j)))
            f.write('|\n')
        f.write('\b')
        for i in object_map:
            for j in i:
                f.write("-")
            break


def plot_moves(object_map, moves, filename):
    obj_map = copy.deepcopy(object_map)
    bot_i = None
    bot_j = None
    for i in range(obj_map):
        if bot_i is not None and bot_j is not None:
            break
        for j in range(obj_map[0]):
            if obj_map[i][j] == 2:
                bot_i = i
                bot_j = j
                break
    bot_angle = 90  # upwards
    _i = bot_i
    _j = bot_j
    path_marker = 7.0
    path_len = 0.0
    obj_map[_i][_j] = path_marker
    for _move in moves:
        move, angle = _move[0], _move[1]
        if move:
            path_len += 1
            if bot_angle == 0:
                _i += 1
            elif bot_angle == 90:
                _j -= 1
            elif bot_angle == 180:
                _i -= 1
            elif bot_angle == 270:
                _j += 1
            else:
                print("--------------------------Plot_moves Error: Angle=", bot_angle)
            print("Plot moves: _i = {}, _j = {}".format(_i, _j))
            if obj_map[_i][_j] == 9:  # occupied
                print("--------------------------Plot_moves Error: Map block is already occupied")
            else:
                try:
                    obj_map[_i][_j] = path_marker
                except IndexError:
                    print("--------------------------Plot_moves Error: IndexError")
        else:
            bot_angle += angle
            bot_angle = bot_angle % 360
    save_obj_map(filename, obj_map)

# plot_moves()