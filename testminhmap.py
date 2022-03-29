import numpy as np
import math
import cv2

def rotate_image(image, angle):
    print(angle)
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    # print("Image center: ",image_center)
    # cv2.circle(image,(75,75),5,(0,255,0),2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def compute_skew(src_img):

    if len(src_img.shape) == 3:
        h, w, _ = src_img.shape
    elif len(src_img.shape) == 2:
        h, w = src_img.shape
    else:
        print('upsupported image type')

    # copyimg = cv2.cvtColor(src_img,cv2.COLOR_GRAY2BGR)
    img = cv2.medianBlur(src_img, 3)

    edges = cv2.Canny(img,  threshold1 = 30,  threshold2 = 100, apertureSize = 3, L2gradient = True)
    # cv2.imshow("Canny",edges)
    lines = cv2.HoughLinesP(edges, 1, math.pi/180, 40, minLineLength=w / 4.0, maxLineGap=h/4.0)
    angle = 0.0
    nlines = lines.size
    # if lines is not None:
    #     for i in range(0,len(lines)):
    #         l = lines[i][0]
    #         cv2.line(src_img,(l[0],l[1]),(l[2],l[3]),(0,0,255),1,cv2.LINE_AA)
        # cv2.imshow("CC",src_img)
    #print(nlines)
    cnt = 0
    print(lines)
    for x1, y1, x2, y2 in lines[0]:
        ang = np.arctan2(y2 - y1, x2 - x1)
        #print(ang)
        if math.fabs(ang) <= 30: # excluding extreme rotations
            angle += ang
            cnt += 1

    if cnt == 0:
        return 0.0
    return (angle / cnt)*180/math.pi

def deskew(src_img):
    return rotate_image(src_img, compute_skew(src_img))


if __name__ == '__main__':
    # import cv2
    img = cv2.imread('frame.jpg')
    corrected_img = deskew(img)
    cv2.imshow("Map",corrected_img)
    cv2.waitKey(0)