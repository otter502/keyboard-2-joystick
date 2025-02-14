from dataclasses import dataclass

# this file holds the data structures used in the rest of the program

@dataclass
class KeyboardConfig:
    vjoyID: int             # ID of vJoy gamepad
    suppress: bool
    axes_ids: list[int]

@dataclass
class ButtonMapData:
    to_button: int          # button ID that get's triggered
    from_scan_code: int     # scan code of key that triggers button
    interaction_type: int   # 0 = "hold"; 1 = "toggle on press"

@dataclass
class AxesMapData:
    axis: int               # axis ID
    increase: int           # scan code of key that increases axis
    decrease: int           # scan code of key that decreases axis
    key_rate: float         # rate at which the increase or decrease key affects axis
    decay_rate: float       # rate of decay when no button is pressed
    max_value: float        # max value (symmetric) of axis
    current_value: float    # current value, for use by the program
    interval: float         # time interval between when the rates are applied in seconds 



@dataclass
class ContPovMapData:
    button: int             # scan code of button that triggers POV
    pov_id: int             # ID of the POV
    pov_value: float        # pov_value = pov_value that is set in code 1/100th of a degree)

@dataclass
class KeyboardMap:
    config: KeyboardConfig
    buttons: list[ButtonMapData]
    axes: list[AxesMapData]
    pov: list[ContPovMapData]

