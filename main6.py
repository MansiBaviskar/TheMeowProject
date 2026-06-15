import sys
import math
import time
import random

from PySide6.QtCore import Qt, QByteArray, QTimer, QObject, Signal
from PySide6.QtWidgets import QApplication, QWidget, QMenu
from PySide6.QtSvgWidgets import QSvgWidget

try:
    from pynput import keyboard as pynput_keyboard, mouse as pynput_mouse
    HAVE_PYNPUT = True
except Exception:
    HAVE_PYNPUT = False


# ============================================================
#   EASY SETTINGS  —  your starting cat and size
# ============================================================
DEFAULT_CAT = "Orange Tabby"
DEFAULT_WIDTH = 155
# ============================================================


OUTLINE = "#3D3A3A"
SVG_W = 200


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
  <path d="M52 56 q-6 -26 22 -34 q16 8 10 30 q-18 10 -32 4 Z" fill="#34343C"/>
'''
CALICO_TAIL = '''
  <path d="M146 180 C 190 182, 202 128, 180 114 C 171 108, 160 119, 168 127 C 185 139, 177 172, 144 168 Z" fill="#F2A24A" stroke="#3D3A3A" stroke-width="3"/>
'''


CATS = {
    "Orange Tabby": dict(fur="#F2A24A", inner="#EFA593", belly="#FDEBCF", paws="#FDEBCF", eye="#23202A", markings=tabby_head("#E07E36"), tail_marks=tabby_tail("#E07E36")),
    "Gray Tabby":   dict(fur="#AEB7BE", inner="#EFA593", belly="#E8EDF0", paws="#E8EDF0", eye="#23202A", markings=tabby_head("#808A92"), tail_marks=tabby_tail("#808A92")),
    "White":        dict(fur="#FCFCFC", inner="#F3B6C3", belly="#FFFFFF", paws="#FFFFFF", eye="#23202A", markings="", tail_marks=""),
    "Black":        dict(fur="#34343C", inner="#7A5A5A", belly="#34343C", paws="#34343C", eye="#F2F2EA", pupil="#2B2B30", markings="", tail_marks=""),
    "Gray":         dict(fur="#9AA2A8", inner="#EFA593", belly="#C6CCD0", paws="#C6CCD0", eye="#23202A", markings="", tail_marks=""),
    "Cream":        dict(fur="#E8C79C", inner="#ECB6A6", belly="#F7E8D0", paws="#F7E8D0", eye="#23202A", markings="", tail_marks=""),
    "Tuxedo":       dict(fur="#34343C", inner="#7A5A5A", belly="#FFFFFF", paws="#FFFFFF", eye="#F2F2EA", pupil="#2B2B30", markings=TUX, tail_marks=""),
    "Calico":       dict(fur="#FCFCFC", inner="#F3B6C3", belly="#FFFFFF", paws="#FFFFFF", eye="#23202A", markings=CALICO_HEAD, tail_marks=CALICO_TAIL),
}


def build_keyboard(pressed):
    base = f'<rect x="42" y="230" width="116" height="62" rx="9" fill="#ECEAE6" stroke="{OUTLINE}" stroke-width="2.5"/>'
    keys = []
    idx = 0
    for r in range(3):
        for c in range(6):
            x = 50 + c * 17
            y = 238 + r * 13
            fill = "#FBC65A" if idx == pressed else "#FFFFFF"
            keys.append(f'<rect x="{x}" y="{y}" width="13" height="10" rx="2.2" fill="{fill}" stroke="#C7C4BE" stroke-width="1"/>')
            idx += 1
    keys.append('<rect x="68" y="278" width="64" height="9" rx="3" fill="#FFFFFF" stroke="#C7C4BE" stroke-width="1"/>')
    return base + "".join(keys)


def make_svg(fur, inner, belly, paws, eye, markings="", tail_marks="", pupil=None,
             breath=0.0, eye_open=1.0, tail_angle=0.0,
             leg_angle=0.0, head_dy=0.0, head_tilt=0.0, show_tongue=False,
             body_dy=0.0, leg_dy=0.0, keyboard=False, pressed_key=-1):

    total_h = 300 if keyboard else 220
    sy = 1 + 0.016 * breath
    sx = 1 - 0.009 * breath
    cat_t = f"translate(0,{body_dy:.2f}) translate(100,205) scale({sx:.4f},{sy:.4f}) translate(-100,-205)"
    tail_t = f"rotate({tail_angle:.2f}, 150, 150)"
    lleg_t = f"translate(0,{leg_dy:.2f})"
    rleg_t = f"rotate({leg_angle:.2f}, 116, 164) translate(0,{leg_dy:.2f})"
    head_t = f"translate(0,{head_dy:.2f}) rotate({head_tilt:.2f}, 100, 122)"

    eye_ry = max(0.8, 9.5 * eye_open)
    glossy = eye_open > 0.55

    pup = ''
    if pupil and glossy:
        pr = min(4.0, eye_ry * 0.45)
        pup = (f'<ellipse cx="80" cy="85" rx="3.6" ry="{pr:.2f}" fill="{pupil}"/>'
               f'<ellipse cx="120" cy="85" rx="3.6" ry="{pr:.2f}" fill="{pupil}"/>')

    shine = ''
    if glossy:
        shine = ('<circle cx="82.5" cy="80.5" r="2.5" fill="#FFFFFF"/>'
                 '<circle cx="122.5" cy="80.5" r="2.5" fill="#FFFFFF"/>'
                 '<circle cx="77.5" cy="88" r="1.3" fill="#FFFFFF" opacity="0.85"/>'
                 '<circle cx="117.5" cy="88" r="1.3" fill="#FFFFFF" opacity="0.85"/>')

    tongue = '<ellipse cx="100" cy="104" rx="5" ry="6" fill="#EE7E96"/>' if show_tongue else ''
    kbd = build_keyboard(pressed_key) if keyboard else ''

    return f'''
<svg width="200" height="{total_h}" viewBox="0 0 200 {total_h}" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="100" cy="208" rx="60" ry="8" fill="#000000" opacity="0.08"/>
  <g transform="{cat_t}">

    <g transform="{tail_t}">
      <path d="M146 180 C 190 182, 202 128, 180 114 C 171 108, 160 119, 168 127 C 185 139, 177 172, 144 168 Z" fill="{fur}" stroke="{OUTLINE}" stroke-width="3"/>
      {tail_marks}
    </g>

    <path d="M72 122 C 56 150, 42 180, 50 202 Q 100 214 150 202 C 158 180, 144 150, 128 122 Z" fill="{fur}" stroke="{OUTLINE}" stroke-width="3"/>
    <ellipse cx="100" cy="166" rx="30" ry="38" fill="{belly}"/>

    <g transform="{lleg_t}">
      <rect x="72" y="160" width="23" height="44" rx="11.5" fill="{fur}" stroke="{OUTLINE}" stroke-width="3"/>
      <ellipse cx="83.5" cy="200" rx="11" ry="6" fill="{paws}"/>
      <path d="M83.5 196 l 0 7 M78 197 l 0 6 M89 197 l 0 6" stroke="{OUTLINE}" stroke-width="1.3" opacity="0.45"/>
    </g>

    <g transform="{head_t}">
      <ellipse cx="100" cy="80" rx="52" ry="47" fill="{fur}" stroke="{OUTLINE}" stroke-width="3"/>
      <ellipse cx="86" cy="56" rx="30" ry="17" fill="#FFFFFF" opacity="0.12"/>
      <path d="M62 46 L 52 8 L 96 40 Z" fill="{fur}" stroke="{OUTLINE}" stroke-width="3"/>
      <path d="M138 46 L 148 8 L 104 40 Z" fill="{fur}" stroke="{OUTLINE}" stroke-width="3"/>
      <path d="M66 42 L 60 18 L 88 38 Z" fill="{inner}"/>
      <path d="M134 42 L 140 18 L 112 38 Z" fill="{inner}"/>

      {markings}

      <ellipse cx="80" cy="84" rx="7" ry="{eye_ry:.2f}" fill="{eye}"/>
      <ellipse cx="120" cy="84" rx="7" ry="{eye_ry:.2f}" fill="{eye}"/>
      {pup}
      {shine}

      <ellipse cx="60" cy="100" rx="9" ry="5.5" fill="#F4A7BE" opacity="0.7"/>
      <ellipse cx="140" cy="100" rx="9" ry="5.5" fill="#F4A7BE" opacity="0.7"/>

      <path d="M100 96 l -4 -3.5 l 8 0 Z" fill="#C9667E"/>
      <circle cx="98.4" cy="93.6" r="1" fill="#FFFFFF" opacity="0.65"/>
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
  {kbd}
</svg>
'''


class InputBridge(QObject):
    keyPressed = Signal()
    scrolled = Signal(int)


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
        self.width_px = DEFAULT_WIDTH

        self.start_time = time.time()
        self.next_blink = 2.5
        self.blink_start = None
        self.blink_len = 0.16
        self.lick_start = None
        self.next_lick = random.uniform(5, 9)
        self.lick_total = 2.4

        self.mimic = False
        self.type_until = -10.0
        self.pressed_key = -1
        self.scroll_v = 0.0
        self.k_listener = None
        self.m_listener = None
        self.bridge = InputBridge()
        self.bridge.keyPressed.connect(self.on_key)
        self.bridge.scrolled.connect(self.on_scroll)

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
        self.width_px = width
        canvas_h = 300 if self.mimic else 220
        height = round(width * canvas_h / 200)
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

        lick = 0.0
        if not self.mimic:
            if self.lick_start is None and t >= self.next_lick:
                self.lick_start = t
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
        leg_angle = 165 * lick + bob
        head_dy = 12 * lick
        head_tilt = 6 * lick
        show_tongue = lick > 0.55

        leg_dy = 0.0
        body_dy = 0.0
        pressed = -1
        if self.mimic:
            if t < self.type_until:
                leg_dy = 4.5
                head_dy += 2
                pressed = self.pressed_key
            body_dy = self.scroll_v
            self.scroll_v *= 0.82
            if abs(self.scroll_v) < 0.3:
                self.scroll_v = 0.0

        eye_open = min(blink_open, 1 - 0.8 * lick)

        self.render_cat(breath=breath, eye_open=eye_open, tail_angle=tail,
                        leg_angle=leg_angle, head_dy=head_dy, head_tilt=head_tilt,
                        show_tongue=show_tongue, body_dy=body_dy, leg_dy=leg_dy,
                        keyboard=self.mimic, pressed_key=pressed)

    def on_key(self):
        t = time.time() - self.start_time
        self.type_until = t + 0.16
        self.pressed_key = random.randint(0, 17)

    def on_scroll(self, dy):
        self.scroll_v += dy * 7
        self.scroll_v = max(-22.0, min(22.0, self.scroll_v))

    def start_listeners(self):
        if not HAVE_PYNPUT:
            print("Mimic Mode needs pynput. Install it with:  pip install pynput")
            return
        if self.k_listener is None:
            self.k_listener = pynput_keyboard.Listener(
                on_press=lambda key: self.bridge.keyPressed.emit())
            self.k_listener.start()
        if self.m_listener is None:
            self.m_listener = pynput_mouse.Listener(
                on_scroll=lambda x, y, dx, dy: self.bridge.scrolled.emit(int(dy)))
            self.m_listener.start()

    def stop_listeners(self):
        if self.k_listener is not None:
            self.k_listener.stop()
            self.k_listener = None
        if self.m_listener is not None:
            self.m_listener.stop()
            self.m_listener = None

    def mouseDoubleClickEvent(self, event):
        self.mimic = not self.mimic
        if self.mimic:
            self.start_listeners()
        else:
            self.stop_listeners()
            self.scroll_v = 0.0
        self.apply_size(self.width_px)

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
        mimic_act = menu.addAction("Turn Mimic Mode OFF" if self.mimic else "Turn Mimic Mode ON")
        quit_act = menu.addAction("Quit DeskCat")

        chosen = menu.exec(event.globalPos())
        if chosen is None:
            return
        if chosen == quit_act:
            self.stop_listeners()
            QApplication.quit()
            return
        if chosen == mimic_act:
            self.mouseDoubleClickEvent(None)
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
