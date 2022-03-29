# Update 15 thang 5 nam 2021

# Create by: On Tu Quoc Dat - Matsuya R&D Co.Ltd - MIC Department
#
# WARNING ! All changes made in this file will be lost !
from numpy import Infinity
import RPi.GPIO as GPIO
import time
from threading import Thread

from main import NGsignal3

den_status = 6
denNG = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(den_status, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(denNG, GPIO.OUT,initial=GPIO.LOW)

def status():
    while True:
        GPIO.output(den_status,GPIO.HIGH)
        time.sleep(1.5)
        GPIO.output(den_status,GPIO.LOW)
        time.sleep(1.5)

def output_den(flag,NGsignal1,NGsignal2,NGsignal3,NGsignal4):
    while flag == 1:
        while NGsignal1 == 1 or NGsignal2 == 1 or NGsignal1 == 5:
            GPIO.output(denNG,1)
        while NGsignal3 == 1 or NGsignal4 == 1 or NGsignal3 == 5:
            GPIO.output(denNG,1)
        GPIO.output(denNG,0)