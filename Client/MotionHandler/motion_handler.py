import RPi.GPIO as GPIO
from gpiozero import Servo
import threading
import time
class motion_handler:
    def __init__(self, sweep_delay_sec=3, movement_speed=0.25, motor_pin=19, tick_interval_sec=0.45):
        self.motor = Servo(motor_pin)
        self.movementSpeed = movement_speed
        self.motorPin = motor_pin
        self.tickIntervalSec = tick_interval_sec
        self.sweepDelaySec = sweep_delay_sec
        # setup feedback thread
        self.sweepTimeMarker = time.time()
        self.sweepMode = False
        self.delta = 0
        self.thread = threading.Thread(target=self.motion_tick)
        self.thread.setDaemon(True)
        self.thread.setName("motion_handler_thread")
        # Run feedback tick loop
        self.isRunning = True
        self.thread.start()

    def set_motion_delta(self, sweep_mode, delta):
        #print("Sweep:",sweep_mode,", Delta:",delta)
        if(sweep_mode):
            if(time.time()-self.sweepTimeMarker>self.sweepDelaySec):
                self.sweepMode = True
        else:
            self.sweepMode = False
            self.sweepTimeMarker = time.time()
        angle_of_sight_degree = 12
        # +ve: look up, -ve: look down
        self.delta = delta * angle_of_sight_degree/90
    
    def motion_tick(self):
        # start at 90 degree
        pos = 0 # range from -1 to 1
        sweep = 1
        self.motor.value = pos
        while self.isRunning:
            if(self.sweepMode):
                pos += self.movementSpeed * sweep
            else:
                pos += self.delta
            if(pos>1):
                pos = 1
                sweep = -1
            elif(pos<-1):
                pos = -1
                sweep = 1
            self.motor.value = pos
            time.sleep(self.tickIntervalSec)
    
    def __del__(self):
        self.motor.stop()
        GPIO.cleanup()