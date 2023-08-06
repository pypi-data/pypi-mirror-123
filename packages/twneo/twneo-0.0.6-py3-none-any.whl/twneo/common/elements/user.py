class User:

    def __init__(self, id, name , location ='NA'):
        self.id = id
        self.name = name
        self.location = location

    def __str__(self) -> str:
        return __name__+",".join(self.__dict__.values())




