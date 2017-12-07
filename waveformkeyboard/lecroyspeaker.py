class LecroySpeaker:
    def __init__(self):
        self.device = LecroySpeaker.get_device()
        if self.device == None:
            self.write = print
        else:
            self.write = self.device.write

    @classmethod
    def get_device(cls):
        print("Gathering available devices...")
        try:
            import visa
        except Exception as e:
            print('Failed to import `visa`: Using `print`.')
            return print

        # visa.log_to_screen()
        ports=visa.ResourceManager()
        avail_ports = ['Standard Out'] + list(ports.list_resources())
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
            device = ports.open_resource(avail_ports[val])
            print("Write command for: " + avail_ports[val])
        else:
            device = None
            print("Writing commands to screen.")

        return device

    def play(self,channel):
        def play_internal(frq):
            if frq == None:
                command = channel + ':outp off'
            else:
                command = channel + ':outp on;'
                command += channel + ':bswv frq,{:.3f}hz;'.format(frq)

            self.write(command)
        return play_internal
