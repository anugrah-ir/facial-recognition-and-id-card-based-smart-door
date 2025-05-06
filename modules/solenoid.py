from gpiozero import OutputDevice

pin = 18
relay = OutputDevice(pin, active_high=False, initial_value=False)

def unlock():
    relay.on()

def lock():
    relay.off()