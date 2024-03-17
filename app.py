import json
import yaml

from flask import Flask, render_template, request
from pynput.keyboard import Controller, Key

app = Flask(__name__)
virtual_keyboard = Controller()


def format_buttons(buttons: dict) -> dict:
    formatted_buttons = []

    for button in buttons:
        if "inputs" in button:
            button["inputs"] = (
                [button["inputs"]]
                if isinstance(button["inputs"], str)
                else button["inputs"]
            )
        else:
            button = [
                {
                    "label": key,
                    "inputs": [value] if isinstance(value, str) else value,
                }
                for key, value in button.items()
            ][0]

        formatted_buttons.append(button)
    return formatted_buttons


@app.route("/")
def main():
    with open("layout.yaml", "r") as layout_file:
        layout = yaml.safe_load(layout_file)

    buttons = format_buttons(layout["buttons"])
    print(buttons)
    return render_template("index.html", buttons=buttons)


@app.route("/inputs", methods=["POST"])
def perform_input():
    modifiers = ["shift", "alt", "control", "cmd"]

    req_data = json.loads(request.data)

    inputs = req_data["inputs"]

    mods = [getattr(Key, mod) for mod in inputs if mod in modifiers]
    keys = [key for key in inputs if key not in modifiers]
    keys = [getattr(Key, current_key, current_key) for current_key in keys]

    print("Mods: %", mods)
    print("Keys: %", keys)

    if len(keys) == 1:
        with virtual_keyboard.pressed(*mods):
            virtual_keyboard.press(keys[0])
            virtual_keyboard.release(keys[0])
    else:
        print("Currently only support mods and 1 key.")

    return "Done"
