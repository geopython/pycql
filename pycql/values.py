class _Value:
    def __init__(self, value):
        self.value = value
    
    def __eq__(self, other):
        if type(self) != type(other):
            return False

        return self.value == other.value

class Geometry(_Value):
    pass

class Time(_Value):
    pass

class Duration(_Value):
    pass

class BBox(_Value):
    pass
