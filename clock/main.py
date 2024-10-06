import argparse
from clock import Clock


parser = argparse.ArgumentParser(description='Clock, Timer, and Stopwatch')
group = parser.add_mutually_exclusive_group()
group.add_argument('-c', '--clock', action='store_true' )
group.add_argument('-t', '--timer', nargs=3, type=int)

args = parser.parse_args()
clock = Clock()

if args.clock:
    clock.display_clock()
elif args.timer:
    clock.set_timer(args.timer[0], args.timer[1], args.timer[2])