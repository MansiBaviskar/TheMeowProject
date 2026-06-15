import sys
from PySide6.QtCore import Qt, QByteArray
from PySide6.QtWidgets import QApplication, QWidget, QMenu
from PySide6.QtSvgWidgets import QSvgWidget


# ============================================================
#   EASY SETTINGS  —  change this number, save, and re-run
# ============================================================
CAT_WIDTH = 220     # how wide the cat is, in pixels.
                    # Try 120 for tiny, 220 for medium, 360 for big.
# ============================================================


# ---- The cat's artwork, drawn as text (an SVG) right inside the program ----
# It's a vector drawing, so it stays sharp at ANY size, and its background
# is fully transparent — only the cat shape will show on your desktop.
CAT_SVG = """
<svg width="240" height="260" viewBox="0 0 240 260" xmlns="http://www.w3.org/2000/svg">
  <!-- Tail -->
  <path d="M150 210 C 200 215, 232 188, 220 148 C 215 132, 198 130, 195 146 C 202 176, 180 194, 148 188 Z" fill="#F2913B" stroke="#C75B2A" stroke-width="3"/>
  <path d="M203 165 q 9 -4 14 3" stroke="#D9622A" stroke-width="7" fill="none" stroke-linecap="round"/>
  <path d="M196 182 q 10 -2 15 4" stroke="#D9622A" stroke-width="7" fill="none" stroke-linecap="round"/>

  <!-- Body -->
  <path d="M60 250 C 50 180, 70 150, 110 150 C 150 150, 170 180, 160 250 Z" fill="#F2913B" stroke="#C75B2A" stroke-width="3"/>
  <!-- Chest cream -->
  <path d="M86 248 C 80 196, 96 176, 110 176 C 124 176, 140 196, 134 248 Z" fill="#FBE0B8"/>
  <!-- Front paws -->
  <ellipse cx="92" cy="246" rx="18" ry="11" fill="#FBE0B8" stroke="#C75B2A" stroke-width="2"/>
  <ellipse cx="128" cy="246" rx="18" ry="11" fill="#FBE0B8" stroke="#C75B2A" stroke-width="2"/>
  <!-- Body stripes -->
  <path d="M150 178 q 7 9 4 19" stroke="#D9622A" stroke-width="7" fill="none" stroke-linecap="round"/>
  <path d="M156 200 q 4 10 -1 20" stroke="#D9622A" stroke-width="7" fill="none" stroke-linecap="round"/>

  <!-- Ears -->
  <path d="M50 72 L 40 18 L 92 54 Z" fill="#F2913B" stroke="#C75B2A" stroke-width="3"/>
  <path d="M170 72 L 180 18 L 128 54 Z" fill="#F2913B" stroke="#C75B2A" stroke-width="3"/>
  <path d="M56 64 L 50 32 L 82 52 Z" fill="#E89A86"/>
  <path d="M164 64 L 170 32 L 138 52 Z" fill="#E89A86"/>

  <!-- Head -->
  <circle cx="110" cy="95" r="62" fill="#F2913B" stroke="#C75B2A" stroke-width="3"/>

  <!-- Forehead stripes -->
  <path d="M110 44 l 0 24" stroke="#D9622A" stroke-width="7" fill="none" stroke-linecap="round"/>
  <path d="M90 50 l -5 18" stroke="#D9622A" stroke-width="7" fill="none" stroke-linecap="round"/>
  <path d="M130 50 l 5 18" stroke="#D9622A" stroke-width="7" fill="none" stroke-linecap="round"/>

  <!-- Muzzle -->
  <ellipse cx="110" cy="122" rx="42" ry="26" fill="#FBE0B8"/>

  <!-- Eyes -->
  <circle cx="84" cy="92" r="21" fill="#FFFFFF"/>
  <circle cx="136" cy="92" r="21" fill="#FFFFFF"/>
  <circle cx="84" cy="92" r="17" fill="#8CC63F"/>
  <circle cx="136" cy="92" r="17" fill="#8CC63F"/>
  <circle cx="84" cy="94" r="9" fill="#222222"/>
  <circle cx="136" cy="94" r="9" fill="#222222"/>
  <circle cx="89" cy="87" r="4" fill="#FFFFFF"/>
  <circle cx="141" cy="87" r="4" fill="#FFFFFF"/>

  <!-- Nose -->
  <path d="M110 116 l -8 -7 l 16 0 Z" fill="#E86F8F" stroke="#C75B2A" stroke-width="1"/>
  <!-- Mouth -->
  <path d="M110 119 q -8 9 -15 3" stroke="#7A4A2A" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <path d="M110 119 q 8 9 15 3" stroke="#7A4A2A" stroke-width="2.5" fill="none" stroke-linecap="round"/>

  <!-- Whiskers -->
  <line x1="72" y1="116" x2="28" y2="110" stroke="#7A4A2A" stroke-width="2" stroke-linecap="round"/>
  <line x1="72" y1="124" x2="30" y2="130" stroke="#7A4A2A" stroke-width="2" stroke-linecap="round"/>
  <line x1="148" y1="116" x2="192" y2="110" stroke="#7A4A2A" stroke-width="2" stroke-linecap="round"/>
  <line x1="148" y1="124" x2="190" y2="130" stroke="#7A4A2A" stroke-width="2" stroke-linecap="round"/>
</svg>
"""

# The artwork is drawn on a 240 x 260 canvas. We keep that shape when we
# resize so the cat never looks squished or stretched.
SVG_W, SVG_H = 240, 260
CAT_HEIGHT = round(CAT_WIDTH * SVG_H / SVG_W)


class DeskCat(QWidget):
    def __init__(self):
        super().__init__()

        # Frameless + always-on-top + no taskbar button.
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )
        # See-through background, so only the cat shows.
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Load the baked-in artwork and size it from your CAT_WIDTH setting.
        self.cat = QSvgWidget(self)
        self.cat.load(QByteArray(CAT_SVG.encode("utf-8")))
        self.cat.setGeometry(0, 0, CAT_WIDTH, CAT_HEIGHT)
        self.resize(CAT_WIDTH, CAT_HEIGHT)

        self._drag_offset = None  # remembers your grab point while dragging

    # ---- Left-click and drag to move the cat ----
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

    # ---- Right-click the cat to quit (your only "close button"!) ----
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        quit_action = menu.addAction("Quit DeskCat")
        chosen = menu.exec(event.globalPos())
        if chosen == quit_action:
            QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    cat = DeskCat()
    cat.show()
    sys.exit(app.exec())
