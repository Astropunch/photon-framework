import photon
import os
import curses
import time

from photon.components import Modal, Input, Text, Slider, Checkbox
from photon.core import theme
from photon.theme import Variants

#TODO: Checkbox, Slide toggle, Table, Sidebar, App Shell, List, Spinner/Loader

class Index(photon.Page):
    def __init__(self, app):
        self.app = app
        self.__key__ = 1
        
        self.start = time.time()
        
        self.checkbox = Checkbox(self.app, "This is a checkbox", y=15, variant=Variants.DEFAULT, reverse=False, auto_render=False)
    
    def on_render(self, sc):
        Text(self.app, f"FPS: {self.app.fps}", y=12, variant=Variants.PRIMARY)
        Slider(self.app, value=self.app.fps, max=150_000, width=110, border=False, char_pre="-", variant=Variants.PRIMARY, reverse=True)
        
        self.checkbox.text = f"I am {'checked' if self.checkbox.checked else 'unchecked'}"
        
        self.checkbox.on_render(sc)
        
        
    def on_input(self, key):
        self.__key__ = key
        
        self.checkbox.on_input(key)