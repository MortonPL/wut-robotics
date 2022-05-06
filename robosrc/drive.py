from ev3dev2.motor import LargeMotor, SpeedPercent

class Drive:
    left_motor = LargeMotor()
    right_motor = LargeMotor()
    lospeed = -5
    medspeed = 5
    hispeed = 10
    rotspeed = 0.01

    def __init__(self, left_motor_addr, right_motor_addr, lospeed=-5, medspeed=5, hispeed=5, rotspeed=0.01):
        self.left_motor = LargeMotor(left_motor_addr)
        self.right_motor = LargeMotor(right_motor_addr)
        self.lospeed = lospeed
        self.medspeed = medspeed
        self.hispeed = hispeed
        self.rotspeed = rotspeed

    def stop(self):
        self.left_motor.off()
        self.right_motor.off()

    def _left(self, speed):
        self.left_motor.on(-speed)

    def _right(self, speed):
        self.right_motor.on(-speed)

    def move_forward(self):
        self._left(self.medspeed)
        self._right(self.medspeed)

    def move_turn_left(self):
        #self._left(self.lospeed)
        #self._right(self.hispeed)
        self.right_motor.on_for_rotations(SpeedPercent(self.lospeed), self.rotspeed)
        self.left_motor.on_for_rotations(SpeedPercent(self.hispeed), self.rotspeed)

    def move_turn_right(self):
        #self._left(self.hispeed)
        #self._right(self.lospeed)
        self.right_motor.on_for_rotations(SpeedPercent(self.hispeed), self.rotspeed)
        self.left_motor.on_for_rotations(SpeedPercent(self.lospeed), self.rotspeed)
    
    def correct(self, angle):
        val = angle
        self.left_motor.on_for_rotations(SpeedPercent(val), self.rotspeed, block=False)
        self.right_motor.on_for_rotations(SpeedPercent(-val), self.rotspeed, block=False)

    def set_speeds(self, low_speed, normal_speed, high_speed):
        self.lospeed = low_speed
        self.mespeed = normal_speed
        self.hispeed = high_speed
