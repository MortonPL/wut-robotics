import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--mode', action='store', nargs='?',
                    choices=['black', 'color'], default='black', help='mode of action')
parser.add_argument('--def-speed', action='store', nargs='?',
                    default=10, type=int, help='default speed')
parser.add_argument('-p', '--printer', action='store', nargs='?',
                    choices=['mini', 'thin', 'pretty'], default='mini', help='extended (slow) diagnostics')
args = vars(parser.parse_args())

if args['printer'] == 'pretty':
    from prettyprinter import Printer
elif args['printer'] == 'thin':
    from thinprinter import Printer
else:
    from minprinter import Printer

p = Printer()
p.print_layout()
p.print_args(args)
p.jump_prompt()
