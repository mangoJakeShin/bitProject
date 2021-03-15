from time import sleep, time
import datetime
import RPi.GPIO as GPIO

class mover():
    PUL = 27  # Stepper Drive Pulses
    DIR = 18  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
    ENA = 17  # Controller Enable Bit (High to Enable / LOW to Disable).

    GPIO.setup(PUL, GPIO.OUT)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(ENA, GPIO.OUT)

    pulse = 200  # This is the duration of the motor spinning. used for forward direction
    delay_org = 0.0005

    delay_H = delay_org  # This is actualy a delay between PUL pulses - effectively sets the mtor rotation speed.
    delay_L = delay_H / 2


    def mv_left(self, cycles):

        GPIO.output(self.DIR, GPIO.LOW)
        GPIO.output(self.ENA, GPIO.HIGH)
        for cyclecount in range(0,cycles):
            for x in range(self.pulse):
                GPIO.output(self.PUL, GPIO.HIGH)
                sleep(self.delay_H)
                GPIO.output(self.PUL, GPIO.LOW)
                sleep(self.delay_L)
        return


    def mv_right(self, cycles):
        GPIO.output(self.ENA, GPIO.HIGH)
        GPIO.output(self.DIR, GPIO.HIGH)
        for cyclecount in range(0, cycles):
            for y in range(self.pulse):
                GPIO.output(self.PUL, GPIO.HIGH)
                sleep(self.delay_H)
                GPIO.output(self.PUL, GPIO.LOW)
                sleep(self.delay_L)
        return

class rev_mover():
    PUL = 27  # Stepper Drive Pulses
    DIR = 18  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
    ENA = 17  # Controller Enable Bit (High to Enable / LOW to Disable).

    GPIO.setup(PUL, GPIO.OUT)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(ENA, GPIO.OUT)

    pulse = 200  # This is the duration of the motor spinning. used for forward direction
    delay_org = 0.0005

    delay_H = delay_org  # This is actualy a delay between PUL pulses - effectively sets the mtor rotation speed.
    delay_L = delay_H / 2


    def mv_left(self,cycles):

        GPIO.output(self.DIR, GPIO.HIGH)
        GPIO.output(self.ENA, GPIO.HIGH)
        for cyclecount in range(0, cycles):
            for x in range(self.pulse):
                GPIO.output(self.PUL, GPIO.HIGH)
                sleep(self.delay_H)
                GPIO.output(self.PUL, GPIO.LOW)
                sleep(self.delay_L)
        return


    def mv_right(self,cycles):
        global cur_x
        GPIO.output(self.ENA, GPIO.HIGH)
        GPIO.output(self.DIR, GPIO.LOW)
        for cyclecount in range(0, cycles):
            for y in range(self.pulse):
                GPIO.output(self.PUL, GPIO.HIGH)
                sleep(self.delay_H)
                GPIO.output(self.PUL, GPIO.LOW)
                sleep(self.delay_L)

        return