#!/usr/bin/env python3
"""set_screen_brightness.py
author     : Jackson Cole
email      : <jackson@jacksoncole.io>
contact    : Jackson Cole <jackson@jacksoncole.io>
description: A simple program to control my screen brightness on my
             archbook pro. Note: it's not perfect!
"""
import argparse
import os
import subprocess
import sys

# TODO (Jackson Cole <jackson@jacksoncole.io>)
# - The case where the brightness value dips below the minimum brightness
# setting in this file is a bit wonky. This needs to be sorted.


def main(argv):
    path = '/sys/class/backlight/intel_backlight'
    files = {
        'current': os.path.join(path, 'brightness'),
        'max': os.path.join(path, 'max_brightness'),
    }

    bl = Backlight(files)

    parser = setup_parser()
    args = parser.parse_args()

    if 'get' in args:
        print({
            'p': bl.get_brightness(brightness_type='current', convert=True,),
            'a': bl.get_brightness(brightness_type='current', convert=False,),
        }[args.get[0]])

    if 'set' in args:
        bl.set_brightness(args.set[0])

    elif 'increase' in args:
        bl.change_brightness_setting(args.increase[0], 'increase')

    elif 'decrease' in args:
        bl.change_brightness_setting(args.decrease[0], 'decrease')


class Backlight:
    """The Backlight class handles all configuration of the backlight on the
    screen.
    """
    def __init__(self, path_to_config_files: dict):
        self.files = path_to_config_files
        self.max = self.get_brightness('max')
        self.min = int(0.10 * self.max)
        self.current = {}
        self.current['abs'] = self.get_brightness('current')

    def get_brightness(self, brightness_type: str, convert=False) -> int:
        with open(self.files[brightness_type], 'r') as f:
            val = int(f.readline())
        if not convert:
            return val
        else:
            return self.convert_to_percent(val)

    def convert_to_percent(self, val_abs: int) -> int:
        return int((val_abs/self.max) * 100)

    def convert_to_abs(self, val_percent: int) -> int:
        return int((val_percent/100) * self.max)

    def check_brightness_setting(self, val: int) -> bool:
        if val <= self.max and val >= self.min:
            brightness_valid = True
        else:
            brightness_valid = False
            print("Error: brightness value invalid.")

        return brightness_valid

    def set_brightness(self, val: int, set_at_lim=False) -> bool:
        brightness_abs = self.convert_to_abs(val)
        if self.check_brightness_setting(brightness_abs):
            os.system("sudo echo {} > {}".format(
                str(brightness_abs),
                self.files['current']
                )
            )
            return True
        elif set_at_lim:
            os.system("sudo echo {} > {}".format(
                str(self.max),
                self.files['current']
                )
            )
            return False
        else:
            return False

    def change_brightness_setting(self, val: int, direction: str) -> bool:
        if direction not in ('increase', 'decrease'):
            return False

        current = self.get_brightness('current', convert=True)
        val_to_set = {
            'increase': current + val,
            'decrease': current - val,
        }[direction]
        self.set_brightness(val_to_set, set_at_lim=True)

        return True


def setup_parser() -> argparse.ArgumentParser:
    '''Sets up the argument parser and all associated command line arguments.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--get',
        nargs=1,
        choices=['a', 'p'],
        default=argparse.SUPPRESS,
        type=str,
        help='Get the current backlight value.',
    )
    parser.add_argument(
        '--set',
        type=int,
        nargs=1,
        default=argparse.SUPPRESS,
        help='Set the backlight value using a percentage value.'
    )
    parser.add_argument(
        '--increase',
        type=int,
        nargs=1,
        default=argparse.SUPPRESS,
        help='Increase the backlight value using a percentage value.'
    )
    parser.add_argument(
        '--decrease',
        type=int,
        nargs=1,
        default=argparse.SUPPRESS,
        help='Decrease the backlight value using a percentage value.'
    )

    return parser


if __name__ == "__main__":
    if os.geteuid() == 0:
        main(sys.argv)
    else:
        subprocess.call(["sudo", "python3", *sys.argv])
