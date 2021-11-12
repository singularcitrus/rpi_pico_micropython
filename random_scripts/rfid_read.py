from rfid.mfrc522 import MFRC522
from machine import Pin, PWM, I2C
from time import sleep
from lcd import I2cLcd

buzzer = Pin(17, Pin.OUT)

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
lcd.clear()
lcd.backlight_on()

lcd.move_to(2,0)
lcd.putstr("PRESENT CARD")

def Buzz(t=0.1):
    #buzzer.high()
    sleep(t)
    #buzzer.low()

reader = MFRC522(spi_id=1,sck=10,miso=12,mosi=11,cs=14,rst=15)

key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

print("")
print("Please place card on reader")
print("")

PreviousCard = [0]

try:
    while True:
        reader.init()
        stat, tag_type = reader.request(reader.REQIDL)
        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            
            if uid == PreviousCard:
                continue
            
            if stat == reader.OK:
                lcd.clear()
                lcd.move_to(0,0)
                lcd.putstr("Card {}".format(hex(int.from_bytes(bytes(uid),"little",False)).upper()))
                
                absoluteBlock = 62
                status1 = reader.authKeys(uid,absoluteBlock,key)
                status2, block = reader.read(absoluteBlock)
                if len(block) == 16:
                    Buzz()
                    finalString = ""
                    for value in block:
                        charInt = int(value)
                        if charInt > 0:
                            finalString = finalString + chr(charInt)
                    lcd.move_to(0,1)
                    if len(finalString) > 0:
                        lcd.putstr(finalString)
                    else:
                        lcd.move_to(7,1)
                        lcd.putstr("[[EMPTY]]")
                    PreviousCard = uid
                else:
                    lcd.clear()
                    lcd.move_to(2,0)
                    lcd.putstr("READ FAILED")
                    Buzz(t=0.5)
            else:
                pass
        else:
            PreviousCard=[0]
except KeyboardInterrupt:
    pass