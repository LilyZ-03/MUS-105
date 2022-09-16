#
# tet.py : Twelve-tone Equal Temperment (TET) 
# See tet.html for module documentation.

from curses.ascii import isdigit
import math

def round(n):
    decimal = n - int(n)
    r = int(n)
    if n < 0:
        if decimal <= -0.5:
            r -= 1
    else: 
        if decimal >= 0.5:
            r += 1
    return r

def hertz_to_midi(hertz):
    if hertz < 0:
        raise ValueError("hertz value less than zero")
    midi_num = 69 + round(math.log(hertz/440.0, 2) * 12)
    if midi_num > 127 or midi_num < 0:
        raise ValueError("invalid midi key number")
    return midi_num

def midi_to_hertz(midi):
    if midi > 127 or midi < 0 or not isinstance(midi, int):
        raise ValueError("invalid midi key number")
    return 440.0 * 2 ** ((midi - 69) / 12)

def midi_to_pc(midi):
    if midi > 127 or midi < 0:
        raise ValueError("invalid midi key number")
    return midi % 12

def pitch_to_midi(pitch):
    whitekey_pc = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    valid_accidentals = ['#','##','b','bb','f','ff','s','ss','']
    accidental = ''
    midi_num = -1

    if pitch[(len(pitch) - 2):] == '00':
        accidental = pitch[1:(len(pitch) - 2)]
        midi_num = 0
    else:
        accidental = pitch[1:(len(pitch) - 1)]
        midi_num = (int(pitch[(len(pitch) - 1)]) + 1) * 12
    if accidental not in valid_accidentals or pitch[0] not in whitekey_pc.keys() or not isdigit(pitch[len(pitch) - 1]):
        raise ValueError("invalid pitch name")
    midi_num += whitekey_pc[pitch[0]]

    if accidental == '#' or accidental == 'f':
        midi_num += 1
    elif accidental == '##' or accidental == 'ff':
        midi_num += 2
    elif accidental == 'b' or accidental == 's':
        midi_num -= 1
    elif accidental == 'bb' or accidental == 'ss':
        midi_num -= 2
    if midi_num > 127 or midi_num < 0:
        raise ValueError("invalid midi number")
    return midi_num

def midi_get_octave_str(midi):
    if midi > 127 or midi < 0 or not isinstance(midi, int):
        raise ValueError("invalid midi key number")
    if midi < 12:
            return '00'
    return str(int(midi / 12 - 1))

def midi_get_octave_int(midi):
    if midi > 127 or midi < 0 or not isinstance(midi, int):
        raise ValueError("invalid midi key number")
    return int(midi / 12 - 1)

def midi_to_pitch(midi, accidental=None):
    if midi > 127 or midi < 0 or not isinstance(midi, int):
        raise ValueError("invalid midi key number")
    default_pc = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
    
    # these are the pitch class number: names dictionaries 
    # the numbers only include classes that can be expressed with corresponding accidentals
    single_sharp = {0: 'B#', 1: 'C#', 3: 'D#', 5: 'E#', 6: 'F#', 8: 'G#', 10: 'A#'}
    double_sharp = {1: 'B##', 2: 'C##', 4: 'D##', 6: 'E##', 7: 'F##', 9: 'G##', 11: 'A##'}
    single_flat = {1: 'Db', 3: 'Eb', 4: 'Fb', 6: 'Gb', 8: 'Ab', 10: 'Bb', 11: 'Cb'}
    double_flat = {0: 'Dbb', 2: 'Ebb', 3: 'Fbb', 5: 'Gbb', 7: 'Abb', 9: 'Bbb', 10: 'Cbb'}
    no_accidental_applicable = [0, 2, 4, 5, 7, 9, 11]

    valid_accidentals = ['#','##','b','bb','f','ff','s','ss','']
    if accidental != None and accidental not in valid_accidentals:
        raise ValueError("invalid accidental")
    elif midi == 0 and (accidental == '#' or accidental == '##' or accidental == 'f' or accidental == 'ff'):
        raise ValueError("invalid accidental use")
    elif midi == 1 and (accidental == '##' or accidental == 'ff'):
        raise ValueError("invalid accidental use")
    
    pitch_class = midi_to_pc(midi)
    pitch_name = default_pc[pitch_class] 
    if accidental == None or accidental == '':
        if accidental == '' and pitch_class not in no_accidental_applicable:
            raise ValueError("this note must have an accidental")
        return pitch_name + midi_get_octave_str(midi)
    elif accidental == '#' or accidental == 'f':
        if pitch_class not in single_sharp.keys():
            raise ValueError("accidental not applicable")
        elif pitch_class == 0:
            return single_sharp[pitch_class] + str(midi_get_octave_int(midi) - 1)
        return single_sharp[pitch_class] + midi_get_octave_str(midi)
    elif accidental == '##' or accidental == 'ff':
        if pitch_class not in double_sharp.keys():
            raise ValueError
        elif pitch_class == 1:
            return double_sharp[pitch_class] + str(midi_get_octave_int(midi) - 1)
        return double_sharp[pitch_class] + midi_get_octave_str(midi)
    elif accidental == 'b' or accidental == 's':
        if pitch_class not in single_flat.keys():
            raise ValueError("accidental not applicable")
        elif pitch_class == 11:
            return single_flat[pitch_class] + str(midi_get_octave_int(midi) + 1)
        return single_flat[pitch_class] + midi_get_octave_str(midi)
    elif accidental == 'bb' or accidental == 'ss':
        if pitch_class not in double_flat.keys():
            raise ValueError("accidental not applicable")
        elif pitch_class == 10:
            return double_flat[pitch_class] + str(midi_get_octave_int(midi) + 1)
        return double_flat[pitch_class] + midi_get_octave_str(midi)


def hertz_to_pitch(hertz):
    midi_num = hertz_to_midi(hertz)
    pitch_class = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
    pitch_name = pitch_class[midi_num % 12]
    if midi_num < 12:
        return pitch_name + '00'
    return pitch_name + str(int(midi_num / 12 - 1))

def pitch_to_hertz(pitch):
    midi_num = pitch_to_midi(pitch)
    return 440 * 2 ** ((midi_num - 69) / 12)


if __name__ == '__main__':
    print("Testing...")
    
    assert hertz_to_midi(440) == 69
    assert hertz_to_midi(442) == 69
    assert hertz_to_midi(432) == 69
    assert hertz_to_midi(698.46) == 77
    assert hertz_to_midi(700.01) == 77
    assert hertz_to_midi(8) == 0
    assert hertz_to_midi(10) == 3

    # also need to check whether it correctly raises error
    try:
        m = hertz_to_midi(-5)
    except ValueError as e:
        pass
    else:
        print("ValueError isn't correctly raised.")

    try:
        m = hertz_to_midi(30000)
    except ValueError as e:
        pass
    else:
        print("ValueError is not correctly raised.")

    assert hertz_to_pitch(442) == 'A4'
    assert hertz_to_pitch(432) == 'A4'
    assert hertz_to_pitch(860) == 'A5'
    assert hertz_to_pitch(698.46) == 'F5'
    assert hertz_to_pitch(700.01) == 'F5'
    assert hertz_to_pitch(8) == 'C00'
    assert hertz_to_pitch(10) == 'Eb00'
    # need to test 0 pitch class

    print("Test midi_to_hertz:")
    print("midi: 69  hertz:", midi_to_hertz(69))
    print("midi: 60  hertz:", midi_to_hertz(60))
    print("midi: 0 hertz:", midi_to_hertz(0))

    try:
        h = midi_to_hertz(-5)
    except ValueError as e:
        pass
    else:
        print("ValueError is not correctly raised.")

    try:
        h = midi_to_hertz(128)
    except ValueError as e:
        pass
    else:
        print("ValueError is not correctly raised.")
    
    try:
        h = midi_to_hertz(25.9)
    except ValueError as e:
        pass
    else:
        print("ValueError is not correctly raised.")
    
    print("Test midi to pitch:")
    print(midi_to_pitch(70, 'bb'))
    assert midi_to_pitch(50) == 'D3'
    assert midi_to_pitch(61) == 'C#4'
    assert midi_to_pitch(68) == 'Ab4'
    assert midi_to_pitch(61, 'b') == 'Db4'
    assert midi_to_pitch(61, 's') == 'Db4'
    assert midi_to_pitch(61, '#') == 'C#4'
    assert midi_to_pitch(86, '##') == 'C##6'
    assert midi_to_pitch(0) == 'C00'
    assert midi_to_pitch(0, 'ss') == 'Dbb00'
    assert midi_to_pitch(127) == 'G9'
    assert midi_to_pitch(127, 'bb') == 'Abb9'

    assert pitch_to_midi('C4') == 60
    assert pitch_to_midi('C#8') == 109
    assert pitch_to_midi('G##6') == 93
    assert pitch_to_midi('Db8') == 109
    assert pitch_to_midi('B##5') == 85

    print("Test pitch_to_hertz:")
    print("pitch: C4 hertz:", pitch_to_hertz('C4'))
    print("pitch: A4 hertz:", pitch_to_hertz('A4'))
    print("pitch: G#8 hertz:", pitch_to_hertz('G#8'))
    print("pitch: Ab2 hertz:", pitch_to_hertz('Ab2'))
    print("pitch: B##5 hertz:", pitch_to_hertz('B##5'))

    print("Done!")

