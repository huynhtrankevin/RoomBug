import RPi.GPIO as GPIO

class Motor:
    FORWARD = 0
    REVERSE = 1
    HALT = 2
    
    def __init__(self, IN1_PIN, IN2_PIN, PWM_PIN, PWM_FREQ):
        self.IN1_PIN = IN1_PIN
        self.IN2_PIN = IN2_PIN
        self.PWM_PIN = PWM_PIN
        self.pwm = GPIO.PWM(PWM_PIN,PWM_FREQ)
        self.duty_cycle = 0
        self.pwm_started = False
        self.dir = FORWARD
        
        GPIO.setup(IN1_PIN,GPIO.OUT)
        GPIO.setup(IN2_PIN,GPIO.OUT)
        GPIO.setup(PWM_PIN,GPIO.OUT)
        
    def set_dir(self,dir):
        self.dir = dir
        
        if dir == FORWARD:
            GPIO.output(self.IN1_PIN, True)
            GPIO.output(self.IN2_PIN, False)
        if dir == REVERSE:
            GPIO.output(self.IN1_PIN, False)
            GPIO.output(self.IN2_PIN, True)
        if dir == HALT:
            GPIO.output(self.IN1_PIN, False)
            GPIO.output(self.IN2_PIN, False)
            
    def set_PWM(self,duty_cycle):
        self.duty_cycle = duty_cycle
        
        if self.pwm_started == False:
            self.pwm_started = True
            self.pwm.start(duty_cycle)
        else:
            self.pwm.changeDutyCycle(duty_cycle)
    
    
    def drive(self,dir, duty_cycle):
        if self.dir != dir & self.dir != HALT:
            set_dir(HALT)
            set_PWM(duty_cycle)
            set_dir(dir)
        else:
            set_PWM(duty_cycle)
            
    
        
        