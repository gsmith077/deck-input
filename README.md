# deck-input
A method of using a Steam Deck as a (limited) input for PC

Initially conceived for Star Citizen, I wanted a way to use my steam deck to 
send commands during gamestate to my PC. After some searching, I was not pleased
with any of the avialable solutions.

So I took what I know (python) and created a method of sending keystrokes 
through a web app that I can load on my deck.

Obvious security concern: If you let arbitrary devices send arbitrary inputs, 
you will have arbitrary results. Use with caution and make sure you know what 
you're doing.

## Modularity

Since I didn't know what potential applications I'd interact with, I decided to 
make the application build off a YAML manifest that defines the buttons, 
their appearance, and their function.