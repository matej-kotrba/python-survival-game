import math


def get_angle(p1, p2):
        return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

