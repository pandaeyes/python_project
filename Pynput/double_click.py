import threading
import time
import datetime
from pynput.mouse import Button, Controller

class MyThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        print ("start thread:")
        self.DoSomething()
        # self.DoMove()
        print ("end thread:")

    def DoSomething(self):
        # self.TimerSleep()
        mouse = Controller()
        while 1:
            mouse.position = (152, 600)
            mouse.click(Button.left, 1)
            time.sleep(5)
            mouse.position = (152, 660)
            mouse.click(Button.left, 1)
            time.sleep(10)

    def DoMove(self):
        mouse = Controller()
        while 1:
            mouse.move(2, 0)
            time.sleep(5)
            mouse.move(-2, 0)
            time.sleep(10)



    def TimerSleep(self):
        d1 = datetime.datetime.now()
        d2 = datetime.datetime(d1.year, d1.month, d1.day, 13, 55, 1)
        # d2 = datetime.datetime(d1.year, d1.month, d1.day, 18, 55, 1)
        sec = (d2 - d1).seconds
        time.sleep(sec)

if __name__ == "__main__":
    thread1 = MyThread()
    thread1.start()
