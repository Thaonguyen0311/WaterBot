import RPi.GPIO as GPIO
import time
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone

# =========================
# GPIO SETUP
# =========================
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# INPUT - Water level sensors
LEVEL_25 = 17
LEVEL_50 = 27
LEVEL_75 = 22
LEVEL_100 = 23

# INPUT - Push button
BUTTON = 5

# OUTPUT - LEDs
LED_25 = 6 
LED_50 = 13
LED_75 = 19
LED_100 = 26
BUZ_PIN = 18

inputs = [LEVEL_25, LEVEL_50, LEVEL_75, LEVEL_100, BUTTON]
outputs = [LED_25, LED_50, LED_75, LED_100]

for pin in inputs:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

for pin in outputs:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

buzzer = TonalBuzzer(BUZ_PIN)
print("System started...")
# =========================
# FUNCTIONS
# =========================
def buttonPress():
    button_pressed = not GPIO.input(BUTTON)

    if button_pressed:
        GPIO.output(LED_25, not GPIO.input(LEVEL_25))
        GPIO.output(LED_50, not GPIO.input(LEVEL_50))
        GPIO.output(LED_75, not GPIO.input(LEVEL_75))
        GPIO.output(LED_100, not GPIO.input(LEVEL_100))
    else:
        # Button not pressed → turn off all LEDs
        for led in outputs:
            GPIO.output(led, GPIO.LOW)
def readLevel():
    if not GPIO.input(LEVEL_100):
        return ("=100%")
    elif not GPIO.input(LEVEL_75):
        return(">=75%")
    elif not GPIO.input(LEVEL_50):
        return(">=50%")
    elif not GPIO.input(LEVEL_25):
        return(">=25%")
    else:
        return("ALERT: <25%")
def buzzerAlert(blink_state):
    low_water = GPIO.input(LEVEL_25)
    if low_water:
        if blink_state:
            buzzer.play(Tone(800.0))
        else:
            buzzer.stop()
    else:
        buzzer.stop()
# =========================
# MAIN LOOP
# =========================
try:
    last_toggle=time.time()
    blink_state=True
    last_level = None
    while True:
        now=time.time()
        if now-last_toggle >=3:
            blink_state=not blink_state
            last_toggle=now
        buzzerAlert(blink_state)
        buttonPress()
        level = readLevel()
        if level != last_level:
            print("water level:", level)
            last_level = level
        
        time.sleep(0.05)        

except KeyboardInterrupt:
    print("Exiting program")

finally:
    buzzer.stop()
    GPIO.cleanup()
