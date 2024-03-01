import photon
import os
import curses
import time

from photon.components import Modal, Input, Text, Slider
from photon.core import theme
from photon.theme import Variants


class Index(photon.Page):
    def __init__(self, app):
        self.app = app
        self.__key__ = 1
        
        self.start = time.time()
    
    def on_render(self, sc):
        Text(self.app, f"FPS: {self.app.fps}", y=12, variant=Variants.PRIMARY)
        Slider(self.app, value=self.app.fps, max=150_000, width=110, border=False, char_pre="-", variant=Variants.PRIMARY, reverse=True)
        
        
    def on_input(self, key):
        self.__key__ = key