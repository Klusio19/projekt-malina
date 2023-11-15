import gpiozero
import time
from datetime import datetime
from numpy import arange
import light_utils
import w1thermsensor as w1
from colorsys import hsv_to_rgb
from rgbxy import Converter
from rgbxy import GamutC
import urllib3

converter = Converter(GamutC)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # Disable warning about insecure connection
power_button = gpiozero.Button(14)
temp_to_colors_button = gpiozero.Button(15)
colors_button = gpiozero.Button(4)
program_running_blue_led = gpiozero.LED(21)
temp_to_colors_green_led = gpiozero.LED(20)
power_led = gpiozero.LED(19)
colors_led = gpiozero.LED(16)
powered_on_flag = False
temp_to_colors_on_flag = False


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


def power_button_callback(self):
    global powered_on_flag, temp_to_colors_on_flag
    if light_utils.powered_on():
        terminate_displaying()
        powered_on_flag = False
        temp_to_colors_on_flag = False
    else:
        powered_on_flag = True
    light_utils.change_power()


def cycle_colors():
    while True:
        for j in arange(0, 1.01, 0.01):
            # TODO
            # if break_from_function:
            #     return
            x, y = hsv2xy(j)
            light_utils.change_color(x, y)


def temp_to_colors_cycle():
    if (not powered_on_flag) or (not temp_to_colors_on_flag):
        return
    temp_to_colors_green_led.on()
    while True:
        if (not powered_on_flag) or (not temp_to_colors_on_flag):
            return
        current_time = datetime.now()
        temperature = sensor.get_temperature()
        hue_value = translate_temp_to_hsv_color(temperature, 20, 30, 0.65, 0)
        x, y = hsv2xy(hue_value)
        print("Time " + current_time.strftime('%H:%M:%S.%f'))
        print(f'Temperature: {temperature}')
        print(f'Translated hue (0-1) value based on that temperature: {hue_value}')
        print(f'x and y values: {x}, {y}')
        print('-------------------------------------------------------------------------')
        light_utils.change_color(x, y)


def temp_to_colors_cycle_button_callback(self):
    if not powered_on_flag:
        return
    global temp_to_colors_on_flag
    temp_to_colors_on_flag = not temp_to_colors_on_flag
    if temp_to_colors_on_flag:
        temp_to_colors_green_led.on()
    else:
        temp_to_colors_green_led.off()


def terminate_displaying():
    temp_to_colors_green_led.off()


def setup():
    global powered_on_flag
    if light_utils.powered_on():
        powered_on_flag = True
        power_led.on()
    program_running_blue_led.on()
    temp_to_colors_button.when_activated = temp_to_colors_cycle_button_callback
    power_button.when_activated = power_button_callback
    global sensor
    sensor = w1.W1ThermSensor()


def loop():
    while True:
        if not powered_on_flag:
            terminate_displaying()
            power_led.off()
        else:
            power_led.on()
        if temp_to_colors_on_flag:
            temp_to_colors_cycle()
        time.sleep(0.1)


if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        quit()
