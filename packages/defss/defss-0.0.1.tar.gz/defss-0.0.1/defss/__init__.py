import keyboard as k
import os
import time

def ts(time):
    time.sleep(time)

def write(text):
    k.write(text)
    time.sleep(0.4)
    k.press_and_release("enter")

def altf4():
    k.press("alt")
    time.sleep(0.3)
    k.press("f4")
    time.sleep(0.2)
    k.release("alt, f4")


def winrun(runtext):
    os.startfile(runtext)

def winsearch(searchtext):
    k.press_and_release("windows")
    time.sleep(0.4 * 2)
    k.write(searchtext)   
    time.sleep(0.3)
    k.press_and_release("enter")

def cmd(cmdtext):
    os.system(cmdtext) 
  