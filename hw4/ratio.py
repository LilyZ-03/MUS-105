###############################################################################
# ratio.py : A class that implements fractional numbers.
# See ratio.html for module documentation.

from math import gcd, pow
from decimal import Decimal
from collections import namedtuple

# A namedtuple base class for Ratio with num and den properties.
RatioBase = namedtuple('RatioBase', ['num', 'den'])

class Ratio (RatioBase):

    #cls is the super class/class passed in, num - numerator, den - denominator
    def __new__(cls, num, den=None):
        if den == None and not (isinstance(num, int) or isinstance(num, float) or isinstance(num, str)):
            raise TypeError("num must be a integer, string or float.")
        if den != None and (not isinstance(den, int) or not isinstance(num, int)):
            raise TypeError("num & den must both be integers.")
        if den != None and den == 0:
            raise ZeroDivisionError("denominator can't be 0.")
        
        if den == None:
            if isinstance(num, int):
                den = 1
            elif isinstance(num, float):
                num, den = Decimal(str(num)).as_integer_ratio()
            elif isinstance(num, str):
                data = num.split('/')
                if not len(data) == 2:
                    raise TypeError("invalid input string.")
                judge1, judge2 = data[0], data[1]
                if data[0][0] == "-":
                    judge1 = data[0][1:]
                if data[1][0] == "-":
                    judge2 = data[1][1:]
                if not (judge1.isdigit() and judge2.isdigit()):
                    raise TypeError("invalid input string.")
                num, den = int(data[0]), int(data[1])
        
        if (num < 0 and den < 0) or (num >= 0 and den < 0):
            num, den = num * -1, den * -1
        factor = gcd(num, den)
        num, den = num / factor, den / factor

        self = super(Ratio, cls).__new__(cls, num, den)
        return self

    
    def __str__(self):
        cname = self.__class__.__name__
        attrs = ', '.join([i[0] + ": " + str(i[1]) for i in vars(self).items()])
        num = int(self.num)
        den = int(self.den)
        return f'<{cname} {num}/{den} {hex(id(self))}>'

    def __repr__(self):
        num = int(self.num)
        den = int(self.den)
        return f"Ratio(\"{num}/{den}\")"


    def __mul__(self, other):
        if isinstance(other, Ratio):
            return Ratio(int(self.num * other.num), int(self.den * other.den))
        elif isinstance(other, int):
            return Ratio(int(self.num * other), int(self.den))
        elif isinstance(other, float):
            m_num, m_den = Decimal(str(other)).as_integer_ratio()
            return (self.num * m_num) / (self.den * m_den)
        raise TypeError("wrong data type for multiplication.")

    
    # Implements right side multiplication (same code as __mul__)
    __rmul__ = __mul__


    def __truediv__(self, other):
        if isinstance(other, Ratio):
            return Ratio(int(self.num * other.den), int(self.den * other.num))
        elif isinstance(other, int):
            return Ratio(int(self.num), int(self.den * other))
        elif isinstance(other, float):
            m_num, m_den = Decimal(str(other)).as_integer_ratio()
            return (self.num * m_den) / (self.den * m_num)
        raise TypeError("wrong data type for division.")


    def __rtruediv__(self, other):
        if isinstance(other, Ratio):
            return other / self
        elif isinstance(other, int):
            return Ratio(int(other * self.den), int(self.num))
        elif isinstance(other, float):
            return self.den * other / self.num
        raise TypeError("wrong data type for rdivision.")
    
    def __invert__(self):
        return Ratio(int(self.den), int(self.num))


    def __add__(self, other):
        if isinstance(other, Ratio):
            den_lcm = self.lcm(other.den, self.den)
            return Ratio(int(self.num * (den_lcm / self.den) + other.num * (den_lcm / other.den)), int(den_lcm))
        elif isinstance(other, int):
            return Ratio(int(self.num + other * self.den), int(self.den))
        elif isinstance(other, float):
            return self.num / self.den + other
        raise TypeError("wrong data type for addition.")

    
    # Implements right side addition (same code as __add__)
    __radd__ = __add__


    def __neg__(self):
        return Ratio(int(self.num), -int(self.den))
    

    def __sub__(self, other):
        if isinstance(other, Ratio):
            den_lcm = self.lcm(other.den, self.den)
            return Ratio(int(self.num * (den_lcm / self.den) - other.num * (den_lcm / other.den)), int(den_lcm))
        elif isinstance(other, int):
            return Ratio(int(self.num - other * self.den), int(self.den))
        elif isinstance(other, float):
            return self.num / self.den - other
        raise TypeError("wrong data type for subtraction.")
    

    def __rsub__(self, other):
        if isinstance(other, Ratio):
            den_lcm = self.lcm(other.den, self.den)
            r = Ratio(int(other.num * (den_lcm / other.den) - self.num * (den_lcm / self.den)), int(den_lcm))
            if r.den == 1:
                return r
            else:
                return r.num / r.den
        elif isinstance(other, int):
            return Ratio(int(other * self.den - self.num), int(self.den))
        elif isinstance(other, float):
            return other - self.num / self.den
        raise TypeError("wrong data type for rsubtraction")


    def __mod__(self, other):
        if not isinstance(other, Ratio):
            raise TypeError("wrong type for modulo")
        common_den = self.lcm(self.den, other.den)
        this_num = int(self.num * (common_den / self.den))
        other_num = int(other.num * (common_den / other.den))
        return Ratio(int(this_num % other_num), int(common_den))


    def __pow__(self, other):
        if isinstance(other, Ratio):
            return pow(self.num / self.den, other.num / other.den)
        elif isinstance(other, int):
            return Ratio(int(pow(self.num, other)), int(pow(self.den, other)))
        elif isinstance(other, float):
            return pow(self.num / self.den, other)
        raise TypeError("wrong data type for power")


    def __rpow__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return pow(other, self.num / self.den)
        raise TypeError("wrong data type for power")


    def __lt__(self, other):
        if isinstance(other, Ratio):
            return self.compare(other) < 0
        elif isinstance(other, int) or isinstance(other, float):
            return self.compare(Ratio(other)) < 0
        raise TypeError("wrong data type for __lt__")

    
    def __le__(self, other):
        if isinstance(other, Ratio):
            return self.compare(other) <= 0
        elif isinstance(other, int) or isinstance(other, float):
            return self.compare(Ratio(other)) <= 0
        raise TypeError("wrong data type for __le__")

    
    def __eq__(self, other):
        if isinstance(other, Ratio):
            return self.compare(other) == 0
        elif isinstance(other, int) or isinstance(other, float):
            return self.compare(Ratio(other)) == 0
        raise TypeError("wrong data type for __eq__")         


    def __ne__(self, other):
        if isinstance(other, Ratio):
            return not (self.compare(other) == 0)
        elif isinstance(other, int) or isinstance(other, float):
            return not (self.compare(Ratio(other)) == 0)
        raise TypeError("wrong data type for __ne__")


    def __ge__(self, other):
        if isinstance(other, Ratio):
            return self.compare(other) >= 0
        elif isinstance(other, int) or isinstance(other, float):
            return self.compare(Ratio(other)) >= 0
        raise TypeError("wrong data type for __ge__")


    def __gt__(self, other):
        if isinstance(other, Ratio):
            return self.compare(other) > 0
        elif isinstance(other, int) or isinstance(other, float):
            return self.compare(Ratio(other)) > 0
        raise TypeError("wrong data type for __gt__")


    def __hash__(self):
        return int(self.num) << 16 + int(self.den)
    

    def compare(self, other):
        if not isinstance(other, Ratio):
            raise TypeError("incorrect type for comparison")
        return (self.num * other.den) - (other.num * self.den)


    @staticmethod
    def lcm(a, b):
        return (a * b) // gcd(int(a),int(b))

    
    def string(self):
        return f'{int(self.num)}/{int(self.den)}'


    def reciprocal(self):
        return self.__invert__()


    def dotted(self, dots=1):
        if not isinstance(dots, int) or dots <= 0:
            raise ValueError("invalid value for dotted")
        add_ratio = Ratio(int(self.num), int(self.den) * 2)
        while dots > 0:
            self += add_ratio
            add_ratio = Ratio(int(add_ratio.num), int(add_ratio.den) * 2)
            dots -= 1
        return self


    def tuplets(self, num, intimeof=1):
        if not isinstance(num, int) or not isinstance(intimeof, int):
            raise TypeError("invalid type for tuplets")
        return [Ratio(int(self.num * intimeof), int(self.den * num))] * num

    def tup(self, num):
        if not isinstance(num, int):
            raise ValueError("invalid value for tup")
        return Ratio(int(self.num), int(self.den) * num)


    def float(self):
        return self.num / self.den


    def seconds(self, tempo=60, beat=None):
        if not isinstance(tempo, int) or (beat is not None and not isinstance(beat, Ratio)):
            raise TypeError("invalid type for seconds")
        if beat is None:
            beat = Ratio(1,4)
        return 60 / (tempo * beat) * self.float()


if __name__ == '__main__':
    print("Testing...")

    # static method test
    print("testing lcm...")
    assert(Ratio.lcm(2, 5) == 10)
    assert(Ratio.lcm(6, 10) == 30)
    print("lcm test passed")

    print("testing __new__:")
    r = Ratio(8)
    print("testing: 8, num:", r.num, "den:", r.den)
    print(repr(r))

    r = Ratio(5.9)
    print("testing: 5.9, num:", r.num, "den:", r.den)
    print(r)

    r = Ratio('-4/-61')
    print("testing: '-4/-61', num:", r.num, "den:", r.den)
    print(r)

    r = Ratio(5, 20)
    print("testing: 5, 20, num:", r.num, "den:", r.den)
    print(r)
    print(repr(r * r))

    r = Ratio(1/-33)
    print("testing: 1, -33, num:", r.num, "den:", r.den)
    print(repr(r))

    r = Ratio(2, 9)
    print(r, r * 3)
    print(r * 0.3)

    print(Ratio(1, 4).tuplets(3), "answer: [Ratio(‘1/12’), Ratio(‘1/12’), Ratio(‘1/12’)]")
    print(Ratio(1, 4).tuplets(3, 2), "answer: [Ratio(‘1/6’), Ratio(‘1/6’), Ratio(‘1/6’)]")
    print(Ratio(1, 4).dotted(2), "desired_output = < Ratio: 7 / 16 >")
    print(Ratio(1, 4).dotted(3), " desired_output = < Ratio: 15 / 32 >")
    print(Ratio(7, 5) ** (-0.1), "answer: 0.9669125483457489")
    print(Ratio(11, 12) ** Ratio(7, 4), "answer: 0.8587564627309803")
    print(Ratio(3, 4) - 1.0, " desired_output = -0.25")
    print(Ratio(3, 4) + 1, " answer: < Ratio: 7 / 4 >")
    print(Ratio(3, 4) + 1.0, "answer: 1.75")
    print(Ratio(10, 5) * 1.2, " answer: 2.4")
    print(Ratio(4, 6) * Ratio(12), " answer: < Ratio: 8 / 1 >")
    print("< Ratio: -5 / 4 >,  ", Ratio(-10, 8))
    # print(Ratio('4'), " exception,")
    # print(Ratio('bob'), " exception")   

    print(Ratio(13,11)%Ratio(1,7), 'mod test')
    print(Ratio(1,4).dotted(1), 'dotted test')
    print(Ratio(1,4).dotted(3), 'dotted test')
    print(Ratio(1,1).dotted(3), 'dotted test')

    print(Ratio(1,4).seconds(), "test seconds")
    print(Ratio(3,8).seconds(90), "test seconds")
    print(Ratio(3,4).seconds(110,Ratio(1,8)), "test seconds")

    print(2 - Ratio(3,4))

    print("Done!")
