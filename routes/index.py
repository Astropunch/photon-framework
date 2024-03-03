import photon
import os
import curses
import time

from photon.components import (Modal, Input, Text, Slider, CheckBox, SlideToggle,
    Enum, Button, Table, TableRow, Spinner, NavBar, NavTab)

from photon.core import theme
from photon.theme import Variants
from photon.keymap import get_key

#TODO: Sidebar, App Shell
#DOING: Navbar

class Index(photon.Page):
    def __init__(self, app):
        self.app = app
        self.key = 1
        
        self.navbar = NavBar(self.app, "Photon", [
            NavTab("Home", ["x"], "Index"),
            NavTab("About", ["c"], "About"),
            NavTab("Settings", ["v"], "Settings"),
        ], large=True, auto_render=False)
        
    def on_render(self, sc):        
        sc.addstr(self.app.screenY,0, f"Key: {self.key} / {get_key(self.key)}")
        
        self.navbar.on_render(sc)
        
    def on_input(self, key):
        self.key = key
        
        self.navbar.on_input(key)