from ..page import Page
from ..core import theme
from ..theme import Variants
from .. import utils

import curses

class Text:
    def __init__(self, app, text = "", x=None, y=None, variant:Variants = Variants.DEFAULT, reverse = False,
                auto_render = True):

        self.app = app
        
        self.x = x if x != None else utils.centerX(app, len(text))
        self.y = y if y != None else utils.centerY(app, 1)
        self.reverse = reverse
        
        self.text = text
        self.variant = variant
        
        if not auto_render: return
        
        if not app.sc:
            raise Exception("App screen is not initialized.")
        
        self.on_render(app.sc)
        
    def on_render(self, sc):
        primary = theme.get_colors(self.variant)[1 if self.reverse else 0]
        
        sc.addstr(self.y, self.x, self.text, curses.color_pair(primary))