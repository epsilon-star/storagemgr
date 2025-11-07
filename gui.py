import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QTreeWidget, QTreeWidgetItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QSplitter, QLabel, QMenu, QDialog
)
from PySide6.QtCore import Qt

from storage import Storage

# ---------------------------
# Simulated functions (replace with your engine's methods)
# ---------------------------
# s = Storage('storage-h3Sfj_.sxa')
s = Storage('storage-tvkwsl.sxa')
# s.newStorage()
s.loadStorage()
# def getPath():
#     return "/"

# def changePath(path):
#     print(f"changePath called with: {path}")

# def correctPath(folder):
#     return f"/{folder}"

# def dirList():
#     # Example data
#     return [
#         ['Musics1', 'f'],
#         ['JoneyMusic.mp3', 2554794],
#         ['Text1.txt', 11],
#         ['readme.md', 1940]
#     ]

# def folderList(path=None):
#     return [['/', 'Musics1']]

def human_size(size):
    """Convert bytes to a human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"


# ---------------------------
# Quick Dialogs
class QuickDialog(QDialog):
    def __init__(self,parent=None,title="",style_code=0):
        super().__init__(parent=parent)


# ---------------------------

# ---------------------------
# File Manager Class
# ---------------------------
class CustomFileManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom File Manager")
        self.setGeometry(100, 100, 900, 600)

        # Layout
        main_layout = QVBoxLayout(self)

        # context menu
        self.context = {}
        self.subcontext = {}

        self.context = QMenu(self)

        self.contexti = {}
        self.contexti['addf'] = self.context.addAction('Add File')
        self.contexti['newf'] = self.context.addAction('New File')
        self.contexti['newfo'] = self.context.addAction('New Folder')
        self.contexti['copy'] = self.context.addAction('Copy')
        self.contexti['move'] = self.context.addAction('Move')
        self.contexti['del'] = self.context.addAction('Delete')
        self.contexti['ren'] = self.context.addAction('Rename')

        self.subcontext['newf'] = {}
        self.subcontext['newf']['object'] = QMenu(self)
        self.subcontext['newf']['items'] = {}
        self.subcontext['newf']['items']['type.txt'] = self.subcontext['newf']['object'].addAction('New Text Document (txt)')
        self.subcontext['newf']['items']['type.txt'].triggered.connect(lambda am='txt': self.newFile('',am))
        self.contexti['newf'].setMenu(self.subcontext['newf']['object'])
        
        self.contexti['newfo'].triggered.connect(self.newFolder)

        # Path bar + Back Button
        path_layout = QHBoxLayout()
        self.back_button = QPushButton("← Back")
        self.back_button.clicked.connect(self.go_back)

        self.path_line = QLineEdit()
        self.path_line.setText(s.getPath())
        self.path_line.returnPressed.connect(self.manual_path_change)

        path_layout.addWidget(self.back_button)
        path_layout.addWidget(QLabel("Path:"))
        path_layout.addWidget(self.path_line)
        main_layout.addLayout(path_layout)

        # Splitter for Tree and Table
        splitter = QSplitter(Qt.Horizontal)

        # Folder Tree
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Folders"])
        self.tree.itemClicked.connect(self.on_tree_item_click)
        splitter.addWidget(self.tree)

        # File Table
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Name", "Size"])
        self.table.cellDoubleClicked.connect(self.on_table_double_click)
        splitter.addWidget(self.table)

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        # Initial load
        self.refresh_tree()
        self.refresh_table()

    # ---------------------------
    # Navigation & UI Updates
    # ---------------------------

    def newFolder(self,event): pass
        
    def newFile(self,path,type): 
        bm = QuickDialog(self)
        bm.show()

    def contextMenuEvent(self,event):
        self.context.exec(event.globalPos())

    def refresh_tree(self):
        """Populate the folder tree from current path."""
        self.tree.clear()
        folders = s.folderList(s.getPath())
        root_item = QTreeWidgetItem([s.getPath()])
        self.tree.addTopLevelItem(root_item)

        for _, folder_name in folders:
            QTreeWidgetItem(root_item, [folder_name])

        self.tree.expandAll()

    def refresh_table(self):
        """Populate file table with files and folders."""
        data = s.dirList()
        self.table.setRowCount(len(data))

        for row, entry in enumerate(data):
            name_item = QTableWidgetItem(entry[0])
            # name_item.setFlags(Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 0, name_item)

            if entry[1] == 'f':  # Folder
                size_item = QTableWidgetItem("<DIR>")
            else:
                size_item = QTableWidgetItem(human_size(entry[1]))
            self.table.setItem(row, 1, size_item)

        self.path_line.setText(s.getPath())
        self.table.resizeColumnsToContents()

    def go_back(self):
        """Go up one directory."""
        s.changePath("..")
        self.refresh_tree()
        self.refresh_table()

    def manual_path_change(self):
        """Change path from QLineEdit."""
        path = self.path_line.text().strip()
        s.changePath(path)
        self.refresh_tree()
        self.refresh_table()

    # ---------------------------
    # Tree & Table Actions
    # ---------------------------
    def on_tree_item_click(self, item):
        folder_name = item.text(0)
        if folder_name != s.getPath():
            s.changePath(folder_name)
            self.refresh_tree()
            self.refresh_table()

    def on_table_double_click(self, row, column):
        entry_name = self.table.item(row, 0).text()
        entry_size = self.table.item(row, 1).text()

        if entry_size == "<DIR>":
            s.changePath(entry_name)
            self.refresh_tree()
            self.refresh_table()
        else:
            # Placeholder for file open action
            print(f"Double-clicked file: {entry_name}")
            pass


# ---------------------------
# Main
# ---------------------------
def main():
    app = QApplication(sys.argv)
    fm = CustomFileManager()
    fm.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
