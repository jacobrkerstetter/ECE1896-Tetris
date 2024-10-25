# class to hold the colors of the blocks

class Color:
    colors = {
        'red': 'r',
        'darkBlue': 'd',
        'green': 'g',
        'purple': 'p',
        'yellow': 'y',
        'lightBlue': 'l',
        'orange': 'o'
    }

    pairMap = {
        'r': 1,
        'd': 4,
        'g': 2,
        'p': 5,
        'y': 3,
        'l': 6,
        'o': 7
    }

    @classmethod
    def getColorList(cls):
        return cls.colors