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
