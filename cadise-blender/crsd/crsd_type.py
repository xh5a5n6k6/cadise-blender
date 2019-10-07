import mathutils

class CrsdReal:
    def __init__(self, value: float=0.0):
        self.__value = value
    
    def to_string(self):
        return "{:.6f}".format(self.__value)

class CrsdVector3r:
    def __init__(self, vector: mathutils.Vector=mathutils.Vector((0, 0, 0))):
        self.__x = vector.x
        self.__y = vector.y
        self.__z = vector.z
    
    def to_string(self):
        return "{:.6f} {:.6f} {:.6f}".format(self.__x, self.__y, self.__z)

class CrsdVector3rArray:
    def __init__(self):
        self.__vectors = []

    def to_string(self):
        return ",".join([vector.to_string() for vector in self.__vectors])

    def append(self, vector: CrsdVector3r):
        self.__vectors.append(vector)