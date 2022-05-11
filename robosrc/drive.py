from ev3dev2.motor import LargeMotor, SpeedPercent

class Drive:
    left_motor = LargeMotor()
    right_motor = LargeMotor()
    lospeed = 0
    medspeed = 0
    hispeed = 0
    rotspeed = 0

    def __init__(self, left_motor_addr, right_motor_addr, lospeed=0, medspeed=0, hispeed=0, rotspeed=0):
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
        self.left_motor.on(speed)

    def _right(self, speed):
        self.right_motor.on(speed)

    def move_forward(self):
        self._left(self.medspeed)
        self._right(self.medspeed)

    def move_turn_left(self):
        self.right_motor.on_for_rotations(SpeedPercent(self.lospeed), self.rotspeed)
        self.left_motor.on_for_rotations(SpeedPercent(self.hispeed), self.rotspeed)

    def move_turn_right(self):
        self.right_motor.on_for_rotations(SpeedPercent(self.hispeed), self.rotspeed)
        self.left_motor.on_for_rotations(SpeedPercent(self.lospeed), self.rotspeed)
    
    def correct(self, angle):
        val = min(max(angle / 2, self.hispeed), -self.lospeed)
        self.left_motor.on_for_rotations(SpeedPercent(val), self.rotspeed, block=False)
        self.right_motor.on_for_rotations(SpeedPercent(-val), self.rotspeed, block=False)
