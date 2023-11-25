import os
from time import sleep
from datetime import datetime
from numpy import arange
import color_conversions
import light_utils
import setup

static_color_index = 0


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


def temperature_to_colors_cycle():
    if (not setup.powered_on_flag) or (not setup.temperature_to_colors_is_on_flag):
        return
    setup.green_led.on()
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        if (not setup.powered_on_flag) or (not setup.temperature_to_colors_is_on_flag):
            return
        current_time = datetime.now()
        temperature = setup.sensor.get_temperature()
        hue_value = translate_temperature_to_hsv_color(temperature, 20, 30, 0.65, 0)
        x, y = color_conversions.hsv2xy(hue_value)
        print("Time " + current_time.strftime('%H:%M:%S.%f'))
        print(f'Temperature: {temperature}')
        print(f'Translated hue (0-1) value based on that temperature: {hue_value}')
        print(f'x and y values: {x}, {y}')
        print('-------------------------------------------------------------------------')
        light_utils.change_color(x, y)


def terminate_displaying():
    setup.temperature_to_colors_is_on_flag = False
    setup.powered_on_flag = False
    setup.cycling_colors_is_on_flag = False

    setup.red_led.off()
    setup.green_led.off()
    setup.yellow_led.off()


def cycle_colors():
    if not setup.powered_on_flag:
        return
    setup.green_led.off()
    setup.yellow_led.pulse(fade_in_time=0.5, fade_out_time=0.5)
    setup.cycling_colors_is_on_flag = True
    setup.temperature_to_colors_is_on_flag = False
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        for j in arange(0, 1.01, 0.01):
            if (not setup.powered_on_flag) or (not setup.cycling_colors_is_on_flag):
                return
            x, y = color_conversions.hsv2xy(j)
            current_time = datetime.now()
            print("Time " + current_time.strftime('%H:%M:%S.%f'))
            print(f'x and y values: {x}, {y}')
            print('----------------------------------------------')
            light_utils.change_color(x, y)


def cycle_static_colors():
    global static_color_index
    setup.green_led.off()
    setup.yellow_led.on()
    setup.yellow_led.off()
    sleep(0.1)
    setup.yellow_led.on()
    if setup.cycling_colors_is_on_flag:
        setup.cycling_colors_is_on_flag = False
    if setup.temperature_to_colors_is_on_flag:
        setup.temperature_to_colors_is_on_flag = False
    x, y = static_xy_colors[static_color_index][0], static_xy_colors[static_color_index][1]
    light_utils.change_color(x, y)
    if static_color_index >= 11:
        static_color_index = 0
    else:
        static_color_index += 1


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
