import photon
import os
import curses
import time

from photon.components import Modal, Input, Text, Slider, Checkbox, SlideToggle, Enum
from photon.core import theme
from photon.theme import Variants
from photon.keymap import get_key

#TODO: Table, Sidebar, App Shell, Spinner/Loader, Navbar, Button
class Index(photon.Page):
    def __init__(self, app):
        self.app = app
        self.__key__ = 1
        
        self.start = time.time()
        
        self.enum = Enum(self.app, values=["Hello", "World", "This", "Is", "A", "Test"], y=10, selected=0, variant=Variants.PRIMARY, reverse=True, auto_render=False)
    
    def on_render(self, sc):
        Text(self.app, f"FPS: {self.app.fps}", y=12, variant=Variants.PRIMARY)
        Slider(self.app, value=self.app.fps, max=150_000, width=110, border=False, char_pre="-", variant=Variants.PRIMARY, reverse=True)
        
        self.enum.on_render(sc)
        
        
    def on_input(self, key):
        self.__key__ = key
        
        self.enum.on_input(key)