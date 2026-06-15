import sys
from PySide6.QtCore import Qt, QByteArray
from PySide6.QtWidgets import QApplication, QWidget, QMenu
from PySide6.QtSvgWidgets import QSvgWidget


# ---- The cat's artwork, baked right into the program as text ----
# Because it lives here, this single file IS the whole app.
CAT_SVG = """
<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="100" cy="150" rx="55" ry="40" fill="#F4A340"/>
  <path d="M150 150 q40 -10 35 -45 q-2 -2 -8 0 q-3 30 -32 38 z" fill="#F4A340"/>
  <circle cx="100" cy="90" r="50" fill="#F4A340"/>
  <polygon points="60,55 55,15 90,45" fill="#F4A340"/>
  <polygon points="140,55 145,15 110,45" fill="#F4A340"/>
  <polygon points="65,48 63,28 82,44" fill="#E07B5A"/>
  <polygon points="135,48 137,28 118,44" fill="#E07B5A"/>
  <circle cx="80" cy="90" r="8" fill="#2D2D2D"/>
  <circle cx="120" cy="90" r="8" fill="#2D2D2D"/>
  <circle cx="82" cy="87" r="3" fill="#FFFFFF"/>
  <circle cx="122" cy="87" r="3" fill="#FFFFFF"/>
  <polygon points="100,100 94,108 106,108" fill="#E07B5A"/>
  <path d="M100 108 q-8 10 -16 4" stroke="#2D2D2D" stroke-width="2" fill="none" stroke-linecap="round"/>
  <path d="M100 108 q8 10 16 4" stroke="#2D2D2D" stroke-width="2" fill="none" stroke-linecap="round"/>
  <line x1="60" y1="95" x2="30" y2="90" stroke="#2D2D2D" stroke-width="2" stroke-linecap="round"/>
  <line x1="60" y1="102" x2="32" y2="104" stroke="#2D2D2D" stroke-width="2" stroke-linecap="round"/>
  <line x1="140" y1="95" x2="170" y2="90" stroke="#2D2D2D" stroke-width="2" stroke-linecap="round"/>
  <line x1="140" y1="102" x2="168" y2="104" stroke="#2D2D2D" stroke-width="2" stroke-linecap="round"/>
</svg>
"""


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

        # Load the baked-in artwork into the window.
        self.cat = QSvgWidget(self)
        self.cat.load(QByteArray(CAT_SVG.encode("utf-8")))
        self.cat.setGeometry(0, 0, 200, 200)
        self.resize(200, 200)

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
