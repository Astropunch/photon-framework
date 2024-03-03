import photon
import os
import curses
import time

from photon.components import Modal, Input, Text, Slider, Checkbox, SlideToggle, Enum, Button, Table, TableRow
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
            rows.append(TableRow([f"Song {x}", f"Artist {x}", f"Album {x}", f"0:00"]))
        
        self.table = Table(
            self.app, sizeY=20, y=3,
            headers=["Song", "Artist", "Album", "Duration"], rows=rows, selected=0, 
            on_click=self.on_table_click,
            variant=Variants.DEFAULT, auto_render=False)

        self.text = Text(self.app, "Press enter", x=0, y=self.app.screenY, variant=Variants.PRIMARY, auto_render=False)
        
    def on_render(self, sc):        
        self.table.on_render(sc)
        self.text.on_render(sc)
        
    def on_input(self, key):
        self.key = key
        
        self.table.on_input(key)
        
    def on_table_click(self, index, row:TableRow):
        print(f"Clicked on row {index}")
        self.text.text = f"Clicked on row {index} ({row.values[0]})"