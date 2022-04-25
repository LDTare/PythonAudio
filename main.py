#Importaciones para UI
from tkinter import *
from tkinter import filedialog

#Importaciones de clases para funciones
import numpy as np
import sounddevice as sd
import soundfile as sf
import subprocess

root = Tk()

#Seccion de funciones

Ruta = ""

def SeleccionArchivos(): #Funcion para seleccionar archivos
    global filename
    filename = filedialog.askopenfilename(initialdir="D:/", title="Selecciona un archivo de audio", filetypes=(("Archivos MP3", "*.MP3"), ("Archivos WAV", "*.WAV"),("Archivos OGG", "*.OGG")))
    global Ruta
    Ruta = filename

def PlayArchivo():
    #Reproducir audio
    subprocess.call(['ffmpeg', '-y' , '-i', Ruta, 'test.wav'])
    x, fs = sf.read('test.wav', dtype='float32')
    print('reproduciendo musica original')
    sd.play(x,fs)

def StopArchivo():
    sd.stop()

def InvertirCanales():
    subprocess.call(['ffmpeg','-y','-i', Ruta, 'test.wav'])
    x, fs = sf.read('test.wav', dtype='float32')
    can1 = x[0:len(x), 0]
    can1 = can1.reshape(len(can1), 1)
    # print('Canal 1: ',can1)
    can2 = x[0:len(x), 1]
    can2 = can2.reshape(len(can2), 1)
    # print('Canal 2: ',can2)

    y = np.append(can2, can1, axis=1)
    print('Canales invertidos: ', y)
    print('Frecuencia de muestreo: ', fs)

    print('reproduciendo canales cambiados')
    sd.play(y, fs)


def ReflejarCanales():
    subprocess.call(['ffmpeg', '-y', '-i', Ruta, 'test.wav'])
    x, fs = sf.read('test.wav', dtype='float32')
    can1 = np.array(x[0:len(x), 0])
    can1 = can1.reshape(len(can1), 1)

    can2 = np.array(x[0:len(x), 1])
    can2 = can2.reshape(len(can2), 1)

    y = np.append(can1, can2, axis=1)
    y = y[::-1]
    print('Canales Reflejados: ', y)
    print('Frecuencia de muestreo: ', fs)

    print('reproduciendo reflexion de canales')
    sd.play(y, fs)

def Alteracion():
    subprocess.call(['ffmpeg', '-y', '-i', Ruta, 'test.wav'])
    x, fs = sf.read('test.wav', dtype='float32')

    Data = float(valor.get())
    Data = 5 + Data/100

    print(Data)

    can1 = np.array(x[0:len(x), 0])
    can2 = np.array(x[0:len(x), 1])

    Tmp = np.array([Data])
    print(Tmp)
    print(can1)

    cntemp1 = np.convolve(can1, Tmp)
    cntemp2 = np.convolve(can2, Tmp)

    cntemp1 = cntemp1.reshape(len(cntemp1),1)
    cntemp2 = cntemp2.reshape(len(cntemp2), 1)

    y = np.append(cntemp1, cntemp2, axis=1)

    sd.play(y,fs)

def Decremento():
    subprocess.call(['ffmpeg', '-y', '-i', Ruta, 'test.wav'])
    x, fs = sf.read('test.wav', dtype='float32')

    Data = float(valor.get())
    Data = 1 - Data / 100

    print(Data)

    can1 = np.array(x[0:len(x), 0])
    can2 = np.array(x[0:len(x), 1])

    Tmp = np.array([Data])
    print(Tmp)
    print(can1)

    cntemp1 = np.convolve(can1, Tmp)
    cntemp2 = np.convolve(can2, Tmp)

    cntemp1 = cntemp1.reshape(len(cntemp1), 1)
    cntemp2 = cntemp2.reshape(len(cntemp2), 1)

    y = np.append(cntemp1, cntemp2, axis=1)

    sd.play(y, fs)

def Recorte():
    subprocess.call(['ffmpeg', '-y', '-i', Ruta, 'test.wav'])
    x, fs = sf.read('test.wav', dtype='float32')

    i = int(DesdeINP.get())
    f = int(HastaINP.get())
    inicio = i * fs
    final = f * fs
    # restriccion
    if inicio < 0:
        inicio = 0
    if final > len(x):
        final = len(x)
    print(len(x), inicio, final)
    can1 = x[inicio:final, 0]
    can1 = can1.reshape(len(can1), 1)
    can2 = x[inicio:final, 1]
    can2 = can2.reshape(len(can2), 1)
    y = np.append(can1, can2, axis=1)
    print('reproduciendo extracción:')
    sd.play(y, fs)

def Efecto():
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
Bienvenida = Label(root, text="Proyecto Corto #1 Teoria de sistemas", pady=5, padx=5)
Footer = Label(root, text="Estudiantes", padx=5, pady=5)

#Seleccion de archivo
SeleccionMSG = Label(root, text="Seleccion de archivo")
BTNSeleccion = Button(root, text="Seleccionar un archivo", command= SeleccionArchivos)

#Reproduccion del archivo
AudioName = Label(root, text=Ruta)
BTNReproduccion = Button(root, text="Reproducir archivo", command=PlayArchivo)
BTNParar = Button(root, text="Detener Reproduccion", command= StopArchivo)

#invertir matriz
BTNInverCanales = Button(root, text="Invertir canales", command=InvertirCanales)

#reflejar matriz
BTMReflejar = Button(root, text="Reflejar canales", command=ReflejarCanales)

#Alteracion de intensidad
LabelAlt1 = Label(root, text="Alteracion de intensidad")
valor = INPcantidad = Entry(root, width=5)
BTNaumentar = Button(root, text="Aumentar", command=Alteracion)
BTNDecrementar = Button(root, text="Reducir", command=Decremento)

#Extraccion
LabelExt = Label(root, text="Corte de fragmento")
DesdeINP = Entry(root, width=25)
HastaINP = Entry(root, width=25)
BTNCortar = Button(root, text="Recortar", command=Recorte)

#Efecto
BTnEfecto = Button(root, text="Efecto", command= Efecto)

#Ordenamiento del UI
Bienvenida.grid(row=0, column=1)

#Seleccion de Audio
SeleccionMSG.grid(row=1, column=0)
BTNSeleccion.grid(row=1, column=1)

#Reproduccion
AudioName.grid(row=2, column=0)
BTNReproduccion.grid(row=3, column=1)
BTNParar.grid(row=3, column=2)

#Inversion
BTNInverCanales.grid(row=4, column=2)

#Refleccion
BTMReflejar.grid(row=5, column=2)

#Alteracion
LabelAlt1.grid(row=6, column=0)
INPcantidad.grid(row=6, column=1)
BTNaumentar.grid(row=6, column=2)
BTNDecrementar.grid(row=7, column=2)

#Recorte
LabelExt.grid(row=8, column=1)
DesdeINP.grid(row=9, column=0)
HastaINP.grid(row=9, column=1)
BTNCortar.grid(row=9, column=2)

#Personalizado
BTnEfecto.grid(row=10, column=2)

Footer.grid(row=11, column=1)

root.mainloop()