from ..page import Page
from ..core import theme
from ..theme import Variants
from ..keymap import get_key
from .. import utils

import curses

class TableRow:
    def __init__(self, values: list = []):
        self.values = values
        
    def max_size(self):
        return max([len(str(x)) for x in self.values])

class Table(Page):
    def __init__(self, app, x = None, y = None, sizeY = 10, headers = [], rows:list[TableRow] = [], selected: int = None, variant:Variants = Variants.DEFAULT, auto_render = True):
        self.app = app
        
        self.x = x
        self.y = y
        self.sizeY = sizeY
        
        self.headers = headers
        self.rows = rows
        self.selected = selected
        
        self.variant = variant
        
        for row in self.rows:
            if type(row) != TableRow:
                raise ValueError("Rows must be of an insance of TableRow")
        
        if not auto_render: return
        if not app.sc:
            raise Exception("App screen is not initialized.")
        
        self.on_render(app.sc)
        
    def on_render(self, sc):
        colors = theme.get_colors(self.variant)
        fg = colors[0]
        bg = colors[1]
        
        #calculate max sizes
        max_sizes = [len(x) for x in self.headers]
        for row in self.rows:
            for i, value in enumerate(row.values):
                size = len(str(value))
                if size > max_sizes[i]:
                    max_sizes[i] = size
                    
                #  row sizes   &  space between rows
        sizeX = sum(max_sizes) + len(max_sizes) - 1    
        sizeY = self.sizeY if self.sizeY + self.y < self.app.screenY else self.app.screenY - self.y
        
        #WIP - add scroll, rendering only visible rows
        