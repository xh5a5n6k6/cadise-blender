"""
Each SdData has its type and lots of SdDataUnits.
Its string format follow the rule:

    SdData_type {
        [sdDataUnit]
        [sdDataUnit]
        ...
    }

"""
class SdData:
    def __init__(self, sd_type):
        self.__type       = sd_type
        self.__data_units = []

    def to_string(self):
        total_string = ""
        total_string += self.__type + " {\n"
        for data_unit in self.__data_units:
            total_string += data_unit.to_string()
        total_string += "}\n"

        return total_string
    
    def add_data_unit(self, data_unit):
        self.__data_units.append(data_unit)

"""
Each SdDataUnit is enclosed by [].
Its string format follows the rule:

    \t[name type "value"]

    Ex. [output-filename string "cadise-blender-scene.jpg"]
        [albedo rgb "1.0 1.0 1.0"]

"""
class SdDataUnit:
    def __init__(self, name, sd_data_unit_type, value):
        self.__name  = name
        self.__type  = sd_data_unit_type
        self.__value = value

    def to_string(self):
        return "\t[{} {} \"{}\"]\n".format(self.__name, self.__type, self.__value)