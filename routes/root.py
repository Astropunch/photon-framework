import photon
import os
import curses

from photon.components import Text
from photon.theme import Variants


class Root(photon.Page):
    def __init__(self, app):
        self.app = app
        self.__key__ = 1
    
    def on_render(self, sc):
        Text(self.app, "Devbuild", y=self.app.screenY, variant=Variants.ERROR)
        
        
    def on_input(self, key):
        self.__key__ = key 