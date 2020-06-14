import random


class Colors:
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    GRAY = (128, 128, 128)
    LATE_GRAY = (47, 79, 79)
    ORANGE = (255, 80, 10)
    BORDO = (128, 0, 0)
    CHOCOLAT = (210, 115, 50)
    FIOLET = (133, 87, 171)
    C1 = (110, 114, 144)
    WHITE1 = (255, 255, 255)
    RED1 = (255, 0, 0)
    GREEN1 = (0, 255, 0)
    BLACK1 = (0, 0, 0)
    BLUE1 = (0, 0, 255)
    GRAY1 = (128, 128, 128)
    LATE_GRAY1 = (47, 79, 79)
    ORANGE1 = (255, 80, 10)
    BORDO1 = (128, 0, 0)
    CHOCOLAT1 = (210, 115, 50)
    FIOLET1 = (133, 87, 171)

    ArrayColors = [
        WHITE,
        RED,
        GREEN,
        BLACK,
        BLUE,
        GRAY,
        LATE_GRAY,
        ORANGE,
        BORDO,
        CHOCOLAT,
        FIOLET,
        C1,
        WHITE1,
        RED1,
        GREEN1,
        BLACK1,
        BLUE1,
        GRAY1,
        LATE_GRAY1,
        ORANGE1,
        BORDO1,
        CHOCOLAT1,
        FIOLET1
        ]

    def get_color_for_index(self, idx):
        return self.ArrayColors[idx]

    def get_random_color(self):
        return random.randint(60, 255), random.randint(60, 255), random.randint(60, 255)

