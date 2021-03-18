import time
import VL53L0X
import RPi.GPIO as GPIO

UpDownSensor = 20
RightLeftSensor = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(UpDownSensor, GPIO.OUT)
GPIO.setup(RightLeftSensor, GPIO.OUT)

GPIO.output(sensor1_shutdown, GPIO.HIGH)
GPIO.output(sensor2_shutdown, GPIO.HIGH)

tof_X = VL53L0X.VL53L0X(address=0x2D)
tof_Y = VL53L0X.VL53L0X(address=0x2B)

time.sleep(0.50)
tof_X.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
tof_Y.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

dist_X = tof_X.get_distance()
print(dist_X)
dist_Y = tof_Y.get_distance()
print(dist_Y)
