import photon
import os
import curses

from photon.components import Modal, Input, Text
from photon.core import theme
from photon.theme import Variants


class Root(photon.Page):
    def __init__(self, app):
        self.app = app
        self.__key__ = 1
        

    
    def on_render(self, sc):
        Text(self.app, "PhotonUI Framework Application", y=0, variant=Variants.PRIMARY)
        Text(self.app, "https://github.com/astropunch/photon-framework", y=1)
        
        Modal(self.app, "PhotonUI", f"Running at {self.app.fps} frames")
        
        
    def on_input(self, key):
        self.__key__ = key 