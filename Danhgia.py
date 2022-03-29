import cv2
from time import sleep, strftime, time
import time
from datetime import datetime

def save_excel_tem12(x_small,y_small,R_small,x_big,y_big,R_big,Gocphantu,Goctem):
    with open("/home/mic/backup_ktnut/DulieuExcel/1_Report"+str(datetime.now().strftime("%d%m%Y"))+".csv","a") as log:
        log.write("{0},{1},{2},{3},{4},{5},{6},{7},{8}\n".format(strftime("%H:%M:%S"),x_small,y_small,R_small,x_big,y_big,R_big,Gocphantu,Goctem))


def save_excel_tem34(x_small,y_small,R_small,x_big,y_big,R_big,Gocphantu,Goctem):
    with open("/home/mic/backup_ktnut/DulieuExcel/2_Report"+str(datetime.now().strftime("%d%m%Y"))+".csv","a") as log:
        log.write("{0},{1},{2},{3},{4},{5},{6},{7},{8}\n".format(strftime("%H:%M:%S"),x_small,y_small,R_small,x_big,y_big,R_big,Gocphantu,Goctem))

# def save_excel_dev(LeftRight,Numofpress,Numofproduct,Decision,Note):
#     with open("/home/mic/backup_ktnut/DulieuExcel/Report"+str(datetime.now().strftime("%d%m%Y"))+".csv","a") as log:
#         log.write("{0},{1},{2},{3},{4},{5}\n".format(strftime("%H:%M:%S"),LeftRight,Numofpress,Numofproduct,Decision,Note))