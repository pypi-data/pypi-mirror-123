import keyboard as k
import os
import time
#setting time
def ts(time):
    time.sleep(time)
#writing stuff
def write(text):
    k.write(text)
    time.sleep(0.4)
    k.press_and_release("enter")
#quick exit(alt+f4)
def altf4(keys):
    k.press("alt")
    time.sleep(0.3)
    k.press("f4")
    time.sleep(0.2)
    k.release("alt, f4")

#Run search
def winrun(runtext):
    os.startfile(runtext)
#windows search bar
def winsearch(searchtext):
    k.press_and_release("windows")
    time.sleep(0.4 * 2)
    k.write(searchtext)   
    time.sleep(0.3)
    k.press_and_release("enter")
#command prompt 
def cmd(cmdtext):
    os.system(cmdtext) 
#any key to be the same
def key(any):
    k.press_and_release("key")
    time.sleep(3)
    k.press_and_release("enter")