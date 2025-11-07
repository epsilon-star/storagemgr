import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog, QToolBar, QMessageBox
)
from PySide6.QtGui import QFont, QIcon, QAction
from PySide6.QtCore import Qt, QSize

from tkinter import messagebox
from tkinter.filedialog import askopenfile


class TextEditor(QMainWindow):
    def __init__(self, filepath=None):
        super().__init__()
        self.setWindowTitle("Text Editor")
        self.resize(600, 500)

        textera = '''
        QTextEdit {
            color: #d1d1d1;
            background: #0e0f17;
        }
        '''

        # Central text area
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Consolas", 11))
        self.setCentralWidget(self.text_edit)
        self.setStyleSheet(textera)

        # Keep track of current file
        self.current_file = None
        if filepath:
            self.load_file(filepath)

        # Toolbar
        toolbar = QToolBar("Main Toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)
        toolbar.setMovable(False)

        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)

        save_as_action = QAction("Save As", self)
        save_as_action.triggered.connect(self.save_file_as)
        toolbar.addAction(save_as_action)

        close_action = QAction("Close", self)
        close_action.triggered.connect(self.close_action)
        toolbar.addAction(close_action)

    def open_file(self): 
        self.current_file = askopenfile("r").name # type: ignore
        with open(self.current_file,'r') as fs:
            self.text_edit.setText(fs.read())
            fs.close()

        self.setWindowTitle(f"Text Editor | {self.current_file}")

    def load_file(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                self.text_edit.setPlainText(f.read())
            self.current_file = filepath
            self.setWindowTitle(f"Text Editor - {filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open file:\n{e}")

    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, "w", encoding="utf-8") as f:
                    f.write(self.text_edit.toPlainText())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file:\n{e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save File As")
        if filepath:
            self.current_file = filepath
            self.save_file()
            self.setWindowTitle(f"Text Editor | {self.current_file}")

    def close_action(self):
        if self.current_file and len(self.text_edit.toPlainText()): 
            if messagebox.askyesno("Closing ?","Do you want to close the file without saving ?"):
                self.current_file = None
                self.text_edit.setText('')
                self.setWindowTitle("Text Editor")
            else: return False


def main():
    app = QApplication(sys.argv)
    editor = TextEditor()  # pass a file path like TextEditor("readme.md")
    editor.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
