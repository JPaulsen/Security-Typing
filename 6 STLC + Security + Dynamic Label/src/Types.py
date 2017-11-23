class FunctionType:
    def __init__(self, returnType, parameterTypes):
        self.returnType = returnType
        self.parameterTypes = parameterTypes

    def __str__(self):
        return 'function ' + str(self.returnType) + ' [' + ', '.join(map(str, self.parameterTypes)) + ']'


class SecurityType:
    def __init__(self, type, securityLabel):
        self.type = type
        self.securityLabel = securityLabel

    def __str__(self):
        return '(' + str(self.type) + ', ' + str(self.securityLabel) + ')'


class SecurityLabel:
    lattice = {
        'b': 0,
        'l': 1,
        'h': 2,
        't': 3,
        '?': -1,
    }

    def __init__(self, type):
        self.type = type
        self.value = SecurityLabel.lattice[type]

    def __lt__(self, other):
        return self.isDynamicLabel() or other.isDynamicLabel() or self.value < other.value

    def __le__(self, other):
        return other.isDynamicLabel() or self.value <= other.value

    def __str__(self):
        return self.type

    def isDynamicLabel(self):
        return self.value == SecurityLabel.lattice['?']

    @staticmethod
    def join(securityLabel1, securityLabel2):
        if securityLabel1.isDynamicLabel():
            return securityLabel1
        if securityLabel2.isDynamicLabel():
            return securityLabel2
        return securityLabel1 if securityLabel1 >= securityLabel2 else securityLabel2

    @staticmethod
    def joinMultiple(securityLabels):
        return reduce(SecurityLabel.join, securityLabels, SecurityLabel('b'))

    @staticmethod
    def meet(securityLabel1, securityLabel2):
        if securityLabel1.isDynamicLabel():
            return securityLabel1
        if securityLabel2.isDynamicLabel():
            return securityLabel2
        return securityLabel1 if securityLabel1 <= securityLabel2 else securityLabel2

    @staticmethod
    def meetMultiple(securityLabels):
        return reduce(SecurityLabel.meet, securityLabels, SecurityLabel('t'))


class SecurityValue:
    def __init__(self, value, securityLabel):
        self.value = value
        self.securityLabel = securityLabel

    def __str__(self):
        return '(' + str(self.value) + ', ' + str(self.securityLabel) + ')'

    def __add__(self, other):
        return SecurityValue(self.value + other.value, SecurityLabel.join(self.securityLabel, other.securityLabel))

    def __mul__(self, other):
        return SecurityValue(self.value * other.value, SecurityLabel.join(self.securityLabel, other.securityLabel))

    def __sub__(self, other):
        return SecurityValue(self.value - other.value, SecurityLabel.join(self.securityLabel, other.securityLabel))

    def __mod__(self, other):
        return SecurityValue(self.value % other.value, SecurityLabel.join(self.securityLabel, other.securityLabel))

    def __div__(self, other):
        return SecurityValue(self.value / other.value, SecurityLabel.join(self.securityLabel, other.securityLabel))

    def __lt__(self, other):
        return SecurityValue(self.value < other.value, SecurityLabel.join(self.securityLabel, other.securityLabel))

    def __le__(self, other):
        return SecurityValue(self.value <= other.value, SecurityLabel.join(self.securityLabel, other.securityLabel))

    def __eq__(self, other):
        return SecurityValue(self.value == other.value, SecurityLabel.join(self.securityLabel, other.securityLabel))

    def __ne__(self, other):
        return SecurityValue(not self == other, SecurityLabel.join(self.securityLabel, other.securityLabel))

    def __gt__(self, other):
        return SecurityValue(self.value > other.value, SecurityLabel.join(self.securityLabel, other.securityLabel))

    def __ge__(self, other):
        return SecurityValue(self.value >= other.value, SecurityLabel.join(self.securityLabel, other.securityLabel))

    def boolAnd(self, other):
        return SecurityValue(self.value and other.value, SecurityLabel.join(self.securityLabel, other.securityLabel))

    def boolOr(self, other):
        return SecurityValue(self.value or other.value, SecurityLabel.join(self.securityLabel, other.securityLabel))

    def boolNot(self):
        return SecurityValue(not self.value, self.securityLabel)
