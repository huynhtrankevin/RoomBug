import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO_PWM_PIN = 32 # GPIO12
GPIO_CTRL_PIN1 = 36 # GPIO16
GPIO_CTRL_PIN2 = 38 # GPIO20

# setup GPIO pin
GPIO.setup(GPIO_PWM_PIN,GPIO.OUT)
# setup GPIO pin
GPIO.setup(GPIO_CTRL_PIN1,GPIO.OUT)
# setup GPIO pin
GPIO.setup(GPIO_CTRL_PIN2,GPIO.OUT)


GPIO.output(GPIO_CTRL_PIN1, True)
GPIO.output(GPIO_CTRL_PIN2, False)
pwmA = GPIO.PWM(GPIO_PWM_PIN,0.5)

duty_cycle = 50
pwmA.start(duty_cycle)

while 1:    
    time.sleep(2)
    duty_cycle = 30
    pwmA.ChangeDutyCycle(duty_cycle)
    print("duty cycle = {}".format(duty_cycle))
    time.sleep(2)
    duty_cycle = 50
    print("duty cycle = {}".format(duty_cycle))
    pwmA.ChangeDutyCycle(duty_cycle)
