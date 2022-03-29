# import cv2
# import numpy as np

# img = cv2.imread('vidu.jpg',0)
# img2 = img.copy()
# template = cv2.imread('template_mau.jpg',0)
# w, h = template.shape[::-1]

# # Method
# meth = cv2.TM_CCOEFF
# # method = eval(meth)

# #Apply template matching
# res = cv2.matchTemplate(img2,template,meth)
# threshold = 0.8
# loc = np.where( res >= threshold)
# for pt in zip(*loc[::-1]):
#     cv2.rectangle(img2,pt,(pt[0] + w,pt[1]+h),(0,0,255),2)
# cv2.imwrite('res.jpg',img2)

# # img = img[400:600,20:220]
# # cv2.imwrite("template_mau.jpg",img)


# cv2.imshow("Hinh",img2)



# cv2.waitKey()

# keyCode = cv2.waitKey(1)
# # Stop the program on the ESC key
# if keyCode == 27 or keyCode == ord('q'):
#     cv2.destroyAllWindows()


import cv2
import numpy as np 



def template_matching(im_rgb):
    count = 0
    tem1_signal = 0
    tem2_signal = 0
    #Read template
    # im_rgb = cv2.imread('test_img/test3.jpg')
    im_gray = cv2.cvtColor(im_rgb,cv2.COLOR_BGR2GRAY)

    template = cv2.imread('template_mau.jpg',0)
    # template = template[450:650,150:350]
    w, h = template.shape[::-1]
    # cv2.imshow("Template",template)
    # cv2.waitKey(0)
    res = cv2.matchTemplate(im_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    if sorted(zip(*loc[::-1])) == []:
        # print("Ko co tem")
        return 0,0
    else:
        for pt in zip(*loc[::-1]):
            cv2.rectangle(im_rgb, pt, (pt[0]+w, pt[1]+h),(0,255,255),1)
            # count += 1
            # print("Point 0 and Point 1: ",(pt[0],pt[1]))
            if pt[1] > 300 and pt[1] < 500:
                if pt[0] > 1600 and pt[0] < 1920:
                    print("Tem 2 appeared")
                    tem2_signal = 1
                elif pt[0] > 10 and pt[0] < 100:
                    print("Tem 1 appeared")
                    tem1_signal = 1
                else:
                    print("Tem sai vi tri")
                    tem1_signal = 0
                    tem2_signal = 0
            else:
                print("Error bat thuong")
                tem1_signal = 0
                tem2_signal = 0

    cv2.imshow("Template matching",cv2.resize(im_rgb,(640,480)))
    # cv2.waitKey(0)

    if tem1_signal == 1 and tem2_signal == 1:
        # print("Da co tem day du")
        return True,True
    else:
        # print("Ko co du tem tren ban- bao NG")
        return False,False

# if __name__=='__main__':
#     template_matching()