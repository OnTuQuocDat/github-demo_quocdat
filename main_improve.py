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
from Left_function_1 import process_left_1
from Left_function_2 import process_left
from Right_function_1 import process_right_1
from Right_function_2 import process_right
from LED_Signal import status
from calib_cam import undistor_cam_left,undistor_cam_right
from Danhgia import save_excel_tem12, save_excel_tem34
from ImageProcessing import *
from template_matching import *
from object_detect import object_detection
left_camera = None
right_camera = None
i = 0
switch_left = 26
switch_right = 19
shutdown_pin = 17
denNG = 22
den_trai = 4
den_phai = 27
#Configure GPIO pin
GPIO.setmode(GPIO.BCM)
#Switch left signal
GPIO.setup(switch_left,GPIO.IN,pull_up_down = GPIO.PUD_UP)
#Switch right signal
GPIO.setup(switch_right,GPIO.IN,pull_up_down = GPIO.PUD_UP)
#Shutdown signal
GPIO.setup(shutdown_pin,GPIO.IN,pull_up_down = GPIO.PUD_UP)

#Den bao NG quen nhan nut
GPIO.setup(denNG,GPIO.OUT,initial = GPIO.LOW)
#Den bao da chup hinh trai
GPIO.setup(den_trai,GPIO.OUT,initial = GPIO.LOW)
#Den bao da chup hinh phai
GPIO.setup(den_phai,GPIO.OUT,initial = GPIO.LOW)

def gstreamer_pipeline(
    sensor_id=0,
    sensor_mode=3,
    capture_width=1920,
    capture_height=1080,
    display_width=1920,
    display_height=1080,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d sensor-mode=%d ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            sensor_mode,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )



class CSI_Camera:

    def __init__ (self) :
        # Initialize instance variables
        # OpenCV video capture element
        self.video_capture = None
        # The last captured image from the camera
        self.frame = None
        self.grabbed = False
        # The thread where the video capture runs
        self.read_thread = None
        self.read_lock = threading.Lock()
        self.running = False


    def open(self, gstreamer_pipeline_string):
        try:
            self.video_capture = cv2.VideoCapture(
                gstreamer_pipeline_string, cv2.CAP_GSTREAMER
            )
            
        except RuntimeError:
            self.video_capture = None
            print("Unable to open camera")
            print("Pipeline: " + gstreamer_pipeline_string)
            return
        # Grab the first frame to start the video capturing
        self.grabbed, self.frame = self.video_capture.read()

    def start(self):
        if self.running:
            print('Video capturing is already running')
            return None
        # create a thread to read the camera image
        if self.video_capture != None:
            self.running=True
            self.read_thread = threading.Thread(target=self.updateCamera)
            self.read_thread.start()
        return self

    def stop(self):
        self.running=False
        self.read_thread.join()

    def updateCamera(self):
        # This is the thread to read images from the camera
        while self.running:
            try:
                grabbed, frame = self.video_capture.read()
                with self.read_lock:
                    self.grabbed=grabbed
                    self.frame=frame
            except RuntimeError:
                print("Could not read image from camera")
        # FIX ME - stop and cleanup thread
        # Something bad happened
        

    def read(self):
        with self.read_lock:
            frame = self.frame.copy()
            grabbed=self.grabbed
        return grabbed, frame

    def release(self):
        if self.video_capture != None:
            self.video_capture.release()
            self.video_capture = None
        # Now kill the thread
        if self.read_thread != None:
            self.read_thread.join()


class Video():
    def __init__(self):
        self.thread = threading.Thread(target=status)
        self.thread.daemon = True
        self.thread.start()
        self.i_left = 0
        self.i_right = 0
        self.filename = str(datetime.now().strftime("%d_%m_%Y_%Hh-%Mp"))
        self.path, self.imagePath,self.reportPath = folderCreateByDay()
    def start_cameras(self):
        # global i
        self.left_camera = CSI_Camera()
        self.left_camera.open(
            gstreamer_pipeline(
                sensor_id=0,#0,
                sensor_mode=1,#3,
                flip_method=0,
                display_height=1080,
                display_width=1920,
            )
        )
        self.left_camera.start()

        self.right_camera = CSI_Camera()
        self.right_camera.open(
            gstreamer_pipeline(
                sensor_id=1,
                sensor_mode=1,#3,
                flip_method=0,
                display_height=1080,
                display_width=1920,
            )
        )
        self.right_camera.start()

        cv2.namedWindow("CSI Cameras", cv2.WINDOW_AUTOSIZE)

        if (
            not self.left_camera.video_capture.isOpened()
            or not self.right_camera.video_capture.isOpened()
        ):
            # Cameras did not open, or no camera attached

            print("Unable to open any cameras")
            # TODO: Proper Cleanup
            SystemExit(0)

class Read_button():
    def __init__(self):
        self.enable = 0
        self.solantao = 0
    def timer_output(self):
        os.system("poweroff")
    def read_shutdown(self):
        self.button_shutdown = GPIO.input(shutdown_pin)
        while True:
            self.button_shutdown = GPIO.input(shutdown_pin)
            # sleep(0.1)
            if self.button_shutdown == False:
                # print("False")
                if self.solantao == 0:
                    self.enable = 1
            else:
                # print("True")
                if self.enable == 2:
                    self.timer.cancel()
                    self.solantao = 0
                self.enable = 0
                    
            if self.enable == 1:
                self.timer = threading.Timer(2,self.timer_output)
                self.timer.start()
                self.solantao = 1
                self.enable = 2
                print("Timer shutdown bat dau dem")        

class Limit_switch():
    def __init__(self):
        self.step = 0
        self.step_function_flag = 0
        #Tin hieu cho main chinh chup hinh
        self.takeshot_left_signal = 0
        self.takeshot_right_signal = 0
        #Tin hieu bao la da nhan nut
        self.danhan_trai = 0
        self.danhan_phai = 0
        self.right_flag = 0
        self.left_flag = 0
        #Time
        self.time_start_left = 0
        self.time_end_left = 0
        self.time_start_right = 0
        self.time_end_right = 0
        self.onetime = 0
    def step_function(self):
        while self.step_function_flag == 1:
            self.left_flag = 1
            self.right_flag = 1
            if self.onetime == 0:
                t_left = threading.Thread(target = self.nutnhan_trai)
                t_left.start()
                t_right = threading.Thread(target = self.nutnhan_phai)
                t_right.start()
                self.onetime = 1               

    def nutnhan_trai(self):
        self.left_switch_signal = GPIO.input(switch_left)
        while self.left_flag == 1:
            while self.left_switch_signal == 1:
                # print("Chua nhan nut chup hinh trai")
                self.left_switch_signal = GPIO.input(switch_left)
                sleep(0.1)
                self.time_start_left = time.time()
            while self.left_switch_signal == 0:
                # print("Dang nhan nut chup hinh trai")
                self.left_switch_signal = GPIO.input(switch_left)
                sleep(0.1)
                self.time_end_left = time.time()
                if self.time_end_left - self.time_start_left > 0.051:
                    break
            if self.time_end_left - self.time_start_left > 0.05:
                self.takeshot_left_signal = 1
                self.time_start_left = 0
                # self.left_flag = 0
                self.danhan_trai = 1
            


    def nutnhan_phai(self):
        self.right_switch_signal = GPIO.input(switch_right)
        while self.right_flag == 1:
            while self.right_switch_signal == 1:
                # print("Chua nhan nut chup hinh phai")
                self.right_switch_signal = GPIO.input(switch_right)
                sleep(0.1)
                self.time_start_right = time.time()
            while self.right_switch_signal == 0:
                # print("Dang nhan nut chup hinh phai")
                self.right_switch_signal = GPIO.input(switch_right)
                sleep(0.1)
                self.time_end_right = time.time()
                if self.time_end_right - self.time_start_right > 0.051:
                    break
            if self.time_end_right - self.time_start_right > 0.05:
                self.takeshot_right_signal = 1
                self.time_start_right = 0
                # self.right_flag = 0
                self.danhan_phai = 1          


########################################MAIN######################################################3
if __name__=='__main__':
    # with open ("/home/mic/backup_ktnut/DulieuExcel/2_Report"+str(datetime.now().strftime("%d%m%Y"))+".csv","a") as log:
    #     log.write("{0},{1},{2},{3},{4},{5},{6},{7},{8}\n".format('Datetime','x_small','y_small','R_small','x_big','y_big','R_big','Gocphantu','Goctem'))    

    #Khoi tao doi tuong video
    vid = Video()
    #Khoi tao doi tuong nut nhan
    nut_nhan = Read_button()

    switch = Limit_switch()

    filename = str(datetime.now().strftime("%d_%m_%Y"))
    path, NGPath,reportPath = folderCreateByDay()

    if os.path.isfile(os.path.join(reportPath + str(datetime.now().strftime("%d%m%Y"))+'.csv')):
        print("Already")
    else:
        with open (reportPath + str(datetime.now().strftime("%d%m%Y"))+'.csv',"a") as log:
            log.write("{0},{1},{2},{3},{4},{5}\n".format('Datetime','LeftRight','Num of press','Num of product','Decision','Note'))   

    if os.path.isfile(os.path.join(reportPath + str('Evaluate'+datetime.now().strftime("%d%m%Y"))+'.csv')):
        print("Already evaluation")
    else:
        with open(reportPath + str('Evaluate'+datetime.now().strftime("%d%m%Y"))+".csv","a") as log:
            log.write("{0},{1},{2},{3},{4},{5},{6},{7}\n".format(strftime("%H:%M:%S"),'alpha1','alpha2','alpha3','alpha4','Decisionleft','Decisionright','Num of product'))   

    vid.start_cameras()
    #Khoi tao thread tat may
    t1 = threading.Thread(target = nut_nhan.read_shutdown)
    t1.start()
    #Khoi tao thread doc step
    switch.step_function_flag = 1
    #Khoi tao thread doc step_function
    # t2 = threading.Thread(target = switch.step_function)
    # t2.start()
    switch.left_flag = 1
    switch.right_flag = 1
    # if switch.onetime == 0:
    t_left = threading.Thread(target = switch.nutnhan_trai)
    t_left.start()
    t_right = threading.Thread(target = switch.nutnhan_phai)
    t_right.start()
        # switch.onetime = 1 

    num_product = 0
    NGsignal1 = None
    NGsignal2 = None
    NGsignal3 = None
    NGsignal4 = None
    numofpress_left = 0
    numofpress_right = 0
    result_fabric = None
    onetime = 0
    count1 = 0
    count2 = 0
    tem1_appear_signal = None
    tem2_appear_signal = None
    tem3_appear_signal = None
    tem4_appear_signal = None

    try:
        while cv2.getWindowProperty("CSI Cameras", 0) >= 0 :
            _ , vid.left_image=vid.left_camera.read()
            _ , vid.right_image=vid.right_camera.read()
            input_img = vid.left_image
            input_img2 = vid.right_image
            #Doc tin hieu mieng vai
            vid.left_image,result_fabric_1 = fabric_signal(input_img)
            vid.right_image,result_fabric_2 = fabric_signal_2(input_img2)

            camera_images = np.hstack((vid.left_image, vid.right_image))
            cv2.imshow("CSI Cameras",cv2.resize(camera_images,(1280,720)))
            keyCode = cv2.waitKey(1)
            # Stop the program on the ESC key
            if keyCode == 27 or keyCode == ord('q'):
                # break
                vid.left_camera.release()
                vid.right_camera.release()
                vid.left_camera.stop()
                vid.right_camera.stop()
                cv2.destroyAllWindows()

            if result_fabric_1 is True and result_fabric_2 is True:
                result_fabric = True
                # print("Con vai")
            elif result_fabric_1 is False and result_fabric_2 is False:
                result_fabric = False
                # print("Da lay vai ra")

            if result_fabric is True:
                if switch.takeshot_left_signal == 1:
                    vid.left_image = undistor_cam_left(vid.left_image)
                    print("Xu ly tem ben trai 1")
                    dateStore = datetime.now().strftime("%d%m%Y_%Hh_%Mp_%Ss")
                    ## Check xem co tem hay ko co tem bang template matching
                    tem1_appear_signal,tem2_appear_signal = template_matching(vid.left_image)
                    ####
                    if tem1_appear_signal == True and tem2_appear_signal == True:
                        Gocmepvai1,im_crop_2,angle1,NGsignal1 = process_left_1(vid.left_image,vid.i_left)
                        numofpress_left += 1
                        onetime = 0
                        if NGsignal1 != 5: #and Gocmepvai is not None:
                            print("Xu ly tem ben phai 1")
                            angle2, NGsignal2 = process_right_1(Gocmepvai1,im_crop_2,vid.left_image,vid.i_left)
                            if NGsignal1 == 1 or NGsignal2 == 1:
                                print("NG left")
                                save_image_NGleft(vid.left_image,vid.i_left,NGPath,dateStore)
                                #
                                LeftRight = 'Left'
                                Numofpress = numofpress_left
                                Numofproduct = num_product
                                Decision = 'NG'
                                Note = ' '
                                save_excel_dev(reportPath,LeftRight,Numofpress,Numofproduct,Decision,Note)
                                #
                                GPIO.output(den_trai,0)
                                GPIO.output(denNG,1)
                                # vid.i_left -= 1
                            elif NGsignal1 == 0 and NGsignal2 == 0:
                                print("OK left")
                                save_image_left(vid.left_image,vid.i_left,path,dateStore)
                                vid.i_left += 1
                                #
                                LeftRight = 'Left'
                                Numofpress = numofpress_left
                                Numofproduct = num_product
                                Decision = 'OK'
                                Note = ' '
                                save_excel_dev(reportPath,LeftRight,Numofpress,Numofproduct,Decision,Note)
                                #
                                numofpress_left = 0
                                GPIO.output(den_trai,1)
                                GPIO.output(denNG,0)
                                # sleep(2)
                                # GPIO.output(den_trai,0)
                            #Evaluate

                            Decisionleft = Decision
                            Decisionright = ' '
                            alpha1 = angle1
                            alpha2 = angle2
                            alpha3 = ' '
                            alpha4 = ' '
                            save_excel_eval(reportPath,alpha1,alpha2,alpha3,alpha4,Decisionleft,Decisionright,Numofproduct)

                        else:
                            print("Khong phat hien dc mep vai trai - Bao NG")
                            GPIO.output(den_trai,0)
                            GPIO.output(denNG,1)
                    else:
                        print("Ko xuat hien day du tem - bao NG")
                        GPIO.output(den_trai,0)
                        GPIO.output(den_phai,0)
                        GPIO.output(denNG,1)


                elif switch.takeshot_right_signal == 1:
                    vid.right_image = undistor_cam_right(vid.right_image)
                    print("Xu ly tem ben trai 2")

                    dateStore = datetime.now().strftime("%d%m%Y_%Hh_%Mp_%Ss")
                    ## Check xem co tem hay ko co tem bang template matching
                    tem3_appear_signal,tem4_appear_signal = template_matching(vid.right_image)
                    ####
                    if tem3_appear_signal == True and tem4_appear_signal == True:                    
                        Gocmepvai2,im_crop_22,angle3,NGsignal3 = process_left(vid.right_image,vid.i_right)
                        numofpress_right += 1
                        onetime = 0
                        count1 = 0
                        count2 = 0
                        if NGsignal3 != 5:
                            print("Xu ly tem ben phai 2")
                            angle4,NGsignal4 = process_right(Gocmepvai2,im_crop_22,vid.right_image,vid.i_right)
                            if NGsignal3 == 1 or NGsignal4 == 1:
                                print("NG right")
                                save_image_NGright(vid.right_image,vid.i_right,NGPath,dateStore)
                                #
                                LeftRight = 'Right'
                                Numofpress = numofpress_right
                                Numofproduct = num_product
                                Decision = 'NG'
                                Note = ' '
                                save_excel_dev(reportPath,LeftRight,Numofpress,Numofproduct,Decision,Note)
                                #
                                GPIO.output(den_phai,0)
                                GPIO.output(denNG,1)
                                ############
                                # vid.i_right -= 1
                            elif NGsignal3 == 0 and NGsignal4 == 0:
                                print("OK right")
                                save_image_right(vid.right_image,vid.i_right,path,dateStore)
                                vid.i_right += 1
                                #
                                LeftRight = 'Right'
                                Numofpress = numofpress_right
                                Numofproduct = num_product
                                Decision = 'OK'
                                Note = ' '
                                save_excel_dev(reportPath,LeftRight,Numofpress,Numofproduct,Decision,Note)
                                #
                                GPIO.output(den_phai,1)
                                GPIO.output(denNG,0)
                                # sleep(2)
                                # GPIO.output(den_phai,0)
                            #Evaluate
                            Decisionleft = ' '
                            Decisionright = Decision
                            alpha1 = ' '
                            alpha2 = ' '
                            alpha3 = angle3
                            alpha4 = angle4
                            save_excel_eval(reportPath,alpha1,alpha2,alpha3,alpha4,Decisionleft,Decisionright,Numofproduct)
                        else:
                            print("Khong phat hien duoc mep vai phai - Bao NG")
                            GPIO.output(den_phai,0)
                            GPIO.output(denNG,1)
                    else:
                        print("Ko xuat hien day du tem - bao NG")
                        GPIO.output(den_trai,0)
                        GPIO.output(den_phai,0)
                        GPIO.output(denNG,1) 
                                               
                tem1_appear_signal = None
                tem2_appear_signal = None
                tem3_appear_signal = None
                tem4_appear_signal = None
                switch.takeshot_right_signal = 0
                switch.takeshot_left_signal = 0
            
            else:
                GPIO.output(den_trai,0)
                GPIO.output(den_phai,0)
                GPIO.output(denNG,0)
                if NGsignal1 == 1 or NGsignal2 == 1 or NGsignal3 == 1 or NGsignal4 == 1:
                    print("Hang NG - chan luu xuat")
                elif NGsignal1 == 0 and NGsignal2 == 0 and NGsignal3 == 0 and NGsignal4 == 0:
                    if count2 == 0:
                        num_product += 1
                        count2 += 1
                    print("All of them are OK")
                    NGsignal1 = None
                    NGsignal2 = None
                    NGsignal3 = None
                    NGsignal4 = None

            #So thanh pham
            # if vid.i_left == vid.i_right:
            #     num_product = vid.i_left
            # else:
            #     num_product = min(vid.i_left,vid.i_right)

            if onetime == 0:
                print("So thanh pham: ",num_product)
                onetime += 1


    except KeyboardInterrupt:
        print("Shut down program")
        vid.left_camera.stop()
        vid.right_camera.stop()
        vid.left_camera.release()
        vid.right_camera.release()        
        GPIO.cleanup()
        cv2.destroyAllWindows()
