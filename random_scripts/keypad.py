# =====================
# Imports
# =====================

from machine import Pin
import time

# =====================
# Static
# =====================

# Keypad Layout
keys = [["1", "2", "3", "A"],
        ["4", "5", "6", "B"],
        ["7", "8", "9", "C"],
        ["*", "0", "#", "D"]]
    
# Pin definitions
rows = [Pin(21, Pin.OUT), Pin(20, Pin.OUT), Pin(19, Pin.OUT), Pin(18, Pin.OUT)]
columns = [Pin(6, Pin.IN, Pin.PULL_UP), Pin(7, Pin.IN, Pin.PULL_UP), Pin(8, Pin.IN, Pin.PULL_UP), Pin(9, Pin.IN, Pin.PULL_UP)]

# =====================
# Global Variables
# =====================

row = 0

# =====================
# Class Definitions
# =====================

class KeyPress:
    def __init__(self, index):
        self.index = index
        self.shouldGo = True
        self.lastFall = time.ticks_ms()
    
    def falling(self, pin):
        timeNow = time.ticks_ms()
        
        if timeNow - self.lastFall > 100:
            self.shouldGo = True

        if self.shouldGo == True:
            self.shouldGo = False
            print(keys[row][self.index])
        
        self.lastFall = timeNow


# =====================
# Intial Setup
# =====================

# Set all the rows to low
for rowIndex in range(4):
    rows[rowIndex].high()

# Set up triggers for column inputs
for colIndex in range(4):
    columns[colIndex].irq(trigger= Pin.IRQ_FALLING, handler=KeyPress(colIndex).falling)

# =====================
# Main Program Thread loop
# =====================

while True:
    # Set each row low for 0.001s and back to high to check columns
    for row in range(4):
        rows[row].low()
        time.sleep(0.001)
        rows[row].high()
        time.sleep(0.001)
