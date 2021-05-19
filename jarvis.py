import speech_recognition as sr
import pyttsx3  # Este import es para pasar a voz lo que escribimos
import pywhatkit  # Este immport es para que reconosca las musica de youtube
import datetime  # Este metodo es para la hora
import wikipedia  # Para poder usar wikipedia
from tkinter import *
from PIL import Image
import pygame  # Este import es para poder reproducir musica, como el de onichan
import os  # Este import es para poder abrir las apps de la pc

root = Tk()

frame = Frame(root)

frame.pack()
frame.config(bg="white")
label1 = Label(frame, text="Reconocimiento por voz")
label1.pack(padx=10, pady=4)
label1.config(font="Curier 30", bg="white")

# Musica, ejemplo : El sonido de onichan
# Inicializamos el pygame
pygame.mixer.init()


def play():
    pygame.mixer.music.load("OnichanCorte.mp3")
    pygame.mixer.music.play(loops=0)


# Animacion-------------------------------------------------------------------------------------------

file = "miku.gif"

info = Image.open(file)

frames = info.n_frames  # gives total number of frames that gif contains

# creating list of PhotoImage objects for each frames
im = [PhotoImage(file=file, format=f"gif -index {i}") for i in range(frames)]

count = 0
anim = None


def animation(count):
    global anim
    im2 = im[count]

    gif_label.configure(image=im2)
    count += 1
    if count == frames:
        count = 0
    anim = root.after(50, lambda: animation(count))#el 50 es la velocidad en ms del gif , si lo aumento iria mas lento


def stop_animation():
    root.after_cancel(anim)


gif_label = Label(frame, image="")
gif_label.pack(pady=10)

gif_label.config(bg="white")
animation(count)
# ---------------------------------------------------------------------------------------------------------------------------


boton1 = Button(frame, text="Active voz")
boton1.pack()


name = 'alexa'  # Nombre del Asistente de Voz

listener = sr.Recognizer()  # Esto hace que reconosca la voz

# De esta forma esstamos inicializando la variable para usar el pyttsx3
engine = pyttsx3.init()

# Esto trae un listado de voces que tiene mi pc
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # voice es un metodo de pyttsx3

# Con este for veo que voces tengo
# for i  in voices:
# print(i)

# Aqui creo una cariable para poder cambiar la velocidad de la voz
velocidad = engine.getProperty('rate')
# A qui le pongo cuanto quito a la velocidad de la voz
engine.setProperty('rate', velocidad-50)


# voz con acento mexicano
engine.setProperty('voice', 'TTS_MS_ES-MX_SABINA_11.0')


def talk(texto):
    engine.say(texto)
    engine.runAndWait()


def listen():
    try:
        with sr.Microphone() as source:  # Al microfono lo vamos a renonbrar como source
            print("Hola!, te escucho!")
            # Lo que se escucha se guardara en voice
            voice = listener.listen(source)
            # recognize_google es una api de google
            rec = listener.recognize_google(voice, language='es-MX')
            rec = rec.lower()
            # Hacemos una validacion
            if name in rec:  # Si al hablar no escucha el valor que le pusimos a name no nos respondera

                print(rec)
    except:  # Esto es como el catch de java
        pass
    return rec

# Metodo para abrir el notepad


def blocDeNotas():

    os.system('notepad.exe')
# ---------------------------------------------------


def run():
    engine.say("Hola Miguel, Te escucho!")
    engine.runAndWait()
    engine.stop()

    rec = listen()  # Aqui asignamos a la variable rec lo que saLga del listen

    def mostrarLabel():
        labelEscrito.config(text=f"E dicho: {rec}", font=("Curier", 20))
    mostrarLabel()
    if name in rec:  # Si el nombre, en este caso "alexa" se encuentra dentro de lo que hemos dicho, se ejecutara el metodo

        if 'reproduce' in rec:
            # Este comando es para que cuando cel boot hable no diga su nombre
            rec = rec.replace(name, '')
            # Esto quiere decir , que si digo reproduce , no se dira eso,en cambio se dira lo que dice el el talk de abajo
            music = rec.replace('reproduce', '')
            talk('Reproduciendo'+music)

            # Este metodo hace que  lo que diga se busque en youtube
            pywhatkit.playonyt(music)
            # Esta condicional es para que nos diga la hora
        elif 'hora' in rec:
            if name in rec:
                hora = datetime.datetime.now().strftime('%I:%M %p')
                talk("Son las " + hora)
            else:
                talk("Error, di mi nombre bien")
                print(rec)
        elif 'busca' in rec:
            # Esto es para que la informacion de wikipedia sea en espnol
            wikipedia.set_lang("es")
            order = rec.replace('busca', '')
            info = wikipedia.summary(order, 1)
            talk("Wikipedia dice que ")

            talk(info)
        elif 'onii-chan' in rec:
            play()
        elif 'presentanos' in rec:
            pygame.mixer.music.load ( "introGrupo.mp3" )
            pygame.mixer.music.play ( loops=0 )#Si ponemos -1 envez del 0 va a reproducirse aleatoriamente
        elif 'bloc' in rec:
            talk("Abriendo bloc de notas")
            blocDeNotas()
        elif 'google' in rec:
            talk("Abriendo google Crom")
            os.startfile('chrome.exe')
        elif 'youtube' in rec:
            talk("Abriendo youtube")
            os.startfile('https://www.youtube.com')
        elif 'java' in rec:
            talk("abriendo netbeans para programar mi lord")
            os.startfile(
                "C:/Program Files/NetBeans-11.3/netbeans/bin/netbeans64.exe")
        elif 'excel' in rec:
            talk("Abriendo excel")
            os.startfile(
                "C:/Program Files/Microsoft Office/root/Office16/EXCEL.EXE")
        elif 'word' in rec:
            talk("Abriendo Word")
            os.startfile(
                'C:/Program Files/Microsoft Office/root/Office16/WINWORD.EXE')
        else:  # Si no se encuentra la palabra en amarillo dentro de lo que dictamos , no se reconocera el comando
            talk("Comando Desconocido")
    else:  # Si no decimos 'alexa" no se ejecutara el metodo y finalizara la app
        talk("Error, di mi nombre bien")
        print(rec)


labelEscrito = Label(frame, text="!!Escuchando!!")
# En el pack se pone el padx y pady para margin
labelEscrito.pack(padx=10, pady=10)
# El pad en el config se vuelve como un padding
labelEscrito.config(font=("Curier", 20), padx=20, pady=5, bg="green")


boton1.config(command=run, font="Curier 40", bg="green")


root.mainloop()
