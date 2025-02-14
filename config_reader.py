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
        0.0,
        tomlAxes.get("interval", 0.02)
    )

last_pov_id = 1

def convertToPov(tomlPov: dict[str, Any]) -> ContPovMapData:
    global last_pov_id
    last_pov_id  = tomlPov.get("pov_id", last_pov_id)
    return ContPovMapData(
        tomlPov.get("scan_code"),
        last_pov_id,
        tomlPov.get("pov_value")
    )

# this function takes in the toml dictionary and returns a keyboard map
# it fills out the dataclass classes in structures.py
def getKeyboardMap(tomlConfig: dict[str, Any]) -> KeyboardMap:
    return KeyboardMap(
        KeyboardConfig(
            tomlConfig.get("KeyboardConfig").get("vjoyID"),
            tomlConfig.get("KeyboardConfig").get("suppress", False),
            tomlConfig.get("KeyboardConfig").get("axes_ids", list())
        ),
        [convertToButtonMap(button) for button in tomlConfig.get("buttons")],
        [convertToAxesMap(axis) for axis in tomlConfig.get("axes")],
        [convertToPov(pov) for pov in tomlConfig.get("cont_pov")]
    )

