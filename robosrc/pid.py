class PID:
    def __init__(self, Kp, Ki, Kd, target_val=0):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.I = 0
        self.target_val = target_val
        self.error_last = 0
        self.time_last = 0
        self.val = 0

    def first(self, time_):
        self.time_last = time_

    def next(self, time_, wanted, real):
        error = wanted + real

        P = self.Kp * error
        self.I += self.Ki * error * (time_ - self.time_last)
        D = self.Kd * (error - self.error_last) / (time_ - self.time_last)

        val = self.target_val + P + self.I + D
        self.time_last = time_
        self.error_last = error
        return val
