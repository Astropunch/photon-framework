import curses

class Theme:
    def __init__(self, primary, success, warning, error):
        self.primary = primary
        
        self.success = success
        self.warning = warning
        self.error = error
        
        self.PRIMARY = 1
        self.PRIMARY_BG = 2
        
        self.SUCCESS = 3
        self.SUCCESS_BG = 4
        
        self.WARNING = 5
        self.WARNING_BG = 6
        
        self.ERROR = 7
        self.ERROR_BG = 8
        
    def apply(self):
        # Primary
        curses.init_pair(self.PRIMARY, self.primary, Colors.BLACK)
        curses.init_pair(self.PRIMARY_BG, Colors.BLACK, self.primary)
        
        # Success
        curses.init_pair(self.SUCCESS, self.success, Colors.BLACK)
        curses.init_pair(self.SUCCESS_BG, Colors.BLACK, self.success)
        
        # Warning
        curses.init_pair(self.WARNING, self.warning, Colors.BLACK)
        curses.init_pair(self.WARNING_BG, Colors.BLACK, self.warning)
        
        # Error
        curses.init_pair(self.ERROR, self.error, Colors.BLACK)        
        curses.init_pair(self.ERROR_BG, Colors.BLACK, self.error)
         


class Colors:
    WHITE = curses.COLOR_WHITE
    BLACK = curses.COLOR_BLACK
    RED = curses.COLOR_RED
    GREEN = curses.COLOR_GREEN
    YELLOW = curses.COLOR_YELLOW
    BLUE = curses.COLOR_BLUE
    MAGENTA = curses.COLOR_MAGENTA
    CYAN = curses.COLOR_CYAN
    
default_theme = Theme(
    primary = Colors.BLUE,
    success = Colors.GREEN,
    warning = Colors.YELLOW,
    error = Colors.RED
)