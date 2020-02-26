#import requests
import sys
import time
import threading
import drivers.lcd
import signal

# Created by Evgeny Panferov
# Time
# TODO: launch as thread

lcd = drivers.lcd.LCD()

def time_thread():
    for i in range(900):
        lcd.clear()
        time_val = time.localtime(time.time())
        time_str = str(time_val[3]%12) + ":" + str(time_val[4]) + ";" + str(time_val[5])
        print time_str
        lcd.message("Gene's Clock\n")
        lcd.message(time_str)
        time.sleep(1)


# Stock price SPY


# Main function
if __name__ == "__main__":

    try:
        t_thread = threading.Thread(target=time_thread)
        t_thread.daemon=True
        t_thread.start()
        signal.pause()
    except KeyboardInterrupt, SystemExit:
        print "Exiting..."
        lcd.clear()
        lcd.destroy()
