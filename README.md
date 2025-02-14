# Keyboard 2 joystick

> [!Warning]
> This project is currently under development! it might have bugs, weird typos, debug code, and other weirdness, explore at your own ~~risk~~ enjoyment!


This project requires VJoy and it's python interface pyVjoy in order to work properly

This project is specifically made for use in FRC and attempts to provide GLASS-like keyboard to joystick control
Currently POV buttons aren't implemented

## Setup

### dependency

install [vjoy](https://sourceforge.net/projects/vjoystick/)!

this program uses [pyvjoy](https://github.com/tidzo/pyvjoy) to communicate with vjoy.

it also uses [tomllib](https://docs.python.org/3/library/tomllib.html) to read the configuration and [keyboard](https://pypi.org/project/keyboard/) to read the keyboard inputs 

### configuration

In order to configure the keyboard you'll use a toml file!

There is an example / template config [in the directory](./Keyboard.toml) with comments!

There are plans to implement a easy config editor but for now I'd reccomend duplicating the template as it has comments for what each variable means!

you can use the [keyboard scanner](./keyboardScanner.py) in the repo to figure out what keys map to which scancodes!

## Development

Goal: have something that converts keyboard inputs to a virtual joystick based on an easily editable config file, similair to the GLASS tool used in FRC

| Needs             | wants | Nice to have |
| --------          | ------- | ---- |
| config            | running in background    |  GUI to edit config   |
| virtual xbox controller  | Easy way to enable and disable (toolbar?)   |  different ways of pressing button (ramping, on-off, sticky, etc)  |
| keyboard to joystick remapping |  switching between configs by loading them   |   |

the keyboard input will be the scan code as a decimal