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
        1.0,
        0.0
    )

def convertToPov(tomlPov: dict[str, Any]) -> ContPovMapData:
    return ContPovMapData(
        tomlPov.get("button"),
        tomlPov.get("pov_id"),
        tomlPov.get("pov_value")
    )

def getKeyboardMap(tomlConfig: dict[str, Any]) -> KeyboardMap:
    return KeyboardMap(
        KeyboardConfig(tomlConfig.get("KeyboardConfig").get("vjoyID")),
        [convertToButtonMap(button) for button in tomlConfig.get("buttons")],
        [convertToAxesMap(axis) for axis in tomlConfig.get("axes")],
        [convertToPov(pov) for pov in tomlConfig.get("cont_pov")]
    )

