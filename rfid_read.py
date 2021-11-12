from rfid.mfrc522 import MFRC522
from machine import Pin, PWM
from time import sleep

buzzer = Pin(17, Pin.OUT)

def Buzz():
    buzzer.high()
    sleep(0.1)
    buzzer.low()

reader = MFRC522(spi_id=1,sck=10,miso=12,mosi=11,cs=14,rst=15)

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
                print("Card detected {}  uid={}".format(hex(int.from_bytes(bytes(uid),"little",False)).upper(),reader.tohexstring(uid)))
                defaultKey = [255,255,255,255,255,255]
                
                absoluteBlock = 0
                status1 = reader.authKeys(uid,absoluteBlock,defaultKey)
                status2, block = reader.read(absoluteBlock)
                for value in block:
                    print(str(int(value)) + "|",end="")
                print("\n======")
                for value in block:
                    print(chr(int(value)),end="")
                print("\n======")    
                #print(chr(65) + " | " + str(ord("A")))
                
                #
                print("Done")
                Buzz()
                PreviousCard = uid
            
            else:
                pass
        else:
            PreviousCard=[0]    
except KeyboardInterrupt:
    pass