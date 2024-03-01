from ..page import Page
from ..core import theme
from ..theme import Variants
from .. import utils

import curses

class Slider(Page):
    def __init__(self, app, value=0, max=100, width: int = 30, x = None, y = None,
                 border = True, char_pre = "#", char_post = " ", char_point = "@", variant: Variants = Variants.DEFAULT, reverse=False,
                 auto_render = True):
        
        self.app = app
        self.variant = variant
        self.width = width - 1
        self.value = value
        self.max = max if max > 0 else 100
        
        self.x = x
        self.y = y
        
        self.border = border
        self.char_pre = char_pre
        self.char_post = char_post
        self.char_point = char_point
        self.reverse = reverse
        
        
        if not auto_render: return
        if not app.sc:
            raise Exception("App screen is not initialized.")
        self.on_render(app.sc)
        
    def on_render(self, sc):
        color = theme.get_colors(self.variant)[1 if self.reverse else 0]
        
        #with border
        # [-----•-----------------]
        #without border
        #  -----•-----------------
        
        if self.value > self.max: self.value = self.max
        
        percentage_full = int(self.value / self.max * self.width)
        percentage_empty = self.width - percentage_full
        
        
        
        if self.border:
            bar = f"[{self.char_pre * percentage_full}{self.char_point}{self.char_post * percentage_empty}]"
        else:
            bar = f"{self.char_pre * percentage_full}{self.char_point}{self.char_post * percentage_empty}"
            
        x = self.x if self.x else utils.centerX(self.app, len(bar))
        y = self.y if self.y else utils.centerY(self.app)
        
        sc.addstr(y, x, bar, curses.color_pair(color))
        
        
        
        