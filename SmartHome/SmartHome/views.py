#Obtubre 2021
#Ejemplo Proyecto PE3
#Paúl Solórzano

#--------------------------------------
#Librerias
from django.http import HttpResponse
import datetime
from django.template import Template, Context
from django.template import loader
import RPi.GPIO as GPIO
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import time
import os

#--------------------------------------
# Variables de estado/pines/template-render
AC = 37
eAC = 1
bt1c = "apagado"
bt1t = "OFF"

LS = 36
eS = 1
bt2c = "apagado"
bt2t = "OFF"

LC = 15
eC = 1
bt3c = "apagado"
bt3t = "OFF"

LD = 31
eD = 1
bt4c = "apagado"
bt4t = "OFF"

LB = 29
eB = 1
bt5c = "apagado"
bt5t = "OFF"

SM = 22
E_m = 1
bt6c = "apagado"
bt6t = "CERRADO"

LE = 18
LDR = 11
E_le = 1
E_auto_ldr = 1
N = 1
M = 1

bt7c = "apagado"
bt7t = "OFF"

T = 1

E_LCD = 1

Tr = 7
Ec = 12

med = "procesando..."
e_med = 1

fecha = None
#--------------------------------------
#GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
# Pin jardin_ac
GPIO.setup(AC, GPIO.OUT)
GPIO.output(AC, GPIO.HIGH)
# Pin Led_sala
GPIO.setup(LS, GPIO.OUT)
GPIO.output(LS, GPIO.LOW)
# Pin Led_cocina
GPIO.setup(LC, GPIO.OUT)
GPIO.output(LC, GPIO.LOW)
#Pin Led_dormitorio
GPIO.setup(LD, GPIO.OUT)
GPIO.output(LD, GPIO.LOW)
# Pin Led_bano
GPIO.setup(LB, GPIO.OUT)
GPIO.output(LB, GPIO.LOW)
# Pin Led_entrada
GPIO.setup(LE, GPIO.OUT)
GPIO.output(LE, GPIO.LOW)
#Pin servo_motor
GPIO.setup(SM, GPIO.OUT)
p = GPIO.PWM(SM, 50) #PWM with 50Hz
p.start(5) # Initialization
#Pin Sensor ultrasonico
GPIO.setup(Tr, GPIO.OUT)
GPIO.output(Tr, 0)
GPIO.setup(Ec, GPIO.IN)
#Pantalla LCD
lcd = LCD()

def safe_exit(signum, frame):
    exit(1)
    
signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

#--------------------------------------
#Clases y funciones
class Estado:#Clase estado para la iluminación según parámetros de estado
    def run(self):
        self.run = True
    def estado(self, x, y, z, k):#variable de estado, response, pines
        self.x = x
        self.y = y
        self.z = z
        self.k = k
        q = int(x)
        r = str(y)
        s = str(z)
        while self.run:#condicioanles de estado generales para la iluminación
            if q == 0:
                q += 1
                r = "apagado"
                s = "OFF"
                GPIO.output(k, GPIO.LOW)
                Li = [q, r, s]
                return Li
                break
            elif q == 1:
                q = 0
                r = "encendido"
                s = "ON"
                GPIO.output(k, GPIO.HIGH)
                Li = [q, r, s]
                return Li
                break
            else:
                break
            
def r():#Loader formato HttpResponse para todas las solicitudes
    template0 = loader.get_template('index.html')
    doc=template0.render({"bt1c":bt1c, "bt1t":bt1t, "bt2c":bt2c, "bt2t":bt2t, "bt3c":bt3c, "bt3t":bt3t, "bt4c":bt4c, "bt4t":bt4t, "bt5c":bt5c, "bt5t":bt5t, "bt6c":bt6c, "bt6t":bt6t, "bt7c":bt7c, "bt7t":bt7t, "btm": med, "f":fecha})
    return doc

def fecha():#Función para la fecha actual
    global fecha
    fecha = datetime.datetime.now()
    return fecha 
#--------------------------------------     
#Respuesta para la primer solicitud que lleva al index
def index(request):
    return HttpResponse(r())

#Solicitud/Respuesta para AC, utiliza otro formato debido a que es low trigger
def estado_AC(request):
    print("-------------AC-------------")
    global eAC, bt1c, bt1t
    if eAC == 0:
        eAC += 1
        bt1c = "apagado"
        bt1t = "OFF"
        GPIO.output(AC, GPIO.HIGH)
        pass
    elif eAC == 1:
        eAC = 0
        bt1c = "encendido"
        bt1t = "ON"
        GPIO.output(AC, GPIO.LOW)
        pass
    else:
        pass
    return HttpResponse(r())

#Estado para el led de la sala
def estado_LS(request):
    print("-------------LS-------------")
    Luz2 = Estado()
    Luz2.run()
    global eS, bt2c, bt2t
    P = Luz2.estado(eS, bt2c, bt2t, LS)
    eS = P[0]
    bt2c = P[1]
    bt2t = P[2]
    print(eS, bt2c, bt2t)
    return HttpResponse(r())
    
#Estado para el led de la cocina
def estado_LC(request):
    print("-------------LC-------------")
    Luz3 = Estado()
    Luz3.run()
    global eC, bt3c, bt3t
    P = Luz3.estado(eC, bt3c, bt3t, LC)
    eC = P[0]
    bt3c = P[1]
    bt3t = P[2]
    print(eC, bt3c, bt3t)
    return HttpResponse(r())

#Estado para el led del dormitorio
def estado_LD(request):
    print("-------------LD-------------")
    Luz4 = Estado()
    Luz4.run()
    global eD, bt4c, bt4t
    P = Luz4.estado(eD, bt4c, bt4t, LD)
    eD = P[0]
    bt4c = P[1]
    bt4t = P[2]
    print(eD, bt4c, bt4t)
    return HttpResponse(r())

#Estado para el led del baño
def estado_LB(request):
    print("-------------LB-------------")
    Luz5 = Estado()
    Luz5.run()
    global eB, bt5c, bt5t
    P = Luz5.estado(eB, bt5c, bt5t, LB)
    eB = P[0]
    bt5c = P[1]
    bt5t = P[2]
    print(eB, bt5c, bt5t)
    return HttpResponse(r())

#Solicitud/Respuesta para el servomotor, control pwm
def estado_SM(request):
    print("-------------SM-------------")
    global E_m, bt6c, bt6t
    if E_m == 0:
        E_m += 1
        bt6c = "apagado"
        bt6t = "CERRADO"
        p.ChangeDutyCycle(5)
        print(bt6t)
        time.sleep(0.1)
        pass
    elif E_m == 1:
        E_m = 0
        bt6c = "encendido"
        bt6t = "ABIERTO"
        p.ChangeDutyCycle(1)
        print(bt6t)
        time.sleep(0.1)
        pass
    else:
        pass
    return HttpResponse(r())

#Solicitud/Respuesta para el led de la entrada
#Parámetros adicionales para evitar que interfiera con el porceso automático ldr
def estado_LDR(request):
    print("-------------LDR-------------")
    global E_le, E_auto_ldr, bt7c, bt7t, bt7c1, M
    if M == 1:
        if E_le == 0:
            E_auto_ldr = 1
            E_le += 1
            bt7c = "apagado"
            bt7t = "OFF"
            GPIO.output(LE, GPIO.LOW)
            pass
        elif E_le == 1:
            E_auto_ldr = 0
            E_le = 0
            bt7c = "encendido"
            bt7t = "ON"
            GPIO.output(LE, GPIO.HIGH)
            pass
        else:
            pass
        pass
    else:
        pass  
    return HttpResponse(r())

#Ejecución por terminal del script separado para ldr
#Parámetros adicionales para evitar que interfiera con el porceso individual del led de entrada
def estado_LDRon(request):
    print("-------------LDR_ON-------------")
    global N, M
    if N == 1:
        if E_auto_ldr == 1:
            N = 0
            M = 0
            os.system('python3 /home/pi/Desktop/Proyecto/SmartHome/SmartHome/files/LDR.py') 
        else:
            pass
    else:
        pass
    return HttpResponse(r())

#Detención por terminal del script separado para ldr
def estado_LDRoff(request):
    print("-------------LDR_OFF-------------")
    global N, M
    if E_auto_ldr == 1:
        os.system('pkill -f /home/pi/Desktop/Proyecto/SmartHome/SmartHome/files/LDR.py') 
        GPIO.output(LE, GPIO.LOW)
        N = 1
        M = 1
    else:
        pass
    return HttpResponse(r())

#Ejecución por terminal del script separado para temp
#Parámetros adicionales para no remarcar el estado activado
def estado_TEMPon(request):
    print("-------------TEMP_ON-------------")
    global T
    if T == 1:
        T = 0
        os.system('python3 /home/pi/Desktop/Proyecto/SmartHome/SmartHome/files/Temp.py') 
    else:
        pass
    return HttpResponse(r())

#Detención por terminal del script separado para temp
def estado_TEMPoff(request):
    print("-------------TEMP_OFF-------------")
    global T
    if T == 0:
        os.system('pkill -f /home/pi/Desktop/Proyecto/SmartHome/SmartHome/files/Temp.py') 
        T = 1
    else:
        pass
    return HttpResponse(r())

#Ejecución por terminal del script separado para lcd
#Parámetros adicionales para no remarcar el estado activado
def estado_LCDon(request):
    print("-------------LCD_ON-------------")
    global E_LCD, e_med
    if E_LCD == 1:
        E_LCD = 0
        e_med = 0
        os.system('python3 /home/pi/Desktop/Proyecto/SmartHome/SmartHome/files/LCD.py') 
    else:
        pass
    return HttpResponse(r())

#Detención por terminal del script separado para lcd
def estado_LCDoff(request):
    print("-------------LCD_OFF-------------")
    global E_LCD, e_med
    if E_LCD == 0:
        os.system('pkill -f /home/pi/Desktop/Proyecto/SmartHome/SmartHome/files/LCD.py') 
        E_LCD = 1
        e_med = 1
    else:
        pass
    return HttpResponse(r())

#Respuesta a la solicitud de medición que se mostrará en al página
def medicion(request):
    print("-------------MED-------------")
    global med
    if e_med == 1:
        time.sleep(0.1)
        GPIO.output(Tr, 1)
        time.sleep(0.00001)
        GPIO.output(Tr, 0)

        while GPIO.input(Ec) == 0:
            pass
        start = time.time()

        while GPIO.input(Ec) == 1:
            pass
        stop = time.time()

        dist= (stop - start) * 17155

        
        m = "{:.2f}".format(dist)
        med = str(m)
        time.sleep(0.2)
    else:
        pass
    return HttpResponse(r())

#--------------------------------------     