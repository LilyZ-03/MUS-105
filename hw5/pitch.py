###############################################################################
"""
A class that implements musical pitches.

The Pitch class represent equal tempered pitches and returns information
in hertz, keynum, pitch class, Pnum  and pitch name formats.  Pitches
can be compared using standard math relations and maintain proper spelling
when complemented or transposed by an Interval.
"""

from curses.ascii import isdigit
from enum import IntEnum
from math import pow
from collections import namedtuple
# import tet

# Create the namedtuple super class for Pitch with three attributes:
# letter, accidental, and octave.  See your ratio.py file for an example.
PitchBase = namedtuple('PitchBase', ['letter', 'accidental', 'octave'])
valid_accidentals = {'#': '#','##': '##','b': 'b','bb': 'bb','f': 'b','ff': 'bb','s': '#','ss': '##','': '', 'n': ''}
accidental_as_char = {'ff': 0, 'f': 1, '': 2, 's': 3, 'ss': 4}
symbolic_to_safe_acc = {'bb': 'ff', 'b': 'f', '': '', '#': 's', '##': 'ss'}
valid_pitch_class = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
int_to_accidental = {0: 'bb', 1: 'b', 2: '', 3: '#', 4: '##'}
accidental_to_int = {'bb': 0, 'b': 1, '': 2, '#': 3, '##': 4}
octave_to_int = {'00': 0, '0': 1, '1': 2, '2': 3, '3': 4, '4': 5, '5': 6, '6': 7, '7': 8, '8': 9, '9': 10}
int_to_octave = {0: '00', 1: '0', 2: '1', 3: '2', 4: '3', 5: '4', 6: '5', 7: '6', 8: '7', 9: '8', 10: '9'}
int_to_pitch_class = {0: 'C', 1: 'D', 2: 'E', 3: 'F', 4: 'G', 5: 'A', 6: 'B'}
pitch_class_to_int = {'C': 0, 'D': 1, 'E': 2, 'F': 3, 'G': 4, 'A': 5, 'B': 6}

def midi_to_pc(midi):
    if midi > 127 or midi < 0:
        raise ValueError("invalid midi key number")
    return midi % 12

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

def pitch_to_hertz(pitch):
    midi_num = pitch_to_midi(pitch)
    return 440 * 2 ** ((midi_num - 69) / 12)
class Pitch (PitchBase):

    # Create the pnum class here, see documentation in pitch.html
    pc_to_int = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    pnum_list = []
    for pn in valid_pitch_class:
        for ac in accidental_as_char:
            pnum_list.append((pn + ac, (pitch_class_to_int[pn] << 4) + accidental_as_char[ac]))
    pnums = IntEnum('Pnum', pnum_list)
 

    def __new__(cls, arg=None):
        letter, accidental, octave = None, None, None
        if arg is None:
            self = super(Pitch, cls).__new__(cls, letter, accidental, octave)
            return self
        elif isinstance(arg, str):
            letter = arg[0].upper()
            if arg[(len(arg) - 2):] == '00':
                accidental = arg[1:(len(arg) - 2)]
                octave = '00'
            else:
                accidental = arg[1:(len(arg) - 1)]
                octave = arg[len(arg) - 1]
            if accidental not in valid_accidentals.keys() or letter not in valid_pitch_class or not octave.isdigit():
                raise TypeError("invalid string argument to make a new pitch.")
        elif isinstance(arg, list):
            if len(arg) != 3 or not (arg[0] in int_to_pitch_class.keys() and arg[1] in int_to_accidental.keys() and isinstance(arg[2], int) and arg[2] > 0 and arg[2] <= 12):
                raise TypeError("invalid list argument to make a new pitch.")
            # arg[0] - letter, arg[1] - accidental, arg[2] - octave
            letter = int_to_pitch_class[arg[0]]
            accidental = int_to_accidental[arg[1]]
            octave = str(arg[2] - 1)
        else:
            raise TypeError("invalid argument to make a new pitch.")
        
        accidental = valid_accidentals[accidental]
        midi_num = pitch_to_midi(letter + accidental + octave)
        self = super(Pitch, cls).__new__(cls, pitch_class_to_int[letter], accidental_to_int[accidental], octave_to_int[octave])
        return self

    

    @classmethod
    def _values_to_pitch(cls, let, acc, ova):
        letter_name = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        symbolic_acc = ['bb', 'b', '', '#', '##']
        safe_acc = ['ff', 'f', 'n', 's', 'ss']
        octave_nums = ['00', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if not (isinstance(let, str) and isinstance(acc, str)and isinstance(ova, str)):
            raise TypeError("wrong type for new pitch")
        if let not in letter_name or ova not in octave_nums or (acc not in symbolic_acc and acc not in safe_acc):
            raise TypeError("invalid arg for new pitch")
        return super(Pitch, cls).__new__(cls, pitch_class_to_int[let], accidental_to_int[acc], octave_to_int[ova])

    @classmethod
    def _string_to_pitch(cls, arg):
        if not isinstance(arg, str):
            raise TypeError("arg is not string")
        if arg[len(arg) - 2:] == '00':
            return cls._values_to_pitch(arg[0], arg[1:len(arg) - 2], '00')
        else:
            return cls._values_to_pitch(arg[0], arg[1:len(arg) - 1], arg[len(arg) - 1])
    
    def __str__(self):
        # It is important that you implement the __str__ method precisely.
        # In particular, for __str__ you want to see '<', '>', '0x' in 
        # your output string.  The format of your output strings from your
        # version of this function must look EXACTLY the same as in the two
        # examples below.
        # 
        #     >>> str(Pitch("C#6"))
        #     '<Pitch: C#6 0x7fdb17e2e950>'
        #     >>> str(Pitch())
        #     '<Pitch: empty 0x7fdb1898fa70>'
        if self.is_empty():
            return f'<Pitch: empty {hex(id(self))}>'
        return f'<Pitch: {self.string()} {hex(id(self))}>'


    def __repr__(self):
        # Note: It is the __repr__ (not the __str__) function that the autograder
        # uses to compare results. So it is very important that you implement this
        # method precisely. In particular, for __repr__ you want to see double
        # quotes inside single quotes and NOT the other way around. The format of
        # your output strings from your version of this function must look 
        # EXACTLY the same as in the two examples below.
        #
        #     >>> str(Pitch("C#6"))
        #     '<Pitch: C#6 0x7fdb17e2e950>'
        #     >>> repr(Pitch("Bbb3"))
        #     'Pitch("Bbb3")'
        if self.is_empty():
            return f'Pitch()'
        return 'Pitch("{}")'.format(self.string())


    def __lt__(self, other):
        if not isinstance(other, Pitch):
            raise TypeError("needs a Pitch to compare.")
        # self_midi = pitch_to_midi(self.letter + self.accidental + self.octave)
        # other_midi = pitch_to_midi(other.letter + other.accidental + other.octave)
        # return self_midi < other_midi
        return self.pos() < other.pos()


    def __le__(self, other):
        if not isinstance(other, Pitch):
            raise TypeError("needs a Pitch to compare.")
        # self_midi = pitch_to_midi(self.letter + self.accidental + self.octave)
        # other_midi = pitch_to_midi(other.letter + other.accidental + other.octave)
        return self.pos() <= other.pos()

    def __eq__(self, other):
        if not isinstance(other, Pitch):
            raise TypeError("need a Pitch to compare.")
        if self.letter == other.letter and self.accidental == other.accidental and self.octave == other.octave:
            return True
        return False


    def __ne__(self, other):
        if not isinstance(other, Pitch):
            raise TypeError("need a Pitch to compare.")
        if self.letter == other.letter and self.accidental == other.accidental and self.octave == other.octave:
            return False
        return True

    def __ge__(self, other):
        if not isinstance(other, Pitch):
            raise TypeError("needs a Pitch to compare.")
        # self_midi = pitch_to_midi(self.letter + self.accidental + self.octave)
        # other_midi = pitch_to_midi(other.letter + other.accidental + other.octave)
        return self.pos() >= other.pos()


    def __gt__(self, other):
        if not isinstance(other, Pitch):
            raise TypeError("needs a Pitch to compare.")
        # self_midi = pitch_to_midi(self.letter + self.accidental + self.octave)
        # other_midi = pitch_to_midi(other.letter + other.accidental + other.octave)
        return self.pos() > other.pos()

    def pos(self):
        # do we differentiate octave 00 and 0??
        return (self.octave << 8) + (self.letter << 4) + self.accidental


    def is_empty(self):
        if self.letter == None or self.accidental == None or self.octave == None:
            return True
        return False

    def string(self):
        if self.is_empty():
            return f''
        return f'{int_to_pitch_class[self.letter]}{int_to_accidental[self.accidental]}{int_to_octave[self.octave]}'

    def keynum(self):
        return pitch_to_midi(self.string())

    def pnum(self):
        pitch_class = int_to_pitch_class[self.letter] + symbolic_to_safe_acc[int_to_accidental[self.accidental]]
        print(pitch_class)
        return self.pnums[pitch_class]
    
    def pc(self):
        # do we differentiate octace 00 and 0??
        return (self.pc_to_int[int_to_pitch_class[self.letter]] + self.accidental - 2) % 12

    
    def hertz(self):
        return pitch_to_hertz(self.string())


    @classmethod
    def from_keynum(cls, keynum, acci=None):
        if not isinstance(keynum, int) or 127 < keynum or 0 > keynum:
            raise ValueError("invalid keynum")
        print(keynum, acci)
        pitch_name = midi_to_pitch(keynum, acci)
        return cls._string_to_pitch(pitch_name)
        

if __name__ == '__main__':
    # Add your testing code here!
    # test whether import is successful
    c = Pitch("Cbb0")
    d = Pitch("Cb0")
    print(Pitch().string())
    print(repr(c))
    print(repr(d))
    print(c.pnum())
    test_pnum = c.pnum()
    s = str(test_pnum)
    print(isinstance(s, str))
    print(d.pnum())
