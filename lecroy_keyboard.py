class Keyboard:
    def __init__(self, keys, key_mod, play=print, frq=55):
        self.keys = keys
        self.modifier_keys = dict(tuple(k) for k in key_mod)
        self.modifier_state = {k: False for k in self.modifier_keys.values()}
        self.pressed_keys = ""
        self.current_note = {'keys':"", 'mods':self.modifier_state.copy()}
        self.play = play
        self.base_frq = frq
        self.step = 12

    def release(self, key):
        self.pressed_keys = self.pressed_keys.replace(key,"")
        if key in self.modifier_keys:
            self.modifier_state[self.modifier_keys[key]] = False
        self.play_note()

    def press(self, key):
        if (key in self.keys) and (key not in self.pressed_keys):
            self.pressed_keys += key
        if key in self.modifier_keys:
            self.modifier_state[self.modifier_keys[key]] = True
        self.play_note()

    def play_note(self):
        try:
            next_key = self.pressed_keys[-1]
        except IndexError:
            next_key = ''
            if self.modifier_state.get('sustain',False):
                next_key = self.current_note['keys']
        next_note = {'keys': next_key, 'mods': self.modifier_state.copy()}

        if next_note != self.current_note:
            self.current_note = next_note
            self.play(self.current_frq())

    def current_frq(self):
        note = list(self.current_note['keys'])
        if note == []:
            return None

        return ( self.base_frq*2**(self.keys.index(note[-1])/self.step)
            *2**(self.modifier_state.get('octave',0)) )


class LecroySpeaker:
    def __init__(self):
        self.write = LecroySpeaker.get_write_command()
        self.amp = self.write(':bswv amp?')

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
        avail_ports = ['No device; use `print`'] + list(ports.list_resources())
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

    def play(self,channel):
        def play_internal(frq):
            if frq == None:
                command = channel + ':bswv amp,4mv'
                # command = self.channel + ':outp off'
            else:
                command = channel + ':bswv frq,{:.3f}hz;'.format(frq)
                command += channel + ':bswv amp,{}'.format(self.amp)
                # command += self.channel + ':outp on;'
            self.write(command)
        return play_internal


class KeyboardListener:
    def __init__(self,*args):
        self.keyboards = args
        try:
            self.pnk = __import__('pynput').keyboard
        except Exception as e:
            print("Failed to import `pynput.keyboard`")
            raise e

    @classmethod
    def parse_input(cls,key):
        try:
            return key.char.lower()
        except AttributeError:
            return str(key)[4:]

    def on_press(self):
        def internal_on_press(key):
            # print("Pressed: {0} '{1}''".format(key,self.parse_input(key)))
            for k in self.keyboards:
                k.press(self.parse_input(key))
        return internal_on_press

    def on_release(self):
        def internal_on_release(key):
            if key == self.pnk.Key.esc:
                return False
            # print("Released: {0} '{1}''".format(key,self.parse_input(key)))
            for k in self.keyboards:
                k.release(self.parse_input(key))
        return internal_on_release

    def listen(self):

        print("N.B.-- This program intercepts all key strokes while running.")
        print("\tBe wise what you type while this is running")
        print("Ready to play! Hit 'esc' to stop.")
        with self.pnk.Listener(
                on_press=self.on_press(),
                on_release=self.on_release()) as listener:
            listener.join()
            # Collect events until terminated



def main():

    print("Connecting Speakers...")
    s1 = LecroySpeaker()

    print("Creating keyboards...")
    k1 = Keyboard("=-0987654321", [("up","octave"),("down","sustain")], s1.play("c1"), 110)

    k2 = Keyboard("][poiuytrewq", [("up","octave"),("down","sustain")], s1.play("c2"), 110*2**(7/12))

    kl = KeyboardListener(k1,k2)

    kl.listen()


main()
