# Keyboard 2 joystick

> [!Warning]
> This project is currently under development! it might have bugs, weird typos, debug code, and other weirdness, explore at your own ~~risk~~ enjoyment!

> [!Caution]
> Currently POV buttons aren't implemented

This project requires VJoy and it's python interface pyVjoy in order to work properly

This project is specifically made for use in FRC and attempts to provide GLASS-like keyboard to joystick control
Currently POV buttons aren't implemented

## Setup

### dependency

install vjoy, setup continous POV

### configuration

how scan codes work

# Development

Goal: have something that converts keyboard inputs to a virtual joystick based on an easily editable config file, similair to the GLASS tool used in FRC

| Needs             | wants | Nice to have |
| --------          | ------- | ---- |
| config            | running in background    |  GUI to edit config   |
| virtual xbox controller  | Easy way to enable and disable (toolbar?)   |  different ways of pressing button (ramping, on-off, sticky, etc)  |
| keyboard to joystick remapping |  switching between configs by loading them   |   |

the keyboard input will be the scan code as a decimal