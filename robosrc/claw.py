from ev3dev2.motor import MediumMotor, SpeedPercent

class Claw:
    motor = MediumMotor()

    def __init__(self, motor_addr):
        self.motor = MediumMotor(motor_addr)

    def stop(self):
        self.motor.off()

    def pick_up(self):
        self.motor.on_for_rotations(SpeedPercent(-20), 0.5)

    def put_down(self):
        self.motor.on_for_rotations(SpeedPercent(20), 0.5)
