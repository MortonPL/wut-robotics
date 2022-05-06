from ev3dev2.motor import LargeMotor

class Drive:
    left_motor: LargeMotor
    right_motor: LargeMotor
    lospeed: int
    medspeed: int
    hispeed: int

    def __init__(self, left_motor_addr, right_motor_addr, lospeed=0, medspeed=50, hispeed=100):
        self.left_motor = LargeMotor(left_motor_addr)
        self.right_motor = LargeMotor(right_motor_addr)
        self.lospeed = lospeed
        self.medspeed = medspeed
        self.hispeed = hispeed

    def stop(self):
        self.left_motor.off()
        self.right_motor.off()

    def _left(self, speed):
        self.left_motor.on(speed)

    def _right(self, speed):
        self.right_motor.on(speed)

    def move_forward(self):
        self.left_motor.on(self.medspeed)
        self.right_motor.on(self.medspeed)

    def move_turn_left(self):
        self.left_motor.on(self.lospeed)
        self.right_motor.on(self.hispeed)

    def move_turn_right(self):
        self.left_motor.on(self.hispeed)
        self.right_motor.on(self.lospeed)
