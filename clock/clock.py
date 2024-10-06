import datetime as dt
import threading
from time import sleep


class Clock():

    def __init__(self):
        self.stop_event = threading.Event()
        
    def display_clock(self):
        print('Press Ctrl + C to exit')
        today = dt.date.today()
        print(today)
        try:
            while True:
                now = dt.datetime.strftime(dt.datetime.now(), '%I:%M:%S %p')
                print(now, end='\r')
                sleep(0.2)
        except KeyboardInterrupt:
            print('\nExiting')

    def set_timer(self, hours, minutes, seconds):
        now = dt.datetime.now() + dt.timedelta(seconds=0.5)
        target = now + dt.timedelta(hours=hours,
                                    minutes=minutes, 
                                    seconds=seconds)
        try:
            while now < target:
                timer = target-now
                print(str(timer).split('.')[0], end='\r')
                now = dt.datetime.now()
                sleep(0.1)
            print('time up')
        except KeyboardInterrupt:
            print('timer stopped\n', str(timer).split('.')[0])


    def _print_stopwatch(self,start):
        while not self.stop_event.is_set():
            timer = dt.datetime.now() - start
            print(str(timer), end='\r')
            sleep(0.01)


    def _print_lap(self,start):
        while not self.stop_event.is_set():
            try:
                a = input()
            except EOFError:
                break
            timer = dt.datetime.now() - start
            print('lap: ', str(timer), end='\n')

    def start_stopwatch(self):
        self.stop_event.clear()
        start = dt.datetime.now()
        print("Press Enter to mark a lap. Press Ctrl+C to quit.")
        t1 = threading.Thread(target=self._print_stopwatch, args=(start,))
        t2 = threading.Thread(target=self._print_lap, args=(start,))
        t1.start()
        t2.start()
        try:
            while True:
                sleep(0.001)
        except KeyboardInterrupt:
            self.stop_event.set()
            print("\nStopwatch stopped.")