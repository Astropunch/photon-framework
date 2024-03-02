from ..page import Page
from ..core import theme
from ..theme import Variants
from ..keymap import get_key
from .. import utils

import curses

class SlideToggle:
    def __init__(self, app, x = None, y = None, checked = False, enabled:Variants = Variants.SUCCESS, disabled:Variants = Variants.ERROR,
                 char:str = "@", auto_render = True):
        self.app = app 
        
        self.x = x if x != None else utils.centerX(app, 4)
        self.y = y if y != None else utils.centerY(app, 1)
        
        self.checked = checked
        
        self.char = char
        self.enabled = enabled
        self.disabled = disabled
        
        if not auto_render: return
        
        if not app.sc:
            raise Exception("App screen is not initialized.")
        
        self.on_render(app.sc)
        
    def on_render(self, sc):
        enabled = theme.get_colors(self.enabled)[1]
        disabled = theme.get_colors(self.disabled)[1]
        
        box = f"[ {self.char}]" if self.checked else f"[{self.char} ]"
        sc.addstr(self.y, self.x, box, curses.color_pair(enabled if self.checked else disabled))
        
        
    def on_input(self, key):
        if get_key(key) in [" ", "enter"]:
            self.checked = not self.checked