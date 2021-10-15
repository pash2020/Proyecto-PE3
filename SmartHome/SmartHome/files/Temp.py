# Sensor Temp
import RPi.GPIO as GPIO
import time

B = 16
K = 13
E_B = 1
#--------------------------------------

#GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
#pin Buzzer
GPIO.setup(B, GPIO.OUT)
GPIO.output(B, GPIO.HIGH)
#Pin Temp digital
GPIO.setup(K, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#--------------------------------------

def temp(x, y, z):
    if x == 1:
        GPIO.output(y,not z)
        print(z)
        time.sleep(0.1)
    elif x == 0:
        GPIO.output(y, GPIO.HIGH)
        time.sleep(0.1)
    else:
        pass
    return
#--------------------------------------

try:
    while True:
        E_temp = GPIO.input(K)
        temp(E_B, B, E_temp)
       
#--------------------------------------
#Interrupcion/final    
except KeyboardInterrupt:
  GPIO.cleanup()
  exit()