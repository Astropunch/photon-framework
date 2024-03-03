import photon
import os
import curses
import time

from photon.components import (Modal, Input, Text, Slider, CheckBox, SlideToggle,
    Enum, Button, Table, TableRow, Spinner, NavBar, NavTab, SideBar, SideBarRow)

from photon.core import theme
from photon.theme import Variants
from photon.keymap import get_key

#TODO: Sidebar, App Shell

class Index(photon.Page):
    def __init__(self, app):
        self.app = app
        self.key = 1
        
        self.bar = SideBar(self.app, items=[
            SideBarRow("App", False),
            SideBarRow("Home"),
            SideBarRow("More", False),
            SideBarRow("About"),
            SideBarRow("Contact"),
        ], y=1, selected=0, variant=Variants.PRIMARY, auto_render=False)
        
    def on_render(self, sc):        
        sc.addstr(self.app.screenY,0, f"Key: {self.key} / {get_key(self.key)}")
        
        self.bar.on_render(sc)
        
    def on_input(self, key):
        self.key = key
        
        self.bar.on_input(key)