from gpiozero import LED, PWMLED, Button
import urllib3
import light_utils
import buttons_handling
import w1thermsensor as w1

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # Disables warning about insecure connection
power_button = Button(14)
temperature_to_colors_button = Button(15)
colors_button = Button(4, hold_time=2)
blue_led = LED(21)
green_led = LED(20)
red_led = LED(19)
yellow_led = PWMLED(16)

powered_on_flag = False
temperature_to_colors_is_on_flag = False
cycling_colors_is_on_flag = False

sensor = w1.W1ThermSensor()


def init():
    global powered_on_flag
    blue_led.on()
    if light_utils.powered_on():
        powered_on_flag = True
        red_led.on()

    power_button.when_activated = buttons_handling.power_button_pressed
    temperature_to_colors_button.when_activated = buttons_handling.temperature_to_colors_cycle_button_pressed
    colors_button.when_held = buttons_handling.colors_button_held
    colors_button.when_released = buttons_handling.colors_button_released
