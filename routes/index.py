import photon
import os
import curses
import time

from photon.components import Modal, Input, Text, Slider, Checkbox, SlideToggle, Enum, Button
from photon.core import theme
from photon.theme import Variants
from photon.keymap import get_key

#TODO: Table, Sidebar, App Shell, Spinner/Loader, Navbar

class Index(photon.Page):
    def __init__(self, app):
        self.app = app
        self.key = 1
        
        self.btn = Button(self.app, "Open Modal", on_click=self.open_modal, auto_render=False) 
        self.modal = False
        
    def on_render(self, sc):
        self.btn.on_render(sc)
        
        if self.modal:
            Modal(self.app, "Hello World", "This is a modal window.\nPress 'q' to close.", auto_render=True)
        
    def on_input(self, key):
        self.key = key
        self.btn.on_input(key)
        
        if get_key(key) == "q":
            self.modal = False
        
    def open_modal(self):
        self.modal = True