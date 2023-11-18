from rgbxy import Converter
from rgbxy import GamutC
from colorsys import hsv_to_rgb

converter = Converter(GamutC)


def hsv2rgb(h, s, v):
    """Converts hsv to rgb in 0-255 range"""
    return tuple(round(i * 255) for i in hsv_to_rgb(h, s, v))


def hsv2xy(h):
    """Converts hsv to xy values, with hard-coded 's' and 'v' values to 1"""
    r, g, b = hsv2rgb(h, 1, 1)
    x, y = converter.rgb_to_xy(r, g, b)
    return x, y
