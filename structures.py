from dataclasses import dataclass
from enum import Enum

@dataclass
class KeyboardConfig:
    vjoyID: int             # ID of vJoy gamepad

@dataclass
class buttonMap:
    to_button: int          # button ID that get's triggered
    from_scan_code: int     # scan code of key that triggers button
    interaction_type: int   # 0 = "hold"; 1 = "toggle on press"

@dataclass
class axes:
    axis: int               # axis ID
    increase: int           # scan code of key that increases axis
    decrease: int           # scan code of key that decreases axis
    key_rate: float         # rate at which the increase or decrease key affects axis
    decay_rate: float       # rate of decay when no button is pressed
    max_value: float        # max value (symmetric) of axis

@dataclass
class pov:
    button: int             # scan code of button that triggers POV
    pov_value: float        # pov_value = pov_value that is set in code #TODO: figure out units!
