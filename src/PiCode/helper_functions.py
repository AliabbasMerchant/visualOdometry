import yaml
import constants
import cv2
import numpy as np
import pyastar
from Bot_functions import Bot

print("Helper has imported")
# main is right
right = True
camR = None
camL = None


bot = Bot()
# print("bot object created")

def logger(f):
    def log(*args, **kwargs):
        print("---Log--- {}".format(f.__name__))
        # print("{}, {}".format(f.__name__, *args, *kwargs))
        ret = f(*args, **kwargs)
        print(ret)
        return ret

    return log


@logger
def calibrate(image):
    # with open('calibration.yaml') as f:
    #     loadeddict = yaml.load(f)
    # mtxloaded = loadeddict.get('camera_matrix')
    # distloaded = loadeddict.get('dist_coeff')
    # h, w = image.shape[:2]
    # newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtxloaded, distloaded, (w, h), 1, (w, h))
    # # undistort
    # dst = cv2.undistort(image, mtxloaded, distloaded, None, newcameramtx)
    # # crop the image
    # x, y, w, h = roi
    # dst = dst[y:y + h, x:x + w]
    # return dst
    return image


@logger
def get_img(main=True, raw=False, Width=constants.Width, Height=constants.Height, second=False):
    right = True
    if (main and right) or (not main and not right):
        cam = cv2.VideoCapture(0)
        _, img = cam.read()
        cam.release()
        # img = cv2.imread('pics/pics/54077.5137136-R.png')
        if second:
            img = cv2.imread('pics/pics/54104.5399387-R.png')
        # img = cv2.imread('pics/pics/IMG_20180614_115813.jpg')
    else:
        cam = cv2.VideoCapture(1)
        _, img = cam.read()
        cam.release()
        # img = cv2.imread('pics/pics/54077.5137136-L.png')
        if second:
            img = cv2.imread('pics/pics/54104.5399387-L.png')
    if raw:
        pass
    else:
        img = cv2.resize(img, (Width, Height))
        kernel = np.ones((5, 5), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)  # erosion, followed by dilation
        img = cv2.GaussianBlur(img, (31, 31), 0)
    return img


# def get_img(main=True, raw=False, Width=constants.Width, Height=constants.Height):
#     global camL, camR
#     if (main and right) or (not main and not right):
#         if camR is None:
#             camR = cv2.VideoCapture(0)  # Right cam
#         _, img = camR.read()
#     else:
#         if camL is None:
#             camL = cv2.VideoCapture(1)  # Left cam
#         _, img = camL.read()
#     if raw:
#         pass
#     else:
#         img = cv2.resize(img, (Width, Height))
#         img = calibrate(img)
#         kernel = np.ones((5, 5), np.uint8)
#         img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)  # erosion, followed by dilation
#         img = cv2.GaussianBlur(img, (13, 13), 0)
#     return img


@logger
def release_cameras():
    global camL, camR
    camL.release()
    camR.release()


@logger
def get_avg_color(area):
    # takes in a 3 channel area
    # returns a 3 channel color (np.array)
    h, w = area.shape[:2]
    avg = np.array([0, 0, 0])
    num = 0
    for i in range(h - 1):
        for j in range(w - 1):
            num += 1
            try:
                avg[0] += area[i, j][0]
                avg[1] += area[i, j][1]
                avg[2] += area[i, j][2]
            except Exception:
                print("Error", i, h, j, w)
                print(area[i, j])
    avg[0] //= num
    avg[1] //= num
    avg[2] //= num
    return np.array(avg)


@logger
def remove_ground_and_horizon(_image, cam, limit=None):
    # TODO: Warning: A wall may also be considered as being the horizon
    if limit is None:
        limit = np.array([30, 70, 70])
    horizon_height = 50
    shifted = cv2.pyrMeanShiftFiltering(_image, 51, 21)
    bgr = shifted
    #if cam == 'right':
        #bgr = cv2.cvtColor(bgr, cv2.COLOR_BGR2LAB)
    hsv_shifted = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    cv2.imshow('original', _image)
    cv2.imshow('hsv', hsv_shifted)
    if cam == 'right':
        cv2.imwrite('original_right.png', _image)
        cv2.imwrite('hsv_right.png', hsv_shifted)
    else:
        cv2.imwrite('original_left.png', _image)
        cv2.imwrite('hsv_left.png', hsv_shifted)
    ground = hsv_shifted[constants.Height - horizon_height:constants.Height,
             (constants.Width // 2) - horizon_height // 2:(constants.Width // 2) + horizon_height // 2]
    ground = get_avg_color(ground)
    ground_upper = np.array(ground + limit)
    ground_lower = np.array(ground - limit)
    horizon = hsv_shifted[0:horizon_height + 1, 0:constants.Width]
    horizon = get_avg_color(horizon)
    horizon_upper = np.array(horizon + limit)
    horizon_lower = np.array(horizon - limit)
    mask_ground = cv2.inRange(hsv_shifted, ground_lower, ground_upper)
    mask_horizon = cv2.inRange(hsv_shifted, horizon_lower, horizon_upper)
    f_mask = cv2.add(mask_horizon, mask_ground)
    res = cv2.bitwise_and(_image, _image, mask=f_mask)
    res = _image - res
    cv2.imshow("res", res)
    if cam == 'right':  # first the right image is processed
        cv2.imwrite('res_right.png', res)
    else:
        cv2.imwrite('res_left.png', res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return res


@logger
def get_object_contours(_image, cam='left'):
    # contour structure: (x,y,w,h,color,(centerX,centerY))
    only_objects = remove_ground_and_horizon(_image, cam)
    gray = cv2.cvtColor(only_objects, cv2.COLOR_BGR2GRAY)
    # ret, thresh = cv2.threshold(gray, 127, 255, 0)
    # image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    image, contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    _contours = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if constants.Area * 0.001 <= area <= constants.Area * 0.5:  # check limits
            x, y, w, h = cv2.boundingRect(cnt)
            # img = cv2.rectangle(_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # cv2.imshow('img', img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            _contours.append((x, y, w, h, get_avg_color(_image[y:y + h, x:x + h]), (x + (w // 2), y + (h // 2))))

            # rect = cv2.minAreaRect(cnt)
            # box = cv2.boxPoints(rect)
            # box = np.int0(box)
            # img = cv2 .drawContours(img, [box], 0, (0, 0, 255), 2)
    return sorted(_contours, key=lambda cntr: cntr[5][0])  # key is the x coordinate of the center


@logger
def match_contours(contoursR, contoursL):
    match = []
    if len(contoursR) == len(contoursL):
        for i in range(len(contoursR)):
            contour_pair = [contoursR[i], contoursL[i]]
            match.append(contour_pair)
    else:
        # Matching using closest centers
        smaller_list, bigger_list = (contoursR, contoursL) if len(contoursR) < len(contoursL) else (
            contoursL, contoursR)
        # structure: (x,y,w,h,color,(centerX,centerY))
        import math

        def distance_btwn_points(x1, y1, x2, y2):
            return round(math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2)))

        for i in smaller_list:
            suitable = ()
            dist = constants.Area  # a large number
            for j in bigger_list:
                try_dist = distance_btwn_points(i[0], i[1], j[0], j[1])
                if try_dist < dist:
                    suitable = j
                    dist = try_dist
            if smaller_list == contoursR:
                contour_pair = [i, suitable]
            else:  # smaller_list == contoursL
                contour_pair = [suitable, i]
            match.append(contour_pair)
    return match


@logger
def calculate_distance(contourR, contourL):
    # Wikipedia method:
    # https://en.wikipedia.org/wiki/Computer_stereo_vision
    # If in center of 2 cameras:
    #   distance = (dist_between_cameras*bf)/(ef+gh)
    #   bf = distance between image plane and camera hole
    #   ef = distance between center and point in lhs image
    #   gh = distance between center and point in rhs image
    #   else distance = (dist_between_cameras*bf)/|(ef-gh)|

    distance = 0
    cR = contourR[:4]  # x,y,w,h
    cL = contourL[:4]
    print(cR, cL)

    # Mirror Image
    s1 = constants.Width - cR[0]
    s2 = constants.Width - cL[0]
    e1 = constants.Width - (cR[0] + cR[2])
    e2 = constants.Width - (cL[0] + cL[2])
    # Taking average of distances  mjuu
    gh = s1 - constants.Width / 2
    ef = constants.Width / 2 - s2
    print(gh, ef, ef + gh)
    if ef + gh != 0:  # 0 when both have the same x-coordiante
        distance1 = abs((constants.distance_between_cameras * constants.bf) / (ef + gh))
        gh = e1 - constants.Width / 2
        ef = constants.Width / 2 - e2
        print(gh, ef, ef + gh)
        if ef + gh != 0:
            distance2 = abs((constants.distance_between_cameras * constants.bf) / (ef + gh))
            distance = round((distance1 + distance2) / 2, 3)
        else:
            distance = round(distance1, 3)
    else:
        gh = e1 - constants.Width / 2
        ef = constants.Width / 2 - e2
        print(gh, ef, ef + gh)
        if ef + gh != 0:
            distance2 = abs((constants.distance_between_cameras * constants.bf) / (ef + gh))
            distance = round(distance2, 3)
        else:
            print("Error! Distance cannot be calculated.", cR, cL, sep='\n')
    print(distance1, distance2, "Distance = ", distance)
    return distance


@logger
def calculate_width(contr, dist):
    # contr: x,y,w,h .....
    # pyImageSearch Method
    # https://www.pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/
    # may be a bit inaccurate due to parallax errors and not an exactly plane object (i.e. at 90 degrees)
    px_width = contr[2]
    width = round(((dist * px_width) / constants.perceived_focal_length), 3)
    print(width)
    return width


@logger
def calculate_dist_from_center_of_bot(contr, dist):
    # considering left camera
    # contr: x,y,w,h .....
    # pyImageSearch Method
    # https://www.pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/
    # may be a bit inaccurate due to parallax errors and not an exactly plane object (i.e. at 90 degrees)
    # Pixel distance of center of object from center of LHS camera
    px_dist = contr[0] + contr[2] / 2 - constants.Width / 2
    distance_from_left = ((dist * px_dist) / constants.perceived_focal_length)
    distance_from_cent = round((distance_from_left - (constants.distance_between_cameras / 2)), 3)
    print(distance_from_cent)
    return distance_from_cent


@logger
def calculate_height(contr, dist):
    # contr: x,y,w,h .....
    # pyImageSearch Method
    # https://www.pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/
    # may be a bit inaccurate due to parallax errors and not an exactly plane object (i.e. at 90 degrees)
    px_height = contr[3]
    height = round(((dist * px_height) / constants.perceived_focal_length), 3)
    print(height)
    return height


@logger
def get_commands(object_map):  # From Swapnil
    moves = pyastar.fpath(grid=object_map)
    return moves


@logger
def bot_move(time):
    bot.forward(time * 1000)


@logger
def bot_rotate(angle):
    bot.rotate(angle)


@logger
def move(obj_map, limit=3):
    moves = get_commands(obj_map)
    print(moves)
    # list of [bool_move, angle_to_rotate]
    blocks_to_move = 0
    while blocks_to_move <= limit:
        move = 0
        while moves[blocks_to_move][0] and move <= limit:
            blocks_to_move += 1
            move += 1
        angle = moves[blocks_to_move][1]
        constants.effAngle += angle
        if move > 0:
            bot_move(constants.avg_block_movement_time * move)  # Move 3 blocks at max
        bot_rotate(angle)
        

# print(calculate_distance([121,None,23 , None], [168, None,26 , None]))