import cv2
from time import sleep, strftime, time
import time
from datetime import datetime
import pandas as pd
import os
import numpy as np
import math
def folderCreateByDay(path='/home/mic/Desktop/report/'):
    if os.path .isdir(path + str(datetime.now().strftime("%d_%m_%Y"))):
        pass
    else:
        print("Ok")
        os.mkdir(path + str(datetime.now().strftime("%d_%m_%Y")))
        os.mkdir(path + str(datetime.now().strftime("%d_%m_%Y")) + '/Image')
        os.mkdir(path + str(datetime.now().strftime("%d_%m_%Y")) + '/Image' + str(datetime.now().strftime("%d%m%Y_%Hh_%Mp")))
        os.mkdir(path + str(datetime.now().strftime("%d_%m_%Y")) + '/NGImage')
        os.mkdir(path + str(datetime.now().strftime("%d_%m_%Y")) + '/Report')
    return str(path + str(datetime.now().strftime("%d_%m_%Y"))) + '/Image' + '/', str(path + str(datetime.now().strftime("%d_%m_%Y"))) + '/NGImage' + '/' , str(path + str(datetime.now().strftime("%d_%m_%Y"))) + '/Report' + '/'

def save_image_left(im,sotem,path,dateStore):
    cv2.imwrite(path + '/ProductL_' + str(sotem) + '_' + str(dateStore) + '.jpg', im)

def save_image_right(im,sotem,path,dateStore):
    cv2.imwrite(path + '/ProductR_' + str(sotem) + '_' + str(dateStore) + '.jpg', im)

def save_image_NGleft(im,sotem,path,dateStore):
    cv2.imwrite(path + '/NGProductL_' + str(sotem) + '_' + str(dateStore) + '.jpg', im)

def save_image_NGright(im,sotem,path,dateStore):
    cv2.imwrite(path + '/NGProductR_' + str(sotem) + '_' + str(dateStore) + '.jpg', im)

def save_excel_dev(reportPath,LeftRight,Numofpress,Numofproduct,Decision,Note):
    with open(reportPath + str(datetime.now().strftime("%d%m%Y"))+".csv","a") as log:
        log.write("{0},{1},{2},{3},{4},{5}\n".format(strftime("%H:%M:%S"),LeftRight,Numofpress,Numofproduct,Decision,Note))

def save_excel_eval(reportPath,alpha1,alpha2,alpha3,alpha4,Decisionleft,Decisionright,Numofproduct):
    with open(reportPath + str('Evaluate'+datetime.now().strftime("%d%m%Y"))+".csv","a") as log:
        log.write("{0},{1},{2},{3},{4},{5},{6},{7}\n".format(strftime("%H:%M:%S"),alpha1,alpha2,alpha3,alpha4,Decisionleft,Decisionright,Numofproduct))   

def fabric_signal(img):
    # cv2.rectangle(img,(500,500),(700,700),(255,0,0),5)
    # img_cut = img[500:700,500:700]
    fabric_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    num_fabric = np.asarray(cv2.mean(fabric_img), dtype = "uint8")
    # print("Num fabric 1: ",num_fabric[1])
    if 20 < num_fabric[1] < 45:
        #Co vai
        result_fabric = True
        # print("Co vai")
    else:
        result_fabric = False
        # print("Ko co vai")
    return img,result_fabric    

def fabric_signal_2(img):
    # cv2.rectangle(img,(500,500),(700,700),(255,0,0),5)
    # img_cut = img[500:700,500:700]
    fabric_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    num_fabric = np.asarray(cv2.mean(fabric_img), dtype = "uint8")
    # print("Num fabric 2: ",num_fabric[1])
    if 20 < num_fabric[1] < 45:
        #Co vai
        result_fabric = True
        # print("Co vai")
    else:
        result_fabric = False
        # print("Ko co vai")
    return img,result_fabric  

def calculate_angle(x_small,y_small,x_big,y_big):
    # pointO = (x_big,y_big)
    # pointA = (0,y_big)
    # pointB = (x_small,y_small)
    OA = (-x_big,0)
    OB = (x_small - x_big,y_small - y_big)
    tuso = abs(OA[0]*OB[0] + OA[1]*OB[1])
    mauso = math.sqrt(pow(OA[0],2)+pow(OA[1],2))*math.sqrt(pow(OB[0],2)+pow(OB[1],2))
    goclimit = math.acos(tuso/mauso)
    goclimit = goclimit*180/3.14
    goclimit = round(goclimit,2)
    return goclimit


def choose_theworst_angle(Gocmepvai_min,Gocmepvai_max,Ax_min,Ay_min,Bx_min,By_min,Ax_max,Ay_max,Bx_max,By_max,Cx_min,Cy_min,Dx_min,Dy_min,Cx_max,Cy_max,Dx_max,Dy_max):
    #Tinh goc hop boi (Amin,Bmin) va (Cmin,Dmin)
    u11 = (Ax_min-Bx_min,Ay_min-By_min)
    u21 = (Cx_min-Dx_min,Cy_min-Dy_min)
    tuso1 = abs(u11[0]*u21[0]+u11[1]*u21[1])
    mauso1 = math.sqrt(pow(u11[0],2)+pow(u11[1],2))*math.sqrt(pow(u21[0],2)+pow(u21[1],2))
    angle_1st = math.acos(tuso1/mauso1)
    angle_1st = round(angle_1st*180/3.14,2)
    #Tinh goc hop boi (Amin,Bmin) va (Cmax,Dmax)
    u12 = (Ax_min-Bx_min,Ay_min-By_min)
    u22 = (Cx_max-Dx_max,Cy_max-Dy_max)
    tuso2 = abs(u12[0]*u22[0]+u12[1]*u22[1])
    mauso2 = math.sqrt(pow(u12[0],2)+pow(u12[1],2))*math.sqrt(pow(u22[0],2)+pow(u22[1],2))
    angle_2nd = math.acos(tuso2/mauso2)
    angle_2nd = round(angle_2nd*180/3.14,2)
    #Tinh goc hop boi (Amax,Bmax) va (Cmin,Dmin)
    u13 = (Ax_max-Bx_max,Ay_max-By_max)
    u23 = (Cx_min-Dx_min,Cy_min-Dy_min)
    tuso3 = abs(u13[0]*u23[0]+u13[1]*u23[1])
    mauso3 = math.sqrt(pow(u13[0],2)+pow(u13[1],2))*math.sqrt(pow(u23[0],2)+pow(u23[1],2))
    angle_3th = math.acos(tuso3/mauso3)
    angle_3th = round(angle_3th*180/3.14,2)
    #Tinh goc hop boi (Amax,Bmax) va (Cmax,Dmax)
    u14 = (Ax_max-Bx_max,Ay_max-By_max)
    u24 = (Cx_max-Dx_max,Cy_max-Dy_max)
    tuso4 = abs(u14[0]*u24[0]+u14[1]*u24[1])
    mauso4 = math.sqrt(pow(u14[0],2)+pow(u14[1],2))*math.sqrt(pow(u24[0],2)+pow(u24[1],2))
    angle_4th = math.acos(tuso4/mauso4)
    angle_4th = round(angle_4th*180/3.14,2)

    #Chon 1 goc lon nhat
    if angle_1st > 90:
        angle_1st = 180 - angle_1st
    elif angle_2nd > 90:
        angle_2nd = 180 - angle_2nd
    elif angle_3th > 90:
        angle_3th = 180 - angle_3th
    elif angle_4th > 90:
        angle_4th = 180 - angle_4th
    max_angle = max(angle_1st,angle_2nd,angle_3th,angle_4th)

    if max_angle == angle_1st or max_angle == angle_2nd:
        Gocmepvai = Gocmepvai_min
        Ax = Ax_min
        Ay = Ay_min
        Bx = Bx_min
        By = By_min
        ###
        if max_angle == angle_1st:
            if Cy_min < Dy_min:
                max_angle = -max_angle
        elif max_angle == angle_2nd:
            if Cy_max < Dy_max:
                max_angle = -max_angle
        ###
    elif max_angle == angle_3th or max_angle == angle_4th:
        Gocmepvai = Gocmepvai_max
        Ax = Ax_max
        Ay = Ay_max
        Bx = Bx_max
        By = By_max
        ###
        if max_angle == angle_3th:
            if Cy_min < Dy_min:
                max_angle = -max_angle
        elif max_angle == angle_4th:
            if Cy_max < Dy_max:
                max_angle = -max_angle        
        ###
    if max_angle > 13 or max_angle < -13:
        NG = 1
    else:
        NG = 0
        
    return max_angle,Gocmepvai,Ax,Ay,Bx,By,NG

def choose_theworst_angle2(Ax,Ay,Bx,By,Cx_min,Cy_min,Dx_min,Dy_min,Cx_max,Cy_max,Dx_max,Dy_max):
    #Tinh goc hop boi (A,B) va (Cmin,Dmin)
    u11 = (Ax-Bx,Ay-By)
    u21 = (Cx_min-Dx_min,Cy_min-Dy_min)
    tuso1 = abs(u11[0]*u21[0]+u11[1]*u21[1])
    mauso1 = math.sqrt(pow(u11[0],2)+pow(u11[1],2))*math.sqrt(pow(u21[0],2)+pow(u21[1],2))
    angle_1st = math.acos(tuso1/mauso1)
    angle_1st = round(angle_1st*180/3.14,2)
    #Tinh goc hop boi (A,B) va (Cmax,Dmax)
    u12 = (Ax-Bx,Ay-By)
    u22 = (Cx_max-Dx_max,Cy_max-Dy_max)
    tuso2 = abs(u12[0]*u22[0]+u12[1]*u22[1])
    mauso2 = math.sqrt(pow(u12[0],2)+pow(u12[1],2))*math.sqrt(pow(u22[0],2)+pow(u22[1],2))
    angle_2nd = math.acos(tuso2/mauso2)
    angle_2nd = round(angle_2nd*180/3.14,2)

    #Chon 1 goc lon nhat
    if angle_1st > 90:
        angle_1st = 180 - angle_1st
    elif angle_2nd > 90:
        angle_2nd = 180 - angle_2nd
    max_angle = max(angle_1st,angle_2nd)

    ###
    if max_angle == angle_1st:
        if Cy_min < Dy_min:
            max_angle = -max_angle
    elif max_angle == angle_2nd:
        if Cy_max < Dy_max:
            max_angle = -max_angle
    ###

    if max_angle > 13 or max_angle < -13:
        NG = 1
    else:
        NG = 0

    return max_angle,NG 

def choose_theworst_angle_ver2(Gocmepvai_min,Gocmepvai_max,min_alpha2,max_alpha2):
    case = None
    # print("Goc vai max: ",Gocmepvai_max)
    # print("Goc vai min: ",Gocmepvai_min)
    # print("Min alpha 2: ",min_alpha2)
    # print("Max alpha 2: ",max_alpha2)
    #Chia thanh 6 truong hop
    #TH1 v-v-t-t
    if Gocmepvai_min >= max_alpha2:
        max_angle = -(Gocmepvai_max - min_alpha2)
        case = 1
    #TH2 v-t-v-t
    elif Gocmepvai_max >= max_alpha2 and max_alpha2 >= Gocmepvai_min and Gocmepvai_min >= min_alpha2:
        max_angle = -(Gocmepvai_max - min_alpha2)
        case = 2
    #TH3 t-v-t-v
    elif max_alpha2 >= Gocmepvai_max and Gocmepvai_max >= min_alpha2 and min_alpha2 >= Gocmepvai_min:
        max_angle = max_alpha2 - Gocmepvai_min
        case = 3
    #TH4 t-t-v-v
    elif min_alpha2 >= Gocmepvai_max:
        max_angle = max_alpha2 - Gocmepvai_min
        case = 4
    #TH5 v-t-t-v
    elif Gocmepvai_max >= max_alpha2 and min_alpha2 >= Gocmepvai_min:
        max_angle_1 = -(Gocmepvai_max - min_alpha2)
        max_angle_2 = max_alpha2 - Gocmepvai_min
        max_angle = max(abs(max_angle_1),abs(max_angle_2))
        if max_angle == max_angle_1:
            case = 5
        else:
            case = 6
    #TH6 t-v-v-t
    elif max_alpha2 >= Gocmepvai_max and Gocmepvai_min >= min_alpha2:
        max_angle_1 = max_alpha2 - Gocmepvai_min
        max_angle_2 = -(Gocmepvai_max - min_alpha2)
        max_angle = max(abs(max_angle_1),abs(max_angle_2))
        if max_angle == abs(max_angle_1):
            max_angle = max_angle_1
            case = 7
        elif max_angle == abs(max_angle_2):
            max_angle = max_angle_2
            case = 8
    #Th7 other
    else:
        print("Other case in function worst 1")
        case = 9
        NG = 1

    #### Bien luan tim ra Goc mep vai
    if case == 1 or case == 2 or case == 5 or case == 8:
        Gocmepvai = Gocmepvai_max
    elif case == 3 or case == 4 or case == 6 or case == 7:
        Gocmepvai = Gocmepvai_min
    else:
        Gocmepvai = None
        NG = 1

    #Ket luan NG hay OK
    if max_angle > 13 or max_angle < -13:
        NG = 1
    else:
        NG = 0

    return round(max_angle,2),Gocmepvai,NG

def choose_theworst_angle2_ver2(Gocmepvai,min_alpha2,max_alpha2):
    case = None
    #TH1: v-t-t
    if Gocmepvai >= max_alpha2:
        max_angle = -(Gocmepvai - min_alpha2)
    #TH2: t-t-v
    elif min_alpha2 >= Gocmepvai:
        max_angle = max_alpha2 - Gocmepvai
    #TH3: t-v-t
    elif max_alpha2 >= Gocmepvai and Gocmepvai >= min_alpha2:
        max_angle_1 = max_alpha2 - Gocmepvai
        max_angle_2 = -(Gocmepvai - min_alpha2)
        max_angle = max(abs(max_angle_1),abs(max_angle_2))
        if max_angle == abs(max_angle_1):
            max_angle = max_angle_1
        elif max_angle == abs(max_angle_2):
            max_angle = max_angle_2
    #TH4 other
    else:
        print("Other case in function worst 2")
        NG = 1
    
    #Ket luan NG hay OK
    if max_angle > 13 or max_angle < -13:
        NG = 1
    else:
        NG = 0
    
    return round(max_angle,2),NG


def interface_user(left_show,right_show,alpha1,alpha2,alpha3,alpha4,numofproduct,user_ok_left,user_ok_right):
    #Put text camera left camera right
    title_above = f"LEFT CAMERA"
    title_below = f"RIGHT CAMERA"
    cv2.putText(left_show,title_above,(750,80),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),2)
    cv2.putText(right_show,title_below,(750,80),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),2)


    #Put text alpha 1,2,3,4 angle after calculating

    alpha1_str = str(alpha1)
    alpha2_str = str(alpha2)
    alpha3_str = str(alpha3)
    alpha4_str = str(alpha4)
    cv2.putText(left_show,alpha1_str,(90,190),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    cv2.putText(left_show,alpha2_str,(1640,190),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    cv2.putText(right_show,alpha3_str,(90,190),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    cv2.putText(right_show,alpha4_str,(1640,240),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)

    #Put text num of product
    numofproduct = str(numofproduct)
    cv2.putText(left_show,numofproduct,(800,200),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),2)
    cv2.putText(right_show,numofproduct,(800,200),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),2)

    # if user_ok_left == 1:
    #     #Ok left
    #     user_left = f"OK"
    #     cv2.putText(left_show,user_left,(850,350),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),2)
    # elif user_ok_left == 0:
    #     #NG left
    #     user_left = f"NG"
    #     cv2.putText(left_show,user_left,(850,350),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),2)
    # elif user_ok_right == 1:
    #     #Ok right
    #     user_right = f"OK"
    #     cv2.putText(right_show,user_right,(850,350),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),2)
    # elif user_ok_right == 0:
    #     #NG right
    #     user_right = f"NG"
    #     cv2.putText(right_show,user_right,(850,350),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),2)

    #Draw rectangle
    # left_show = cv2.rectangle(left_show,(100,200),(300,400),(255,0,0),2)
    left_show = cv2.rectangle(left_show,(108,240),(258,390),(255,0,0),2)
    # right_show = cv2.rectangle(right_show,(100,200),(300,400),(255,0,0),2)
    right_show = cv2.rectangle(right_show,(100,220),(250,370),(255,0,0),2)

    # left_show = cv2.rectangle(left_show,(1650,200),(1850,400),(255,0,0),2)
    left_show = cv2.rectangle(left_show,(1650,200),(1800,350),(255,0,0),2)
    # right_show = cv2.rectangle(right_show,(1650,250),(1850,450),(255,0,0),2)
    right_show = cv2.rectangle(right_show,(1650,280),(1800,430),(255,0,0),2)

    #Ghep camera thanh 2 hang
    return_camera_images = np.vstack((left_show, right_show))
    return return_camera_images
