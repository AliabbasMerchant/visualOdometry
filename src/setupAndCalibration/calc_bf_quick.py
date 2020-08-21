import cv2
import numpy as np
from constants import *


kernel = np.ones((5, 5), np.uint8)

cam = cv2.VideoCapture(0)
_, main_original = cam.read()
main_original = cv2.resize(main_original, (320, 240))
cam.release()
main = cv2.morphologyEx(main_original, cv2.MORPH_OPEN, kernel)  # erosion, followed by dilation
main = cv2.GaussianBlur(main, (13, 13), 0)
cv2.imshow('main_original', main_original)
cv2.waitKey(0)

cv2.destroyAllWindows()

x = int(input("Please enter the pixel lhs of the target object: "))
w = int(input("Please enter the pixel width of the target object: "))
cR = [x,None,w,None]  # x,y,w,h


cam = cv2.VideoCapture(1)
_, other_original = cam.read()
other_original = cv2.resize(other_original, (320, 240))
cam.release()
other = cv2.morphologyEx(other_original, cv2.MORPH_OPEN, kernel)  # erosion, followed by dilation
other = cv2.GaussianBlur(other, (13, 13), 0)
cv2.imshow('other_original', other_original)
cv2.waitKey(0)
cv2.destroyAllWindows()

x = int(input("Please enter the pixel lhs of the target object: "))
w = int(input("Please enter the pixel width of the target object: "))
cL = [x,None,w,None]  # x,y,w,h


real_distance = 113

# Assuming objects of single color, at least a unique average
# Later on, select contours of 2nd image like that of first one and match wrt size and color
# other_contours = []
# for contour in main_contours:
#     x, y, w, h, color = contour
#     color_upper = np.array(color + color_limit//2)
#     color_lower = np.array(color - color_limit//2)
#     # print(horizon_upper, horizon_lower)
#     mask = cv2.inRange(other, color_lower, color_upper)
#     res = cv2.bitwise_and(other, other, mask=mask)
#     # img = cv2.rectangle(main, (x, y), (x + w, y + h), (0, 255, 0), 2)
#     image, contours, hierarchy = cv2.findContours(cv2.cvtColor(res, cv2.COLOR_BGR2GRAY), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     matching_cnt = None
#     max_area = 0
#     for cnt in contours:
#         area = cv2.contourArea(cnt)
#         if area > max_area:
#             matching_cnt = cnt
#             max_area = area
#     x, y, w, h = cv2.boundingRect(matching_cnt)
#     other_contours.append((x, y, w, h, get_avg_color(main[y:y + h, x:x + h])))
#     cv2.imshow("res", res)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#
# assert len(other_contours) == len(main_contours) and "len(other_contours)!=len(main_contours)"
s1 = Width - cR[0]
s2 = Width - cL[0]
e1 = Width - (cR[0] + cR[2])
e2 = Width - (cL[0] + cL[2])

gh = s1 - Width / 2
ef = Width / 2 - s2
print(gh, ef, gh + ef)
BF1 = abs(real_distance*(ef+gh)/distance_between_cameras)

gh = e1 - Width / 2
ef = Width / 2 - e2
print(gh, ef, gh + ef)
BF2 = abs(real_distance*(ef+gh)/distance_between_cameras)

BF = round((BF1 + BF2) / 2, 3)
print(BF1, BF2, "BF = ", BF)