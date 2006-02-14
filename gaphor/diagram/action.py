'''
ActionItem diagram item
'''
# vim:sw=4:et

from __future__ import generators

import math
import gobject
import pango
import diacanvas
from gaphor import UML
from nameditem import NamedItem

def make_arc(radius, edges, q=1):
    """Create a tupple of edges points, which represent a 90 degrees
    arc in the first quadrant
    """
    points = []
    sin = math.sin
    cos = math.cos
    pi2 = (math.pi/2)
    for i in xrange(edges + 1):
        n = (pi2 * i) / edges + pi2*q
        points.append((cos(n) * radius, sin(n) * radius))
    return points

def alter_arc(arc, offsetx=0, offsety=0):
    return [(x+offsetx, y+offsety) for x, y in arc]

class ActionItem(NamedItem):
    RADIUS = 15
    MARGIN_X = 40
    MARGIN_Y = 20
    arc_1 = make_arc(radius=RADIUS, edges=10, q=0)
    arc_2 = make_arc(radius=RADIUS, edges=10, q=1)
    arc_3 = make_arc(radius=RADIUS, edges=10, q=2)
    arc_4 = make_arc(radius=RADIUS, edges=10, q=3)

    __uml__ = UML.Action

    def __init__(self, id=None):
        NamedItem.__init__(self, id)
        self.set(height=50, width=100)
        self._border = diacanvas.shape.Path()
        self._border.set_line_width(2.0)

    def on_update(self, affine):
        # Center the text
        w, h = self.get_name_size()
        self.set(min_width=w + ActionItem.MARGIN_X,
                 min_height=h + ActionItem.MARGIN_Y)
        self.update_name(x=0, y=(self.height - h) / 2,
                         width=self.width, height=h)

        NamedItem.on_update(self, affine)

        r = self.RADIUS
        h = self.height - r
        w = self.width - r
        line = alter_arc(self.arc_1, offsetx=w, offsety=h) + \
               alter_arc(self.arc_2, offsetx=r, offsety=h) + \
               alter_arc(self.arc_3, offsetx=r, offsety=r) + \
               alter_arc(self.arc_4, offsetx=w, offsety=r)
        self._border.line(line)
        self._border.set_cyclic(True)
        self.expand_bounds(1.0)

    def on_shape_iter(self):
        yield self._border
        for s in NamedItem.on_shape_iter(self):
            yield s

