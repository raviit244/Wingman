from settings import *
from helper import _blit_text_horizontal

# Menu class
class Menu:
    def __init__(self, bg=None, buttons=[], heading=None, bg_color=None):
        self.bg = bg
        self.buttons = buttons
        self.bg_color = bg_color
        self.heading = heading
        self.active = False

    def draw(self):
        if not self.active:
            return
        if self.bg:
            win.blit(self.bg, (0, 0))

        if self.heading:
            _blit_text_horizontal(self.heading, 40)
        
        for button in self.buttons:
            button.draw()

    def click(self):
        for i, button in enumerate(self.buttons):
            if button.click():
                return i
        return None