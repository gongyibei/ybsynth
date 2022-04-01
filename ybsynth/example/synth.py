import librosa
from ..module import (ADSR, Delay, KeyboardSource, Mixer, Module, PaSink, Reverb,
                    SawtoothOSC, SineOSC, SquareOSC)

class MonoKeyboardSynth(Module):
    def __init__(self, key, freq):
        Module.__init__(self)
        self.keyboard = KeyboardSource(key)

        self.osc1 = SineOSC(freq)
        self.osc2 = SquareOSC(freq)
        self.osc3 = SawtoothOSC(freq, width=0.5)
        self.mixer = Mixer()

        self.adsr = ADSR(attack_time=0,
                         decay_time=0.2,
                         sustain_val=0.5,
                         release_time=0.5)
        self.delay = Delay(delay_time=0.2, decay=0.5)
        self.reverb = Reverb(delay_time=0.1, decay=0.5, wet=1)

    def forward(self):
        gate = self.keyboard()

        X = self.mixer([
            self.osc1(),
            #  self.osc2(),
            #  self.osc3(),
        ])

        X, adsr = self.adsr(X, gate)
        #  X = self.delay(X)
        #  X = self.reverb(X)
        return X


class PolyKeyboardSynth(Module):
    def __init__(self, mapping):
        Module.__init__(self)

        self.monosynth_list = []
        for key, note in mapping.items():
            self.monosynth_list.append(
                MonoKeyboardSynth(key, librosa.note_to_hz(note)))
        self.mixer = Mixer()
        self.sink = PaSink()

    def forward(self):
        X = self.mixer([synth() for synth in self.monosynth_list])
        self.sink(X)

    def start(self):
        while True:
            self()

