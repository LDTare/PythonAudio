#Importaciones para UI
from ctypes import alignment
from sqlite3 import Row
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as Messagebox
from turtle import left, position

#Importaciones de clases para funciones
import numpy as np
import sounddevice as sd
import soundfile as sf
import subprocess #Libreria para convertir los archivos MP3 a WAV

root = Tk()

#Seccion de funciones

Ruta = ""

root.title("Teoria de sistemas")

def SeleccionArchivos(): #Funcion para seleccionar archivos
    global filename
    #Filtro para seleccionar unicamente archivos MP3, WAV y OGG
    filename = filedialog.askopenfilename(initialdir="D:/", title="Selecciona un archivo de audio", filetypes=(("Archivos MP3", "*.MP3"), ("Archivos WAV", "*.WAV"),("Archivos OGG", "*.OGG")))
    global Ruta
    #Almacenamiento de la ruta en una variable
    Ruta = filename
    Messagebox.showinfo('Seleccion de Archivos', 'Archivo seleccionado: ' + Ruta)

def PlayArchivo(): #Reproducir el archivo
    subprocess.call(['ffmpeg', '-y' , '-i', Ruta, 'test.wav']) #Conversion a WAV
    x, fs = sf.read('test.wav', dtype='float32')
    print('En reproducción: Canción original')
    sd.play(x,fs)

def StopArchivo(): #Deneter reproducción del archivo
    sd.stop()

def InvertirCanales(): #Cambiar el canal 1 al 2 y el canal 2 al 1
    subprocess.call(['ffmpeg','-y','-i', Ruta, 'test.wav']) #Conversion a WAV
    x, fs = sf.read('test.wav', dtype='float32')

    canal1 = x[0:len(x), 0] #Almacenamiento de los valores en la fila 1 del muestreo
    canal1 = canal1.reshape(len(canal1), 1) #Se cambia la dimencion del arreglo
 
    canal2 = x[0:len(x), 1] #Almacenamiento de los valores en la fila 2 del muestreo
    canal2 = canal2.reshape(len(canal2), 1) #se cambia la dimencion del arreglo


    y = np.append(canal2, canal1, axis=1) #Cambio de posicion entre canales

    print('En reproducción: Canción alterada')
    sd.play(y, fs)


def ReflejarCanales(): #Reproducir los canales en sentido inverso
    subprocess.call(['ffmpeg', '-y', '-i', Ruta, 'test.wav']) #Conversion a WAV
    x, fs = sf.read('test.wav', dtype='float32')

    canal1 = x[0:len(x), 0] #Almacenamiento de los valores en la fila 1 del muestreo
    canal1 = canal1.reshape(len(canal1), 1) #Se cambia la dimencion del arreglo
 
    canal2 = x[0:len(x), 1] #Almacenamiento de los valores en la fila 2 del muestreo
    canal2 = canal2.reshape(len(canal2), 1) #se cambia la dimencion del arreglo


    y = np.append(canal1, canal2, axis=1) #Se vuelven a unir los canales

    y = y[::-1] #Se realiza el reflejo de los datos

    print('En reproducción: Canción alterada')
    sd.play(y, fs)


def Alteracion(): #Aumento de la intensidad del archivo
    subprocess.call(['ffmpeg', '-y', '-i', Ruta, 'test.wav']) #Conversion a WAV
    x, fs = sf.read('test.wav', dtype='float32')

    Data = float(valor.get()) #Lectura de la cantidad para aumentar desde el input
    Data = 1 + Data/100 #Limite de aumento nota peronal: duele mucho cuando no lo tiene mas si llega a 100

    canal1 = np.array(x[0:len(x), 0]) #Almacenamiento de los valores en la fila 1 del muestreo
    canal2 = np.array(x[0:len(x), 1]) #Almacenamiento de los valores en la fila 2 del muestreo

    Tmp = np.array([Data]) #Creación de un array temporal para la convolucion

    cntemp1 = np.convolve(canal1, Tmp) #Convolución del canal 1 con el aumento
    cntemp2 = np.convolve(canal2, Tmp) #Convolución del canal 2 con el aumento

    cntemp1 = cntemp1.reshape(len(cntemp1),1)  #se cambia la dimencion del arreglo
    cntemp2 = cntemp2.reshape(len(cntemp2), 1)  #se cambia la dimencion del arreglo

    y = np.append(cntemp1, cntemp2, axis=1) #Se vuelven a unir los canales

    print("Escuhando la cancion incrementada en " + Data)

    print('En reproducción: Canción aumentada')
    sd.play(y,fs)

def Decremento():
    subprocess.call(['ffmpeg', '-y', '-i', Ruta, 'test.wav']) #Conversion a WAV
    x, fs = sf.read('test.wav', dtype='float32')

    Data = float(valor.get()) #Lectura de la cantidad para la reducción desde el input
    Data = 1 - Data / 100 #Limite de aumento nota peronal: duele mucho cuando no lo tiene mas si llega a 100

    canal1 = np.array(x[0:len(x), 0]) #Almacenamiento de los valores en la fila 1 del muestreo
    canal2 = np.array(x[0:len(x), 1]) #Almacenamiento de los valores en la fila 2 del muestreo

    Tmp = np.array([Data]) #Creación de un array temporal para la convolucion

    cntemp1 = np.convolve(canal1, Tmp) #Convolución del canal 1 con la reduccion
    cntemp2 = np.convolve(canal2, Tmp) #Convolución del canal 2 con la reduccion
 
    cntemp1 = cntemp1.reshape(len(cntemp1), 1) #se cambia la dimencion del arreglo
    cntemp2 = cntemp2.reshape(len(cntemp2), 1) #se cambia la dimencion del arreglo

    print("Escuchando la cancion disminuida a " + Data)

    y = np.append(cntemp1, cntemp2, axis=1) #Se vuelven a unir los canales
 
    print('En reproducción: Canción disminuida')
    sd.play(y, fs)

def Recorte(): #Extraccióno de fragmento
    subprocess.call(['ffmpeg', '-y', '-i', Ruta, 'test.wav']) #Conversion a WAV
    x, fs = sf.read('test.wav', dtype='float32')

    i = int(DesdeINP.get()) #Conversion a entero de la entrada para el inicio del corte de segmento
    f = int(HastaINP.get()) #Conversion a entero de la entrada para el fin del corte de segmento

    inicio = i * fs # Calculo de la frecuencia inicial
    final = f * fs # Calculo de la frecuencia final 

    if inicio < 0: #Restriccion para evitar inicar en una canitdad menor a la frecuencia
        inicio = 0 
    if final > len(x): #Restriccion para evitar terminar en una cantidad mayor a la frecuencia
        final = len(x)

    canal1 = x[inicio:final, 0] #Obtencion de muestras de la señal x desde el calculo de la frecuencia inicial hasta la final para el canal 1
    canal1 = canal1.reshape(len(canal1), 1) #se cambia la dimencion del arreglo

    canal2 = x[inicio:final, 1] #Obtencion de muestras de la señal x desde el calculo de la frecuencia inicial hasta la final para el canal 2
    canal2 = canal2.reshape(len(canal2), 1) #se cambia la dimencion del arreglo

    y = np.append(canal1, canal2, axis=1) #Se vuelven a unir los canales

    print('En reproducción: Canción recortada')
    sd.play(y, fs)

def Efecto(): #Efecto prueba
    subprocess.call(['ffmpeg', '-y', '-i', Ruta, 'test.wav'])
    x, fs = sf.read('test.wav', dtype='float32')

    can1 = np.array(x[0:len(x), 0])
    can2 = np.array(x[0:len(x), 1])

    Tmp = np.array([2.5])
    Tmp2 = np.array([0.5])

    cntemp1 = np.convolve(can1, Tmp)
    cntemp2 = np.convolve(can2, Tmp2)

    cntemp1 = cntemp1.reshape(len(cntemp1), 1)
    cntemp2 = cntemp2.reshape(len(cntemp2), 1)

    y = np.append(cntemp1, cntemp2, axis=1)

    sd.play(y, fs)


#Codigo de Componentes

#Mensajes de Bienvenida y final de la UI
Bienvenida = Label(root, text="Proyecto Corto #1", pady=5, padx=5, font=("Arial", 12))
Footer = Label(root, text="Estudiantes", font=("Arial",10), padx=5, pady=5)

#Seleccion de archivo
SeleccionMSG = Label(root, text="Seleccion de archivo", font=("Arial",10))
BTNSeleccion = Button(root, text="Seleccionar un archivo",font=("Arial",10), relief="groove", command= SeleccionArchivos)

#Reproduccion del archivo
AudioName = Label(root, text=Ruta, font=("Arial",10))
BTNReproduccion = Button(root, text="Reproducir archivo", font=("Arial",10), relief="groove", command=PlayArchivo)
BTNParar = Button(root, text="Detener Reproduccion", font=("Arial",10), relief="groove", command= StopArchivo)

#invertir matriz
LabelInv = Label(root, text="Invertir canales", font=("Arial",10))
BTNInverCanales = Button(root, text="Invertir canales", font=("Arial",10), relief="groove", command=InvertirCanales)

#reflejar matriz
LabelRFL = Label(root, text="Reflejar canales de audio", font=("Arial",10))
BTMReflejar = Button(root, text="Reflejar canales", font=("Arial",10), relief="groove", command=ReflejarCanales)

#Alteracion de intensidad
LabelAlt1 = Label(root, text="Alteracion de intensidad", font=("Arial",10))
valor = INPcantidad = Entry(root, width=15, font=("Arial",10))
BTNaumentar = Button(root, text="Aumentar", font=("Arial",10), relief="groove", command=Alteracion)
BTNDecrementar = Button(root, text="Reducir", font=("Arial",10), relief="groove", command=Decremento)

#Extraccion
LabelExt = Label(root, text="Corte de fragmento", font=("Arial",10))
DesdeINP = Entry(root, width=25)
HastaINP = Entry(root, width=25)
BTNCortar = Button(root, text="Recortar", font=("Arial",10), relief="groove", command=Recorte)

#Efecto
BTnEfecto = Button(root, text="Efecto", font=("Arial",10), relief="groove", command= Efecto)

#Ordenamiento del UI
Bienvenida.grid(row=0, column=1)

#Seleccion de Audio
SeleccionMSG.grid(row=1, column=0)
BTNSeleccion.grid(row=1, column=1)

#Reproduccion
AudioName.grid(row=2, column=0, padx=10)
BTNReproduccion.grid(row=3, column=1, padx=10)
BTNParar.grid(row=3, column=2, padx=10)

#Inversion
LabelInv.grid(row=4, column=0, pady=15)
BTNInverCanales.grid(row=4, column=1, pady=15)

#Refleccion
LabelRFL.grid(row=5, column=0, pady=25)
BTMReflejar.grid(row=5, column=1, pady=25)

#Alteracion
LabelAlt1.grid(row=6, column=0, pady=10)
INPcantidad.grid(row=6, column=1, pady=10)
BTNaumentar.grid(row=6, column=2, pady=10)
BTNDecrementar.grid(row=7, column=2, pady=10)

#Recorte
LabelExt.grid(row=8, column=1)
DesdeINP.grid(row=9, column=0, padx=10)
HastaINP.grid(row=9, column=1, padx=10)
BTNCortar.grid(row=9, column=2)

#Personalizado
BTnEfecto.grid(row=10, column=2, pady=10)

Footer.grid(row=11, column=1)
root.mainloop()