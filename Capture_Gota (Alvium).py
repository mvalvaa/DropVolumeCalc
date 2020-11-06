#Instituto Português da Qaulidade - IPQ
#NOVA School of Science and Technologies - NOVA FCT

from pymba import Vimba
from pymba import Frame
import cv2
import time
import numpy as np
import os
import tkinter as tk
import tkinter.filedialog

print('Instituto Português da Qualidade - IPQ \nNOVA School of Science and Thecnologies - NOVA FCT')
print('Capture Gota (Alvium)')

## user inputs
user_time_interval = 1
total_images = 1

def choose_directory():
    root = tk.Tk()
    root.withdraw()

    directory = tk.filedialog.askdirectory()
    print(directory)
    os.chdir(directory)
    cwd = os.getcwd()
    print("Current working directory is:", cwd)

##  CAMERA SETUP (features)
def camera_setup():
    with Vimba() as vimba:
        #camera id
        camera_id = vimba.camera_ids()
        #access camera
        camera = vimba.camera(0)
        camera.open()

        #Change camera features
        fps = camera.feature('AcquisitionFrameRate')
        exposure_time = camera.feature('ExposureTime')
        exposure_time.value = 40000
        pixel_format = camera.feature('PixelFormat')
        pixel_format.value = 'Mono8'
        acquisition_mode = camera.feature('AcquisitionMode')
        acquisition_mode.value = 'SingleFrame'

        print('FPS: ', fps.value)
        print('Exposure time: ', exposure_time.value)
        print('Pixel format: ', pixel_format.value)
        print('Acquisition mode: ', acquisition_mode.value)

        camera.close()
        
def camera_view():
    with Vimba() as vimba:
        camera = vimba.camera(0)
        camera.open()

        camera.arm('SingleFrame')
        fps = camera.feature('AcquisitionFrameRate')
        fps = fps.value
        print('FPS = ',fps)

        while(True):
            a = time.time()
            frame = camera.acquire_frame()
            image = frame.buffer_data_numpy()
            image = cv2.resize(image,(1280,720))
            cv2.imshow('Video', image)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        camera.disarm()
        camera.close()
        cv2.destroyAllWindows()

## CAPTURE IMAGES WITH TIME INTERVAL BETWWEN
def camera_capture():
    with Vimba() as vimba:
        camera = vimba.camera(0)
        camera.open()

        camera.arm('SingleFrame')
        fps = camera.feature('AcquisitionFrameRate')
        fps = fps.value
        print('FPS = ',fps)
        time1 = 0
        vector_of_time = []
        while(True):
            
            frame = camera.acquire_frame()
            image = frame.buffer_data_numpy()
            image_resize = cv2.resize(image,(1280,720))            
            i = int(format(frame.data.frameID))
            cv2.imshow('Gota', image_resize)
            #cv2.destroyAllWindows()
            cv2.imwrite('Gota ('+str(i+1)+').jpg',image)
            print("capture "+str(i+1))
            time_interval = time.time() - time1
            print(time_interval)
            vector_of_time.append(time_interval)
            time1 = time.time()
            time.sleep(user_time_interval)
                
            if cv2.waitKey(1) & 0xFF == ord('q') or (i+1)==total_images:
                print('Images saved:' + str(i+1))
                file = open('Time.txt','w')
                for c in range (len(vector_of_time)):
                    b = str(vector_of_time[c])
                    file.write(b+'\n')
                file.close()
                break

        camera.disarm()
        camera.close()
        cv2.destroyAllWindows()    

## CAPTURE SINGLE IMAGE
def background_capture():
    with Vimba() as vimba:
        camera = vimba.camera(0)
        camera.open()

        camera.arm('SingleFrame')
        fps = camera.feature('AcquisitionFrameRate')
            
        frame = camera.acquire_frame()
        background = frame.buffer_data_numpy()
        background_resize = cv2.resize(background,(1280,720))
        cv2.imshow('Background Image', background_resize)
        cv2.waitKey(0)
        
        cv2.imwrite('Background.jpg',background)

        camera.disarm()
        camera.close()
        cv2.destroyAllWindows()    

## MAIN
def main():

    end = False
    setup = False
    
    while not end == True:
        
        input_ = int(input('\nChoose task: \n\n-Camera Setup -> 1\n-Choose Directory -> 2\n-Camera View -> 3\n-Background Capture -> 4\n-Camera Capture -> 5\n-Close -> 0\n\n Input: '))
        if input_ == 1:
            camera_setup()
            setup = True

        if input_ == 2:
            choose_directory()
            
        if input_ == 3:
            camera_view()
                        
        if input_ == 4:
            background_capture()
            
        if input_ == 5:
            camera_capture()
                
        if input_ == 0:               
            end = True
            print('Finish')

## START MAIN 
main()
