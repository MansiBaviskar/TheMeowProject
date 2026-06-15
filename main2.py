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


CAT_SVG = """
<svg width="240" height="270" viewBox="0 0 240 270" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="fur" x1="0" y1="0" x2="0" y2="270" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FBB163"/>
      <stop offset="1" stop-color="#E87A2B"/>
    </linearGradient>
    <linearGradient id="cream" x1="0" y1="150" x2="0" y2="260" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#FCEAC8"/>
      <stop offset="1" stop-color="#F4CF96"/>
    </linearGradient>
    <radialGradient id="eye" cx="0.5" cy="0.38" r="0.62">
      <stop offset="0" stop-color="#B6E36A"/>
      <stop offset="0.65" stop-color="#86C53F"/>
      <stop offset="1" stop-color="#5E9E2C"/>
    </radialGradient>
    <radialGradient id="ear" cx="0.5" cy="0.7" r="0.7">
      <stop offset="0" stop-color="#F2B6A2"/>
      <stop offset="1" stop-color="#DC8870"/>
    </radialGradient>
  </defs>

  <ellipse cx="108" cy="257" rx="70" ry="11" fill="#000000" opacity="0.10"/>

  <path d="M150 205 C 202 212, 234 184, 221 142 C 215 124, 196 124, 193 142 C 201 174, 180 192, 146 184 Z" fill="url(#fur)" stroke="#C25E27" stroke-width="3"/>
  <path d="M204 160 q 9 -4 14 4" stroke="#CF6326" stroke-width="8" fill="none" stroke-linecap="round" opacity="0.85"/>
  <path d="M197 180 q 10 -2 15 5" stroke="#CF6326" stroke-width="8" fill="none" stroke-linecap="round" opacity="0.85"/>

  <path d="M58 252 C 48 178, 70 148, 110 148 C 150 148, 172 178, 162 252 Z" fill="url(#fur)" stroke="#C25E27" stroke-width="3"/>
  <path d="M85 250 C 78 196, 96 174, 110 174 C 124 174, 142 196, 135 250 Z" fill="url(#cream)"/>
  <ellipse cx="91" cy="248" rx="19" ry="11" fill="url(#cream)" stroke="#C25E27" stroke-width="2"/>
  <ellipse cx="129" cy="248" rx="19" ry="11" fill="url(#cream)" stroke="#C25E27" stroke-width="2"/>
  <path d="M91 241 l 0 7 M85 242 l 0 6 M97 242 l 0 6" stroke="#C99A63" stroke-width="1.5" opacity="0.6"/>
  <path d="M129 241 l 0 7 M123 242 l 0 6 M135 242 l 0 6" stroke="#C99A63" stroke-width="1.5" opacity="0.6"/>
  <path d="M150 176 q 8 9 5 20" stroke="#CF6326" stroke-width="8" fill="none" stroke-linecap="round" opacity="0.85"/>
  <path d="M158 200 q 4 11 -1 21" stroke="#CF6326" stroke-width="8" fill="none" stroke-linecap="round" opacity="0.85"/>

  <path d="M50 70 L 38 14 L 92 52 Z" fill="url(#fur)" stroke="#C25E27" stroke-width="3"/>
  <path d="M170 70 L 182 14 L 128 52 Z" fill="url(#fur)" stroke="#C25E27" stroke-width="3"/>
  <path d="M56 62 L 48 28 L 82 50 Z" fill="url(#ear)"/>
  <path d="M164 62 L 172 28 L 138 50 Z" fill="url(#ear)"/>

  <circle cx="110" cy="94" r="63" fill="url(#fur)" stroke="#C25E27" stroke-width="3"/>
  <ellipse cx="95" cy="58" rx="34" ry="20" fill="#FFFFFF" opacity="0.15"/>

  <path d="M110 40 l 0 26" stroke="#CF6326" stroke-width="8" fill="none" stroke-linecap="round" opacity="0.85"/>
  <path d="M88 48 l -5 20" stroke="#CF6326" stroke-width="8" fill="none" stroke-linecap="round" opacity="0.85"/>
  <path d="M132 48 l 5 20" stroke="#CF6326" stroke-width="8" fill="none" stroke-linecap="round" opacity="0.85"/>

  <ellipse cx="110" cy="122" rx="44" ry="27" fill="url(#cream)"/>

  <circle cx="83" cy="93" r="22" fill="#FCFCF4"/>
  <circle cx="137" cy="93" r="22" fill="#FCFCF4"/>
  <circle cx="83" cy="93" r="18" fill="url(#eye)"/>
  <circle cx="137" cy="93" r="18" fill="url(#eye)"/>
  <circle cx="83" cy="95" r="9.5" fill="#222222"/>
  <circle cx="137" cy="95" r="9.5" fill="#222222"/>
  <circle cx="88" cy="88" r="4.5" fill="#FFFFFF"/>
  <circle cx="142" cy="88" r="4.5" fill="#FFFFFF"/>
  <circle cx="79" cy="99" r="2" fill="#FFFFFF" opacity="0.85"/>
  <circle cx="133" cy="99" r="2" fill="#FFFFFF" opacity="0.85"/>

  <path d="M110 117 l -8 -7 q8 -3 16 0 Z" fill="#E8718F" stroke="#C25E27" stroke-width="1"/>
  <circle cx="106" cy="111" r="1.6" fill="#FFFFFF" opacity="0.7"/>

  <path d="M110 119 q -8 9 -15 3" stroke="#7A4A2A" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <path d="M110 119 q 8 9 15 3" stroke="#7A4A2A" stroke-width="2.5" fill="none" stroke-linecap="round"/>

  <path d="M72 115 q -22 -3 -44 -7" stroke="#7A4A2A" stroke-width="2" fill="none" stroke-linecap="round"/>
  <path d="M72 123 q -22 3 -42 9" stroke="#7A4A2A" stroke-width="2" fill="none" stroke-linecap="round"/>
  <path d="M148 115 q 22 -3 44 -7" stroke="#7A4A2A" stroke-width="2" fill="none" stroke-linecap="round"/>
  <path d="M148 123 q 22 3 42 9" stroke="#7A4A2A" stroke-width="2" fill="none" stroke-linecap="round"/>
</svg>
"""

SVG_W, SVG_H = 240, 270
CAT_HEIGHT = round(CAT_WIDTH * SVG_H / SVG_W)


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
        self.cat.load(QByteArray(CAT_SVG.encode("utf-8")))
        self.cat.setGeometry(0, 0, CAT_WIDTH, CAT_HEIGHT)
        self.resize(CAT_WIDTH, CAT_HEIGHT)

        self._drag_offset = None

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
        quit_action = menu.addAction("Quit DeskCat")
        chosen = menu.exec(event.globalPos())
        if chosen == quit_action:
            QApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    cat = DeskCat()
    cat.show()
    sys.exit(app.exec())
