#Importaciones para UI
from tkinter import *
from tkinter import filedialog

#Importaciones de clases para funciones
import numpy as np
import sounddevice as sd
import soundfile as sf
import subprocess #Libreria para convertir los archivos MP3 a WAV

root = Tk()

#Seccion de funciones

Ruta = ""

def SeleccionArchivos(): #Funcion para seleccionar archivos
    global filename
    #Filtro para seleccionar unicamente archivos MP3, WAV y OGG
    filename = filedialog.askopenfilename(initialdir="D:/", title="Selecciona un archivo de audio", filetypes=(("Archivos MP3", "*.MP3"), ("Archivos WAV", "*.WAV"),("Archivos OGG", "*.OGG")))
    global Ruta
    #Almacenamiento de la ruta en una variable
    Ruta = filename

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
    Data = 5 + Data/100 #Limite de aumento nota peronal: duele mucho cuando no lo tiene mas si llega a 100

    print(Data)

    canal1 = np.array(x[0:len(x), 0]) #Almacenamiento de los valores en la fila 1 del muestreo
    canal2 = np.array(x[0:len(x), 1]) #Almacenamiento de los valores en la fila 2 del muestreo

    Tmp = np.array([Data]) #Creación de un array temporal para la convolucion

    cntemp1 = np.convolve(canal1, Tmp) #Convolución del canal 1 con el aumento
    cntemp2 = np.convolve(canal2, Tmp) #Convolución del canal 2 con el aumento

    cntemp1 = cntemp1.reshape(len(cntemp1),1)  #se cambia la dimencion del arreglo
    cntemp2 = cntemp2.reshape(len(cntemp2), 1)  #se cambia la dimencion del arreglo

    y = np.append(cntemp1, cntemp2, axis=1) #Se vuelven a unir los canales

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