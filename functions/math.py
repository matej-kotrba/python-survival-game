import math as m


def get_distance(o1, o2):
    return m.sqrt((o2[0] - o1[0]) ** 2 + (o2[1] - o1[1]) ** 2)

def get_xys(o1, o2):
    distance = get_distance(o1, o2)
    if distance == 0:
        return (0, 0)
    return ((o2[0] - o1[0]) / distance, (o2[1] - o1[1]) / distance)