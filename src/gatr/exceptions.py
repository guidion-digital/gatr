class GATRError(Exception):
    def __init__(self, errors: str):
        self.errors = errors
