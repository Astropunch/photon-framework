from ..page import Page
from ..core import theme
from ..theme import Variants
from ..keymap import get_key
from .. import utils

import curses

class Checkbox(Page):
    def __init__(self, app, text = None, x = None, y = None, checked = False, variant:Variants = Variants.DEFAULT, reverse = False, auto_render = True):
        self.app = app 
        
        self.text = text if text else ""
        self.x = x if x != None else utils.centerX(app, len(self.text) + 4)
        self.y = y if y != None else utils.centerY(app, 1)
        
        self.checked = checked
        self.reverse = reverse
        self.variant = variant
        
        if not auto_render: return
        
        if not app.sc:
            raise Exception("App screen is not initialized.")
        
        self.on_render(app.sc)
        
    def on_render(self, sc):
        primary = theme.get_colors(self.variant)[1 if self.reverse else 0]
        sc.addstr(self.y, self.x, ("[x] " if self.checked else f"[ ] ") + str(self.text), curses.color_pair(primary))
        
    def on_input(self, key):
        if get_key(key) in [" ", "enter"]:
            self.checked = not self.checked