from ..page import Page
from ..core import theme
from ..theme import Variants
from ..keymap import get_key
from .. import utils

import curses

class SideBarRow:
    def __init__(self, name, selectable = True):
        self.name = name
        self.selectable = selectable

class SideBar(Page):
    """
    Represents a sidebar component that displays a list of items.

    Args:
        app (Photon): The parent application object.
        items (list[SideBarRow], optional): The list of sidebar row items. Defaults to an empty list.
        y (int, optional): The y-coordinate position of the sidebar. Defaults to 0 if not set.
        selected (int, optional): The index of the currently selected item. If not set, selecting is disabled.
        variant (Variants, optional): The variant style of the sidebar. Defaults to Variants.DEFAULT.
        on_click (callable, optional): The callback function to be called when an item is clicked. Defaults to None.
        auto_render (bool, optional): Whether to automatically render the sidebar. Defaults to True.
    """

    def __init__(self, app, items: list[SideBarRow] = [], y=None, selected: int = None, variant: Variants = Variants.DEFAULT, on_click: callable = None, auto_render=True):
        self.app = app
        self.items = items
        self.variant = variant
        self.selected = selected
        self.callback = on_click
        self.y = y if y else 0

        if not auto_render:
            return
        if not app.sc:
            raise Exception("App screen is not initialized.")

        self.on_render(app.sc)

    def on_render(self, sc):
        colors = theme.get_colors(self.variant)
        width = max([len(item.name) for item in self.items]) + 4
        sizeY = self.app.screenY - self.y

        for i in range(self.y, self.app.screenY):
            sc.addstr(i, 0, " " * width, curses.color_pair(colors[1]))

        selected = self.selected if self.selected else 0
        visible_rows = self.items[selected - sizeY:selected + sizeY]

        for i, row in enumerate(visible_rows):
            if i >= sizeY:
                break
            rowY = self.y + i
            index = self.items.index(row)
            if row.selectable:
                sc.addstr(rowY, 0, f"> {row.name.ljust(width-4)} <" if index == self.selected else f"  {row.name}  ", curses.color_pair(colors[1]))
            else:
                sc.addstr(rowY, 0, f"-[{row.name.ljust(width-4)}]-", curses.color_pair(colors[1]))

    def on_input(self, key):
        if get_key(key) in ["enter", " "]:
            self.callback(self.selected, self.items[self.selected])

        if get_key(key) == "up":
            for _ in range(len(self.items)):
                self.selected -= 1
                if self.selected < 0:
                    self.selected = len(self.items) - 1
                if self.items[self.selected].selectable:
                    break

        if get_key(key) == "down":
            for _ in range(len(self.items)):
                self.selected += 1
                if self.selected >= len(self.items):
                    self.selected = 0
                if self.items[self.selected].selectable:
                    break
        