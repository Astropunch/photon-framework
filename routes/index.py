import photon
import os
import curses
import time

from photon.components import Modal, Input, Text, Slider, Checkbox, SlideToggle, Enum, Button, Table, TableRow, Spinner
from photon.core import theme
from photon.theme import Variants
from photon.keymap import get_key

#TODO: Sidebar, App Shell, Spinner/Loader, Navbar

class Index(photon.Page):
    def __init__(self, app):
        self.app = app
        self.key = 1
        
        self.spinner = Spinner(app, auto_render=False)
        
    def on_render(self, sc):        
        self.spinner.on_render(sc)
        
    def on_input(self, key):
        self.key = key