from time import sleep
import setup
import lighting_functions


def loop():
    while True:
        if not setup.powered_on_flag:  # checking in loop, in case of powering the light off, with external source
            lighting_functions.terminate_displaying()
            continue
        else:
            setup.red_led.on()
        if setup.temperature_to_colors_is_on_flag:
            lighting_functions.temperature_to_colors_cycle()
        if setup.cycling_colors_is_on_flag:
            lighting_functions.cycle_colors()
        sleep(0.1)
