from pkg_resources import resource_filename, Requirement
class ConfigEnum(Enum):
    def __init__(self):
        self.dict = {
            "IMAGE_HEIGHT": 128,
            "IMAGE_WIDTH": 128,
            "CNN_30MIN_MODEL": resource_filename(__name__, 'model/modelCNN-1630841987.h5'),
            "CNN_DEFAULT_MODEL": resource_filename(__name__, 'model/modelCNN-1605022224.h5')
        }
    def get(self, key):
        return self.dict[key]
