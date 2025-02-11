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

registedAxis: dict[int] = set([])
toggleButton: dict[int, bool] = {}
povLocks: dict[int, list[int]] = {
    #axis ID : scan codes list
}

#this function will be called by the joystick buttons in order to simulate pushing a button towards or away from a value
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

    threading.Timer(0.02, axisPeriodic,[axisData, device]).start()

def setupHoldButton(buttonConfig: ButtonMapData, device: VJoyDevice):
    def pressButton():
        device.set_button(buttonConfig.to_button, True)
    def releaseButton():
        device.set_button(buttonConfig.to_button, False)

    keyboard.on_press_key(buttonConfig.from_scan_code, lambda e: pressButton())
    keyboard.on_release_key(buttonConfig.from_scan_code, lambda e: releaseButton())

def setupToggleButton(buttonConfig: ButtonMapData, device: VJoyDevice):
    toggleButton[buttonConfig.to_button] = False #registers button
    
    def pressButton():
        toggleButton[buttonConfig.to_button] = not toggleButton[buttonConfig.to_button]
        device.set_button(buttonConfig.to_button, toggleButton[buttonConfig.to_button])

    keyboard.on_press_key(buttonConfig.from_scan_code, lambda e: pressButton())

def setupAxis(axisConfig: AxesMapData, device: VJoyDevice):
    def startPeriodic():
        if not registedAxis.__contains__(axisConfig.axis):
            registedAxis.add(axisConfig.axis)
            axisPeriodic(axisConfig, device, True)

    keyboard.on_press_key(axisConfig.increase, lambda e: startPeriodic())
    keyboard.on_press_key(axisConfig.decrease, lambda e: startPeriodic())

def setupPOV(povConfig: ContPovMapData, device: VJoyDevice):
    def pressButton():
        device.set_cont_pov(ContPovMapData.pov_id, ContPovMapData.pov_value)
    def releaseButton():
        if all([not keyboard.is_pressed(key) for key in povLocks.get(povConfig.pov_id)]):
            device.set_cont_pov(ContPovMapData.pov_id, 0) # default state
        pass
    
    if not povLocks[povConfig.pov_id]:
        povLocks[povConfig.pov_id] = list()

    povLocks[povConfig.pov_id].append(povConfig.button)

    keyboard.on_press_key(povConfig.button, lambda e: pressButton())
    keyboard.on_release_key(povConfig.button, lambda e: releaseButton())


def mapKeys(config: KeyboardMap):
    keyboard.unhook_all()
    virtualController = VJoyDevice(config.config.vjoyID)
    for button in config.buttons:
        if button.interaction_type == 0:
            setupHoldButton(button, virtualController)
        if button.interaction_type == 1:
            setupToggleButton(button, virtualController)

    for axis in config.axes:
        setupAxis(axis, virtualController)

