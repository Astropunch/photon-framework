from ..page import Page
from ..core import theme
from ..theme import Variants
from .. import utils

import curses

class Slider(Page):
    """
    Represents a slider component that can be rendered on the screen.

    Args:
        app (Photon): The parent application object.
        value (int): The initial value of the slider (default is 0).
        max (int): The maximum value of the slider (default is 100).
        width (int): The width of the slider in characters (default is 30).
        x (int): The x-coordinate of the top-left corner of the slider (centered by default).
        y (int): The y-coordinate of the top-left corner of the slider (centered by default).
        border (bool): Whether to display a border around the slider (default is True).
        char_pre (str): The character used to represent the filled portion of the slider (default is "#").
        char_post (str): The character used to represent the empty portion of the slider (default is " ").
        char_point (str): The character used to represent the slider's current value (default is "@").
        variant (Variants): The variant of the slider (default is Variants.DEFAULT).
        reverse (bool): Whether to reverse the color of the slider (default is False).
        auto_render (bool): Whether to automatically render the slider (default is True).

    Raises:
        Exception: If the app screen is not initialized.

    """

    def __init__(self, app, value=0, max=100, width: int = 30, x=None, y=None,
                 border=True, char_pre="#", char_post=" ", char_point="@", variant: Variants = Variants.DEFAULT, reverse=False,
                 auto_render=True):
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

        if not auto_render:
            return
        if not app.sc:
            raise Exception("App screen is not initialized.")
        self.on_render(app.sc)

    def on_render(self, sc):
        """
        Renders the slider on the screen.

        Args:
            sc (curses.window): The curses window object to render the slider on.

        """
        color = theme.get_colors(self.variant)[1 if self.reverse else 0]

        # with border
        # [-----•-----------------]
        # without border
        #  -----•-----------------

        if self.value > self.max:
            self.value = self.max

        percentage_full = int(self.value / self.max * self.width)
        percentage_empty = self.width - percentage_full

        if self.border:
            bar = f"[{self.char_pre * percentage_full}{self.char_point}{self.char_post * percentage_empty}]"
        else:
            bar = f"{self.char_pre * percentage_full}{self.char_point}{self.char_post * percentage_empty}"

        x = self.x if self.x else utils.centerX(self.app, len(bar))
        y = self.y if self.y else utils.centerY(self.app)

        sc.addstr(y, x, bar, curses.color_pair(color))

    def on_input(self, key):
        """
        Handles input events for the slider.

        Args:
            key (int): The key code of the input event.

        Returns:
            None

        """
        return