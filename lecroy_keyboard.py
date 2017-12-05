from pynput import keyboard
import visa

def on_press(key):
    # print("Hit: '{}'".format(parse_input(key)))
    k1.press(key)
    k2.press(key)

def on_release(key):
    # print("Released: '{}'".format(parse_input(key)))
    k1.release(key)
    k2.release(key)
    if key == keyboard.Key.esc:
        return False

class Keyboard:
    def __init__(self, keys, key_mod_pair, channel, speaker):
        self.keys = keys
        self.modifier_keys = dict(tuple(k) for k in key_mod_pair)
        self.modifier_state = {k: False for k in self.modifier_keys.values()}
        self.pressed_keys = ""
        self.current_note = {'keys':"", 'mods':self.modifier_state}
        self.channel = channel
        self.speaker = speaker

    def parse_input(self,key):
        try:
            return key.char.lower()
        except AttributeError:
            return str(key)[4:]

    def release(self, key):
        released = self.parse_input(key)
        self.pressed_keys = self.pressed_keys.replace(released,"")
        if released in self.modifier_keys.keys:
            self.modifier_state[self.modifier_keys[released]] = False
        self.play_note()

    def press(self, key):
        pressed = self.parse_input(key)
        if (pressed in self.keys) and (pressed not in self.pressed_keys):
            self.pressed_keys += pressed
        if pressed in self.modifiers_keys.keys:
            self.modifier_state[self.modifier_keys[pressed]] = True
        self.play_note()

    def play_note(self):
        try:
            next_key = pressed_keys[-1]
        except IndexError:
            next_key = ""
        next_note['keys'] = next_key
        next_note['mods'] = self.modifier_state

        if next_note != self.curent_note:
            self.current_note = next_note
            self.make_noise()

    def make_noise(self):
        frq = self.current_frq()
        self.speaker.write(self.channel+':outp on')
        if frq == None:
            command = self.channel + ':outp off'
        else:
            command=self.channel + ':bswv frq,{:.3f}hz'.format(frq)
        self.speaker.write(command)

    def current_frq(self):
        note = list(self.current_note['keys'])
        if note == []:
            return None

        return ( self.base_frq*2**(note[-1]/len(self.keys))
            *2**(self.modifier_state.get('octave',0)) )


print("Program started.")
print("Gathering available devices...")
ports=visa.ResourceManager()
val == None
while val == None
    i=0
    print("Connect to:")
    for port in ports.list_resources():
        print('\t'+ i + '. ' + str(port))
        i++
    try:
        val = int(input())
    except:
        print("Not an integer.")
    if val > len(ports.list_resources())-1
        print("Not an available device.")
        val = None

connection = ports.open_resource(ports.list_resources()[val])
print("Connected to: " + ports.list_resources()[val])

print("Creating keyboards...")
k1 = Keyboard("qwerasdfzxcv", [["shift","octave"]], "C1", connection)

k2 = Keyboard("uiopjk;lm,./", [["shift_r","octave"]], "C2", connection)

print("Ready to play! Hit 'esc' to stop.")
# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
