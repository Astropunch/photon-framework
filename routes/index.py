import photon
import os

from . import about

class Index(photon.Page):
    def __init__(self, app):
        self.app = app
        self.__key__ = None
    
    def on_render(self, sc):
        sc.addstr(0, 0, "Hello, world!")
        sc.addstr(2, 0, f"Screen dimensions: {self.app.screenX}x{self.app.screenY}")
        sc.addstr(3, 0, f"Press any key: {self.__key__}")
        sc.addstr(5, 0, "Press 'enter' to go to the about page.")
        
    def on_input(self, key):
        self.__key__ = key
        
        if key == 10: #enter
            self.app.open("About")
            return