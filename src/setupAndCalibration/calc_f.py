import cv2
import numpy as np
import math
from helper_functions import *
from Object import *

cam = cv2.VideoCapture(0)
_, main_original = cam.read()
# main_original = cv2.imread('/mnt/187C7C937C7C6D7E/projects_workspaces/computerVision/pics/camera/Things-R.jpg') # temp
main_original = cv2.resize(main_original, (320, 240))
cam.release()
cv2.imshow('sdfdf', main_original)

Height, Width = main_original.shape[:2]
Diagonal = round(math.sqrt(Height ** 2 + Width ** 2))
Area = Width * Height
# print(Height, Width)
cv2.waitKey(0)
cv2.destroyAllWindows()

kernel = np.ones((5, 5), np.uint8)

main = cv2.morphologyEx(main_original, cv2.MORPH_OPEN, kernel)  # erosion, followed by dilation
main = cv2.GaussianBlur(main, (13, 13), 0)

real_distance = 182.88
real_width = 9.6

print("---------")
main_contours, ground, horizon = get_object_contours(main)
print("---------")

print(len(main_contours))
# assert len(main_contours) == 1 and "Multiple objects detected"

for i in main_contours:
    print(i)

for i in range(len(main_contours)):
    print(main_contours[i])
    main_copy = main[:]
    x, y, w, h = main_contours[i][:4]
    main_copy = cv2.rectangle(main_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("main", main_copy)
    if cv2.waitKey(0) == ord('q'):
        cv2.destroyAllWindows()
    elif cv2.waitKey(0) == ord('a'):
        contour1 = main_contours[i]
        c = contour1[:4]  # x,y,w,h
        factor = real_distance/real_width
        print(factor)
        print(c[2])
        F = c[2] * factor
        print("F = ", F)
        cv2.destroyAllWindows()
        break
