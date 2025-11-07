# profile_app.py
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QTextEdit, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QVBoxLayout, QGridLayout, QFrame, QSizePolicy, QSpacerItem
)
from PySide6.QtGui import QFont, QPixmap, QColor, QPainter, QPalette
from PySide6.QtCore import Qt, QSize


class ProfileApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Human Profile")
        self.setMinimumSize(800, 780)
        self.setup_fonts()
        self.setup_ui()
        self.apply_styles()
        self.populate_demo()

    def setup_fonts(self):
        # Fonts used in the layout
        self.header_font = QFont("Britannic", 28, QFont.Weight.Bold) 
        self.title_font = QFont("Courier New", 25, QFont.Weight.Bold) 
        self.info_font = QFont("Courier New", 11)
        self.body_font = QFont("Consolas", 10)
        self.small_font = QFont("Courier New", 10)

    def setup_ui(self):
        # Root layout
        root = QVBoxLayout(self)
        root.setContentsMargins(18, 18, 18, 18)
        root.setSpacing(14)

        # Top header text (centered)
        header_lbl = QLabel("E/D/C/B/A/S/SS/U PROFILE / Top-Class")
        header_lbl.setFont(self.header_font)
        header_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_lbl.setFixedHeight(54)
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.addWidget(header_lbl)
        # thin separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFixedHeight(2)
        sep.setObjectName("topSeparator")

        root.addWidget(header_frame)
        root.addWidget(sep)

        # Upper content (name, avatar and small info)
        upper = QHBoxLayout()
        upper.setSpacing(16)

        # Left side: Name + details
        left_col = QVBoxLayout()
        left_col.setSpacing(8)

        full_name_lbl = QLabel("FULL NAME")
        full_name_lbl.setFont(self.title_font)
        full_name_lbl.setObjectName("fullname")
        left_col.addWidget(full_name_lbl)

        # info block (age, gender, job, phone, address)
        info_block = QTextEdit()
        info_block.setReadOnly(True)
        info_block.setFixedHeight(110)
        info_block.setFont(self.info_font)
        info_block.setObjectName("infoblock")
        info_block.setFrameStyle(QFrame.Shape.NoFrame)
        left_col.addWidget(info_block)

        upper.addLayout(left_col)

        # Right side: avatar placeholder
        avatar_frame = QFrame()
        avatar_frame.setFixedSize(120, 160)
        avatar_layout = QVBoxLayout(avatar_frame)
        avatar_layout.setContentsMargins(8, 8, 8, 8)

        self.avatar_lbl = QLabel()
        self.avatar_lbl.setFixedSize(96, 128)
        self.avatar_lbl.setObjectName("avatar")
        self.avatar_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar_layout.addStretch()
        avatar_layout.addWidget(self.avatar_lbl, alignment=Qt.AlignmentFlag.AlignRight)
        avatar_layout.addStretch()
        upper.addWidget(avatar_frame)

        root.addLayout(upper)

        # Large description box (monospace)
        self.description = QTextEdit()
        self.description.setReadOnly(True)
        self.description.setFont(self.body_font)
        self.description.setObjectName("desc")
        self.description.setMinimumHeight(420)
        self.description.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        root.addWidget(self.description)

        # Bottom table area
        # self.table = QTableWidget(8, 6)  # 8 rows, 6 columns like screenshot
        # self.table.setObjectName("grid")
        # self.table.setFixedHeight(180)
        # self.table.verticalHeader().setVisible(False)
        # self.table.horizontalHeader().setVisible(False)
        # self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        # self.table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        # self.table.setShowGrid(True)
        # root.addWidget(self.table)

        # Keep references to widgets for populating
        self.info_block = info_block

    def apply_styles(self):
        # Basic dark theme and widget styles using QSS
        qss = """
        QWidget {
            background-color: #121212;
            color: #dcdcdc;
        }
        QLabel#fullname {
            letter-spacing: 2px;
        }
        QFrame#topSeparator {
            background-color: #2b2b2b;
            border: none;
        }
        QTextEdit#infoblock {
            background: transparent;
            border: none;
            color: #bfbfbf;
        }
        QTextEdit#desc {
            background-color: #1e1e1e;
            border: 1px solid #2f2f2f;
            padding: 12px;
            color: #e9e9e9;
        }
        QLabel#avatar {
            background-color: #2b2b2b;
            border-radius: 4px;
            color: #9e9e9e;
        }
        QTableWidget#grid {
            background-color: transparent;
            gridline-color: #3a3a3a;
        }
        QTableWidget#grid QTableCornerButton::section {
            background: #1b1b1b;
        }
        """
        self.setStyleSheet(qss)

    def populate_demo(self):
        # Avatar: draw simple person icon as placeholder
        pix = QPixmap(self.avatar_lbl.size())
        pix.fill(QColor("#2b2b2b"))
        painter = QPainter(pix)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#8f8f8f"))
        # head
        painter.drawEllipse(18, 6, 60, 60)
        # body
        painter.drawRoundedRect(18, 68, 60, 56, 8, 8)
        painter.end()
        self.avatar_lbl.setPixmap(pix)

        # Info block content
        info_text = (
            "Age: 00\n"
            "Gender: F/M/U\n"
            "Job: Uknown\n"
            "Phone: +98 000 000 0000\n"
            "Address: Uknown\n"
        )
        self.info_block.setPlainText(info_text)

        # Large lorem ipsum (monospace)
        lorem = (
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
            "tempor incididunt ut labore et dolore magna aliqua. Quis ipsum suspendisse "
            "ultrices gravida. Risus commodo viverra maecenas accumsan lacus vel facilisis.\n\n"
        )
        self.description.setPlainText(lorem * 10)
        self.description.setReadOnly(True)

        # # Fill table with empty-ish styled cells
        # for r in range(self.table.rowCount()):
        #     for c in range(self.table.columnCount()):
        #         item = QTableWidgetItem("")  # empty cell
        #         # subtle background to mimic screenshot
        #         item.setBackground(QColor("#252525"))
        #         item.setFlags(Qt.ItemFlag.ItemIsEnabled)
        #         self.table.setItem(r, c, item)

        # # Make columns stretch evenly
        # from PySide6.QtWidgets import QHeaderView
        # self.table.horizontalHeader().setSectionResizeMode(
        #     QHeaderView.ResizeMode.Stretch
        # )

    # Public API: allow setting data from your engine
    def set_profile(self, full_name: str, info_dict: dict, description_text: str):
        # full name
        fname_lbl = self.findChild(QLabel, "fullname")
        if fname_lbl:
            fname_lbl.setText(full_name.upper())

        # info block
        info_lines = []
        for k, v in info_dict.items():
            info_lines.append(f"{k}: {v}")
        self.info_block.setPlainText("\n".join(info_lines))

        # description
        self.description.setPlainText(description_text)

    def set_avatar_pixmap(self, pixmap: QPixmap):
        self.avatar_lbl.setPixmap(pixmap.scaled(
            self.avatar_lbl.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        ))


def main():
    app = QApplication(sys.argv)
    window = ProfileApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
