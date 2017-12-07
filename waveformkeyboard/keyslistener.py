class KeysListener:
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
