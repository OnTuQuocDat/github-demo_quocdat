#Code an 's' tren ban phim de luu anh
#Chuan bi data de train
from threading import Thread
import threading
import cv2
import os
# import time
import numpy as np
import math
import RPi.GPIO as GPIO
from time import sleep, strftime, time
import time
from datetime import datetime

maylai_pin = 6
GPIO.setmode(GPIO.BCM)
GPIO.setup(maylai_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#Khai bao GStreamer
gstreamer_pipeline = "nvarguscamerasrc sensor-id=1 sensor-mode=1 ! video/x-raw(memory:NVMM), width=(int)1920, height=(int)1080, format=(string)NV12, framerate=(fraction)30/1 ! nvvidconv flip-method=0 ! video/x-raw, width=(int)1920, height=(int)1080, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink"
capture = cv2.VideoCapture(gstreamer_pipeline,cv2.CAP_GSTREAMER)
sleep(4)
print("Done pipeline")

class Video():
    def __init__(self,capture):
        self.capture = capture
        self.i = 0
    def create_video(self):
        (self.ret_val, self.frame) = self.capture.read()
        cv2.imshow("Show video",self.frame)

        # if cv2.waitKey(1) & 0xFF == ord("q"):
        #     self.capture.release()
        #     cv2.destroyAllWindows()
        #     exit(1)
        # if cv2.waitKey(0) == ord('s'):
        #     print("Chup hinh")

        self.k = cv2.waitKey(1)

        if self.k == 27:
            self.capture.release()
            cv2.destroyAllWindows()
        elif self.k == ord('s'):
            print("Chup hinh")
            cv2.imwrite('/home/mic/Hinhanh/frameb'+str(self.i)+'.jpg',self.frame)
            self.i += 1



    def press_img(self):
        # self.key = GPIO.input(maylai_pin)
        self.key = input()
        if self.key == ord('s'):
            print("Bien dem i:",self.i)
            cv2.imwrite('/home/micx14/Dulieuhinhanh2/frame'+str(self.i)+'.jpg',self.frame)
            self.i += 1

############## MAIN PRORAm #######
if __name__ == '__main__':
    vid = Video(capture)
    # out_led = Hienthi()
    try:
        while True:
            vid.create_video()
            #vid.press_img()
    except KeyboardInterrupt:

        cv2.destroyAllWindows()
