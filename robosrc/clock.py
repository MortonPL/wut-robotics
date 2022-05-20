from time import time

def tps(tick):
    while True:
        tock = time()
        tock = yield 1 / (tock - tick)
        tick = tock

def avgtps():
    sum_ = yield None
    cnt_ = 1
    while True:
        tps = yield sum_ / cnt_
        sum_ += tps
        cnt_ += 1
