class ResourceAlreadyExist(Exception):
    def __init__(self, arg):
        self.args = arg

class ResourceNotFound(Exception):
    pass