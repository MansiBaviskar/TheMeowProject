# DeskCat 🐱

A cute cartoon cat that lives on your desktop — transparent, frameless, always on
top. Drag it anywhere with the mouse. Right-click it to quit.

This is **Step 1** of the project: a draggable, see-through cat. More life
(blinking, hunger, ball-play, etc.) comes next.

---

## What's in this folder

- `main.py` — the whole app. The cat artwork is baked inside, so this single file
  is everything.
- `requirements.txt` — the list of tools the project needs (just PySide6 for now).
- `README.md` — this file.

---

## A few words explained (for beginners)

- **PATH** — a list Windows checks to find programs. If Python isn't on it, typing
  `python` won't work. (The installer has a checkbox to add it — don't miss it!)
- **venv** (virtual environment) — a private toolbox just for this project, so it
  never interferes with the rest of your computer.
- **PyInstaller** — a tool that bundles everything into one double-clickable `.exe`.

---

## How to run it (Windows)

### One-time setup
1. Install Python from <https://python.org/downloads>. In the installer, **tick the
   box "Add python.exe to PATH"** at the bottom *before* clicking **Install Now**.
2. Put this folder somewhere easy, like your Desktop.
3. Open the folder, click the **address bar** in File Explorer, type `powershell`,
   and press **Enter**. A terminal opens already inside the folder.
4. Run these three lines, one at a time:
   ```
   python -m venv venv
   venv\Scripts\Activate
   pip install PySide6
   ```
   After activating, you should see `(venv)` at the start of the line.

   > If line 2 gives a "running scripts is disabled" error, run this once and retry:
   > `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

### Run the cat
```
python main.py
```
The cat appears! Drag it around. **Right-click → Quit** to close it.
(Running from the terminal like this shows any errors, so test this way first.)

---

## Make it a double-click app (a real .exe)

With your `(venv)` still active, in the same folder:
```
pip install pyinstaller
pyinstaller --onefile --windowed --name DeskCat main.py
```
When it finishes, open the new **`dist`** folder and find **`DeskCat.exe`**.
Double-click it — the cat runs with **no terminal and no Python needed**. You can
move that `.exe` anywhere, or right-click it → *Create shortcut* for your desktop.

---

## Emergency stop

If you ever lose the right-click menu, press **Ctrl + Shift + Esc** to open Task
Manager, find **DeskCat** (or **python**), and click **End task**.
