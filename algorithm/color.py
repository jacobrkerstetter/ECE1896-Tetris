# class to hold the colors of the blocks

class Color:
    colors = {
        'red': (255, 0, 0),
        'darkBlue': (0, 0, 255),
        'green': (0, 255, 0),
        'purple': (128, 0, 128),
        'yellow': (255, 255, 0),
        'lightBlue': (0, 255, 255),
        'orange': (255, 127, 0)
    }

    @classmethod
    def getColorList(cls):
        return cls.colors