###############################################################################

from .pitch import Pitch
from enum import IntEnum

_quality_to_int = {"ooooo": 0, "ddddd": 0, "oooo": 1, "dddd": 1, "ooo": 2, "ddd": 2, 
    "oo": 3, "dd": 3, "o": 4, "d": 4, "m": 5, "P": 6, "p": 6, "M": 7, "+": 8, "a": 8,
    "++": 9, "aa": 9, "+++": 10, "aaa": 10, "++++": 11, "aaaa": 11, "+++++": 12, "aaaaa": 12}
_int_to_quality_word = {0:"quintuply-diminished" , 1: "quadruply-diminished", 2: "triply-diminished", 
3: "doubly-diminished", 4: "diminished", 5: "minor", 6: "perfect", 
    7: "major", 8: "augmented", 9: "doubly-augmented", 10: "triply-augmented", 
    11: "quadruply-augmented", 12: "quintuply-augmented"}
# _white_keys_int = {'C': 0, 'D': 1, 'E': 2, 'F': 3, 'G': 4, 'A': 5, 'B': 6}

_int_to_quality = {0:"ooooo" , 1: "oooo", 2: "ooo", 3: "oo", 4: "o", 5: "m", 6: "P", 
    7: "M", 8: "+", 9: "++", 10: "+++", 11: "++++", 12: "+++++"}

_span_to_semi = {0: 0, 1: 2, 2: 4, 3: 5, 4: 7, 5: 9, 6: 11, 7: 12}
_start_qual_for_span = {0: 6, 1: 7, 2: 7, 3: 6, 4: 6, 5: 7, 6: 7, 7: 6}
_span_to_word = {0: "unison", 1: "second", 2: "third", 3: "fourth", 4: "fifth", 5: "sixth", 6: "seventh", 7: "octave"}

_perfect_qual_change_semi = {0: -5 , 1: -4, 2: -3, 3: -2, 4: -1, 6: 0, 
    8: 1, 9: 2, 10: 3, 11: 4, 12: 5}
_major_qual_change_semi = {0: -6 , 1: -5, 2: -4, 3: -3, 4: -2, 5: -1, 7: 0, 
    8: 1, 9: 2, 10: 3, 11: 4, 12: 5}
def isdigit(arg):
    if not isinstance(arg, str):
        raise ValueError("must call isdigit on string")
    for i in arg:
        if ord(i) - ord('0') < 0 or ord(i) - ord('0') > 9:
            return False
    return True

def _quality_change(start_qual, change):
    
    if start_qual == 6 and change != 0:
        # perfect
        if change < 0:
            return change - 1
        else:
            return change + 1 
    elif start_qual == 5 and change > 0:
        # minor and increasing, need to get pass perfect
        return change + 1
    elif start_qual == 7 and change < 0:
        # major and decreasing, need to get pass perfect
        return change - 1
    return change

def _quality_semi_change(start_qual, end_qual):
    
    if start_qual == end_qual:
        return 0
    
    if start_qual == 6:
        # perfect
        if start_qual < end_qual:
            return end_qual - start_qual - 1
        else:
            return end_qual - start_qual + 1
    elif start_qual == 5 and end_qual > start_qual:
        # minor and increasing, need to get pass perfect
        return end_qual - start_qual - 1
    elif start_qual == 7 and end_qual < start_qual:
        # major and decreasing, need to get pass perfect
        return end_qual - start_qual + 1
    return end_qual - start_qual

class Interval:

    def __init__(self, arg, other=None):
        if isinstance(arg, str) and other == None:
            self._init_from_string(arg)
        elif isinstance(arg, list) and other == None:
            if not (isinstance(arg[0], int) and isinstance(arg[1], int) and isinstance(arg[2], int) and isinstance(arg[3], int)):
                raise ValueError("wrong list element")
            self._init_from_list(arg[0], arg[1], arg[2], arg[3])
        elif isinstance(arg, Pitch) and isinstance(other, Pitch):
            self._init_from_pitches(arg, other)
        else:
            raise TypeError("wrong argument type to create an interval")
    
    def _init_from_list(self, span, qual, xoct, sign):
        # assume that all four arguments are integers
        if span < 0 or span > 7:
            raise ValueError("span must be 0-7")
        elif qual < 0 or qual > 12:
            raise ValueError("qual must be 0-12")
        elif xoct < 0 or xoct > 10:
            raise ValueError("xoct must be 0-10")
        elif sign != -1 and sign != 1:
            raise ValueError("sign must be -1 or 1")
        if span == 0 and xoct > 0:
            span, xoct = 7, xoct - 1
        self.span, self.qual, self.xoct, self.sign = span, qual, xoct, sign

        
        if self.is_perfect_type():
            if self.is_major() or self.is_minor():
                raise ValueError("can't have major/minor for perfect type")
            if _span_to_semi[span] + _perfect_qual_change_semi[qual] < 0:
                raise ValueError("invalid quality for this interval")
        else:
            if self.is_perfect():
                raise ValueError("can't be perfect")
            if _span_to_semi[span] + _major_qual_change_semi[qual] < 0 and xoct == 0:
                raise ValueError("invalid quality for this interval")
        if qual == 0 and span != 4:
            raise ValueError("fifth (4) is only interval that can be quintuply diminished.")
        if qual == 12 and span != 3:
            raise ValueError("fourth (3) is only interval that can be quintuply augmented.")

    def _init_from_string(self, name):
        sep = 0
        if (len(name) < 2):
            raise ValueError("the string is incorrect")
        for i in range(len(name)):
            if isdigit(name[i]):
                sep = i
                break
        sign = 0
        if name[0] == '-':
            sign = -1
            name = name[1:]
            sep -= 1
        else:
            sign = 1

        qual = name[:sep]
        if name[:sep] != 'M':
            qual = qual.lower()

        if qual not in _quality_to_int.keys():
            raise ValueError("incorrect string for init")
        dif = int(name[sep:])
        if dif - 1 < 0:
            raise ValueError("span can't be negative")
        qual = _quality_to_int[qual]
        if dif - 1 > 0 and (dif - 1) % 7 == 0:
            span = 7
            xoct = int(dif / 7) - 1
            self._init_from_list(span, qual, xoct, sign)
        else:
            span = (dif - 1) % 7
            xoct = int((dif - 1)/ 7)
            self._init_from_list(span, qual, xoct, sign)
    
    def _init_from_pitches(self, pitch1, pitch2):
        keynum_dif, sign, span, xoct = 0, 0, 0, 0
        start_keynum, end_keynum = 0, 0
        if (pitch1.keynum() > pitch2.keynum()):
            sign = -1
            keynum_dif = pitch1.keynum() - pitch2.keynum()
            start_keynum =  pitch2.keynum()
            end_keynum = pitch1.keynum()
        else: 
            sign = 1
            keynum_dif = pitch2.keynum() - pitch1.keynum()
            start_keynum =  pitch1.keynum()
            end_keynum = pitch2.keynum()
        
        span = ((pitch2.letter - pitch1.letter) * sign) % 7

        if span == 0:
            if pitch1.octave == pitch2.octave:
                xoct = 0
            else:
                span = 7
                xoct = ((pitch2.octave - pitch1.octave) * sign) - 1
        else:
            if sign == 1:
                xoct = pitch2.octave - pitch1.octave
                if pitch2.letter < pitch1.letter:
                    xoct -= 1
            else:
                xoct = pitch1.octave - pitch2.octave
                if pitch1.letter < pitch2.letter:
                    xoct -= 1

        model_kn = Pitch.from_keynum(start_keynum + xoct*12 + _span_to_semi[span]).keynum()
        qual = _start_qual_for_span[span]
        qual += _quality_change(qual, end_keynum - model_kn)


        self._init_from_list(span, qual, xoct, sign)
        
    def __str__(self):
        if self.sign < 0:
            return f'<Interval: -{_int_to_quality[self.qual]}{self.span + 7 * self.xoct + 1} [{self.span}, {self.qual}, {self.xoct}, {self.sign}] {hex(id(self))}>'
        return f'<Interval: {_int_to_quality[self.qual]}{self.span + 7 * self.xoct + 1} [{self.span}, {self.qual}, {self.xoct}, {self.sign}] {hex(id(self))}>'


    def __repr__(self):
        if self.sign < 0:
            return f'Interval("-{_int_to_quality[self.qual]}{self.span + 7 * self.xoct + 1}")'
        return f'Interval("{_int_to_quality[self.qual]}{self.span + 7 * self.xoct + 1}")'

    def __lt__(self, other):
        if not isinstance(other, Interval):
            raise TypeError("can only compare with Interval")
        return self.pos() < other.pos()


    def __le__(self, other):
        if not isinstance(other, Interval):
            raise TypeError("can only compare with Interval")
        return self.pos() <= other.pos()

    def __eq__(self, other):
        if not isinstance(other, Interval):
            raise TypeError("can only compare with Interval")
        return self.pos() == other.pos()


    def __ne__(self, other):
        if not isinstance(other, Interval):
            raise TypeError("can only compare with Interval")
        return self.pos() != other.pos()


    def __ge__(self, other):
        if not isinstance(other, Interval):
            raise TypeError("can only compare with Interval")
        return self.pos() >= other.pos()


    def __gt__(self, other):
        if not isinstance(other, Interval):
            raise TypeError("can only compare with Interval")
        return self.pos() > other.pos()

  
    def pos(self):
        return (((self.span + (self.xoct * 7)) + 1) << 8) + self.qual


    def string(self):
        name = ""
        if self.sign < 0:
            name += "-"
        name += _int_to_quality_word[self.qual] + str(self.span + self.xoct * 7 + 1)
        return name


    def full_name(self, *, sign=True):
        if self.sign < 0:
            return "descending " + self.quality_name() + ' ' + self.span_name()
        return self.quality_name() + ' ' + self.span_name()


    def span_name(self):
        return _span_to_word[self.span]

    def quality_name(self):
        return _int_to_quality_word[self.qual]


    def matches(self, other):
        if not isinstance(other, Interval):
            raise ValueError("incorrect interval")
        if self.qual == other.qual and self.span == other.span and self.sign == other.sign:
            return True
        return False


    def lines_and_spaces(self):
        return self.span + (self.xoct * 7) + 1


    def _to_iq(self, name):
        if not isinstance(name, str):
            raise ValueError("need a string")
        if name != 'M':
            name = name.lower()
        if name not in _quality_to_int.keys():
            raise ValueError("wrong quality")
        return _quality_to_int[name]


    def to_list(self):
        return [self.span, self.qual, self.xoct, self.sign]


    def is_unison(self, qual=None):
        if qual == None:
            return self.span == 0
        else:
            return self.span == 0 and self.qual == self._to_iq(qual)


    def is_second(self, qual=None):
        if qual == None:
            return self.span == 1
        else:
            return self.span == 1 and self.qual == self._to_iq(qual)
    
    def is_third(self, qual=None):
        if qual == None:
            return self.span == 2
        else:
            return self.span == 2 and self.qual == self._to_iq(qual)


    def is_fourth(self, qual=None):
        if qual == None:
            return self.span == 3
        else:
            return self.span == 3 and self.qual == self._to_iq(qual)


    def is_fifth(self, qual=None):
        if qual == None:
            return self.span == 4
        else:
            return self.span == 4 and self.qual == self._to_iq(qual)


    def is_sixth(self, qual=None):
        if qual == None:
            return self.span == 5
        else:
            return self.span == 5 and self.qual == self._to_iq(qual)


    def is_seventh(self, qual=None):
        if qual == None:
            return self.span == 6
        else:
            return self.span == 6 and self.qual == self._to_iq(qual)

    
    def is_octave(self, qual=None):
        if qual == None:
            return self.span == 7
        else:
            return self.span == 7 and self.qual == self._to_iq(qual)


    def is_diminished(self):
        if self.qual >= 0 and self.qual <= 4:
            return 5 - self.qual
        else:
            return False

    def is_minor(self):
        if self.qual == 5:
            return True
        return False

    
    def is_perfect(self):
        if self.qual == 6:
            return True
        return False


    def is_major(self):
        if self.qual == 7:
            return True
        return False

    
    def is_augmented(self):
        if self.qual >= 8 and self.qual <= 12:
            return self.qual - 7
        else:
            return False

    
    def is_perfect_type(self):
        if self.is_unison() or self.is_fourth() or self.is_fifth() or self.is_octave():
            return True
        return False

    def is_imperfect_type(self):
        if not self.is_perfect_type():
            return True
        return False


    def is_simple(self):
        if self.xoct == 0:
            return True
        return False

        
    def is_compound(self):
        if self.xoct != 0:
            return True
        return False

    
    def is_ascending(self):
        if self.sign > 0:
            return True
        return False

    
    def is_descending(self):
        if self.sign < 0:
            return True
        return False

    
    def is_consonant(self):
        if (self.span == 2 and (self.qual == 5 or self.qual == 7)) or (self.span == 3 and self.qual == 6) or (self.span == 4 and self.qual == 6) or (self.span == 5 and (self.qual == 5 or self.qual == 7)) or ((self.span == 7 or self.span == 0) and self.qual == 6):
            return True
        return False

                   
    def is_dissonant(self):
        if not self.is_consonant():
            return True
        return False

    
    def complemented(self):
        return Interval([7 - self.span, 12 - self.qual, self.xoct, self.sign])

    
    def semitones(self):
        start_qual = -1
        if self.is_perfect_type():
            start_qual = 6
        else:
            start_qual = 7 
        return self.xoct * 12 + _span_to_semi[self.span] + _quality_semi_change(start_qual, self.qual)

    
    def add(self, other):
        if not isinstance(other, Interval):
            raise TypeError("need another Interval to add")
        if self.sign < 0 or other.sign < 0:
            raise NotImplementedError("adding descending intervals")
        
        span = self.span + other.span
        qual = _start_qual_for_span[span]

        xoct = self.xoct + other.xoct
        if span > 7:
            if span % 7 == 0:
                xoct += int(span / 7) - 1
                span = 7
            else: 
                xoct += int(span / 7)
                span %= 7


        qual_semi_change = self.semitones() + other.semitones() - (xoct * 12 + _span_to_semi[span])

        qual += _quality_change(qual, qual_semi_change)
        
        return Interval([span, qual, xoct, 1])
    
    def transpose(self, p):
        if not isinstance(p, Pitch) and not isinstance(p, IntEnum):
            raise TypeError("can only transpose a pitch")
        if isinstance(p, Pitch):
            original_keynum = p.keynum()
            if self.sign > 0:
                return Pitch.from_keynum(original_keynum + self.semitones())
            else:
                return Pitch.from_keynum(original_keynum - self.semitones())
        else:
            p_str = str(p)
            p_split = p_str.split('.')
            start_pitch = Pitch(p_split[1] + '4')
            original_keynum = start_pitch.keynum()
            if self.sign > 0 or (self.sign < 0 and self.span == 7):
                end_pitch = Pitch.from_keynum(original_keynum + self.semitones() % 12)
                return end_pitch.pnum()
            else:
                end_pitch = Pitch.from_keynum(original_keynum + self.complemented().semitones() % 12)
                return end_pitch.pnum()


if __name__ == '__main__':
    # Add your testing code here!
    print("testing...")
    a = Interval('-++5')
    b = Interval(Pitch('B1'), Pitch('F8'))
    c = Interval('-ooo5')
    print(a)
    print(b)
    print(c)
    print()
    print(Interval(Pitch('Fbb5'), Pitch('B##4')))
    print(Interval('+1').is_unison('A'))

    print("transpose")
    print(Interval('M7').transpose(Pitch('B3')))