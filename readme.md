# ReadMe

This is a little thing I made for fun. It sets the output of Lecroy function generator based off of keyboard inputs.

## Dependencies
- `ni-visa` driver. Can be found [here](https://www.ni.com/visa/).
- `python3`
  - `pyvisa`: to interface with function generator
  - `pynput`: to capture keyboard events

## Usage

### OS Differences
Note that this has only been tested on macOS 10.12.x.

On macOS 10.12 in order for `pynput` to work correctly the program must be run with root privileges.

### Class `LecroySpeaker`
This is a helper class that handles the connection to the Lecroy function generator. Functionally this provides a method which takes a single argument, the frequency to be played and passes that to the function generator to be played.

### Class `Keyboard`
This is the class that computes the frequency to be played based off of the keys being pressed.

#### Choosing the Keyboard
The string you pass as the first argument to the `Keyboard` constructor determines how the keys corresponding to successive half-steps.

#### Modifiers
The program also allows you to input modifiers as the second argument to the constructor. Note that only an `'octave'` and `'sustain'` modifier are currently used.

### Class `KeysListener`
Listens to the keyboard and passes that information as a string to the `Keyboards`. Note that `pynput` listen in on ***all keyboard input*** while the program is running. Be cognizant of what and where you are typing while the program is running.

### Examples
An example program is supplied which shows how to set up four `Keyboard`s using two different function generators. the `Keyboard`'s tuning are set to replicate that of a generic classic string instrument. The program can be run on macOS
