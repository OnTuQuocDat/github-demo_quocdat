#Create by: On Tu Quoc Dat - Matsuya R&D Co.Ltd - MIC Department
#Pokayoke 
# Update code 28 thang 6
import cv2
import os
import threading
import numpy as np
import RPi.GPIO as GPIO
from time import sleep, strftime, time
import time
from datetime import datetime
from Danhgia import save_excel_tem12, save_excel_tem34
# from Excel import save_excel
# from testminhmap import deskew
# import imutils
import math




class Image():
    def __init__(self):
        self.blocksize_mepvai = 37#13
        self.constract_mepvai = -5#-5
        self.blocksize_tem = 23
        self.constract_tem = -5
        self.list_alpha1 = []
        self.list_alpha2 = []
        self.list_alpha3 = []
        self.OK = 0
        self.NG = 2
        # self.alpha1 = 0
        self.step = 0
    def open(self,frame_left,hinhanhtrai):
        # print(hinhanhtrai)
        # self.path = '/home/mic14/Dulieuhinhanh2/frameL0.jpg'
        # self.path = '/home/machine005/Dulieuhinhanh2/frameL'+str(hinhanhtrai)+'.jpg'
        # self.frame = cv2.imread(self.path)
        self.frame = frame_left

    def binary_mepvai(self):
        # print("Binary mep vai")
        im_grayscale = cv2.cvtColor(self.frame,cv2.COLOR_BGR2GRAY)
        #Nguong dong        
        self.kernel = np.ones((3,3),np.uint8)
        # self.blur = cv2.medianBlur(im_grayscale,5)
        # self.blur = cv2.bilateralFilter(im_grayscale,35,5,5) #15 75 75; #15 35 35 tuong doi on;
        self.blur = cv2.GaussianBlur(im_grayscale,(5,5),1)
        blur_mepvai = self.blur[200:360,100:900]
        # cv2.imshow("Blur",blur_mepvai)
        # self.thresh = cv2.Canny(self.blur_mepvai, threshold1 = 10, threshold2 = 50, apertureSize = 3, L2gradient = True)
        thresh = cv2.adaptiveThreshold(blur_mepvai,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,self.blocksize_mepvai,self.constract_mepvai)
        # cv2.imshow("Thresh mep vai",self.thresh)
        erode = cv2.erode(thresh,self.kernel,iterations = 1)
        # cv2.imshow("Erode",self.erode)
        self.dilate = cv2.dilate(erode,self.kernel,iterations = 1)
        self.dilate = cv2.medianBlur(self.dilate,5)
        # cv2.imshow("Dilate",self.dilate)

    # def cut_circle_nut(self):
    #     blur_tem = self.blur[360:680,50:1900]
    #     w = 150
    #     h = 150
    #     y1 = 80
    #     x1 = 8
    #     y2 = 40
    #     x2 = 1700
    #     self.im_crop_1 = blur_tem[y1:(y1+h),x1:(x1+w)]
    #     # cv2.imshow("Cut circle trai",self.im_crop_1)      
    #     self.im_crop_2 = blur_tem[y2:(y2+h),x2:(x2+w)]
    #     # cv2.imshow("Cut circle phai",self.im_crop_2)

    #     return self.im_crop_2  

    def binary_tem(self):
        # self.blur_tem = self.blur[400:600,100:1800]
        blur_tem = self.blur[360:680,50:1900]
        # cv2.imshow("Blur tem",self.blur_tem)
        thresh_tem = cv2.adaptiveThreshold(blur_tem,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,self.blocksize_tem,self.constract_tem)
        erode_tem = cv2.erode(thresh_tem,self.kernel,iterations = 1)
        # cv2.imshow("Erode tem",self.erode_tem)
        self.dilate_tem = cv2.dilate(erode_tem,self.kernel,iterations = 1)
        self.dilate_tem = cv2.medianBlur(self.dilate_tem,5)
        # cv2.imshow("Dilate tem",self.dilate_tem)
        
    def cut_circle_nut(self):
        #Cat khung chua nut tron 1280
        # self.im_crop_1 = self.thresh[100:200,50:180]
        #1920
        w = 150
        h = 150
        y1 = 80
        x1 = 8
        y2 = 40
        x2 = 1700
        self.im_crop_1 = self.dilate_tem[y1:(y1+h),x1:(x1+w)]
        # cv2.imshow("Cut circle trai",self.im_crop_1)      
        self.im_crop_2 = self.dilate_tem[y2:(y2+h),x2:(x2+w)]
        # cv2.imshow("Cut circle phai",self.im_crop_2)
        return self.im_crop_2

    def hough_line_above_left(self,thresh_img,hinhanhtrai):
        tong = 0
        self.copyleft = cv2.cvtColor(thresh_img,cv2.COLOR_GRAY2BGR)
        lines_left = cv2.HoughLinesP(thresh_img,1,np.pi/180,120,None,80,20) ##SUA LAI 50-50-10
        # print(self.lines_left)
        if lines_left is not None:
            for i in range(0,len(lines_left)):
                l = lines_left[i][0]
                cv2.line(self.copyleft,(l[0], l[1]),(l[2],l[3]),(0,0,255),1,cv2.LINE_AA)
                # print("Diem dau: ",(self.l[0],self.l[1]))
                # print("Diem cuoi: ",(self.l[2],self.l[3]))
                #Tinh goc mep vai
                # self.tuso = abs(640*(self.l[2]-self.l[0]))
                # self.mauso = math.sqrt((self.l[2]-self.l[0])*(self.l[2]-self.l[0])+(self.l[3]-self.l[1])*(self.l[3]-self.l[1]))*640
                tuso = l[2]-l[0]
                mauso = math.sqrt(pow(l[2]-l[0],2)+pow(l[3]-l[1],2))
                self.alpha1 = math.acos(tuso/mauso)
                self.alpha1 = self.alpha1*180/3.14
                if l[1] > l[3]:
                    #Goc se thanh goc tu
                    self.alpha1 = 180 - self.alpha1
                #Luu cac gia tri alpha1 vao list_alpha1
                self.list_alpha1.append(self.alpha1)
                

            # if len(self.list_alpha1) == 2:
            #     self.alpha1 = 0.5*(self.list_alpha1[0]+self.list_alpha1[1])
            #     print("Do dai list = 2")
            # else:

            #Tinh trung binh
            # for i in range(0,len(self.list_alpha1)-1):
            #     tong += self.list_alpha1[i]
            #     # print(tong)
            # self.alpha1 = tong/len(self.list_alpha1)

            # print("Goc lech mep vai trai: ",round(min(self.list_alpha1),2))
        else:
            print("Khong co alpha1")
            return 0
        # cv2.imshow("Result left",self.copyleft)
        cv2.imwrite('/home/machine005/Dulieuxuly/Mepvaitrai'+str(hinhanhtrai)+'.jpg',self.copyleft)
        # print("Done goc")
        if self.alpha1 is not None:
            return round(min(self.list_alpha1),2)
    
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
            # print("Toa do tam duong tron: ",(i[0],i[1]))

            # cv2.imshow("left circle",self.copynut)

        # input_img = cv2.cvtColor(input_img,cv2.COLOR_BGR2GRAY)
        big_circles = cv2.HoughCircles(input_img,cv2.HOUGH_GRADIENT,1,300,param1=30,param2=20,minRadius=40,maxRadius=60)
        if big_circles is not None:
            # print("Co duong tron")
            big_circles = np.uint8(np.around(big_circles))
            # print("Ck",circles)
            for self.i_big in big_circles[0,:]:
                # cv2.circle(self.copynut,(self.i_big[0],self.i_big[1]),self.i_big[2],(0,255,0),2)
                cv2.circle(self.copynut,(self.i_big[0],self.i_big[1]),5,(0,0,255),2)
                #Toa do x y la i[0]i[1], radius la i[2]
                # print("Toa do tam duong tron lon",(i_big[0],i_big[1],i_big[2]))
                self.x_big = int(self.i_big[0])
                self.y_big = int(self.i_big[1])
                self.R_big = int(self.i_big[2])
                # cv2.line(self.copynut,(x_big,0),(x_big,150),(0,255,0),2)
                # cv2.line(self.copynut,(0,y_big),(150,y_big),(0,255,0),2)
                
                # cv2.imshow("center",self.copynut)

            if self.x_small < self.x_big and self.y_small < self.y_big:
                self.Gocphantu = 1
                # print("OK = 1")
                self.OK = 1
                self.NG = 0
                cv2.circle(self.copynut,(self.x_big,self.y_big),32,(0,0,0),-1)
                # cv2.imshow("Mask circle",self.copynut)
                
            else:
                self.Gocphantu=234
                self.OK = 0
                self.NG = 1
                # print("OK = 0")

            
        else:
            print("K thay duong tron")
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
        
    def hough_line_above_small(self,input_img,hinhanhtrai):
        # input_img = cv2.cvtColor(input_img,cv2.COLOR_BGR2GRAY)
        kernel = np.ones((3,3),np.uint8)
        # input_img = cv2.erode(input_img,kernel,iterations = 1)
        # input_img = cv2.ximgproc.thinning(input_img, cv2.ximgproc.THINNING_ZHANGSUEN)
        input_img = cv2.Canny(input_img,  threshold1 = 30,  threshold2 = 100, apertureSize = 3, L2gradient = True)
        # cv2.imshow("Input hough line",input_img)
        self.copysmall = cv2.cvtColor(input_img,cv2.COLOR_GRAY2BGR)

        if len(input_img.shape) == 3:
            h, w, _ = input_img.shape
        elif len(input_img.shape) == 2:
            h, w = input_img.shape


        lines_small = cv2.HoughLinesP(input_img,1,np.pi/180,25,minLineLength=37, maxLineGap=5)
        # lines_small = cv2.HoughLinesP(input_img,1,np.pi/180,45,None,60,5)  ##Thong so ban dau 35
        # print(self.lines_small)
        if lines_small is not None:
            # print("Co hough line")
            GPIO.output(22,0)
            for i in range(0,len(lines_small)):
                m = lines_small[i][0]
                cv2.line(self.copysmall,(m[0], m[1]),(m[2],m[3]),(0,0,255),1,cv2.LINE_AA)
                #self.tuso = (640*(self.l[2]-self.l[0]))
                #self.mauso = math.sqrt((self.l[2]-self.l[0])*(self.l[2]-self.l[0])+(self.l[3]-self.l[1])*(self.l[3]-self.l[1]))*640
                tuso = m[2]-m[0]
                mauso = math.sqrt(pow(m[2]-m[0],2)+pow(m[3]-m[1],2))
                self.alpha2 = math.acos(tuso/mauso)
                self.alpha2 = self.alpha2*180/3.14
                #Luu cac gia tri alpha 2 vao list
                self.list_alpha2.append(self.alpha2)
            # print(self.list_alpha2)
                                
            if len(self.list_alpha2) == 2:
                self.alpha2 = 0.5*(self.list_alpha2[0]+self.list_alpha2[1])
                # print("List 2 co do dai la 2")
            else:
                self.alpha2 = max(self.list_alpha2)
            if m[1] > m[3]:
                self.alpha2 = 180 - self.alpha2
            # print("Goc lech tem 1 so voi phuong ngang: ",round(self.alpha2,2))
            #MEP VAI XEO LEN
            if self.alpha2 < 90 and self.alpha1 > 90:
                Goclech1 = 180-self.alpha1+self.alpha2
                # print("CASE 1")
            elif self.alpha1 > 90 and self.alpha2 > 90:
                if self.alpha1 >= self.alpha2:
                    Goclech1 = self.alpha1-self.alpha2
                    Goclech1 = -Goclech1
                    # print("CASE 2")
                else:
                    Goclech1 = self.alpha2-self.alpha1
                    Goclech1 = -Goclech1
                    # print("CASE 3")
            #MEP VAI XEO XUONG
            if self.alpha1 < 90 and self.alpha2 > 90:
                Goclech1 = 180 + self.alpha1 - self.alpha2
                Goclech1 = -Goclech1
                # print("CASE 4")
            elif self.alpha1 < 90 and self.alpha2 < 90:
                if self.alpha1 > self.alpha2:
                    Goclech1 = self.alpha1 - self.alpha2
                    # print("CASE 5")
                else:
                    Goclech1 = self.alpha2 - self.alpha1
                    # print("CASE 6")

            Goctem = round(Goclech1,2)
            print("Goc lech tem 1 so voi mep vai: ",Goctem)
            ###Alarm signal
            if Goctem> 15 or Goctem < -15:
                self.NG = 1
                # GPIO.output(22,1)
                # GPIO.output(4,0)
            else:
                self.NG = 0
                # GPIO.output(22,0)
                # GPIO.output(4,1)
            ###Save excel
            save_excel_tem12(self.x_small,self.y_small,self.R_small,self.x_big,self.y_big,self.R_big,self.Gocphantu,Goctem)

        else:
            print("alpha2 none, bao NG")
            self.NG = 1
            # GPIO.output(22,1)
            # GPIO.output(4,0)
        # print("co bao nhiu hough line: ",self.i)
            # print("Goc lech tem nho trai: ",self.pre_alpha2)
        cv2.imshow("Left 1",self.copysmall)
        # cv2.imwrite('/home/machine005/Dulieuxuly/Tem1'+str(hinhanhtrai)+'.jpg',self.copysmall)
        # print("Done hough")
        return 0  



def process_left_1(frame_left,hinhanhtrai):
    denNG = 22
    den_trai = 4
    #Configure GPIO pin
    GPIO.setmode(GPIO.BCM)
    #Den bao NG quen nhan nut
    GPIO.setup(denNG,GPIO.OUT,initial = GPIO.LOW)
    #Den bao da chup hinh trai
    GPIO.setup(den_trai,GPIO.OUT,initial = GPIO.LOW)

    # start_time = time.time()
    xulyanh = Image()
    #############TIEN XU LY CAMERA BEN TRAI
    xulyanh.open(frame_left,hinhanhtrai)
    #Nhi phan
    xulyanh.binary_mepvai()
    xulyanh.binary_tem()
    #Cat tem
    im_crop_2 = xulyanh.cut_circle_nut()


    #####Xu ly mep vai
    Gocmepvai = xulyanh.hough_line_above_left(xulyanh.dilate,hinhanhtrai)
    # Gocmepvai = 0
    # print("Goc mep vai: ",Gocmepvai)
    #####Xu ly xong mep vai
    # if xulyanh.alpha1:
    if xulyanh.OK == 0:
        xulyanh.find_circle(xulyanh.im_crop_1,hinhanhtrai)
        if xulyanh.OK == 1:
        #     xulyanh.draw_black_circle(xulyanh.copynut,hinhanhtrai)
            xulyanh.bo_duong_doc(xulyanh.copynut,hinhanhtrai)
            xulyanh.hough_line_above_small(xulyanh.mor,hinhanhtrai)
    # print("Thoi gian xu ly tem 1: ",time.time()-start_time)

    return Gocmepvai,im_crop_2,xulyanh.NG

