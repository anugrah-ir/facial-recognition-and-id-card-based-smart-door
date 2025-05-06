from RPLCD.i2c import CharLCD

I2C_ADDRESS = 0x27
lcd = CharLCD('PCF8574', I2C_ADDRESS)

def show_text(text, line):
    lcd.cursor_pos = (line, 0)
    lcd.write_string(text)

def clear():
    lcd.clear()