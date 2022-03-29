import cv2
import numpy as np 


def template_matching():
    #Read template
    im_rgb = cv2.imread('/home/machine005/Dulieuhinhanh2/frameL0.jpg')
    im_gray = cv2.cvtColor(im_rgb,cv2.COLOR_BGR2GRAY)

    template = cv2.imread('template.jpg',0)
    template = template[450:650,150:350]
    w, h = template.shape[::-1]
    # cv2.imshow("Template",template)
    # cv2.waitKey(0)
    res = cv2.matchTemplate(im_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(im_rgb, pt, (pt[0]+w, pt[1]+h),(0,255,255),1)
    cv2.imshow("Template matching",im_rgb)
    cv2.waitKey(0)

if __name__=='__main__':
    template_matching()