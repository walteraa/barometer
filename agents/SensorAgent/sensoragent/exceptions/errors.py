class VariableMissingError(Exception):

    def __init__(self, message):
        self.message = message


class InvalidStateError(Exception):

    def __init__(self, message):
        self.message = message


class InvalidConfigFileError(Exception):

    def __init__(self, message):
        self.message = message


class RetrieveAttributesError(Exception):

    def __init__(self, message):
        self.message = message
