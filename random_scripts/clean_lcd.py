from machine import I2C, Pin
from lcd import I2cLcd
from rfid.mfrc522 import MFRC522

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
lcd.backlight_off()
lcd.putstr("Hello World")
lcd.clear()

reader = MFRC522(spi_id=1,sck=10,miso=12,mosi=11,cs=14,rst=15)
reader.antenna_on(on=False)