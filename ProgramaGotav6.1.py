import cv2
import numpy as np

import os
import tkinter as tk
import tkinter.constants
import tkinter.filedialog


#Choose directory function
def choose_directory():
    window.directory = tk.filedialog.askdirectory()
    label_directory = tk.Label(window, text = window.directory).grid(row=1,column=2)
    os.chdir(window.directory)
    cwd = os.getcwd()
    print("Current working directory is:", cwd) 

#Close window function
def close_window():
    window.destroy()

def main():
    
    ensaios = entry_ensaio.get()
    ensaios = int(ensaios)
    
    img1 = cv2.imread('Background.jpg',0)

    #Select ROI of tube
    ROI = cv2.selectROI(img1)
    img1_Crop = img1[int(ROI[1]):int(ROI[1]+ROI[3]), int(ROI[0]):int(ROI[0]+ROI[2])]
    cv2.destroyAllWindows()

    img1_Crop = cv2.GaussianBlur(img1_Crop,(5,5),0)
    cv2.imwrite(window.directory +'/crop.jpg',img1_Crop)

    ret,threshold = cv2.threshold(img1_Crop, 0, 255, cv2.THRESH_OTSU)
    #threshold = cv2.adaptiveThreshold(img1_Crop,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,5,10)
    #threshold = cv2.adaptiveThreshold(img1_Crop,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,1027,10)
    #ret,threshold = cv2.threshold(img1_Crop,20,255,cv2.THRESH_BINARY)
    #cv2.imshow('',threshold)
    #cv2.waitKey(0)
    cv2.imwrite(window.directory +'/threshold.jpg',threshold)

    dcontours,hierarchy = cv2.findContours(threshold,1,cv2.CHAIN_APPROX_SIMPLE)

    color = cv2.cvtColor(threshold, cv2.COLOR_GRAY2RGB)             
    #contours_draw =cv2.drawContours(color, dcontours, -1, (0,255,0), 1)
    #cv2.imshow('',contours_draw)
    #cv2.waitKey(0)

    diametro_tubo = dcontours[0][0][0][0] - dcontours[(len(dcontours)-1)][2][0][0]
    print('Diametro = ', diametro_tubo, ' px')

    var1 = 0.91188/diametro_tubo  #lado de cada px em mm
    print('Dimensão do pixel',var1, 'mm \n')

    ROI2 = (445, 190, 465, 425)
    img1 = img1[int(ROI2[1]):int(ROI2[1]+ROI2[3]), int(ROI2[0]):int(ROI2[0]+ROI2[2])]

    #Função para aumentar luminusidade/contraste
    def contrast(img):
        alpha = 1                           
        beta = -50                          
        return (cv2.convertScaleAbs(img, alpha=alpha, beta=beta))

    #Função para aplicar Gaussian Blur
    def blur(img):
        img = cv2.GaussianBlur(img,(5,5),0)
        return (img)
    
    img1 = contrast (img1)
    img1 = blur (img1)
    
    vector_of_areas = []            #inicializa vetor para guardar areas
    vector_of_volumes = []          #inicializa vetor para guardar volumes

    for x in range (1,ensaios+1):
        
        a = str(x)
        name = 'Gota ('+a+').jpg'
        img2 = cv2.imread(name,0)
        img2 = img2[int(ROI2[1]):int(ROI2[1]+ROI2[3]), int(ROI2[0]):int(ROI2[0]+ROI2[2])]
        cv2.imshow('',img2)
        cv2.waitKey(0)
        
        #Transforma img2 para o mesmo tamanho que img1
        #img2_Crop = img2[int(ROI[1]):int(ROI[1]+ROI[3]), int(ROI[0]):int(ROI[0]+ROI[2])]
        img2 = contrast (img2)
        img2 = blur (img2)
        
        backless = cv2.subtract(img1,img2)      #Subtrai Background
        cv2.imshow('',backless)
        cv2.waitKey(0)

        #Threshold
        #ret,threshold = cv2.threshold(backless,0,255,cv2.THRESH_OTSU)
        ret,threshold = cv2.threshold(backless,43,255,cv2.THRESH_BINARY)
        cv2.imwrite(window.directory + '/threshold.bmp',threshold)
        cv2.imshow('',threshold)
        cv2.waitKey(0)
        
        #Identifica contornos
        contours,hierarchy = cv2.findContours(threshold,1,cv2.CHAIN_APPROX_NONE)
        
        #Procura a maior área
        largest_area = 0
        for i in range (len(contours)):                                
            contour_area = cv2.contourArea(contours[i])
            if (contour_area > largest_area):
                largest_area = contour_area
                largest_contour = i
            
            #Transforma imagem em RGB
            color = cv2.cvtColor(threshold, cv2.COLOR_GRAY2RGB)             
            contours_draw =cv2.drawContours(color, contours, -1, (0,255,0), 1)
            
            cv2.imwrite(window.directory + '/Contornos/Contorno('+a+').png',contours_draw)
            #Desenha contornos e guarda imagem
            
            #if not cv2.imwrite('C:/Users/migue/OneDrive/Desktop/Hoje/GotaVirtual3/Contorno('+a+').png',contours_draw):
            #	print('\n ATTENTION: Image not saved \n')
     

        #Calcula area da gota
        area = largest_area                 #valor vem em pixeis
        px_area = var1*var1                 #área de um pixel
        px_volume = px_area*var1
        area_mm = (area*px_area)            #transforma em milimetros

        print('Area ',a,': ',area_mm,' mm^2')
        #Guarda area no vetor das areas
        vector_of_areas.append(area_mm)
        
        #Calcula volume da gota
        array_points = contours[largest_contour]
        x_coord = []
        y_coord = []
        for i in range (len(array_points)):
            array_array = array_points[i]
            xy_coord = array_array[0]
            
            x_coord.append(xy_coord[0])
            y_coord.append(xy_coord[1])
            
        x_mean = np.mean(x_coord)
        same_y = 0
        volume_pos=0
        volume_neg=0
        y_previous=None
        
        for i in range (len(x_coord)):
            radius = x_coord[i] - x_mean
            
            if (y_coord[i] != y_previous):
                y_previous = y_coord[i]
                if (radius>0):
                    volume_part_pos = 3.14159*(radius*radius)*1
                    volume_pos = volume_pos + volume_part_pos
        
                if (radius<0):
                    volume_part_neg = 3.14159*(radius*radius)*1
                    volume_neg = volume_neg + volume_part_neg
    
        #print('Volume 1: ',volume_pos*px_volume, 'mm^3 \n')
        #print('Volume 2: ',volume_neg*px_volume, 'mm^3 \n')
    
        volume_average = (volume_pos+volume_neg)/2
        volume_mm = volume_average*px_volume
    
        print('Volume Medio ',a,': ',volume_mm,'mm^3 \n')
        vector_of_volumes.append(volume_mm)

    #Cria ficheiro com valor das áreas
    #file = open('Areas.txt','w')
    #for y in range (1,ensaios+1):
    #    area = str(vector_of_areas[y-1])
    #    file.write(area+'\n')
    #file.close()

    #Cria ficheiro com valor dos volumes
    file = open('Volumes.txt','w')
    for y in range (1,ensaios+1):
        volume = str(vector_of_volumes[y-1])
        file.write(volume+'\n')
    file.close()

    cv2.destroyAllWindows()


#Create Window
window = tk.Tk()
window.title("GOTa")
window.geometry("600x250")

label_1=tk.Label(window, text = "Image processing program to calculate Droplets volume (version 6)").grid(row=0,column=1)

label_directory = tk.Label(window, text = "Choose work directory:").grid(row=1,column=0)
button_directory = tk.Button(window,text="Choose Directory",command = choose_directory).grid(row=1,column=1)

label_entry_ensaio = tk.Label(window, text = "Choose number of trials:").grid(row=2,column=0)
entry_ensaio = tk.Entry(window)
entry_ensaio.grid(row=2,column=1)

label_start = tk.Label(window, text = "Start processing:").grid(row=5,column=0)
button_start = tk.Button(window,text="Start",command = main).grid(row=5,column=1)

button = tk.Button(window, text="Quit", command = close_window).grid(row=7,column=0)

tk.mainloop
