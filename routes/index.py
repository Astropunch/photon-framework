import photon
import os
import curses

from photon.components import Modal, Input, Text
from photon.core import theme
from photon.theme import Variants


class Index(photon.Page):
    def __init__(self, app):
        self.app = app
        self.__key__ = 1
        

    
    def on_render(self, sc):  
        Modal(self.app, "PhotonUI", f"Running at {self.app.fps} frames")
        
        
    def on_input(self, key):
        self.__key__ = key 