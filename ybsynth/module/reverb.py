from .delay import Delay
from .mixer import Mixer
from .module import Module


# ref: https://github.com/Rishikeshdaoo/Reverberator/blob/master/Reverberator/src/com/rishi/reverb/Reverberation.java
class Reverb(Module):

    def __init__(self, delay_time, decay, wet):
        Module.__init__(self)
        self.delay_time = delay_time
        self.decay = decay
        self.wet = wet

        self.delay1 = Delay(delay_time, decay)
        self.delay2 = Delay(delay_time - 0.01173, decay - 0.1313)
        self.delay3 = Delay(delay_time + 0.01931, decay - 0.2743)
        self.delay4 = Delay(delay_time - 0.00797, decay - 0.3100)

        self.mixer = Mixer()

    def forward(self, X):
        R = self.mixer([
            self.delay1(X),
            self.delay2(X),
            self.delay3(X),
            self.delay4(X),
        ])
        X = X * (1 - self.wet) + R * self.wet
        return X
