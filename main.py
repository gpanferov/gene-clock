#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import time
import threading
import drivers.lcd
import signal
import requests


# Created by Evgeny Panferov
# Time
# TODO: launch as thread

lcd = drivers.lcd.LCD()

def time_thread():
    old_time = -1
    while True:
        time_str = time.strftime("%I:%M;%S %p")
        print time_str
        if old_time != time_str:
            lcd.clear()
            lcd.message(time_str)
            old_time = time_str
        time.sleep(0.1)


# Stock price SPY

# Stock price MSFT
# Why MSFT? Because I don't have to pay for the API calls okay? I already lost
# a lot of money, leave me alone...
def msft_thread():
    while True:
        response = requests.get("https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=MSFT&apikey=demo")
        symbol = response.json()['Global Quote']['01. symbol']
        open = response.json()['Global Quote']['02. open']
        price = response.json()['Global Quote']['05. price']
        pre_close = response.json()['Global Quote']['08. previous close']
        change = response.json()['Global Quote']['09. change']
        change_percent = response.json()['Global Quote']['10. change percent']
        lcd_line_a = symbol + ": " + "{:.6}".format(price) + "    \n"
        lcd_line_b = "pc" + "{:.6}".format(pre_close) + " " + "{:.6}".format(change)
        print lcd_line_a
        print lcd_line_b
        print '.              .'
        lcd.clear()
        lcd.message(lcd_line_a)
        lcd.message(lcd_line_b)
        time.sleep(5)


# Main function
if __name__ == "__main__":
    print str(sys.argv)
    try:
        if len(sys.argv) > 1 and str(sys.argv[1]) == "msft":
            t_thread = threading.Thread(target=msft_thread)
        else:
            t_thread = threading.Thread(target=time_thread)
        t_thread.daemon=True
        t_thread.start()
        signal.pause()
    except KeyboardInterrupt, SystemExit:
        print "Exiting..."
        lcd.clear()
        lcd.destroy()
