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

    def __init__(self, lowerBoundType, upperBoundType=None):
        if lowerBoundType == '?':
            self.__init__('b', 't')
        elif upperBoundType == None:
            self.__init__(lowerBoundType, lowerBoundType)
        else:
            self.lowerBoundType = lowerBoundType
            self.lowerBoundValue = SecurityLabel.lattice[lowerBoundType]
            self.upperBoundType = upperBoundType
            self.upperBoundValue = SecurityLabel.lattice[upperBoundType]

    def __lt__(self, other):
        return self.isDynamicLabel() or other.isDynamicLabel() or self.upperBoundValue < other.lowerBoundValue

    def __le__(self, other):
        return other.isDynamicLabel() or self.upperBoundValue <= other.lowerBoundValue

    def __str__(self):
        return "(" + self.lowerBoundType + ", " + self.upperBoundType + ")"

    def isDynamicLabel(self):
        return self.lowerBoundValue != self.upperBoundValue

    @staticmethod
    def staticJoin(securityLabel1, securityLabel2):
        if securityLabel1.isDynamicLabel():
            return securityLabel1
        if securityLabel2.isDynamicLabel():
            return securityLabel2
        return securityLabel1 if securityLabel1 >= securityLabel2 else securityLabel2

    @staticmethod
    def staticJoinMultiple(securityLabels):
        return reduce(SecurityLabel.staticJoin, securityLabels, SecurityLabel('b'))

    @staticmethod
    def dynamicJoin(securityLabel1, securityLabel2):
        lowerBoundType = securityLabel1.lowerBoundType if securityLabel1.lowerBoundValue >= securityLabel2.lowerBoundValue \
            else securityLabel2.lowerBoundType
        upperBoundType = securityLabel1.upperBoundType if securityLabel1.upperBoundValue >= securityLabel2.upperBoundValue \
            else securityLabel2.upperBoundType
        return SecurityLabel(lowerBoundType, upperBoundType)

    @staticmethod
    def dynamicJoinMultiple(securityLabels):
        return reduce(SecurityLabel.dynamicJoin, securityLabels, SecurityLabel('b'))

    @staticmethod
    def staticMeet(securityLabel1, securityLabel2):
        if securityLabel1.isDynamicLabel():
            return securityLabel1
        if securityLabel2.isDynamicLabel():
            return securityLabel2
        return securityLabel1 if securityLabel1 <= securityLabel2 else securityLabel2

    @staticmethod
    def staticMeetMultiple(securityLabels):
        return reduce(SecurityLabel.staticMeet, securityLabels, SecurityLabel('t'))

    @staticmethod
    def dynamicMeet(securityLabel1, securityLabel2):
        lowerBoundType = securityLabel1.lowerBoundType if securityLabel1.lowerBoundValue <= securityLabel2.lowerBoundValue \
            else securityLabel2.lowerBoundType
        upperBoundType = securityLabel1.upperBoundType if securityLabel1.upperBoundValue <= securityLabel2.upperBoundValue \
            else securityLabel2.upperBoundType
        return SecurityLabel(lowerBoundType, upperBoundType)

    @staticmethod
    def dynamicMeetMultiple(securityLabels):
        return reduce(SecurityLabel.staticMeet, securityLabels, SecurityLabel('t'))


class RefType(SecurityType):
    def __init__(self, referencedSecurityType):
        SecurityType.__init__(self, referencedSecurityType.type, referencedSecurityType.securityLabel)
        self.referencedSecurityType = referencedSecurityType

    def __str__(self):
        return '<ref ' + str(self.referencedSecurityType) + '>'


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
