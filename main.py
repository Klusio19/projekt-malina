import RPi.GPIO as GPIO
import time
import sys
import signal
import light_utils
import light_specific_vars
# import w1thermsensor as w1


def translate_temp_to_hsv_color(value, temp_min, temp_max, hsv_color_min, hsv_color_max):
    # Figure out how 'wide' each range is
    temp_span = temp_max - temp_min
    hsv_color_span = hsv_color_max - hsv_color_min

    # Convert the left range into a 0-1 range (float)
    value_scaled = float(value - temp_min) / float(temp_span)

    # Convert the 0-1 range into a value in the right range.
    return hsv_color_min + (value_scaled * hsv_color_span)


# def main():
#     sensor = w1.W1ThermSensor()
#     while True:
#         temperature = sensor.get_temperature()
#         print(temperature)


if __name__ == '__main__':
    try:
        # main()
        temp = translate_temp_to_hsv_color(29.9, 20, 30, 0, 1)
        print(temp)
    except KeyboardInterrupt:
        # GPIO.cleanup()
        try:
            sys.exit(130)
        except SystemExit:
            sys.exit(130)
