from ev3dev2.motor import LargeMotor, SpeedPercent

class Drive:
    left_motor = LargeMotor()
    right_motor = LargeMotor()
    minspeed = 1

    def __init__(self, left_motor_addr, right_motor_addr, defspeed,turnmod):
        self.left_motor = LargeMotor(left_motor_addr)
        self.right_motor = LargeMotor(right_motor_addr)
        self.defspeed = defspeed
        self.turnmod = turnmod

    def stop(self):
        self.left_motor.off()
        self.right_motor.off()

    def _left(self, speed):
        self.left_motor.on(speed)

    def _right(self, speed):
        self.right_motor.on(speed)
    
    # defspeed 10 mnożnik 5

    def correct(self, lval, rval):
        mod = abs(rval - lval) * self.turnmod
        self._left(SpeedPercent(-(self.defspeed - rval*mod + rval)))
        self._right(SpeedPercent(-(self.defspeed - lval*mod + lval)))
