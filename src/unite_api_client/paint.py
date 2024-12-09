import enum


class Colors(enum.Enum):
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    ORANGE = "\033[38;5;208m"
    LIGHT_RED = "\033[38;5;204m"
    LIGHT_GREEN = "\033[38;5;85m"
    LIGHT_YELLOW = "\033[38;5;229m"
    LIGHT_BLUE = "\033[38;5;33m"
    LIGHT_MAGENTA = "\033[38;5;225m"
    LIGHT_CYAN = "\033[38;5;117m"
    LIGHTER_GREEN = "\033[38;5;158m"
    LIGHTER_BLUE = "\033[38;5;159m"
    RESET = "\033[0m"


class Paint:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.colors = Colors

    def set_enabled(self, is_enabled=True):
        self.enabled = is_enabled

    def paint(self, text, color):
        if not self.enabled:
            return text
        return f"{color.value}{text}{self.colors.RESET.value}"

    def red(self, text):
        return self.paint(text, Colors.RED)

    def green(self, text):
        return self.paint(text, Colors.GREEN)

    def yellow(self, text):
        return self.paint(text, Colors.YELLOW)

    def blue(self, text):
        return self.paint(text, Colors.BLUE)

    def magenta(self, text):
        return self.paint(text, Colors.MAGENTA)

    def cyan(self, text):
        return self.paint(text, Colors.CYAN)

    def orange(self, text):
        return self.paint(text, Colors.ORANGE)

    def light_red(self, text):
        return self.paint(text, Colors.LIGHT_RED)

    def light_green(self, text):
        return self.paint(text, Colors.LIGHT_GREEN)

    def light_yellow(self, text):
        return self.paint(text, Colors.LIGHT_YELLOW)

    def light_blue(self, text):
        return self.paint(text, Colors.LIGHT_BLUE)

    def light_magenta(self, text):
        return self.paint(text, Colors.LIGHT_MAGENTA)

    def light_cyan(self, text):
        return self.paint(text, Colors.LIGHT_CYAN)

    def lighter_green(self, text):
        return self.paint(text, Colors.LIGHTER_GREEN)

    def lighter_blue(self, text):
        return self.paint(text, Colors.LIGHTER_BLUE)
