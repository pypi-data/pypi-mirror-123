class SerializableDataclassRegistry(object):
    __instance = None
    __registered_classes = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(SerializableDataclassRegistry, cls).__new__(cls)
        return cls.__instance

    def register(self, cls: type):
        self.__registered_classes[cls.__qualname__] = cls

    def __len__(self):
        return len(self.__registered_classes)
