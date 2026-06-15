import sys
import math
import time
import random

from PySide6.QtCore import Qt, QByteArray, QTimer
from PySide6.QtWidgets import QApplication, QWidget, QMenu
from PySide6.QtSvgWidgets import QSvgWidget


# ============================================================
#   EASY SETTINGS  —  your starting cat and size
# ============================================================
DEFAULT_CAT = "Orange Tabby"
DEFAULT_WIDTH = 150
# ============================================================


OUTLINE = "#333333"
SVG_W, SVG_H = 200, 210


def tabby_head(c):
    return f'''
  <path d="M100 50 l 0 16" stroke="{c}" stroke-width="6" fill="none" stroke-linecap="round"/>
  <path d="M82 54 l -4 14" stroke="{c}" stroke-width="6" fill="none" stroke-linecap="round"/>
  <path d="M118 54 l 4 14" stroke="{c}" stroke-width="6" fill="none" stroke-linecap="round"/>
'''


def tabby_tail(c):
    return f'''
  <path d="M174 116 q8 -2 12 4" stroke="{c}" stroke-width="6" fill="none" stroke-linecap="round"/>
  <path d="M170 134 q9 0 13 5" stroke="{c}" stroke-width="6" fill="none" stroke-linecap="round"/>
'''


TUX = '''
  <ellipse cx="100" cy="98" rx="13" ry="42" fill="#FFFFFF"/>
  <path d="M66 120 q34 24 68 0 q-8 22 -34 22 q-26 0 -34 -22 Z" fill="#FFFFFF" stroke="#333333" stroke-width="2"/>
'''

CALICO_HEAD = '''
  <path d="M104 48 q44 -2 46 44 q-28 6 -50 -12 q-6 -20 4 -32 Z" fill="#F2A24E"/>
  <path d="M52 64 q-6 -24 20 -34 q18 8 12 30 q-18 10 -32 4 Z" fill="#3C3C3C"/>
'''
CALICO_TAIL = '''
  <path d="M150 170 C 196 168, 200 112, 176 100 C 168 96, 160 105, 167 113 C 184 124, 178 158, 148 158 Z" fill="#F2A24E" stroke="#333333" stroke-width="3"/>
'''


CATS = {
    "Orange Tabby": dict(fur="#F2A24E", inner="#E89A86", belly="#FBE6C4", paws="#FBE6C4", eye="#2A2A2A", markings=tabby_head("#DC7A30"), tail_marks=tabby_tail("#DC7A30")),
    "Gray Tabby":   dict(fur="#B9C0C5", inner="#E89A86", belly="#E4E8EB", paws="#E4E8EB", eye="#2A2A2A", markings=tabby_head("#868E95"), tail_marks=tabby_tail("#868E95")),
    "White":        dict(fur="#FCFCFC", inner="#F2B4C2", belly="#FFFFFF", paws="#FFFFFF", eye="#2A2A2A", markings="", tail_marks=""),
    "Black":        dict(fur="#3C3C3C", inner="#6E4F4F", belly="#3C3C3C", paws="#3C3C3C", eye="#FFFFFF", markings="", tail_marks=""),
    "Gray":         dict(fur="#8E969C", inner="#E89A86", belly="#A7AEB3", paws="#A7AEB3", eye="#2A2A2A", markings="", tail_marks=""),
    "Cream":        dict(fur="#E9C9A1", inner="#EBB6A8", belly="#F6E6CE", paws="#F6E6CE", eye="#2A2A2A", markings="", tail_marks=""),
    "Tuxedo":       dict(fur="#3C3C3C", inner="#6E4F4F", belly="#FFFFFF", paws="#FFFFFF", eye="#FFFFFF", markings=TUX, tail_marks=""),
    "Calico":       dict(fur="#FCFCFC", inner="#F2B4C2", belly="#FFFFFF", paws="#FFFFFF", eye="#2A2A2A", markings=CALICO_HEAD, tail_marks=CALICO_TAIL),
}


def make_svg(fur, inner, belly, paws, eye, markings="", tail_marks="",
             breath=0.0, eye_open=1.0, tail_angle=0.0):

    sy = 1 + 0.018 * breath
    sx = 1 - 0.010 * breath
    breath_t = f"translate(100,192) scale({sx:.4f},{sy:.4f}) translate(-100,-192)"
    tail_t = f"rotate({tail_angle:.2f}, 150, 158)"

    eye_ry = max(0.8, 9.5 * eye_open)
    hi = ''
    if eye_open > 0.5:
        hi = ('<circle cx="80.5" cy="94" r="2.4" fill="#FFFFFF"/>'
              '<circle cx="124.5" cy="94" r="2.4" fill="#FFFFFF"/>')

    return f'''
<svg width="200" height="210" viewBox="0 0 200 210" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="100" cy="198" rx="58" ry="8" fill="#000000" opacity="0.08"/>
  <g transform="{breath_t}">

    <g transform="{tail_t}">
      <path d="M150 170 C 196 168, 200 112, 176 100 C 168 96, 160 105, 167 113 C 184 124, 178 158, 148 158 Z" fill="{fur}" stroke="{OUTLINE}" stroke-width="3"/>
      {tail_marks}
    </g>

    <path d="M50 92 C 50 50, 150 50, 150 92 C 168 120, 166 192, 100 192 C 34 192, 32 120, 50 92 Z" fill="{fur}" stroke="{OUTLINE}" stroke-width="3"/>
    <ellipse cx="100" cy="152" rx="32" ry="36" fill="{belly}"/>
    <ellipse cx="78" cy="189" rx="15" ry="9" fill="{paws}" stroke="{OUTLINE}" stroke-width="2.5"/>
    <ellipse cx="122" cy="189" rx="15" ry="9" fill="{paws}" stroke="{OUTLINE}" stroke-width="2.5"/>
    <path d="M60 60 L 50 20 L 96 52 Z" fill="{fur}" stroke="{OUTLINE}" stroke-width="3"/>
    <path d="M140 60 L 150 20 L 104 52 Z" fill="{fur}" stroke="{OUTLINE}" stroke-width="3"/>
    <path d="M64 56 L 58 33 L 88 50 Z" fill="{inner}"/>
    <path d="M136 56 L 142 33 L 112 50 Z" fill="{inner}"/>

    {markings}

    <ellipse cx="78" cy="98" rx="7" ry="{eye_ry:.2f}" fill="{eye}"/>
    <ellipse cx="122" cy="98" rx="7" ry="{eye_ry:.2f}" fill="{eye}"/>
    {hi}

    <ellipse cx="58" cy="116" rx="9" ry="5.5" fill="#F4A7BE" opacity="0.7"/>
    <ellipse cx="142" cy="116" rx="9" ry="5.5" fill="#F4A7BE" opacity="0.7"/>

    <path d="M100 110 l -4 -3.5 l 8 0 Z" fill="#C9667E"/>
    <path d="M100 113 q -6 6 -11 2 M100 113 q 6 6 11 2" stroke="{OUTLINE}" stroke-width="1.8" fill="none" stroke-linecap="round"/>
    <path d="M62 108 q -22 -2 -42 -6 M62 116 q -22 2 -40 7" stroke="{OUTLINE}" stroke-width="1.6" fill="none" stroke-linecap="round"/>
    <path d="M138 108 q 22 -2 42 -6 M138 116 q 22 2 40 7" stroke="{OUTLINE}" stroke-width="1.6" fill="none" stroke-linecap="round"/>
  </g>
</svg>
'''


class DeskCat(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.cat = QSvgWidget(self)
        self._drag_offset = None

        self.start_time = time.time()
        self.next_blink = 2.5
        self.blink_start = None
        self.blink_len = 0.16

        self.apply_cat(DEFAULT_CAT)
        self.apply_size(DEFAULT_WIDTH)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33)

    def render_cat(self, breath=0.0, eye_open=1.0, tail_angle=0.0):
        svg = make_svg(**CATS[self.current],
                       breath=breath, eye_open=eye_open, tail_angle=tail_angle)
        self.cat.load(QByteArray(svg.encode("utf-8")))

    def apply_cat(self, name):
        self.current = name
        self.render_cat()

    def apply_size(self, width):
        height = round(width * SVG_H / SVG_W)
        self.cat.setGeometry(0, 0, width, height)
        self.resize(width, height)

    def update_frame(self):
        t = time.time() - self.start_time

        breath = math.sin(t * 1.8)
        tail = 6 * math.sin(t * 1.3)

        if self.blink_start is None and t >= self.next_blink:
            self.blink_start = t

        if self.blink_start is not None:
            progress = (t - self.blink_start) / self.blink_len
            if progress >= 1:
                eye_open = 1.0
                self.blink_start = None
                self.next_blink = t + random.uniform(2.5, 5.5)
            else:
                eye_open = abs(math.cos(progress * math.pi))
        else:
            eye_open = 1.0

        self.render_cat(breath=breath, eye_open=eye_open, tail_angle=tail)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_offset = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )

    def mouseMoveEvent(self, event):
        if self._drag_offset is not None and event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_offset)

    def mouseReleaseEvent(self, event):
        self._drag_offset = None

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        choose = menu.addMenu("Choose cat")
        for name in CATS:
            act = choose.addAction(name)
            act.setData(("cat", name))

        size = menu.addMenu("Size")
        for label, w in [("Small", 110), ("Medium", 160), ("Large", 230)]:
            act = size.addAction(label)
            act.setData(("size", w))

        menu.addSeparator()
        quit_act = menu.addAction("Quit DeskCat")

        chosen = menu.exec(event.globalPos())
        if chosen is None:
            return
        if chosen == quit_act:
            QApplication.quit()
            return
        data = chosen.data()
        if data:
            kind, value = data
            if kind == "cat":
                self.apply_cat(value)
            elif kind == "size":
                self.apply_size(value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    cat = DeskCat()
    cat.show()
    sys.exit(app.exec())
