import argparse
from clock import Clock


parser = argparse.ArgumentParser(description='Clock, Timer, and Stopwatch')
group = parser.add_mutually_exclusive_group()
group.add_argument('-c', '--clock', action='store_true', help='Display the current clock')
group.add_argument('-t', '--timer', nargs=3, type=int, help='Set a timer with hours, minutes, and seconds (e.g., -t 1 30 0)')
group.add_argument('-sw', '--stopwatch', action='store_true', help='Start a stopwatch')


args = parser.parse_args()
clock = Clock()

if args.clock:
    clock.display_clock()
elif args.timer:
    clock.set_timer(args.timer[0], args.timer[1], args.timer[2])
elif args.stopwatch:
    clock.start_stopwatch()