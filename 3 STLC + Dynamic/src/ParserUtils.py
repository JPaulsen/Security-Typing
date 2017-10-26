def checkLengthExpected(name, expr, n):
    if len(expr) != n:
        lastPart = ' elements.'
        if n == 1:
            lastPart = ' element.'
        raise ValueError(name + ' expressions must have ' + str(n) + lastPart)
