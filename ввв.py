import random

coord = [[61, 165], [61, 245], [61, 328]]


coord_new = coord[:]

while len(coord_new) > 0:
    a = random.choice(coord_new)
    coord_new.remove(a)
    print(a)
    print(coord_new)
