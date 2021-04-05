"""
Button object for use in pygame projects.
Needs only to be contstructed to draw itself, supports operations to highlight,
do something when hovered over (called externally), and drawing centered text
onto itself.
"""

from pygame import Rect
import pygame.draw
import pygame.freetype

class Button:
    """
    Button class
    """
    def __init__(self, screen, top, left, width, height, color=(255, 0, 0),
                 text_color=(0, 0, 0), highlight_color=(0, 255, 0), value=0,
                 text="", font_size=24):
        self._text = text
        self._value = value
        self._shape = Rect(top, left, width, height)
        self._screen = screen
        self._highlight_color = highlight_color
        self._color = color
        if not text:
            text = str(value)
        font = pygame.freetype.SysFont("Arial", font_size)
        # make the label a class variable, we don't care about the rect for now
        self._label, self._label_rect = font.render(text, text_color)
        self.redraw()

    def collidepoint(self, point):
        return self._shape.collidepoint(point)

    def get_text(self):
        return self._text

    def get_value(self):
        return self._value

    def get_rect(self):
        return self._shape

    def highlight(self):
        pygame.draw.rect(self._screen, self._highlight_color, self._shape)
        self._screen.blit(self._label,
                          (self._shape.centerx - (self._label_rect.width / 2),
                           self._shape.centery - (self._label_rect.height / 2))
                         )

    def redraw(self):
        pygame.draw.rect(self._screen, self._color, self._shape)
        self._screen.blit(self._label,
                    (self._shape.centerx - (self._label_rect.width / 2),
                     self._shape.centery - (self._label_rect.height / 2))
                   )

    def on_hover(self):
        self.highlight()

    def on_dehover(self):
        self.redraw()
