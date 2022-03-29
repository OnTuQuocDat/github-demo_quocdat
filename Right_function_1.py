#Create by: On Tu Quoc Dat - Matsuya R&D Co.Ltd - MIC Department
#Pokayoke 
# Update code 9 thang 11
import cv2
import os
import threading
import numpy as np
import RPi.GPIO as GPIO
from time import sleep, strftime, time
import time
from datetime import datetime
from Danhgia import save_excel_tem12, save_excel_tem34
from ImageProcessing import folderCreateByDay,save_excel_eval,calculate_angle,choose_theworst_angle2_ver2
# import imutils
import math


class Image():
    def __init__(self):
        self.blocksize_mepvai = 33#13
        self.constract_mepvai = -5#-5
        self.blocksize_tem = 23
        self.constract_tem = -5
        self.list_alpha2 = []

        self.list_point3_x = []
        self.list_point3_y = []
        self.list_point4_x = []
        self.list_point4_y = []
        
        self.OK = 0
        self.step = 0
    def open(self,frame_right,hinhanhphai):
        # print(hinhanhtrai)
        # self.path = '/home/mic14/Dulieuhinhanh2/frameL0.jpg'
        # self.path = '/home/machine005/Dulieuhinhanh2/frameR'+str(hinhanhphai)+'.jpg'
        # self.frame = cv2.imread(self.path)
        self.frame = frame_right

    def find_circle(self,input_img,hinhanhtrai):
        self.copynut = cv2.cvtColor(input_img,cv2.COLOR_GRAY2BGR)
        circles = cv2.HoughCircles(input_img,cv2.HOUGH_GRADIENT,1,300,param1=30,param2=10,minRadius=5,maxRadius=8)
        # list_circle.append(circles)
        # if len(list_circle) == []:
        #     print("Loi hough circle")
        # else:
        if circles is not None:
            # print("Co duong tron")
            circles = np.uint8(np.around(circles))
            # print("Ck",circles)
            for i in circles[0,:]:
                cv2.circle(self.copynut,(i[0],i[1]),i[2],(0,255,0),2)
                x_small = int(i[0])
                y_small = int(i[1])
                R_small = int(i[2])

            big_circles = cv2.HoughCircles(input_img,cv2.HOUGH_GRADIENT,10,300,param1=30,param2=20,minRadius=40,maxRadius=60)
            if big_circles is not None:
                # print("Co duong tron")
                big_circles = np.uint8(np.around(big_circles))
                # print("Ck",circles)
                for i_big in big_circles[0,:]:
                    # cv2.circle(self.copynut,(self.i_big[0],self.i_big[1]),self.i_big[2],(0,255,0),2)
                    cv2.circle(self.copynut,(i_big[0],i_big[1]),5,(0,255,0),2)
                    #Toa do x y la i[0]i[1], radius la i[2]
                    # print("Toa do tam duong tron lon",(i_big[0],i_big[1],i_big[2]))
                    x_big = int(i_big[0])
                    y_big = int(i_big[1])
                    R_big = int(i_big[2])
                    # cv2.line(self.copynut,(x_big,0),(x_big,150),(0,255,0),2)
                    # cv2.line(self.copynut,(0,y_big),(150,y_big),(0,255,0),2)
                    
                    # cv2.imshow("center",self.copynut)

                if x_small < x_big - 5 and y_small < y_big - 5:
                    goc_limit = calculate_angle(x_small,y_small,x_big,y_big)
                    # print("Goc limit 2 bang:", goc_limit)
                    self.Gocpphantu = 1
                    if goc_limit >= 25: #and goc_limit <= 65:
                        print("Goc ly tuong")
                        self.OK = 1
                        self.NG = 0
                        cv2.circle(self.copynut,(x_big,y_big),32,(0,0,0),-1)
                    else:
                        print("Goc ko ly tuong, bao NG loai")
                        self.OK = 0
                        self.NG = 1
                else:
                    self.Gocphantu=234
                    self.OK = 0
                    # print("OK = 0")
                    self.NG = 1
            else:
                print("Ko tim thay duong tron lon")
                self.NG = 1
           
        else:
            print("K thay duong tron nho")
            self.NG = 1

    def bo_duong_doc(self,input_img,hinhanhphai):
        input_img = cv2.cvtColor(input_img,cv2.COLOR_BGR2GRAY)
        kernel_1 = np.ones((1,11), np.uint8)
        mor = cv2.morphologyEx(input_img, cv2.MORPH_OPEN, kernel_1)
        # cv2.imshow("Hello1",self.mor)
        kernel_1 = np.ones((3, 11), np.uint8)
        self.mor = cv2.morphologyEx(mor, cv2.MORPH_CLOSE, kernel_1)
        # cv2.imshow("Morpho right",mor)

    def hough_line_above_small(self,input_img,Gocmepvai):
        self.alpha1 = Gocmepvai
        # print("GOC MEP VAI: ",self.alpha1)
        input_img = cv2.Canny(input_img,  threshold1 = 30,  threshold2 = 100, apertureSize = 3, L2gradient = True)
        # cv2.imshow("Input hough line",input_img)
        self.copysmall = cv2.cvtColor(input_img,cv2.COLOR_GRAY2BGR)


        lines_small = cv2.HoughLinesP(input_img,1,np.pi/180,30,minLineLength=32, maxLineGap=5)
        if lines_small is not None:
            # print("Co hough line")
            for i in range(0,len(lines_small)):
                m = lines_small[i][0]
                m[0] = int(m[0])
                m[1] = int(m[1])
                m[2] = int(m[2])
                m[3] = int(m[3])
                cv2.line(self.copysmall,(m[0], m[1]),(m[2],m[3]),(0,0,255),1,cv2.LINE_AA)
                #self.tuso = (640*(self.l[2]-self.l[0]))
                #self.mauso = math.sqrt((self.l[2]-self.l[0])*(self.l[2]-self.l[0])+(self.l[3]-self.l[1])*(self.l[3]-self.l[1]))*640
                tuso = -(m[3]-m[1])
                mauso = m[2]-m[0]
                alpha2 = math.atan(tuso/mauso)
                if m[2] >= m[0]:
                    self.alpha2 = alpha2*180/3.14
                else:
                    self.alpha2 = 180 - abs(alpha2*180/3.14)
                #Luu cac gia tri alpha 2 vao list
                self.list_alpha2.append(self.alpha2)

            if len(self.list_alpha2) >= 2:
                min_alpha2 = min(self.list_alpha2)
                max_alpha2 = max(self.list_alpha2)
            else:
                min_alpha2 = self.list_alpha2[0]
                max_alpha2 = self.list_alpha2[0]

            return min_alpha2,max_alpha2                      

        else:
            print("Ko co alpha2")
            self.NG = 1
            return None,None



def process_right_1(Gocmepvai,im_crop_2,frame_right,hinhanhphai):
    xulyanh = Image()
    #############TIEN XU LY CAMERA BEN TRAI
    xulyanh.open(frame_right,hinhanhphai)
    
    #Xu ly coi coi tem hay chua
    total_white = cv2.countNonZero(im_crop_2)
    # print("Total white 2: ",total_white)
    if total_white > 3000:
        if Gocmepvai is not None:
            if xulyanh.OK == 0:
                xulyanh.find_circle(im_crop_2,hinhanhphai)
                if xulyanh.OK == 1:
                    # xulyanh.draw_black_circle(xulyanh.copynut,hinhanhphai)
                    xulyanh.bo_duong_doc(xulyanh.copynut,hinhanhphai)
                    min_alpha2,max_alpha2 = xulyanh.hough_line_above_small(xulyanh.mor,Gocmepvai)
                    if xulyanh.NG != 1:
                        angle2,xulyanh.NG = choose_theworst_angle2_ver2(Gocmepvai,min_alpha2,max_alpha2)
                        print("Goc lech tem 2 so voi mep vai: ",angle2)
                    else:
                        angle2 = None
                        xulyanh.NG = 1
                else:
                    print("Ko tim thay duong tron - bao NG")
                    angle2 = None
                    xulyanh.NG = 1

            return angle2,xulyanh.NG
        else:
            return None,1
    else:
        print("Ko du diem trang")
        return None,1


