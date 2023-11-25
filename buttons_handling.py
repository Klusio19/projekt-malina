import light_utils
import lighting_functions
import setup

colors_button_is_held = False


def colors_button_held():
    global colors_button_is_held
    colors_button_is_held = True
    lighting_functions.cycle_colors()


def colors_button_released():
    global colors_button_is_held
    if not colors_button_is_held:
        lighting_functions.cycle_static_colors()
    colors_button_is_held = False


def power_button_pressed():
    if light_utils.powered_on():
        lighting_functions.terminate_displaying()
        setup.powered_on_flag = False
        setup.temperature_to_colors_is_on_flag = False
    else:
        setup.powered_on_flag = True
    light_utils.change_power()


def temperature_to_colors_cycle_button_pressed():
    if not setup.powered_on_flag:
        return
    setup.temperature_to_colors_is_on_flag = not setup.temperature_to_colors_is_on_flag
    setup.yellow_led.off()
    setup.green_led.toggle()
    if setup.cycling_colors_is_on_flag:
        setup.cycling_colors_is_on_flag = False
