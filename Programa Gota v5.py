from cv2 import *
import numpy as np

ensaios = 9

img1 = cv2.imread('Background.jpg',0)

#Selecionar ROI da gota
ROI = cv2.selectROI(img1)
img1_Crop = img1[int(ROI[1]):int(ROI[1]+ROI[3]), int(ROI[0]):int(ROI[0]+ROI[2])]

#Selecionar diâmetro do tubo para definir escala
scale_percent=500
width = int(img1_Crop.shape[1]*scale_percent/100)
height = int(img1_Crop.shape[0]*scale_percent/100)
dim = (width,height)
img1_resize = cv2.resize(img1_Crop, dim, interpolation = cv2.INTER_AREA)
dim = cv2.selectROI(img1_resize)

print('Diâmetro:  ', dim[2], 'px')
var1 = 0.91188/(dim[2]/(scale_percent/100))  #lado de cada px em mm
print('Dimensão do pixel',var1)

def contrast(img):
    alpha = 1                               #luminusidade
    beta = -50                              #contraste
    return (cv2.convertScaleAbs(img, alpha=alpha, beta=beta))

def blur(img):
    img = cv2.GaussianBlur(img,(5,5),0)     #Aplica Gaussian Blur
    return (img)

img1 = contrast (img1_Crop)
img1 = blur (img1)

vector_of_areas = []            #inicializa vetor para guardar areas

for x in range (1,ensaios+1):

    a = str(x)
    name = 'Gota ('+a+').jpg'
    img2 = cv2.imread(name,0)

    #Transforma img2 para o mesmo tamanho que img1
    img2_Crop = img2[int(ROI[1]):int(ROI[1]+ROI[3]), int(ROI[0]):int(ROI[0]+ROI[2])]
    img2 = contrast (img2_Crop)
    img2 = blur (img2)

    backless = cv2.subtract(img1,img2)      #Subtrai Background

    #Threshold
    ret,threshold = cv2.threshold(backless,127,255,cv2.THRESH_BINARY)
    
    #Identifica contornos
    contours,hierarchy = cv2.findContours(threshold,1,2)

    #Procura a maior área
    largest_area = 0
    for i in range (len(contours)):                                
        contour_area = cv2.contourArea(contours[i])
        if (contour_area > largest_area):
            largest_area = contour_area
            largest_contour = i
            
    #Transforma imagem em RGB
    color = cv2.cvtColor(threshold, cv2.COLOR_GRAY2RGB)             
    contours_draw =cv2.drawContours(color, contours, -1, (0,255,0), 3)
    #Desenha contornos e guarda imagem
    outfile = 'C:/Users/migue/OneDrive/Desktop/Nova pasta/contorno'+a+'.png'
    cv2.imwrite(outfile,contours_draw)

    area = largest_area                 #valor vem em pixeis
    px_area = var1*var1                 #área de um pixel
    px_volume = px_area*var1
    area_mm = (area*px_area)         #transforma em milimetros

    print('Area ',a,': ',area_mm,' mm^2')
    #Guarda area no vetor das areas
    vector_of_areas.append(area_mm)

    array_points = contours[largest_contour]
    x_coord = []
    for i in range (len(array_points)):
        array_array = array_points[i]
        xy_coord = array_array[0]
        
        x_coord.append(xy_coord[0])

    x_mean = np.mean(x_coord)
    volume=0
    for i in range (len(x_coord)):
        radius = x_coord[i] - x_mean
        if (radius>0):
            volume_part = 3.14159*(radius*radius)*1
            volume = volume + volume_part
    
    print('Volume: ',volume*px_volume, 'mm^3 \n')

#Cria ficheiro com valor das áreas
file = open('Areas.txt','w')
for y in range (1,ensaios+1):
    area = str(vector_of_areas[y-1])
    file.write(area+'\n')
file.close()


    
