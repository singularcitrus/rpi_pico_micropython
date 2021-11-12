from rfid.mfrc522 import MFRC522
from machine import Pin, PWM, I2C
from sys import exit
from time import sleep
from lcd import I2cLcd

buzzer = Pin(17, Pin.OUT)

def Buzz():
    #buzzer.high()
    sleep(0.1)
    #buzzer.low()
    
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
lcd.clear()
lcd.backlight_on()

'''
BE AWARE that sectors(3,7,11,15,...,63) are access block.
if you want to change  (sector % 4) == 3 you should
know how keys and permission work!
'''

stringToWrite="Hello World"
writeBlock=62

if len(stringToWrite) > 16:
    print("String too Long")
    exit()

if writeBlock % 4 == 3:
    print("No, we can't write to access blocks")
    exit()

def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = "%02X" % i + mystring
    return mystring

reader = MFRC522(spi_id=1,sck=10,miso=12,mosi=11,cs=14,rst=15)

print("")
print("Please place card on reader")
print("")

key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

try:
    while True:
        reader.init()
        stat, tag_type = reader.request(reader.REQIDL)
        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            if stat == reader.OK:
                #print(uid)
                print("Card detected %s" % uidToString(uid))
                #reader.MFRC522_DumpClassic1K(uid,keyA=key)
                absoluteBlock=writeBlock
                valueStringArray= [char for char in stringToWrite]
                
                value=[]
                for item in valueStringArray:
                    value.append(ord(item))
                
                if len(value) > 16:
                    print("String too Long")
                    break
                while len(value) < 16:
                    value.append(0)
                
                print("Writing to card:")
                print(stringToWrite)
                print(valueStringArray)
                print(value)
            
                status = reader.auth(reader.AUTHENT1A, absoluteBlock, key, uid)
                if status == reader.OK:
                    status = reader.write(absoluteBlock,value)
                    if status == reader.OK:
                        print("Done")
                        Buzz()
                        reader.MFRC522_DumpClassic1K(uid,keyA=key)
                    else:
                        print("unable to write")
                else:
                    print("Authentication error for writing")
                break
except KeyboardInterrupt:
    print("Bye")