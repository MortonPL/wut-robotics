ARROWS_L = ['    ◁','   ◁◁','  ◁◁◁',' ◁◁◁◁','◁◁◁◁◁','◁◁◁◁◀','◁◁◁◀◀','◁◁◀◀◀','◁◀◀◀◀','◀◀◀◀◀']
ARROWS_R = ['▷    ','▷▷   ','▷▷▷  ','▷▷▷▷ ','▷▷▷▷▷','▶▷▷▷▷','▶▶▷▷▷','▶▶▶▷▷','▶▶▶▶▷','▶▶▶▶▶']

def pprint(str, row=1, col=1, end=''):
    print("\033[{0};{1}H".format(row, col), end='')
    print(str, end=end)
    print("\033[12;3H")

def pprint_args(slow, normal, high, rot):
    pprint("lo:{0} med:{1} hi:{2} rot:{3}"
        .format(slow, normal, high, rot), row=2, col=3)

def pprint_color(color):
    pprint("I SEE {0}"
        .format(color), row=4, col=3)

def pprint_sensor(left, right):
    print("\033[6;8H", end='')
    print("\u001b[4m\u001b[31m{0:3}\u001b[0m \u001b[4m\u001b[32m{1:3}\u001b[0m \u001b[4m\u001b[34m{2:3}\u001b[0m"
        .format(left[0], left[1], left[2]), end='')
    print("\033[6;22H", end='')
    print("\u001b[4m\u001b[31m{0:3}\u001b[0m \u001b[4m\u001b[32m{1:3}\u001b[0m \u001b[4m\u001b[34m{2:3}\u001b[0m"
        .format(right[0], right[1], right[2]), end='')
    print("\033[12;3H")

def pprint_action(str):
    pprint(str, row=10, col=3)

def pprint_action_move(val):
    val = min(max(val, -99), 99)
    if val > 0:
        pprint_action("STEERING RIGHT {1} {0}".format(val, ARROWS_R[val//10]))
    elif val < 0:
        pprint_action("STEERING LEFT  {1} {0}".format(abs(val), ARROWS_L[abs(val)//10]))
    else:
        pprint_action("GOING FORWARD       ")

def pprint_layout():
    print("\033[2J")
    print("\033[0;0H", end='')
    window = "".join([
        '╔═ ARGUMENTS ══════════════════════════╗\n', # 1
        '║                                      ║\n', # 2
        '╠═ SENSORS ════════════════════════════╣\n', # 3
        '║                                      ║\n', # 4
        '╟──────────────────┬───────────────────╢\n', # 5
        '║ LEFT             │             RIGHT ║\n', # 6
        '╠═ CONTROLLER ═════╧═══════════════════╣\n', # 7
        '║                                      ║\n', # 8
        '╠═ ACTION ═════════════════════════════╣\n', # 9
        '║                                      ║\n', # 10
        '╚══════════════════════════════════════╝\n', # 11
        '>                               '])
    print(window)


if __name__ == "__main__":
    from time import sleep

    pprint_layout()
    pprint_args(10, 20, 30, 0.01)
    pprint_color("WHITE")
    pprint_sensor((255, 255, 255), (0, 0, 255))
    pprint_action_move(1)
    for i in range(200):
        pprint_action_move(i-100)
        sleep(0.1)
