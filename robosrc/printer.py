#            |0-4       |4-8       |8-12     |12-16   |16-20
ARROWS_FL = ['△△△△▲', '△△△▲▲', '△△▲▲▲', '△▲▲▲▲', '▲▲▲▲▲']
ARROWS_FR = ['▲△△△△', '▲▲△△△', '▲▲▲△△', '▲▲▲▲△', '▲▲▲▲▲']
ARROWS_BL = ['▽▽▽▽▼', '▽▽▽▼▼', '▽▽▼▼▼', '▽▼▼▼▼', '▼▼▼▼▼']
ARROWS_BR = ['▼▽▽▽▽', '▼▼▽▽▽', '▼▼▼▽▽', '▼▼▼▼▽', '▼▼▼▼▼']

def pprint(str, row=1, col=1, end=''):
    print("\033[{};{}H".format(row, col), end='')
    print(str, end=end)
    print("\033[12;3H")

def pprint_action(str):
    pprint("{:37}".format(str), row=10, col=3)

def pprint_action_move(lval, rval, z):

    il = min(int(abs(lval))//z, len(ARROWS_FL) - 1)
    ir = min(int(abs(rval))//z, len(ARROWS_FR) - 1)
    if lval < 0:
        lstring = "{}".format(ARROWS_BL[il])
    else:
        lstring = "{}".format(ARROWS_FL[il])
    if rval < 0:
        rstring = "{}".format(ARROWS_BR[ir])
    else:
        rstring = "{}".format(ARROWS_FR[ir])
    pprint_action("{}={}".format(lstring, rstring))

def pprint_args(mode, divspeed, minspeed, defspeed):
    pprint("mode: {} div: {} min: {} def: {}"
        .format(mode, divspeed, minspeed, defspeed), row=2, col=3)

def pprint_color(color):
    pprint(color, row=4, col=9)

def pprint_rawcolor(left, right):
    print("\033[4;8H", end='')
    print("\u001b[4m\u001b[31m{:3}\u001b[0m \u001b[4m\u001b[32m{:3}\u001b[0m \u001b[4m\u001b[34m{:3}\u001b[0m"
        .format(left[0], left[1], left[2]), end='')
    print("\033[4;22H", end='')
    print("\u001b[4m\u001b[31m{:3}\u001b[0m \u001b[4m\u001b[32m{:3}\u001b[0m \u001b[4m\u001b[34m{:3}\u001b[0m"
        .format(right[0], right[1], right[2]), end='')
    print("\033[12;3H")

def pprint_errors(left, right):
    print("\033[6;8H", end='')
    print("\u001b[4m{:11.7f}\u001b[0m".format(left), end='')
    print("\033[6;22H", end='')
    print("\u001b[4m{:11.7f}\u001b[0m".format(right), end='')
    print("\033[12;3H")

def pprint_vals(left, right):
    print("\033[8;8H", end='')
    print("\u001b[4m{:11.7f}\u001b[0m".format(left), end='')
    print("\033[8;22H", end='')
    print("\u001b[4m{:11.7f}\u001b[0m".format(right), end='')
    print("\033[12;3H")

def pprint_time(tps, avg):
    pprint("\u001b[4m{:>5.2f}\u001b[0m".format(tps), row=2, col=42)
    pprint("\u001b[4m{:>5.2f}\u001b[0m".format(avg), row=3, col=42)

def pprint_layout():
    print("\033[2J")
    print("\033[0;0H", end='')
    window = "".join([
        #║ 3                ║ 22                ║ 42
        '╔═ ARGUMENTS ══════════════════════════╦═ TIME ════╗\n', # 1
        '║                                      ║ __.__ TPS ║\n', # 2
        '╠═ COLORS ═════════╦═══════════════════╣ __.__ AVG ║\n', # 3
        '║ LEFT ___ ___ ___ ║ ___ ___ ___ RIGHT ╠═══════════╝\n', # 4
        '╠═ ERRORS ═════════╬═══════════════════╣\n',             # 5
        '║ LEFT ___._______ ║ ___._______ RIGHT ║\n',             # 6
        '╠═ CONTROLLER ═════╬═══════════════════╣\n',             # 7
        '║ LEFT ___._______ ║ ___._______ RIGHT ║\n',             # 8
        '╠═ ACTION ═════════╩═══════════════════╣\n',             # 9
        '║                                      ║\n',             # 10
        '╚══════════════════════════════════════╝\n',             # 11
        '>                               '])
    print(window)


if __name__ == "__main__":
    from time import sleep, time
    from clock import tps, avgtps

    pprint_layout()
    pprint_args("black", 10, 1, 3)
    # pprint_color("WHITE ")
    pprint_errors(0, 10)
    pprint_vals(0.11, 10.9438)
    pprint_rawcolor((255, 255, 255), (0, 0, 255))

    scaled = (100 / 5)
    z = int(scaled / 5)

    tpser = tps(time())
    avger = avgtps()
    tpser.send(None)
    avger.send(None)

    for i in range(200):
        j = (i - 100)/5
        t = time()
        pprint_action_move(j, -j, z)
        tps_ = tpser.send(t) # type: ignore
        pprint_time(tps_, avger.send(tps_))
        sleep(0.1)
