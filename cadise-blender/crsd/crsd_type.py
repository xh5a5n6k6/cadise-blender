import mathutils

class CrsdReal:
    def __init__(self, value: float=0.0):
        self.value = value
    
    def to_string(self):
        return "{:.6f}".format(self.value)

class CrsdVector3r:
    def __init__(self, vector: mathutils.Vector=mathutils.Vector((0, 0, 0))):
        self.x = vector.x
        self.y = vector.y
        self.z = vector.z
    
    def to_string(self):
        return "{:.6f} {:.6f} {:.6f}".format(self.x, self.y, self.z)

class CrsdVector3rArray:
    def __init__(self):
        self.vectors = []

    def to_string(self):
        return ",".join([vector.to_string() for vector in self.vectors])

    def append(self, vector: CrsdVector3r):
        self.vectors.append(vector)