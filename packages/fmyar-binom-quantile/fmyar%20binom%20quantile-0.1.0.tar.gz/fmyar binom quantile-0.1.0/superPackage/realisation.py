from scipy.stats import binom

def getLeftBinom(left, right, n, p, alpha):
    sm = 0
    for i in range(left, right):
        d = binom(n, p).pmf(i)
        if sm + d <= alpha:
            sm += d
        else:
            return i
    return right


def getRightBinom(left, right, n, p, alpha):
    sm = 0
    for i in range(right, left, -1):
        d = binom(n, p).pmf(i)
        if sm + d <= alpha:
            sm += d
        else:
            return i + 1
    return left
