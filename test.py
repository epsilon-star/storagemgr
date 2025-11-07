# a = '/a/d/s/f/f/a/c/c////'

# print(a[len(a)-1 - a[::-1].index('/')])

from PySide6.QtWidgets import QApplication, QMainWindow, QMenu
from PySide6.QtGui import QAction

app = QApplication([])

win = QMainWindow()
menu_bar = win.menuBar()

# Main menu
file_menu = menu_bar.addMenu("File")

# The action that will have a submenu
new_file_action = QAction("New File", win)

# Create the submenu
new_file_menu = QMenu("New File Options", win)
new_file_menu.addAction(QAction("From Template", win, triggered=lambda: print("From Template")))
new_file_menu.addAction(QAction("Blank File", win, triggered=lambda: print("Blank File")))

# Attach submenu to the action
new_file_action.setMenu(new_file_menu)

# Add the action to the File menu
file_menu.addAction(new_file_action)

win.show()
app.exec()