class Printer:
    def print(self, str, row=1, col=1, end=''):
        print("\033[{};{}H".format(row, col), end='')
        print(str, end=end)

    def print_action(self, str):
        print("\033[2;1H", end='')
        print("{:37}".format(str))
        print("\033[4;3H")

    def print_action_move(self, lval, rval, z):
        print("\033[2;1H", end='')
        print("{} {}".format(lval, rval))

    def print_args(self, args):
        print("\033[1;1H")
        print("".join(["{}: {} ".format(k, v) for k, v, in args.items()]))

    def print_color(self, color):
        pass

    def print_rawcolor(self, left, right):
        pass

    def print_errors(self, left, right):
        pass

    def print_vals(self, left, right):
        pass

    def print_time(self, tps, avg):
        print("\033[3;1H")
        print("tps: {:>5.2f} avg: {:>5.2f}".format(tps, avg))
        print("\033[4;3H")
    
    def jump_prompt(self):
        print("\033[4;3H", end='')

    def print_layout(self):
        print("\033[2J")
        print("\033[0;0H", end='')
        window = "".join([
            '\n',                                # 1
            '\n',                                # 2
            '\n',                                # 3
            '>                               ']) # 4
        print(window)
