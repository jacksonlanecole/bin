# utilities

- [set_screen_brightness.py](#set_screen_brightness.py)

## `set_screen_brightness.py`
This script will likely become a general purpose LED/lights controller for
my archbook pro. As of right now it handles getting the current value, setting,
increasing, and decreasing the brightness of the backlight. This can be done via
the following:

Usage:
```
set_screen_brightness.py [--set] [--increase] [--decrease] <value between 0 and 100> [--get]
```

Of course, Pommed and Pommed light exist, but I wanted to tinker.
