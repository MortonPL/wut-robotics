class Printer:
    #            |0-4       |4-8       |8-12     |12-16   |16-20
    ARROWS_FL = ['△△△△▲', '△△△▲▲', '△△▲▲▲', '△▲▲▲▲', '▲▲▲▲▲']
    ARROWS_FR = ['▲△△△△', '▲▲△△△', '▲▲▲△△', '▲▲▲▲△', '▲▲▲▲▲']
    ARROWS_BL = ['▽▽▽▽▼', '▽▽▽▼▼', '▽▽▼▼▼', '▽▼▼▼▼', '▼▼▼▼▼']
    ARROWS_BR = ['▼▽▽▽▽', '▼▼▽▽▽', '▼▼▼▽▽', '▼▼▼▼▽', '▼▼▼▼▼']

    def print(self, str, row=1, col=1, end=''):
        print("\033[{};{}H".format(row, col), end='')
        print(str, end=end)
        print("\033[12;3H")

    def print_action(self, str):
        self.print("{:37}".format(str), row=10, col=3)

    def print_action_move(self, lval, rval, z):

        il = min(int(abs(lval))//z, len(self.ARROWS_FL) - 1)
        ir = min(int(abs(rval))//z, len(self.ARROWS_FR) - 1)
        if lval < 0:
            lstring = "{}".format(self.ARROWS_BL[il])
        else:
            lstring = "{}".format(self.ARROWS_FL[il])
        if rval < 0:
            rstring = "{}".format(self.ARROWS_BR[ir])
        else:
            rstring = "{}".format(self.ARROWS_FR[ir])
        self.print_action("{}={}".format(lstring, rstring))

    def print_args(self, args):
        self.print(print("".join(["{}: {} ".format(k, v) for k, v, in args.items()])), row=2, col=3)

    def print_color(self, color):
        self.print(color, row=4, col=9)

    def print_rawcolor(self, left, right):
        print("\033[4;8H", end='')
        print("\u001b[4m\u001b[31m{:3}\u001b[0m \u001b[4m\u001b[32m{:3}\u001b[0m \u001b[4m\u001b[34m{:3}\u001b[0m"
            .format(left[0], left[1], left[2]), end='')
        print("\033[4;22H", end='')
        print("\u001b[4m\u001b[31m{:3}\u001b[0m \u001b[4m\u001b[32m{:3}\u001b[0m \u001b[4m\u001b[34m{:3}\u001b[0m"
            .format(right[0], right[1], right[2]), end='')
        print("\033[12;3H")

    def print_errors(self, left, right):
        print("\033[6;8H", end='')
        print("\u001b[4m{:11.7f}\u001b[0m".format(left), end='')
        print("\033[6;22H", end='')
        print("\u001b[4m{:11.7f}\u001b[0m".format(right), end='')
        print("\033[12;3H")

    def print_vals(self, left, right):
        print("\033[8;8H", end='')
        print("\u001b[4m{:11.7f}\u001b[0m".format(left), end='')
        print("\033[8;22H", end='')
        print("\u001b[4m{:11.7f}\u001b[0m".format(right), end='')
        print("\033[12;3H")

    def print_time(self, tps, avg):
        self.print("\u001b[4m{:>5.2f}\u001b[0m".format(tps), row=2, col=42)
        self.print("\u001b[4m{:>5.2f}\u001b[0m".format(avg), row=3, col=42)

    def jump_prompt(self):
        print("\033[12;3H", end='')

    def print_layout(self):
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
