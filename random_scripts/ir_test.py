import gc
import time
from machine import Pin, freq
from ir_rx.nec import NEC_16

addressButtons = {
    0x0000: {
        0x45: "1", 0x46: "2", 0x47: "3",
        0x44: "4", 0x40: "5", 0x43: "6",
        0x07: "7", 0x15: "8", 0x09: "9",
        0x16: "*", 0x19: "0", 0x0d: "#",
                   0x18: "^",
        0x08: "<", 0x1c: "OK",0x5a: ">",
                   0x52: "v"
    }}

p = Pin(16, Pin.IN)

def cb(data, addr, ctrl):
    if data >= 0:  # Ignore NEC repeat codes
        if addr in addressButtons:
            buttons = addressButtons[addr]
            if data in buttons:
                print("Received Button: {}".format(buttons[data]))
ir = NEC_16(p, cb)

while True:
    #print('running')
    time.sleep(5)
    gc.collect()
