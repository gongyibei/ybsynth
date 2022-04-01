import numpy as np

from .module import Module


class ADSR(Module):
    def __init__(self, attack_time = 0.5, decay_time = 0.5, sustain_val = 0.5, release_time = 1):
        Module.__init__(self)
        self.buf = np.zeros(self.buf_size)
        self.attack_len = attack_time * self.sample_rate
        self.decay_len = decay_time * self.sample_rate
        self.sustain_val = sustain_val
        self.release_len = release_time * self.sample_rate
        self.release_val = 0

        self.idx = 0
        self.release_idx = 0
    
    def forward(self, I, note_stat):
        adsr = self._make_adsr(note_stat)
        O = I * adsr
        return O, adsr


    def _make_adsr(self, note_stat):
        if note_stat == 0:
            a = self.release_len
            X = np.arange(self.release_idx, self.release_idx + self.buf_size, dtype=self.dtype)
            adsr = np.piecewise(
                X, 
                [X<a,  X>=a],
                [self._make_release, 0]
            )
            self.release_idx = min(self.release_idx + self.buf_size, a)
            self.idx = 0
                
        elif note_stat == 1:
            a = self.attack_len - 1
            b = self.attack_len + self.decay_len - 1
            X = np.arange(self.idx, self.idx + self.buf_size, dtype=self.dtype)
            adsr = np.piecewise(
                X, 
                [X < a,  (X>=a) & (X< b), X >= b],
                [self._make_attack, self._make_decay, self._make_sustain]
            )
            self.idx = min(self.idx + self.buf_size, b)
            self.release_val = adsr[-1]
            self.release_idx = 0
        return adsr

    def _make_attack(self, X):
        return (1 / self.attack_len) * X
    
    def _make_decay(self, X):
        return 1 - (1 - self.sustain_val) / self.decay_len * (X - self.attack_len)

    def _make_sustain(self, X):
        return self.sustain_val

    def _make_release(self, X):
        return self.release_val - self.release_val / self.release_len * X
