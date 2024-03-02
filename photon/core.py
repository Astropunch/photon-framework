from .theme import Theme, default_theme

theme = default_theme

class Version:
    def __init__(self, major:int, minor:int, patch:int):
        self.major = major
        self.minor = minor
        self.patch = patch

        self.release = f"{major}.{minor}.{patch}"

version = Version(0, 1, 0)
        