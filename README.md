# projekt-malina - Simple Raspberry Pi project
Simple Raspberry Pi Project, which uses some LEDs, buttons and DS18B20 temperature sensor used on solderless breadboard to change Philips Hue lights based on the temperature.

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
  * [Hardware setup](#hardware-setup)
  * [Software setup](#software-setup)
* [Usage](#usage)
* [Features](#features)

## General info
This is a simple Raspberry Pi Project, which uses some LEDs, buttons and DS18B20 waterproof temperature sensor, all used on solderless breadboard to change Philips Hue lights based on the temperature, and additional few lightning modes.

## Technologies
Project is created only with python 3.x.

## Setup
Setup is broken up into 2 parts: [hardware setup](#hardware-setup) and [software setup](#software-setup).

### Hardware setup
In this particular project following parts are used:
* Raspberry Pi 3 model B (v1.2)
* Waterproof temperature sensor DS18B20
* Breadboard
* Few LEDs
* Few buttons
* Few jumper cables
* Philips Hue Bridge
* Philips Hue Bulb (not bluetooth variant)

Image of wiring all the parts:

![wiring-schema](https://github.com/Klusio19/projekt-malina/assets/96704102/50f5343e-3722-417f-9533-195223ce88eb)

### Software setup
> [!NOTE]  
> Code used in that project allows to use my particular Philips Hue Bridge. The local IP address and other Philips Hue-specific data is hardcoded to work only with my particular Philis Hue Bridge.
1. **Enable 1-wire support on the Raspberry Pi**
  + Use `sudo raspi-config` to open the tool.
  + Select "3 Interface Options"
  + Select "I7 1-Wire"
  + Select "Yes"
  + Reboot the Raspberry, for example with `sudo systemctl reboot` or `sudo reboot`
> [!IMPORTANT]
> By default, if you enabled 1-wire interface, to make your 1-wire device work, you have to wire it to GPIO4. If you want to use other pin, you have to edit /boot/config.txt file for example with `sudo nano /boot/config.txt` and add at the end of the file: "gpiopin=xx", where xx is your chosen GPIO pin. So last line should look like this: `dtoverlay=w1-gpio,gpiopin=xx`.\
> In this project I wired it up to GPIO 26, so last line looks like that: `dtoverlay=w1-gpio,gpiopin=xx`
2. **Clone this repo**
  + `git clone https://github.com/Klusio19/projekt-malina`
  + `cd projekt-malina`
3. **Install required dependencies**
    + `pip3 install -r requirements.txt`

## Usage
Simply run `python3 main.py` inside projekt-malina directory!

## Features
+ The button on the right (with breadbord oriented as in the picture), is power button, which turns on and off the Philips Hue bulb.
+ Middle button turns on and off mode, in which the Philips Hue bulb is changing color, based on the temperature.
+ The button on the left (with breadbord oriented as in the picture), is used to change colors within 12 predifined values. Every click changes color to the next one. If you hold the button for at least 2 seconds, it enters mode in which the Philips Hue bulb is cycling through all the colors as on the edge of the HSV color circle.
+ Blue LED indicates, if the script is running.
+ Red LED indicates, if the Philips Hue bulb is turned on.
+ Green LED indicates, if the "changing-colors-based-on-the-temperature" mode is enabled
+ Yellow LED idicates, if the "changing-12-predefined-colors" mode is enabled. Every click of the button, when you change the color, the LED blinks. It pulses, when it enters mode which cycle through all the HSV colors.

