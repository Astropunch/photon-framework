from ..page import Page
from . import theme

class Modal(Page):
    def __init__(self, title = "", content = ""):
        self.title = title
        self.content = content