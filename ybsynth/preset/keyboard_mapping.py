BASIC_MAPPING = {
    'a': 'C4' ,
    'w': 'C#4',
    's': 'D4' ,
    'e': 'D#4',
    'd': 'E4' ,
    'f': 'F4' ,
    't': 'F#4',
    'g': 'G4' ,
    'y': 'G#4',
    'h': 'A4' ,
    'u': 'A#4',
    'j': 'B4' ,
    'k': 'C5' ,
    'o': 'C#5',
    'l': 'D5' ,
    'p': 'D#5',
    ';': 'E5' ,
}


def get_random_mapping():
    mapping = dict()
    for i in range(32, 124):
        note = random.choice(['C', 'D', 'E', 'G', 'A'])
        n = random.choice([4, 5])
        mapping[chr(i)] = f'{note}{n}'
    return mapping
