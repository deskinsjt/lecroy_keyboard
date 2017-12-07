import waveformkeyboard as wfkb

print("Connecting Speakers...")
s1 = wfkb.LecroySpeaker()
s2 = wfkb.LecroySpeaker()

print("Creating keyboards...")
mods = [("up","octave"),("down","sustain")]

k1 = wfkb.Keyboard("0987654321", mods, s1.play("c1"), 110)
k2 = wfkb.Keyboard("poiuytrewq", mods, s1.play("c2"), 110*2**(7/12))
k3 = wfkb.Keyboard(";lkjhgfdsa", mods, s2.play("c1"), 110*2**(14/12))
k4 = wfkb.Keyboard("/.,mnbvcxz", mods, s2.play("c2"), 110*2**(21/12))

print("Creating keys listener...")
kl = wfkb.KeysListener(k1,k2,k3,k4)

kl.listen()
