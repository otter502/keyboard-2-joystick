#this file preforms the hot key actions
import threading
import time
from structures import AxesMapData
from structures import KeyboardMap
from structures import ButtonMapData
from structures import ContPovMapData
import config_reader
import keyboard
import math
from pyvjoy import VJoyDevice

# This is a fairly big file which stores the functions, each of the functions map a specific type of binding (POV, button, axis)

# these are things that need to be remembered as the program runs!

# Axes that are currently being controlled with axisPeriodic, preventing a stacking effect if the user clicks the increase button twice
registedAxis: set[int] = set([])

# a list storing the states of toggle buttons
toggleButton: dict[int, bool] = {}

# this prevents behavior when two POV buttons are pressed at once and one superseeds the other
povLocks: dict[int, list[int]] = {
    #axis ID : scan codes list
}

#this function will be called by the joystick buttons in order to simulate pushing a joystick towards or away from a value
def axisPeriodic(axisData: AxesMapData, device: VJoyDevice, bypass: bool = False):
    increase: bool = keyboard.is_pressed(axisData.increase)
    decrease: bool = keyboard.is_pressed(axisData.decrease)

    if not(increase) and not(decrease) and (abs(axisData.current_value) > axisData.decay_rate):
        axisData.current_value -= math.copysign(axisData.decay_rate, axisData.current_value)
    
    if increase and not(decrease):
        axisData.current_value = min(axisData.current_value + axisData.key_rate, axisData.max_value)

    if not(increase) and decrease:
        axisData.current_value= max(axisData.current_value - axisData.key_rate, -axisData.max_value)

    if not(increase) and not(decrease) and (abs(axisData.current_value) < axisData.decay_rate) and not(bypass):
        device.set_axis(axisData.axis, (int) ((0.5) * 0x8000))
        registedAxis.remove(axisData.axis)
        return
    
    device.set_axis(axisData.axis, (int) ((axisData.current_value + 1)/2.0 * 0x8000))

    threading.Timer(axisData.interval, axisPeriodic,[axisData, device]).start()

# this sets up the Axis behavior and binds the buttons!
def setupAxis(axisConfig: AxesMapData, device: VJoyDevice, suppress: bool):
    def startPeriodic():
        if not registedAxis.__contains__(axisConfig.axis):
            registedAxis.add(axisConfig.axis)
            axisPeriodic(axisConfig, device, True)

    device.set_axis(axisConfig.axis, (int) ((0.5) * 0x8000))

    keyboard.on_press_key(axisConfig.increase, lambda e: startPeriodic(), suppress)
    keyboard.on_press_key(axisConfig.decrease, lambda e: startPeriodic(), suppress)

# this sets up a hold button's behavior and binds the button!
def setupHoldButton(buttonConfig: ButtonMapData, device: VJoyDevice, supresss: bool):
    def pressButton():
        device.set_button(buttonConfig.to_button, True)
    def releaseButton():
        device.set_button(buttonConfig.to_button, False)

    keyboard.on_press_key(buttonConfig.from_scan_code, lambda e: pressButton(), supresss)
    keyboard.on_release_key(buttonConfig.from_scan_code, lambda e: releaseButton(), supresss)

# this sets up a toggle button's behavior and binds the button!
def setupToggleButton(buttonConfig: ButtonMapData, device: VJoyDevice, suppress: bool):
    toggleButton[buttonConfig.to_button] = False #registers button
    
    def pressButton():
        toggleButton[buttonConfig.to_button] = not toggleButton[buttonConfig.to_button]
        device.set_button(buttonConfig.to_button, toggleButton[buttonConfig.to_button])

    keyboard.on_press_key(buttonConfig.from_scan_code, lambda e: pressButton(), suppress)

# this sets up a POV's behavior and binds the button!
def setupPOV(povConfig: ContPovMapData, device: VJoyDevice, suppress: bool):
    def pressButton():
        povLocks[povConfig.pov_id].append(povConfig.button)
        device.set_cont_pov(povConfig.pov_id, povConfig.pov_value)

    def releaseButton():
        povLocks[povConfig.pov_id].remove(povConfig.button)
        if all([not keyboard.is_pressed(key) for key in povLocks.get(povConfig.pov_id)]):
            device.reset_povs()
    
    povLocks[povConfig.pov_id] = list()

    keyboard.on_press_key(povConfig.button, lambda e: pressButton(), suppress)
    keyboard.on_release_key(povConfig.button, lambda e: releaseButton(), suppress)

# this is the main function, it'll take in the toml config (as a KeyboardMap dataclass), reset old bindings, then bind every type of binding listed in the config (POV, buttons, axes)
def mapKeys(config: KeyboardMap):
    keyboard.unhook_all()
    virtualController = VJoyDevice(config.config.vjoyID)

    [virtualController.set_axis(axis, (int)(0.5 * 0x8000)) for axis in config.config.axes_ids]

    suppress = config.config.suppress
    for button in config.buttons:
        if button.interaction_type == 0:
            setupHoldButton(button, virtualController, suppress)
        if button.interaction_type == 1:
            setupToggleButton(button, virtualController, suppress)

    for axis in config.axes:
        setupAxis(axis, virtualController, suppress)

    for pov in config.pov:
        setupPOV(pov, virtualController, suppress)

