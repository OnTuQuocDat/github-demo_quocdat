
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
import math
from ImageProcessing import folderCreateByDay,save_excel_eval,calculate_angle,choose_theworst_angle_ver2


class Image():
    def __init__(self):
        self.blocksize_mepvai = 31#33
        self.constract_mepvai = -3#-5
        self.blocksize_tem = 23
        self.constract_tem = -5
        self.list_alpha1 = []
        self.list_alpha2 = []
        self.list_point1_x = []
        self.list_point1_y = []
        self.list_point2_x = []
        self.list_point2_y = []
        
        self.list_point3_x = []
        self.list_point3_y = []
        self.list_point4_x = []
        self.list_point4_y = []

        self.OK = 0
        self.NG = 2
        self.alpha1 = 0
        self.step = 0
    def open(self,frame_left,hinhanhtrai):
        # self.path = '/home/machine005/Dulieuhinhanh2/frameL'+str(hinhanhtrai)+'.jpg'
        # self.frame = cv2.imread(self.path)
        self.frame = frame_left

    def binary_mepvai(self):
        # print("Binary mep vai")
        im_grayscale = cv2.cvtColor(self.frame,cv2.COLOR_BGR2GRAY)
        #Nguong dong        
        self.kernel = np.ones((3,3),np.uint8)
        self.blur = cv2.GaussianBlur(im_grayscale,(15,15),1)
        blur_mepvai = self.blur[200:350,100:900]
        # cv2.imshow("Blur",blur_mepvai)
        # self.thresh = cv2.Canny(self.blur_mepvai, threshold1 = 10, threshold2 = 50, apertureSize = 3, L2gradient = True)
        thresh = cv2.adaptiveThreshold(blur_mepvai,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,self.blocksize_mepvai,self.constract_mepvai)
        # cv2.imshow("Thresh mep vai",self.thresh)
        erode = cv2.erode(thresh,self.kernel,iterations = 1)
        # cv2.imshow("Erode",self.erode)
        dilate = cv2.dilate(erode,self.kernel,iterations = 1)
        self.dilate = cv2.medianBlur(dilate,5)
        # cv2.imshow("Dilate",self.dilate)

    def cut_circle_nut(self):
        blur_tem = self.blur[380:680,20:1900]
        w = 150
        h = 150
        y1 = 40
        x1 = 0
        y2 = 100
        x2 = 1720
        im_crop_1 = blur_tem[y1:(y1+h),x1:(x1+w)]
        # cv2.imshow("Cut circle trai",self.im_crop_1)
        im_crop_1 = cv2.adaptiveThreshold(im_crop_1,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,self.blocksize_tem,self.constract_tem)      
        im_crop_1 = cv2.erode(im_crop_1,self.kernel,iterations = 1)
        im_crop_1 = cv2.dilate(im_crop_1,self.kernel,iterations = 1)
        self.im_crop_1 = cv2.medianBlur(im_crop_1,5)

        im_crop_2 = blur_tem[y2:(y2+h),x2:(x2+w)]
        # cv2.imshow("Cut circle phai",self.im_crop_2)
        im_crop_2 = cv2.adaptiveThreshold(im_crop_2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,self.blocksize_tem,self.constract_tem)      
        im_crop_2 = cv2.erode(im_crop_2,self.kernel,iterations = 1)
        im_crop_2 = cv2.dilate(im_crop_2,self.kernel,iterations = 1)
        self.im_crop_2 = cv2.medianBlur(im_crop_2,5)
        return self.im_crop_2

    def binary_tem(self):
        # self.blur_tem = self.blur[400:600,100:1800]
        blur_tem = self.blur[380:680,20:1900]
        # cv2.imshow("Blur tem",self.blur_tem)
        thresh_tem = cv2.adaptiveThreshold(blur_tem,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,self.blocksize_tem,self.constract_tem)
        erode_tem = cv2.erode(thresh_tem,self.kernel,iterations = 1)
        # cv2.imshow("Erode tem",self.erode_tem)
        self.dilate_tem = cv2.dilate(erode_tem,self.kernel,iterations = 1)
        self.dilate_tem = cv2.medianBlur(self.dilate_tem,5)
        # cv2.imshow("Dilate tem",self.dilate_tem)

    def hough_line_above_left(self,thresh_img):
        tong = 0
        self.copyleft = cv2.cvtColor(thresh_img,cv2.COLOR_GRAY2BGR)
        lines_left = cv2.HoughLinesP(thresh_img,1,np.pi/180,100,None,80,15) #150-80-20

        if lines_left is not None:
            for i in range(0,len(lines_left)):
                l = lines_left[i][0]
                l[0] = int(l[0])
                l[1] = int(l[1])
                l[2] = int(l[2])
                l[3] = int(l[3])
                cv2.line(self.copyleft,(l[0], l[1]),(l[2],l[3]),(0,0,255),1,cv2.LINE_AA)
                # print("Diem dau: ",(self.l[0],self.l[1]))
                # print("Diem cuoi: ",(self.l[2],self.l[3]))

                tuso = -(l[3]-l[1])
                mauso = l[2]-l[0]
                alpha1 = math.atan(tuso/mauso)
                if l[2] >= l[0]:
                    self.alpha1 = alpha1*180/3.14
                else:
                    self.alpha1 = 180 - abs(alpha1*180/3.14)
                #Luu cac gia tri alpha1 vao list_alpha1
                self.list_alpha1.append(self.alpha1)

            if len(self.list_alpha1) >= 2:
                min_alpha1 = min(self.list_alpha1)
                max_alpha1 = max(self.list_alpha1)
            else:
                min_alpha1 = self.list_alpha1[0]
                max_alpha1 = self.list_alpha1[0]

            return min_alpha1,max_alpha1
       
        else:
            print("Khong co alpha1")
            self.NG = 1
            return None,None              
    
    def find_circle(self,input_img,hinhanhtrai):
        self.copynut = cv2.cvtColor(input_img,cv2.COLOR_GRAY2BGR)
        circles = cv2.HoughCircles(input_img,cv2.HOUGH_GRADIENT,1,300,param1=30,param2=10,minRadius=5,maxRadius=8)

        if circles is not None:
            # print("Co duong tron")
            circles = np.uint8(np.around(circles))
            # print("Ck",circles)
            for i in circles[0,:]:
                cv2.circle(self.copynut,(i[0],i[1]),i[2],(0,255,0),2)
                self.x_small = int(i[0])
                self.y_small = int(i[1])
                self.R_small = int(i[2])

            # input_img = cv2.cvtColor(input_img,cv2.COLOR_BGR2GRAY)
            big_circles = cv2.HoughCircles(input_img,cv2.HOUGH_GRADIENT,10,300,param1=30,param2=20,minRadius=40,maxRadius=60)
            if big_circles is not None:
                # print("Co duong tron")
                big_circles = np.uint8(np.around(big_circles))
                # print("Ck",circles)
                for i_big in big_circles[0,:]:
                    # cv2.circle(self.copynut,(self.i_big[0],self.i_big[1]),self.i_big[2],(0,255,0),2)
                    cv2.circle(self.copynut,(i_big[0],i_big[1]),5,(0,0,255),2)
                    #Toa do x y la i[0]i[1], radius la i[2]
                    # print("Toa do tam duong tron lon",(i_big[0],i_big[1],i_big[2]))
                    self.x_big = int(i_big[0])
                    self.y_big = int(i_big[1])
                    self.R_big = int(i_big[2])
                    # cv2.line(self.copynut,(x_big,0),(x_big,150),(0,255,0),2)
                    # cv2.line(self.copynut,(0,y_big),(150,y_big),(0,255,0),2)
                    
                    # cv2.imshow("center",self.copynut)

                if self.x_small < self.x_big - 5 and self.y_small < self.y_big - 5:
                    goc_limit = calculate_angle(self.x_small,self.y_small,self.x_big,self.y_big)
                    # print("Goc limit 3 bang:", goc_limit)
                    self.Gocphantu = 1
                    if goc_limit >= 25: #and goc_limit <= 65:
                        self.OK = 1
                        self.NG = 0
                        cv2.circle(self.copynut,(self.x_big,self.y_big),32,(0,0,0),-1)
                    else:
                        print("Goc ko ly tuong, bao NG loai")
                        self.OK = 0
                        self.NG = 1               
                else:
                    self.Gocphantu=234
                    self.OK = 0
                    self.NG = 1
                    # print("OK = 0")
            else:
                print("Ko tim thay duong tron lon")
                self.NG = 1
            
        else:
            print("K thay duong tron nho")
            self.NG = 1
        # print("Done find circle")

       
    def bo_duong_doc(self,input_img,hinhanhtrai):
        #Cap he so tuong doi on
        #OPEN (1,11)
        #CLOSE (3,11)
        input_img = cv2.cvtColor(input_img,cv2.COLOR_BGR2GRAY)
        # cv2.imshow("Hell1",input_img)
        kernel_1 = np.ones((1,11), np.uint8)
        mor = cv2.morphologyEx(input_img, cv2.MORPH_OPEN, kernel_1)
        # cv2.imshow("Hello1",mor)
        kernel_1 = np.ones((3,11), np.uint8)
        self.mor = cv2.morphologyEx(mor, cv2.MORPH_CLOSE, kernel_1)
        # cv2.circle(self.mor,(self.i_big[0],self.i_big[1]),55,(0,0,0),6)
        # cv2.imshow("Morpho left",self.mor)
        # print("Done bo duong doc")
        
    def hough_line_above_small(self,input_img):
        # input_img = cv2.cvtColor(input_img,cv2.COLOR_BGR2GRAY)
        kernel = np.ones((3,3),np.uint8)
        input_img = cv2.Canny(input_img,  threshold1 = 30,  threshold2 = 100, apertureSize = 3, L2gradient = True)
        # cv2.imshow("Input hough line",input_img)
        self.copysmall = cv2.cvtColor(input_img,cv2.COLOR_GRAY2BGR)


        lines_small = cv2.HoughLinesP(input_img,1,np.pi/180,30,minLineLength=32, maxLineGap=5)
        # lines_small = cv2.HoughLinesP(input_img,1,np.pi/180,45,None,60,5)  ##Thong so ban dau 35
        # print(self.lines_small)
        if lines_small is not None:
            # print("Co hough line")
            # GPIO.output(22,0)
            for i in range(0,len(lines_small)):
                m = lines_small[i][0]
                m[0] = int(m[0])
                m[1] = int(m[1])
                m[2] = int(m[2])
                m[3] = int(m[3])
                cv2.line(self.copysmall,(m[0], m[1]),(m[2],m[3]),(0,0,255),1,cv2.LINE_AA)

                tuso = -(m[3]-m[1])
                mauso = m[2]-m[0]
                alpha2 = math.atan(tuso/mauso)
                #Chon diem lam goc la diem co x nho hon
                if m[2] >= m[0]:
                    self.alpha2 = alpha2*180/3.14
                else:
                    self.alpha2 = 180 - abs(alpha2*180/3.14)
                #Luu cac gia tri alpha 2 vao list
                self.list_alpha2.append(self.alpha2)

            #Luu cac goc alpha2 min max
            if len(self.list_alpha2) >= 2:
                min_alpha2 = min(self.list_alpha2)
                max_alpha2 = max(self.list_alpha2)
            else:
                min_alpha2 = self.list_alpha2[0]
                max_alpha2 = self.list_alpha2[0]

            return min_alpha2,max_alpha2

        else:
            print("alpha2 none, bao NG")
            self.NG = 1
            return None,None


def process_left(frame_left,hinhanhtrai):
    xulyanh = Image()
    #############TIEN XU LY CAMERA BEN TRAI
    xulyanh.open(frame_left,hinhanhtrai)
    #Nhi phan
    xulyanh.binary_mepvai()
    # xulyanh.binary_tem()
    #Cat tem
    im_crop_2 = xulyanh.cut_circle_nut()

    #Xu ly coi coi tem hay chua
    total_white = cv2.countNonZero(xulyanh.im_crop_1)
    # print("Total white 3: ",total_white)
    if total_white > 3000:
        #####Xu ly mep vai
        Gocmepvai_min,Gocmepvai_max = xulyanh.hough_line_above_left(xulyanh.dilate)
        
        if xulyanh.alpha1 is not None:
            if xulyanh.OK == 0:
                xulyanh.find_circle(xulyanh.im_crop_1,hinhanhtrai)
                if xulyanh.OK == 1:
                    xulyanh.bo_duong_doc(xulyanh.copynut,hinhanhtrai)
                    min_alpha2,max_alpha2 = xulyanh.hough_line_above_small(xulyanh.mor)
                    if xulyanh.NG != 1:
                        angle3,Gocmepvai,xulyanh.NG = choose_theworst_angle_ver2(Gocmepvai_min,Gocmepvai_max,min_alpha2,max_alpha2)
                        print("Goc lech tem 3 so voi mep vai: ",angle3)
                    else:
                        Gocmepvai = None
                        im_crop_2 = None
                        xulyanh.NG = 1
                        angle3 = None
                else:
                    print("Khong thoa dieu kien duong tron - Bao NG")
                    angle3 = None
                    Gocmepvai = None
                    im_crop_2 = None
                    xulyanh.NG = 1


            return Gocmepvai,im_crop_2,angle3,xulyanh.NG
        else:
            xulyanh.NG = 5
            print("Bao NG")
            return None,0,None,xulyanh.NG
    else:
        xulyanh.NG = 1
        print("Ko du diem trang - bao NG")
        return None,0,None,xulyanh.NG        

