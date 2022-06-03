from ev3dev2.motor import LargeMotor, SpeedPercent

class Drive:
    left_motor = LargeMotor()
    right_motor = LargeMotor()
    minspeed = 1

    def __init__(self, left_motor_addr, right_motor_addr, defspeed, turnmod, turnflat):
        self.left_motor = LargeMotor(left_motor_addr)
        self.right_motor = LargeMotor(right_motor_addr)
        self.defspeed = defspeed
        self.turnmod = turnmod
        self.turnflat = turnflat

    def stop(self):
        self.left_motor.off()
        self.right_motor.off()

    def _left(self, speed):
        self.left_motor.on(speed)

    def _right(self, speed):
        self.right_motor.on(speed)

    def correct(self, lval, rval):
        mod = abs(rval - lval) * self.turnmod + self.turnflat
        self._left(SpeedPercent(-(self.defspeed - rval*mod + lval)))
        self._right(SpeedPercent(-(self.defspeed - lval*mod + rval)))

    def rotate90(self, side):
        self.stop()
        if side == 'l':
            self.left_motor.on_for_rotations(SpeedPercent(-30), 1)
        else:
            self.right_motor.on_for_rotations(SpeedPercent(-30), 1)

    def rotate180(self):
        self.left_motor.on_for_rotations(SpeedPercent(30), 1, block=False)
        self.right_motor.on_for_rotations(SpeedPercent(-30), 1)

    def last_sprint(self):
        self.left_motor.on_for_rotations(SpeedPercent(10), 0.5)
        self.right_motor.on_for_rotations(SpeedPercent(10), 0.5)

    def short_sprint(self):
        self.left_motor.on_for_rotations(SpeedPercent(10), 0.2)
        self.right_motor.on_for_rotations(SpeedPercent(10), 0.2)
