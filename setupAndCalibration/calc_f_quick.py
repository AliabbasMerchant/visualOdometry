import cv2
import numpy as np

cam = cv2.VideoCapture(0)
_, main_original = cam.read()
main_original = cv2.resize(main_original, (320, 240))
cam.release()
cv2.imshow('main_original', main_original)
cv2.waitKey(0)
cv2.destroyAllWindows()

kernel = np.ones((5, 5), np.uint8)
main = cv2.morphologyEx(main_original, cv2.MORPH_OPEN, kernel)  # erosion, followed by dilation
main = cv2.GaussianBlur(main, (13, 13), 0)

real_distance = 120
real_width = 9.5
pixel_width = int(input("Please enter the pixel width of the target object: "))

factor = real_distance/real_width
print(factor)
print(pixel_width)
F = pixel_width * factor
print("F = ", F)

# 571.3157894736842