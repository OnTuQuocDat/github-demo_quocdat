import cv2
import numpy as np
img = cv2.imread("frame.jpg", 0)

kernel_1 = np.ones((1, 10), np.uint8)
mor = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel_1)
kernel_1 = np.ones((3, 15), np.uint8)
mor = cv2.morphologyEx(mor, cv2.MORPH_CLOSE, kernel_1)
cv2.imshow("HALO", mor)
cv2.waitKey(0)
cv2.destroyAllWindows