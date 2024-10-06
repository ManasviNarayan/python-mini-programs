import datetime as dt
from time import sleep
class Clock():

    def display_clock(self):
        print('Ctrl + C to exit')
        today = dt.date.today()
        print(today)
        exit = False
        while not exit:
            now = dt.datetime.strftime(dt.datetime.now(), '%I:%M:%S %p')
            print(now, end='\r')
            sleep(0.2)
            exit = input()

    def set_timer(self, hours, minutes, seconds):
        now = dt.datetime.now() + dt.timedelta(seconds=0.5)
        target = now + dt.timedelta(hours=hours,
                                    minutes=minutes, 
                                    seconds=seconds)
        while now < target:
            timer = target-now
            print(str(timer).split('.')[0], end='\r')
            now = dt.datetime.now()
            sleep(0.1)
        print('time up')