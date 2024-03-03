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
        
        rows = []
        for x in range(0, 20):
            x += 1
            rows.append(TableRow([f"Song {x}", f"Artist {x}", f"Album {x}", f"Duration {x}"]))
        
        self.table = Table(app, sizeY=5, headers=["Song", "Artist", "Album", "Duration"], rows=rows, selected=0, variant=Variants.DEFAULT, auto_render=False)
        
    def on_render(self, sc):        
        self.table.on_render(sc)
        sc.addstr(0,0, f"Key: {self.key} / {get_key(self.key)}")
        
    def on_input(self, key):
        self.key = key
        
        self.table.on_input(key)