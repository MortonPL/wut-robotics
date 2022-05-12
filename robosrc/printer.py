ARROWS_L = ['    ◁', '   ◁◁', '  ◁◁◁', ' ◁◁◁◁', '◁◁◁◁◁', '◁◁◁◁◀', '◁◁◁◀◀', '◁◁◀◀◀', '◁◀◀◀◀', '◀◀◀◀◀']
ARROWS_R = ['▷    ', '▷▷   ', '▷▷▷  ', '▷▷▷▷ ', '▷▷▷▷▷', '▶▷▷▷▷', '▶▶▷▷▷', '▶▶▶▷▷', '▶▶▶▶▷', '▶▶▶▶▶']

def pprint(str, row=1, col=1, end=''):
    print("\033[{};{}H".format(row, col), end='')
    print(str, end=end)
    print("\033[12;3H")

def pprint_action(str):
    pprint("{:37}".format(str), row=10, col=3)

def pprint_action_move(val):
    if val > 20:
        #pprint_action("STEERING RIGHT      ={} {}".format(ARROWS_R[val//10], val))
        pprint_action("RIGHT {}".format(val))
    elif val < -20:
        #pprint_action("STEERING LEFT  {}=      {}".format(ARROWS_L[abs(val)//10], abs(val)))
        pprint_action("LEFT {}".format(val))
    else:
        pprint_action("GOING FORWARD {}".format(val))

def pprint_args(slow, normal, high, rot):
    pprint("lo:{} med:{} hi:{} rot:{}"
        .format(slow, normal, high, rot), row=2, col=3)

def pprint_color(color):
    pprint(color, row=4, col=9)

def pprint_sensor(left, right):
    print("\033[6;8H", end='')
    print("\u001b[4m\u001b[31m{:3}\u001b[0m \u001b[4m\u001b[32m{:3}\u001b[0m \u001b[4m\u001b[34m{:3}\u001b[0m"
        .format(left[0], left[1], left[2]), end='')
    print("\033[6;22H", end='')
    print("\u001b[4m\u001b[31m{:3}\u001b[0m \u001b[4m\u001b[32m{:3}\u001b[0m \u001b[4m\u001b[34m{:3}\u001b[0m"
        .format(right[0], right[1], right[2]), end='')
    print("\033[12;3H")

def pprint_time(tps, avg):
    pprint("\u001b[4m{:>5.2f}\u001b[0m".format(tps), row=2, col=42)
    pprint("\u001b[4m{:>5.2f}\u001b[0m".format(avg), row=3, col=42)

def pprint_layout():
    print("\033[2J")
    print("\033[0;0H", end='')
    window = "".join([
        #║ 3                | 22                ║ 42
        '╔═ ARGUMENTS ══════════════════════════╦═ TIME ════╗\n', # 1
        '║                                      ║ __.__ TPS ║\n', # 2
        '╠═ SENSORS ════════════════════════════╣ __.__ AVG ║\n', # 3
        '║ I SEE ______                         ╠═══════════╝\n', # 4
        '╟──────────────────┬───────────────────╢\n',             # 5
        '║ LEFT ___ ___ ___ │ ___ ___ ___ RIGHT ║\n',             # 6
        '╠═ CONTROLLER ═════╧═══════════════════╣\n',             # 7
        '║                                      ║\n',             # 8
        '╠═ ACTION ═════════════════════════════╣\n',             # 9
        '║                                      ║\n',             # 10
        '╚══════════════════════════════════════╝\n',             # 11
        '>                               '])
    print(window)


if __name__ == "__main__":
    from time import sleep, time
    from clock import tps, avgtps

    pprint_layout()
    pprint_args(10, 20, 30, 0.01)
    pprint_color("WHITE ")
    pprint_sensor((255, 255, 255), (0, 0, 255))

    tpser = tps(time())
    avger = avgtps()
    tpser.send(None)
    avger.send(None)

    for i in range(200):
        t = time()
        pprint_action_move(i-100)
        tps_ = tpser.send(t) # type: ignore
        pprint_time(tps_, avger.send(tps_))
