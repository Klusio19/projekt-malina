import light_utils
import color_conversions
import gpiozero
import time
from datetime import datetime
from numpy import arange
import w1thermsensor as w1
import urllib3
import os


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # Disables warning about insecure connection
power_button = gpiozero.Button(14)
temperature_to_colors_button = gpiozero.Button(15)
colors_button = gpiozero.Button(4, hold_time=2)
program_running_blue_led = gpiozero.LED(21)
temperature_to_colors_green_led = gpiozero.LED(20)
power_red_led = gpiozero.LED(19)
cycling_colors_yellow_led = gpiozero.PWMLED(16)
powered_on_flag = False
temperature_to_colors_is_on_flag = False
cycling_colors_is_on_flag = False

static_color_index = 0
colors_button_held = False


static_xy_colors = ((0.692, 0.308),
                    (0.6171560730237003, 0.364204634817451),
                    (0.43338253903636664, 0.5022108135972112),
                    (0.2422358728563172, 0.6457539039086659),
                    (0.17000000000000004, 0.7),
                    (0.16746588626319595, 0.6028092849178674),
                    (0.16067246865460033, 0.3422617389882013),
                    (0.15508737697587785, 0.1280570463689621),
                    (0.153, 0.048),
                    (0.20941762533989733, 0.0752144389394681),
                    (0.383316077163507, 0.15909866430892733),
                    (0.5867502773676304, 0.2572301894537735))


def translate_temperature_to_hsv_color(value, temp_min, temp_max, hsv_color_min, hsv_color_max):
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


def power_button_pressed(self):
    global powered_on_flag, temperature_to_colors_is_on_flag
    if light_utils.powered_on():
        terminate_displaying()
        powered_on_flag = False
        temperature_to_colors_is_on_flag = False
    else:
        powered_on_flag = True
    light_utils.change_power()


def cycle_colors():
    global colors_button_held, cycling_colors_is_on_flag, temperature_to_colors_is_on_flag
    if not powered_on_flag:
        return
    temperature_to_colors_green_led.off()
    cycling_colors_yellow_led.pulse(fade_in_time=0.5, fade_out_time=0.5)
    colors_button_held = True
    cycling_colors_is_on_flag = True
    temperature_to_colors_is_on_flag = False
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        for j in arange(0, 1.01, 0.01):
            if (not powered_on_flag) or (not cycling_colors_is_on_flag):
                return
            x, y = color_conversions.hsv2xy(j)
            current_time = datetime.now()
            print("Time " + current_time.strftime('%H:%M:%S.%f'))
            print(f'x and y values: {x}, {y}')
            print('----------------------------------------------')
            light_utils.change_color(x, y)


def cycle_colors_button_released():
    global colors_button_held
    if not colors_button_held:
        cycle_static_colors()
    colors_button_held = False


def temperature_to_colors_cycle():
    if (not powered_on_flag) or (not temperature_to_colors_is_on_flag):
        return
    temperature_to_colors_green_led.on()
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        if (not powered_on_flag) or (not temperature_to_colors_is_on_flag):
            return
        current_time = datetime.now()
        temperature = sensor.get_temperature()
        hue_value = translate_temperature_to_hsv_color(temperature, 20, 30, 0.65, 0)
        x, y = color_conversions.hsv2xy(hue_value)
        print("Time " + current_time.strftime('%H:%M:%S.%f'))
        print(f'Temperature: {temperature}')
        print(f'Translated hue (0-1) value based on that temperature: {hue_value}')
        print(f'x and y values: {x}, {y}')
        print('-------------------------------------------------------------------------')
        light_utils.change_color(x, y)


def temperature_to_colors_cycle_button_pressed(self):
    global temperature_to_colors_is_on_flag, cycling_colors_is_on_flag
    if not powered_on_flag:
        return
    temperature_to_colors_is_on_flag = not temperature_to_colors_is_on_flag
    cycling_colors_yellow_led.off()
    temperature_to_colors_green_led.toggle()
    if cycling_colors_is_on_flag:
        cycling_colors_is_on_flag = False


def terminate_displaying():
    global temperature_to_colors_is_on_flag, powered_on_flag, cycling_colors_is_on_flag
    temperature_to_colors_is_on_flag = False
    powered_on_flag = False
    cycling_colors_is_on_flag = False

    power_red_led.off()
    temperature_to_colors_green_led.off()
    cycling_colors_yellow_led.off()


def cycle_static_colors():
    global static_color_index, static_xy_colors, colors_button_held, cycling_colors_is_on_flag, temperature_to_colors_is_on_flag
    temperature_to_colors_green_led.off()
    cycling_colors_yellow_led.on()
    cycling_colors_yellow_led.off()
    time.sleep(0.1)
    cycling_colors_yellow_led.on()
    if cycling_colors_is_on_flag:
        cycling_colors_is_on_flag = False
    if temperature_to_colors_is_on_flag:
        temperature_to_colors_is_on_flag = False
    x, y = static_xy_colors[static_color_index][0], static_xy_colors[static_color_index][1]
    light_utils.change_color(x, y)
    if static_color_index >= 11:
        static_color_index = 0
    else:
        static_color_index += 1


def setup():
    global powered_on_flag, sensor
    program_running_blue_led.on()
    if light_utils.powered_on():
        powered_on_flag = True
        power_red_led.on()

    power_button.when_activated = power_button_pressed
    temperature_to_colors_button.when_activated = temperature_to_colors_cycle_button_pressed
    colors_button.when_held = cycle_colors
    colors_button.when_deactivated = cycle_colors_button_released
    sensor = w1.W1ThermSensor()


def loop():
    while True:
        if not powered_on_flag:  # checking in loop, in case of powering the light off, with external source
            terminate_displaying()
            continue
        else:
            power_red_led.on()
        if temperature_to_colors_is_on_flag:
            temperature_to_colors_cycle()
        if cycling_colors_is_on_flag:
            cycle_colors()
        time.sleep(0.1)


if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        quit()
