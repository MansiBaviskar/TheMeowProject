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
DEFAULT_WIDTH = 155
# ============================================================


OUTLINE = "#3D3A3A"
SVG_W, SVG_H = 200, 220


def tabby_head(c):
    return f'''
  <path d="M100 36 l 0 16" stroke="{c}" stroke-width="6" fill="none" stroke-linecap="round"/>
  <path d="M82 40 l -4 14" stroke="{c}" stroke-width="6" fill="none" stroke-linecap="round"/>
  <path d="M118 40 l 4 14" stroke="{c}" stroke-width="6" fill="none" stroke-linecap="round"/>
'''


def tabby_tail(c):
    return f'''
  <path d="M170 130 q9 -2 12 5" stroke="{c}" stroke-width="6" fill="none" stroke-linecap="round"/>
  <path d="M166 146 q10 0 13 5" stroke="{c}" stroke-width="6" fill="none" stroke-linecap="round"/>
'''


TUX = '''
  <ellipse cx="100" cy="84" rx="13" ry="40" fill="#FFFFFF"/>
  <path d="M66 104 q34 24 68 0 q-8 22 -34 22 q-26 0 -34 -22 Z" fill="#FFFFFF" stroke="#3D3A3A" stroke-width="2"/>
'''

CALICO_HEAD = '''
  <path d="M104 36 q44 0 44 42 q-26 8 -48 -8 q-6 -20 4 -34 Z" fill="#F2A24A"/>
  <path d="M52 56 q-6 -26 22 -34 q16 8 10 30 q-18 10 -32 4 Z" fill="#3A3A40"/>
'''
CALICO_TAIL = '''
  <path d="M146 180 C 190 182, 202 128, 180 114 C 171 108, 160 119, 168 127 C 185 139, 177 172, 144 168 Z" fill="#F2A24A" stroke="#3D3A3A" stroke-width="3"/>
'''


CATS = {
    "Orange Tabby": dict(fur="#F2A24A", inner="#EFA593", belly="#FDEBCF", paws="#FDEBCF", eye="#2A2A2A", markings=tabby_head("#E07E36"), tail_marks=tabby_tail("#E07E36")),
    "Gray Tabby":   dict(fur="#AEB7BE", inner="#EFA593", belly="#E8EDF0", paws="#E8EDF0", eye="#2A2A2A", markings=tabby_head("#808A92"), tail_marks=tabby_tail("#808A92")),
    "White":        dict(fur="#FCFCFC", inner="#F3B6C3", belly="#FFFFFF", paws="#FFFFFF", eye="#2A2A2A", markings="", tail_marks=""),
    "Black":        dict(fur="#3A3A40", inner="#6E5050", belly="#3A3A40", paws="#3A3A40", eye="#FFFFFF", markings="", tail_marks=""),
    "Gray":         dict(fur="#9AA2A8", inner="#EFA593", belly="#C6CCD0", paws="#C6CCD0", eye="#2A2A2A", markings="", tail_marks=""),
    "Cream":        dict(fur="#E8C79C", inner="#ECB6A6", belly="#F7E8D0", paws="#F7E8D0", eye="#2A2A2A", markings="", tail_marks=""),
    "Tuxedo":       dict(fur="#3A3A40", inner="#6E5050", belly="#FFFFFF", paws="#FFFFFF", eye="#FFFFFF", markings=TUX, tail_marks=""),
    "Calico":       dict(fur="#FCFCFC", inner="#F3B6C3", belly="#FFFFFF", paws="#FFFFFF", eye="#2A2A2A", markings=CALICO_HEAD, tail_marks=CALICO_TAIL),
}


def make_svg(fur, inner, belly, paws, eye, markings="", tail_marks="",
             breath=0.0, eye_open=1.0, tail_angle=0.0,
             leg_angle=0.0, head_dy=0.0, head_tilt=0.0, show_tongue=False):

    sy = 1 + 0.016 * breath
    sx = 1 - 0.009 * breath
    breath_t = f"translate(100,205) scale({sx:.4f},{sy:.4f}) translate(-100,-205)"
    tail_t = f"rotate({tail_angle:.2f}, 150, 150)"
    rleg_t = f"rotate({leg_angle:.2f}, 116, 164)"
    head_t = f"translate(0,{head_dy:.2f}) rotate({head_tilt:.2f}, 100, 122)"

    eye_ry = max(0.8, 9.5 * eye_open)
    hi = ''
    if eye_open > 0.55:
        hi = ('<circle cx="82.5" cy="80" r="2.4" fill="#FFFFFF"/>'
              '<circle cx="122.5" cy="80" r="2.4" fill="#FFFFFF"/>')

    tongue = '<ellipse cx="100" cy="104" rx="5" ry="6" fill="#EE7E96"/>' if show_tongue else ''

    return f'''
<svg width="200" height="220" viewBox="0 0 200 220" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="100" cy="208" rx="60" ry="8" fill="#000000" opacity="0.08"/>
  <g transform="{breath_t}">

    <g transform="{tail_t}">
      <path d="M146 180 C 190 182, 202 128, 180 114 C 171 108, 160 119, 168 127 C 185 139, 177 172, 144 168 Z" fill="{fur}" stroke="{OUTLINE}" stroke-width="3"/>
      {tail_marks}
    </g>

    <path d="M72 122 C 56 150, 42 180, 50 202 Q 100 214 150 202 C 158 180, 144 150, 128 122 Z" fill="{fur}" stroke="{OUTLINE}" stroke-width="3"/>
    <ellipse cx="100" cy="166" rx="30" ry="38" fill="{belly}"/>

    <rect x="72" y="160" width="23" height="44" rx="11.5" fill="{fur}" stroke="{OUTLINE}" stroke-width="3"/>
    <ellipse cx="83.5" cy="200" rx="11" ry="6" fill="{paws}"/>
    <path d="M83.5 196 l 0 7 M78 197 l 0 6 M89 197 l 0 6" stroke="{OUTLINE}" stroke-width="1.3" opacity="0.45"/>

    <g transform="{head_t}">
      <ellipse cx="100" cy="80" rx="52" ry="47" fill="{fur}" stroke="{OUTLINE}" stroke-width="3"/>
      <path d="M62 46 L 52 8 L 96 40 Z" fill="{fur}" stroke="{OUTLINE}" stroke-width="3"/>
      <path d="M138 46 L 148 8 L 104 40 Z" fill="{fur}" stroke="{OUTLINE}" stroke-width="3"/>
      <path d="M66 42 L 60 18 L 88 38 Z" fill="{inner}"/>
      <path d="M134 42 L 140 18 L 112 38 Z" fill="{inner}"/>

      {markings}

      <ellipse cx="80" cy="84" rx="7" ry="{eye_ry:.2f}" fill="{eye}"/>
      <ellipse cx="120" cy="84" rx="7" ry="{eye_ry:.2f}" fill="{eye}"/>
      {hi}

      <ellipse cx="60" cy="100" rx="9" ry="5.5" fill="#F4A7BE" opacity="0.7"/>
      <ellipse cx="140" cy="100" rx="9" ry="5.5" fill="#F4A7BE" opacity="0.7"/>

      <path d="M100 96 l -4 -3.5 l 8 0 Z" fill="#C9667E"/>
      <path d="M100 99 q -6 6 -11 2 M100 99 q 6 6 11 2" stroke="{OUTLINE}" stroke-width="1.8" fill="none" stroke-linecap="round"/>
      {tongue}
      <path d="M64 94 q -22 -2 -42 -6 M64 102 q -22 2 -40 7" stroke="{OUTLINE}" stroke-width="1.6" fill="none" stroke-linecap="round"/>
      <path d="M136 94 q 22 -2 42 -6 M136 102 q 22 2 40 7" stroke="{OUTLINE}" stroke-width="1.6" fill="none" stroke-linecap="round"/>
    </g>

    <g transform="{rleg_t}">
      <rect x="105" y="160" width="23" height="44" rx="11.5" fill="{fur}" stroke="{OUTLINE}" stroke-width="3"/>
      <ellipse cx="116.5" cy="200" rx="11" ry="6" fill="{paws}"/>
      <path d="M116.5 196 l 0 7 M111 197 l 0 6 M122 197 l 0 6" stroke="{OUTLINE}" stroke-width="1.3" opacity="0.45"/>
    </g>
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
        self.lick_start = None
        self.next_lick = random.uniform(5, 9)
        self.lick_total = 2.4

        self.apply_cat(DEFAULT_CAT)
        self.apply_size(DEFAULT_WIDTH)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33)

    def render_cat(self, **kw):
        svg = make_svg(**CATS[self.current], **kw)
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

        breath = math.sin(t * 1.7)
        tail = 6 * math.sin(t * 1.2)

        if self.blink_start is None and t >= self.next_blink:
            self.blink_start = t
        if self.blink_start is not None:
            p = (t - self.blink_start) / self.blink_len
            if p >= 1:
                blink_open = 1.0
                self.blink_start = None
                self.next_blink = t + random.uniform(2.5, 5.5)
            else:
                blink_open = abs(math.cos(p * math.pi))
        else:
            blink_open = 1.0

        if self.lick_start is None and t >= self.next_lick:
            self.lick_start = t
        lick = 0.0
        if self.lick_start is not None:
            e = t - self.lick_start
            if e >= self.lick_total:
                self.lick_start = None
                self.next_lick = t + random.uniform(9, 16)
            elif e < 0.45:
                lick = e / 0.45
            elif e > self.lick_total - 0.45:
                lick = (self.lick_total - e) / 0.45
            else:
                lick = 1.0

        bob = 7 * math.sin(t * 16) if lick > 0.9 else 0.0

        eye_open = min(blink_open, 1 - 0.8 * lick)
        leg_angle = 165 * lick + bob
        head_dy = 12 * lick
        head_tilt = 6 * lick

        self.render_cat(breath=breath, eye_open=eye_open, tail_angle=tail,
                        leg_angle=leg_angle, head_dy=head_dy, head_tilt=head_tilt,
                        show_tongue=lick > 0.55)

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
        for label, w in [("Small", 115), ("Medium", 165), ("Large", 235)]:
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
