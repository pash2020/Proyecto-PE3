#Sensor LDR
import RPi.GPIO as GPIO
import time

#--------------------------------------
LE = 18
LDR = 11
E_LE = 1


#GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LE, GPIO.OUT)
GPIO.output(LE, GPIO.LOW)
GPIO.setup(LDR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#--------------------------------------
def led_exterior(x, y, z):
    if x == 1:
        GPIO.output(y, z)
        print(z)
        time.sleep(0.1)
    else:
        pass
    return

#--------------------------------------
try:
    while True:
        E_LDR = GPIO.input(LDR)
        led_exterior(E_LE, LE, E_LDR)
       
#--------------------------------------
#Interrupcion/final    
except KeyboardInterrupt:
  GPIO.cleanup()
  exit()
