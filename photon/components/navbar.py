from ..page import Page
from ..core import theme
from ..theme import Variants
from ..keymap import get_key
from .. import utils

import curses

class NavTab:
    def __init__(self, name, keys = ["#"], page_id = None):
        self.name = name
        self.keys = keys
        self.page = page_id

class NavBar(Page):
    """
    Represents a navigation bar component that displays a title and a list of tabs.
    
    Args:
        app (Photon): The parent application object.
        title (str): The title of the navigation bar.
        tabs (list[NavTab], optional): The list of tabs to be displayed. Defaults to an empty list.
        variant (Variants, optional): The variant of the navigation bar. Defaults to Variants.DEFAULT.
        large (bool, optional): Specifies whether the navigation bar should be large. Defaults to True.
        on_click (callable, optional): The callback function to be called when a tab is clicked. Defaults to None.
        auto_render (bool, optional): Specifies whether the navigation bar should be automatically rendered. Defaults to True.
    """
    def __init__(self, app, title, tabs:list[NavTab] = [], variant:Variants = Variants.DEFAULT, large:bool = True, on_click:callable = None, auto_render = True):
        self.app = app
        
        self.title = "" if title is None else title
        self.tabs = tabs
        
        self.large = large
        self.variant = variant
        self.callback = on_click
        
        if not auto_render: return
        if not app.sc:
            raise Exception("App screen is not initialized.")
        
        self.on_render(app.sc)
        
    def on_render(self, sc):
        colors = theme.get_colors(self.variant)
        
        #Title     [Tab1] [Tab2] [Tab3]#
        
        sc.addstr(0, 0, " " * self.app.screenX, curses.color_pair(colors[1]))
        if self.large:
            for i in range(2):
                sc.addstr(i+1, 0, " " * self.app.screenX, curses.color_pair(colors[1]))
            
        
        sc.addstr(1 if self.large else 0, 2, self.title, curses.color_pair(colors[1]))
        
        tabs = []
        for tab in self.tabs:
            tabs.append(f"[{tab.keys[0]}] {tab.name}")
        
        tab_size = self.app.screenX - 6 - len(self.title)
        if len("   ".join(tabs)) > tab_size:
            tabs = tabs[:tab_size-3] + "..."
        
        tabX = self.app.screenX - len("   ".join(tabs)) - 2
        for i, tab in enumerate(tabs):
            is_selected = (type(self.app.page).__name__ == self.tabs[i].page)
            sc.addstr(1 if self.large else 0, tabX, tab, curses.color_pair(colors[0 if is_selected else 1]))
            tabX += len(tab) + 3
        
    
    def on_input(self, key):
        for tab in self.tabs:
            if key in tab.keys or get_key(key) in tab.keys:
                self.on_click(tab)
                self.app.open(tab.page)
                break
    
    def on_click(self, tab):
        if self.callback:
            self.callback(self.tabs.index(tab), tab)