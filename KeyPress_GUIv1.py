#Instituto Português da Qaulidade - IPQ
#NOVA School of Science and Technologies - NOVA FCT

import tkinter as tk
import pyautogui
import time


def key_press():

    delay = int(E1.get())
    n = int(E2.get())
    a = 0
    last_time = 0
    
    while True:
        pyautogui.press("f11")
        y = time.time()
        x = y - last_time
        vector_of_time.append(x)
        last_time = y
        
        a += 1
        
        if a > (n-1):
            
            pyautogui.press("f11")
            file = open('Time.txt','w')
            for c in range (len(vector_of_time)):
                b = str(vector_of_time[c])
                file.write(b+'\n')
            file.close()
            L3 = tk.Label(window, text='Done').grid(row=2,column=1)
            break
        else:
            time.sleep(delay)         
            continue

vector_of_time = []

window = tk.Tk()
window.geometry('300x100+300+300')
window.title('Key Press')

L1 = tk.Label(window, text='Intervalo (s)').grid(row=0)
E1 = tk.Entry(window)
E1.grid(row=0, column = 1)
L2 = tk.Label(window, text='Repetições').grid(row=1)
E2 = tk.Entry(window)
E2.grid(row=1, column = 1) 

tk.Button(window, text='Run',command = key_press).grid(row=3,column=1)

window.mainloop()
