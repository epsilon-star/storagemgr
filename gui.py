import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QTreeView, QTableView, QSplitter, QVBoxLayout,
    QFileSystemModel, QHeaderView
)
from PySide6.QtCore import Qt, QDir


class SimpleFileManager(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple File Manager")
        self.setGeometry(100, 100, 900, 600)

        layout = QVBoxLayout(self)

        # Splitter to separate folder tree and file list
        splitter = QSplitter(Qt.Horizontal)

        # Left: Folder Tree
        self.dir_model = QFileSystemModel()
        self.dir_model.setRootPath(QDir.rootPath())
        self.dir_model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs)

        self.tree = QTreeView()
        self.tree.setModel(self.dir_model)
        self.tree.setRootIndex(self.dir_model.index(QDir.rootPath()))
        self.tree.setColumnWidth(0, 250)
        self.tree.hideColumn(1)  # Size
        self.tree.hideColumn(2)  # File Type
        self.tree.hideColumn(3)  # Date Modified
        self.tree.clicked.connect(self.on_tree_clicked)

        splitter.addWidget(self.tree)

        # Right: File List
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath())
        self.file_model.setFilter(QDir.NoDotAndDotDot | QDir.Files)

        self.table = QTableView()
        self.table.setModel(self.file_model)
        self.table.setRootIndex(self.file_model.index(QDir.rootPath()))
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        splitter.addWidget(self.table)

        layout.addWidget(splitter)
        self.setLayout(layout)

    def on_tree_clicked(self, index):
        """Update the file list when folder is clicked."""
        dir_path = self.dir_model.filePath(index)
        self.table.setRootIndex(self.file_model.setRootPath(dir_path))


def main():
    app = QApplication(sys.argv)
    window = SimpleFileManager()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
