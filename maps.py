from utils import MAX_X, MAX_Y

class Location:
    #coordinates = ((x1,y1), (x2,y2), (x3, y3), ...)
    def __init__(self, coordinates, window, char = '#'):
        self.coordinates = coordinates
        self.window = window
        self.char = char
    
    def render(self):
        for x, y in self.coordinates:
            self.window.addstr(y, x, self.char)
    
    @property
    def coor(self):
        return self.coordinates
    
def map1_coor_gen(marginX = 6):
    left_wall = ((marginX + 1, i) for i in range(6, MAX_Y - 6 + 1))
    right_wall = ((MAX_X - marginX, i) for i in range(6, MAX_Y - 6 + 1))

    return tuple(left_wall) + tuple(right_wall)

def map2_coor_gen():
    a = ((i, 1) for i in range(1, 9))
    b = ((1, i) for i in range(2, 6))
    c = ((1, i) for i in range(18, 13, -1))
    d = ((i, 18) for i in range(2, 9))
    e = ((i, 9) for i in range(1, 12))
    f = ((i, 1) for i in range(34, 26, -1))
    g = ((34, i) for i in range(2, 6))
    h = ((i, 9) for i in range(34, 23, -1))
    i = ((34, i) for i in range(18, 13, -1))
    j = ((i, 18) for i in range(33, 26, -1))

    return tuple(a) + tuple(b) + tuple(c) + tuple(d) + tuple(e) + tuple(f) + tuple(g) + tuple(h) + tuple(i) + tuple(j)

def map3_coor_gen():
    a = ((i, 7) for i in range(1, 8))
    b = ((7, i) for i in range(1, 7))
    c = ((i, 14) for i in range(1, 8))
    d = ((18, i) for i in range(1, 6))
    e = ((12, i) for i in range(10, 13))
    f = ((i, 10) for i in range(13, 16))
    g = ((16, i) for i in range(10, 13))
    i = ((28, i) for i in range(7, 19))
    l = ((i, 6) for i in range(34, 27, -1))

    return tuple(a) + tuple(b) + tuple(c) + tuple(d) + tuple(e) + tuple(f) + tuple(g) + tuple(i) + tuple(l)


loc1_coor = map1_coor_gen()
loc1_safe = (13,3)
point1 = 20

loc2_coor = map2_coor_gen()
loc2_safe = (13,3)
point2 = 15

loc3_coor = map3_coor_gen()
loc3_safe = (7, 8)
point3 = 10

if __name__ == '__main__':
    print(loc1_coor, loc1_safe, point1)
    print(loc2_coor, loc2_safe, point2)
    print(loc3_coor, loc3_safe, point3)