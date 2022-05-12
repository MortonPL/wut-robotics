from ev3dev2.motor import LargeMotor, SpeedPercent

class Drive:
    left_motor = LargeMotor()
    right_motor = LargeMotor()
    minspeed = 1
    defspeed = 3

    def __init__(self, left_motor_addr, right_motor_addr, minspeed=1, defspeed=3):
        self.left_motor = LargeMotor(left_motor_addr)
        self.right_motor = LargeMotor(right_motor_addr)
        self.minspeed = minspeed
        self.defspeed = defspeed

    def stop(self):
        self.left_motor.off()
        self.right_motor.off()

    def _left(self, speed):
        self.left_motor.on(speed)

    def _right(self, speed):
        self.right_motor.on(speed)
    
    def correct(self, val):
        val1 = val
        val2 = val
        if abs(val) <= self.minspeed:
            val1 = self.defspeed
            val2 = -self.defspeed
        self._left(SpeedPercent(-val1))
        self._right(SpeedPercent(val2))
