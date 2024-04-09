from field import Field


if __name__ == '__main__':
    field = Field()
    field.add_random_holes(5)
    field.add_random_orbs(5)
    
    for h in field.holes:
        print(h)

    for o in field.orbs:
        print(o)