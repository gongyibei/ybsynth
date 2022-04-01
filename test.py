from ybsynth.example.synth import PolyKeyboardSynth
from ybsynth.preset import keyboard_mapping

if __name__ == '__main__':
    mapping = keyboard_mapping.BASIC_MAPPING
    PolyKeyboardSynth(mapping).start()
