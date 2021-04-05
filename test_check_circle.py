import math

def check_circle(center, radius, point):
    x1, y1 = center[0], center[1]
    x2, y2 = point[0], point[1]
    print(math.sqrt((x1 - x2)**2 + (y1 - y2)**2))
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2) <= radius


def check_if():
    return bool(0)


def main():
    assert check_circle((0, 0), 100, (50, 0))
    assert not check_if()


if __name__ == "__main__":
    main()
