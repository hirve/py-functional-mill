import math, random

random.seed(1)

def sine (x, y):
    return math.sin(0.15 * x + 0.9 * y)

def wood (x, y):
    return min(math.sin(0.25 * x + (0.25 * (y - 25)) ** 2), -0.3) + 0.1

def waves (x, y):
    points = [
        ( -30, -30, 0.5, 6 ),
    ]
    distances = [ math.sqrt((p[0] - x) ** 2 + (p[1] - y) ** 2) for p in points ]
    sum = 0
    i = 0
    for d in distances:
        sum = sum + math.sin(d * points[i][2]) * points[i][3] / (1 + d ** 2 / 300)
        i += 1
    return sum - 1

def chess (x, y):
    return 0 - (int(x % 20 > 10) ^ int(y % 20 > 10))
