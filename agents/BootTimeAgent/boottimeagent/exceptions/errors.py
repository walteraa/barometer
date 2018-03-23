class VariableMissingError(Exception):

    def __init__(self, message):
        self.message = message


class InvalidStateError(Exception):

    def __init__(self, message):
        self.message = message


class InvalidConfigFileError(Exception):

    def __init__(self, message):
        self.message = message


class VMCreationError(Exception):

    def __init__(self, message):
        self.message = message

class VMStatusError(Exception):

    def __init__(self, message):
        self.message = message
