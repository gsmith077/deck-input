"""
Launches a flask app that takes inputs and recreates keystrokes based on those 
inputs.
"""

import json
import yaml

from flask import Flask, render_template, request
from pynput.keyboard import Controller, Key

app = Flask(__name__)
virtual_keyboard = Controller()

# Set a group of recognized "modifier" keys for filtering.
MODIFIERS = ["shift", "alt", "control", "cmd"]


def standardize_long_form(button: dict) -> dict:
    """
    Sanitizes the inputs of the long form to ensure it's the correct format.
    """
    if isinstance(button["inputs"], str):
        button["inputs"] = [button["inputs"]]
    return button


def standardize_short_form(button: dict) -> dict:
    """
    Sanitizes the inputs of the short form to ensure it's the correct format.
    """
    for key, value in button.items():
        standardized_button = {
            "label": key,
            "inputs": [value] if isinstance(value, str) else value,
        }
    return standardized_button


def format_buttons(buttons: dict) -> dict:
    """
    Determines if the button is long form (based on presence of `inputs` key) or
    short term (lacks that key).
    Sends the button for standardization, and returns all formatted buttons.
    """
    formatted_buttons = []

    for button in buttons:
        if "inputs" in button:
            standardized_button = standardize_long_form(button)
        else:
            standardized_button = standardize_short_form(button)
        formatted_buttons.append(standardized_button)
    return formatted_buttons


@app.route("/")
def main():
    """
    Default route of the web app. Parses the YAML, sends it for formatting, and
    returns the rendered template.
    """
    with open("layout.yaml", "r", encoding="utf8") as layout_file:
        layout = yaml.safe_load(layout_file)

    buttons = format_buttons(layout["buttons"])

    return render_template(
        "index.html",
        buttons=buttons,
    )


def prepare_keys(inputs: dict) -> dict:
    """
    This function handles two things:
     - Strips the modifiers from the list.
     - Casts keys into `Keys.{}` objects, for handling F keys and
       multi-character named keys (like backspace)
    """
    return [
        getattr(Key, current_key, current_key)
        for current_key in inputs
        if current_key not in MODIFIERS
    ]


@app.route("/inputs", methods=["POST"])
def perform_input():
    """
    This is the main function. Parses the incoming request for `inputs` and
    turns them into `pynput` calls.
    """

    req_data = json.loads(request.data)

    inputs = req_data["inputs"]

    mods = [getattr(Key, mod) for mod in inputs if mod in MODIFIERS]
    keys = prepare_keys(inputs)

    if len(keys) == 1:
        with virtual_keyboard.pressed(*mods):
            virtual_keyboard.tap(keys[0])
    else:
        print("Currently only support mods and 1 key.")

    return "Done"
