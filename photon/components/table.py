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
    """
    Represents a table component that can be rendered on the screen.

    Args:
        app (Photon): The parent application object.
        x (int, optional): The x-coordinate of the table's top-left corner. If not set, the table will be centered on X axis.
        y (int, optional): The y-coordinate of the table's top-left corner. If not set, the table will be centered on Y axis.
        sizeY (int, optional): The number of rows to display in the table. Defaults to 10.
        headers (list[str], optional): The list of column headers for the table. Defaults to an empty list.
        rows (list[TableRow], optional): The list of table rows. Each row should be an instance of TableRow. Defaults to an empty list.
        selected (int, optional): The index of the currently selected row. Defaults to None.
        variant (Variants, optional): The variant style of the table. Defaults to Variants.DEFAULT.
        on_click (callable, optional): The callback function to be called when a row is clicked. Defaults to None.
        auto_render (bool, optional): Whether to automatically render the table. Defaults to True.
    """

    def __init__(self, app, x=None, y=None, sizeY=10, headers=[], rows: list[TableRow] = [], selected: int = None, variant: Variants = Variants.DEFAULT,
                 on_click: callable = None, auto_render=True):
        self.app = app
        self.x = x
        self.y = y
        self.sizeY = sizeY
        self.headers = headers
        self.rows = rows
        self.selected = selected
        self.variant = variant
        self.callback = on_click

        for row in self.rows:
            if type(row) != TableRow:
                raise ValueError("Rows must be an instance of TableRow")

        if not auto_render:
            return
        if not app.sc:
            raise Exception("App screen is not initialized.")

        self.on_render(app.sc)

    def on_render(self, sc):
        colors = theme.get_colors(self.variant)
        fg = colors[0]
        bg = colors[1]

        # calculate max sizes
        max_sizes = [len(x) for x in self.headers]
        for row in self.rows:
            for i, value in enumerate(row.values):
                size = len(str(value))
                if size > max_sizes[i]:
                    max_sizes[i] = size

        # row sizes & space between rows
        sizeX = sum(max_sizes) + (len(max_sizes) * 2) - 1
        sizeY = self.sizeY if self.sizeY else self.app.screenY - 4

        # WIP - add scroll, rendering only visible rows

        startX = self.x if self.x else utils.centerX(self.app, sizeX)
        startY = self.y if self.y else utils.centerY(self.app, sizeY)

        # draw headers
        headerX = startX
        for i, header in enumerate(self.headers):
            sc.addstr(startY, headerX, str(header).ljust(max_sizes[i]), curses.color_pair(bg))
            headerX += max_sizes[i] + 2

        # implement scroll
        page = self.selected if self.selected else 0 // sizeY
        visible_rows = self.rows[page * self.sizeY: (page + 1) * self.sizeY]

        # draw rows
        for i, row in enumerate(visible_rows):
            if i >= self.sizeY:
                break
            rowY = startY + i + 2
            rowX = startX
            for j, value in enumerate(row.values):
                sc.addstr(rowY, rowX, str(value).ljust(max_sizes[j]), curses.color_pair(bg if row is self.rows[self.selected] else fg))
                rowX += max_sizes[j] + 2

    def on_input(self, key):
        if get_key(key) in ["enter", " "]:
            if self.callback:
                self.callback(self.selected, self.rows[self.selected])

        if self.selected is not None:
            if get_key(key) == "down":
                self.selected += 1
                if self.selected >= len(self.rows):
                    self.selected = 0

            if get_key(key) == "up":
                self.selected -= 1
                if self.selected < 0:
                    self.selected = len(self.rows) - 1

            if get_key(key) in ["page_down", "right"]:
                self.selected += self.sizeY
                if self.selected >= len(self.rows):
                    self.selected = 0

            if get_key(key) in ["page_up", "left"]:
                self.selected -= self.sizeY
                if self.selected < 0:
                    self.selected = len(self.rows) - 1

            if get_key(key) == "home":
                self.selected = 0
            if get_key(key) == "end":
                self.selected = len(self.rows) - 1