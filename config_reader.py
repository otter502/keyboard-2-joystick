import tomllib
from typing import Any
from structures import *



def getToml(filePath: str) -> dict[str, Any]:
    with open(filePath, "rb") as f:
        data = tomllib.load(f)
    
    return data


def convertToButtonMap(tomlButton: dict[str, Any]) -> ButtonMapData:
    return ButtonMapData(
        tomlButton.get("to"),
        tomlButton.get("from"),
        tomlButton.get("type", 0)
    )


def convertToAxesMap(tomlAxes: dict[str, Any]) -> AxesMapData:
    return AxesMapData(
        tomlAxes.get("axis"),
        tomlAxes.get("increase"),
        tomlAxes.get("decrease"),
        tomlAxes.get("key"),
        tomlAxes.get("decay"),
        tomlAxes.get("max")
    )

def convertToPov(tomlPov: dict[str, Any]) -> PovMapData:
    return PovMapData(
        tomlPov.get("button"),
        tomlPov.get("pov_value")
    )

def getKeyboardMap(tomlConfig: dict[str, Any]) -> KeyboardMap:
    return KeyboardMap(
        tomlConfig.get("KeyboardConfig"),
        [convertToButtonMap(button) for button in tomlConfig.get("buttons")],
        [convertToAxesMap(axis) for axis in tomlConfig.get("axes")],
        [convertToPov(pov) for pov in tomlConfig.get("pov")]
    )

print(getKeyboardMap(getToml("./Keyboard.toml")))