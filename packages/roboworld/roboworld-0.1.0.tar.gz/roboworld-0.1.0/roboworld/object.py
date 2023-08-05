class Object():
    def __init__(self, position, name) -> None:
        self.name = name
        self.position = position

    def __str__(self) -> str:
        return self.name

    def set_position(self, position):
        self.position = position
