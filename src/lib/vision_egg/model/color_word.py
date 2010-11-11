__copyright__ = """ Copyright (c) 2010 Torsten Schmits

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this
program; if not, see <http://www.gnu.org/licenses/>.

"""

from itertools import izip
from random import uniform
import logging

from text_list import TextList

class ColorWord(TextList):
    def __init__(self, position=(0, 0), text='', target=None, symbol_size=72,
                 target_size=96, colors=[]):
        TextList.__init__(self, position)
        self._target_index = None
        self.set_size(symbol_size, target_size)
        self.set(text=text, target=target, colors=colors)

    def set(self, text=None, target=None, colors=None):
        if text is not None:
            self.text = text
            self._target_index = None
        if colors is not None:
            self._colors = colors
        if target is not None:
            if isinstance(target, int) and 0 <= target <= len(self.text):
                self._target_index = target
            elif target in self.text:
                self._target_index = self.text.index(target)
            else:
                self._target_index = None
        self.clear()
        for i, l in enumerate(self.text):
            size = self._target_size if target in (i, l) else self._symbol_size
            self.add(l, size)
        self._set_colors()

    def set_size(self, symbol_size=72, target_size=96):
        self._symbol_size = symbol_size
        self._target_size = target_size

    def shuffle_colors(self):
        colors = ([uniform(0, 1) for i in xrange(3)] for e in self)
        self.set_colors(colors)

    def _set_colors(self):
        for color, symbol in izip(self._colors, self):
            symbol.set(color=color)
