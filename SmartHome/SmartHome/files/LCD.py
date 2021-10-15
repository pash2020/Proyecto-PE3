#LCD
import RPi.GPIO as GPIO
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import time
#--------------------------------------

#Pines
T = 7
E = 12

#--------------------------------------
#GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
#Pin Sensor ultrasonico
GPIO.setup(T, GPIO.OUT)
GPIO.output(T, 0)
GPIO.setup(E, GPIO.IN)
#Pantalla LCD
lcd = LCD()

def safe_exit(signum, frame):
    exit(1)
    
signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

#--------------------------------------

def sensor():
    time.sleep(0.1)
    GPIO.output(T, 1)
    time.sleep(0.00001)
    GPIO.output(T, 0)

    while GPIO.input(E) == 0:
        pass
    start = time.time()

    while GPIO.input(E) == 1:
        pass
    stop = time.time()

    dist= (stop - start) * 17155

    print("Distancia:", "{:.2f}".format(dist), "cm")

    lcd.text("-Distancia:", 1)
    lcd.text("    {:.2f}".format(dist)+" cm", 2)
    time.sleep(0.5)
    return

def end():
    return

#--------------------------------------

try:
    while True:
        sensor()
       
#--------------------------------------
#Interrupcion/final    
except KeyboardInterrupt:
  lcd.clear()
  GPIO.cleanup()
  exit()