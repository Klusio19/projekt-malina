import RPi.GPIO as GPIO
import time
import light_utils
import w1thermsensor as w1
from colorsys import hsv_to_rgb
from rgbxy import Converter
from rgbxy import GamutC
import urllib3

converter = Converter(GamutC)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # Disable warning about insecure connection
BUTTON = 14


def translate_temp_to_hsv_color(value, temp_min, temp_max, hsv_color_min, hsv_color_max):
    if value <= temp_min:
        return hsv_color_min
    elif value >= temp_max:
        return hsv_color_max
    # Figure out how 'wide' each range is
    temp_span = temp_max - temp_min
    hsv_color_span = hsv_color_max - hsv_color_min

    # Convert the left range into a 0-1 range (float)
    value_scaled = float(value - temp_min) / float(temp_span)

    # Convert the 0-1 range into a value in the right range.
    return hsv_color_min + (value_scaled * hsv_color_span)


def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in hsv_to_rgb(h, s, v))


def hsv2xy(h):
    r, g, b = hsv2rgb(h, 1, 1)
    x, y = converter.rgb_to_xy(r, g, b)
    return x, y


def button_callback(self):
    light_utils.change_power()


def cycle_colors():
    while True:
        if not light_utils.powered_on():
            return
        t = time.localtime()
        temperature = sensor.get_temperature()
        hue_value = translate_temp_to_hsv_color(temperature, 20, 30, 0.65, 0)
        x, y = hsv2xy(hue_value)
        print(f'Temperature: {temperature}')
        print(f'Translated hue (0-1) value based on that temperature: {hue_value}')
        print(f'x and y values: {x}, {y}')
        print(time.strftime("%H:%M:%S", t))
        print('------------------------------------------------------------------------')
        light_utils.change_color(x, y)


def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(BUTTON, GPIO.RISING, button_callback, 500)
    global sensor
    sensor = w1.W1ThermSensor()


def loop():
    while True:
        if light_utils.powered_on():
            cycle_colors()
        time.sleep(0.5)


if __name__ == '__main__':
    try:
        setup()
        loop()

    except KeyboardInterrupt:
        GPIO.cleanup()
        quit()
