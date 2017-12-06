class Keyboard:
    def __init__(self, keys, key_mod, channel, write_command=print, frq=55):
        self.keys = keys
        self.modifier_keys = dict(tuple(k) for k in key_mod)
        self.modifier_state = {k: False for k in self.modifier_keys.values()}
        self.pressed_keys = ""
        self.current_note = {'keys':"", 'mods':self.modifier_state.copy()}
        self.channel = channel
        self.write_command = write_command
        self.base_frq = frq

    @classmethod
    def parse_input(cls,key):
        try:
            return key.char.lower()
        except AttributeError:
            return str(key)[4:]

    @classmethod
    def get_write_command(cls):
        print("Gathering available devices...")
        try:
            import visa
        except Exception as e:
            print('Failed to import `visa`: Using `print`.')
            return print

        # visa.log_to_screen()
        ports=visa.ResourceManager()
        avail_ports = ['No device; use `print`']+list(ports.list_resources())
        val = None
        while val == None:
            i=0
            print("Choose device to write to:")
            for port in avail_ports:
                print('\t'+ str(i) + '. ' + str(port))
                i = i + 1
            try:
                val = int(input())
            except:
                print("Not an integer.")
                continue
            if val >= len(avail_ports):
                print("Not an available device.")
                val = None

        if val != 0:
            write_command = ports.open_resource(avail_ports[val]).write
            print("Write command for: " + avail_ports[val])
        else:
            write_command = print
            print("Writing commands to screen.")

        return write_command

    def release(self, key):
        released = self.parse_input(key)
        self.pressed_keys = self.pressed_keys.replace(released,"")
        if released in self.modifier_keys:
            self.modifier_state[self.modifier_keys[released]] = False
        self.play_note()

    def press(self, key):
        pressed = self.parse_input(key)
        if (pressed in self.keys) and (pressed not in self.pressed_keys):
            self.pressed_keys += pressed
        if pressed in self.modifier_keys:
            self.modifier_state[self.modifier_keys[pressed]] = True
        self.play_note()

    def play_note(self):
        try:
            next_key = self.pressed_keys[-1]
        except IndexError:
            next_key = ''
        next_note = {'keys': next_key, 'mods': self.modifier_state.copy()}

        if next_note != self.current_note:
            self.current_note = next_note
            self.make_noise()

    def make_noise(self):
        frq = self.current_frq()
        if frq == None:
            command = self.channel + ':outp off'
        else:
            command = self.channel + ':outp on;'
            command += self.channel + ':bswv frq,{:.3f}hz'.format(frq)
        self.write_command(command)

    def current_frq(self):
        note = list(self.current_note['keys'])
        if note == []:
            return None

        return ( self.base_frq*2**(self.keys.index(note[-1])/len(self.keys))
            *2**(self.modifier_state.get('octave',0)) )


class KeyboardListener:
    def __init__(self,*args):
        self.keyboards = args

    def on_press(self):
        def internal_on_press(key):
            # print("Pressed: '{}'".format(Keyboard.parse_input(key)))
            for k in self.keyboards:
                k.press(key)
        return internal_on_press

    def on_release(self):
        def internal_on_release(key):
            if key == pnk.Key.esc:
                return False
            # print("Released: '{}'".format(Keyboard.parse_input(key)))
            for k in self.keyboards:
                k.release(key)
        return internal_on_release

    def listen(self):
        try:
            import pynput.keyboard
        except Exception as e:
            print("Failed to import `pynput.keyboard`")
            raise e
        print("N.B.-- This program intercepts all key strokes while running.")
        print("\tBe wise what you type while this is running")
        print("Ready to play! Hit 'esc' to stop.")
        with pynput.keyboard.Listener(
                on_press=self.on_press(),
                on_release=self.on_release()) as listener:
            listener.join()
            # Collect events until terminated


def main():
    write_command = Keyboard.get_write_command()

    print("Creating keyboards...")

    k1 = Keyboard("0987654321`", [("shift","octave")], "c1", write_command,110)

    k2 = Keyboard("poiuytrewq]", [("shift_r","octave")], "c2", write_command,110*2**(5/12))

    kl = KeyboardListener(k1,k2)

    kl.listen()


main()
