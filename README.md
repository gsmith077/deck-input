# deck-input

![Example Image](/readme_images/example.png)

A method of using a Steam Deck as a (limited) input for PC

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Modularity](#modularity)
- [Setup](#setup)
- [Running](#running)
- [No WSL2?](#no-wsl2)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Initially conceived for Star Citizen, I wanted a way to use my steam deck to
send commands during gamestate to my PC. After some searching, I was not pleased
with any of the avialable solutions.

So I took what I know (python) and created a method of sending keystrokes
through a web app that I can load on my deck.

**Obvious security concern**: If you let arbitrary devices send arbitrary inputs,
you will have arbitrary results. Use with caution and make sure you know what
you're doing.

Currently only tested on Windows, but theoretically cross platform as per
`pynput`. However, it doesn't work on WSL2. More on this later.

## Modularity

Since I didn't know what potential applications I'd interact with, I decided to
make the application build off a YAML manifest that defines the buttons,
their appearance, and their function.

## Setup

After cloning the repo:

- Create a virtual env: `python -m venv venv`
  - Use Python 3. Preferably 3.11.
- Activate venv:
  - Windows: `.\venv\Scripts\Activate.ps1`
  - *nix: `source venv\bin\activate`
- Install requriements: `pip install -r requirements.txt`

## Running

With your venv activated:
`flask run --host 0.0.0.0 --reload`

> `--host 0.0.0.0` allows other devices to reach this instance. Useful on a
> local network.
>
> `--reload` allows live updates to files to be picked up. This shouldn't be an
> issue, since the YAML is loaded on each request to `/`

From alternate device, open a browser window to the private IP of the host,
port `5000`

## No WSL2?

I know, right? I wanted to run this via WSL2, as per everything else. This
caused issues with sending commands through (Linux `pynput` was eating the
commands, but they needed to be sent to Windows to be picked up in game).

So I'm running it in Powershell.

In theory, a game running in Linux while running the application in Linux would
work. A WSL application might take the inputs?
