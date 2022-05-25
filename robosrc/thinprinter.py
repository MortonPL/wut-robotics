class Printer:

    def print(self, str, row=1, col=1, end=''):
        print("\033[{};{}H".format(row, col), end='')
        print(str, end=end)
        print("\033[12;3H")

    def print_args(self, args):
        print("\033[1;11H", end='')
        print("".join(["{}: {} ".format(k, v) for k, v, in args.items()]))

    def print_time(self, tps, avg):
        print("\033[2;12H", end='')
        print("\u001b[4m{:5.2f}\u001b[0m".format(tps), end='')
        print("\033[2;26H", end='')
        print("\u001b[4m{:5.2f}\u001b[0m".format(avg))

    def print_rawcolor(self, left, right):
        print("\033[3;12H", end='')
        print("\u001b[4m\u001b[31m{:3}\u001b[0m \u001b[4m\u001b[32m{:3}\u001b[0m \u001b[4m\u001b[34m{:3}\u001b[0m"
            .format(left[0], left[1], left[2]), end='')
        print("\033[3;26H", end='')
        print("\u001b[4m\u001b[31m{:3}\u001b[0m \u001b[4m\u001b[32m{:3}\u001b[0m \u001b[4m\u001b[34m{:3}\u001b[0m"
            .format(right[0], right[1], right[2]))

    def print_errors(self, left, right):
        print("\033[4;12H", end='')
        print("\u001b[4m{:11.7f}\u001b[0m".format(left), end='')
        print("\033[4;26H", end='')
        print("\u001b[4m{:11.7f}\u001b[0m".format(right))

    def print_vals(self, left, right):
        print("\033[5;12H", end='')
        print("\u001b[4m{:11.7f}\u001b[0m".format(left), end='')
        print("\033[5;26H", end='')
        print("\u001b[4m{:11.7f}\u001b[0m".format(right))

    def print_action(self, str):
        print("\033[6;12H", end='')
        print("{:29}".format(str))
        print("\033[7;3H")

    def print_action_move(self, lval, rval, z):
        pass

    def jump_prompt(self):
        print("\033[7;3H", end='')

    def print_layout(self):
        print("\033[2J")
        print("\033[0;0H", end='')
        window = "".join([
            #           ║ 12          ║ 26
            'ARGUMENTS                           \n', # 1
            'TPS/AVG    __.__       | __.__      \n', # 2
            'COLORS     ___ ___ ___ | ___ ___ ___\n', # 3
            'ERRORS     ___._______ | ___._______\n', # 4
            'CONTROLLER ___._______ | ___._______\n', # 5
            'ACTION                              \n', # 6
            '>                               '])      # 7
        print(window)
