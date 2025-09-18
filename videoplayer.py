# import sys
# import tempfile
# from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
# from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
# from PySide6.QtMultimediaWidgets import QVideoWidget
# from PySide6.QtCore import QUrl

from storage import Storage

# class VideoPlayer(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("In-Memory Video Player")

#         # Storage
#         self.storage = Storage('storage-phhdsd.sxa')
#         self.storage.loadStorage()

#         # Media setup
#         self.media_player = QMediaPlayer()
#         self.audio_output = QAudioOutput()
#         self.media_player.setAudioOutput(self.audio_output)

#         self.video_widget = QVideoWidget()
#         self.media_player.setVideoOutput(self.video_widget)

#         # Play button
#         self.play_btn = QPushButton("Play from Memory")
#         self.play_btn.clicked.connect(self.play_from_memory)

#         # Layout
#         layout = QVBoxLayout()
#         layout.addWidget(self.video_widget)
#         layout.addWidget(self.play_btn)
#         self.setLayout(layout)
#         self.resize(800, 600)

#         # Example: load binary data from a file
#         # with open("example_video.mp4", "rb") as f:
#         #     self.video_data = f.read()  # This is your "variable holding data"
#         self.video_data = self.storage.getFile('Angel Next Door',filename='Angel Next Door [sub] (7).mkv')

#     def play_from_memory(self):
#         # Write the binary data to a temporary file
#         temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mkv")
#         temp.write(self.video_data)
#         temp.flush()
#         temp.close()

#         # Play the temporary file
#         self.media_player.setSource(QUrl.fromLocalFile(temp.name))
#         self.media_player.play()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     player = VideoPlayer()
#     player.show()
#     sys.exit(app.exec())

import sys
import vlc
import tempfile
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QFileDialog, QSlider, QLabel, QComboBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPalette, QColor


class VLCVideoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VLC-PySide6 Video Player")
        self.setMinimumSize(800, 600)

        # VLC setup
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()

        # Storage
        self.storage = Storage('storage-phhdsd.sxa')
        self.storage.loadStorage()
        self.video_data = self.storage.getFile('Angel Next Door',filename='Angel Next Door [sub] (7).mkv')

        # Widgets
        self.video_frame = QWidget(self)
        self.video_frame.setAutoFillBackground(True)
        palette = self.video_frame.palette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        self.video_frame.setPalette(palette)

        self.play_btn = QPushButton("Play")
        self.pause_btn = QPushButton("Pause")
        self.stop_btn = QPushButton("Stop")
        self.open_btn = QPushButton("Open File")

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 1000)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)

        self.status_label = QLabel("Status: Ready")

        self.audio_track_box = QComboBox()
        self.subtitle_track_box = QComboBox()
        self.video_track_box = QComboBox()

        self.audio_track_box.currentIndexChanged.connect(self.set_audio_track)
        self.subtitle_track_box.currentIndexChanged.connect(self.set_subtitle_track)
        self.video_track_box.currentIndexChanged.connect(self.set_video_track)

        # Layout
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.open_btn)
        control_layout.addWidget(self.play_btn)
        control_layout.addWidget(self.pause_btn)
        control_layout.addWidget(self.stop_btn)

        track_layout = QHBoxLayout()
        track_layout.addWidget(QLabel("Audio Track"))
        track_layout.addWidget(self.audio_track_box)
        track_layout.addWidget(QLabel("Subtitle Track"))
        track_layout.addWidget(self.subtitle_track_box)
        track_layout.addWidget(QLabel("Video Track"))
        track_layout.addWidget(self.video_track_box)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.video_frame)
        main_layout.addWidget(self.slider)
        main_layout.addLayout(control_layout)
        main_layout.addWidget(QLabel("Volume"))
        main_layout.addWidget(self.volume_slider)
        main_layout.addLayout(track_layout)
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

        # Connections
        self.open_btn.clicked.connect(self.open_file)
        self.play_btn.clicked.connect(self.media_player.play)
        self.pause_btn.clicked.connect(self.media_player.pause)
        self.stop_btn.clicked.connect(self.media_player.stop)
        self.slider.sliderMoved.connect(self.set_position)
        self.volume_slider.valueChanged.connect(self.set_volume)

        # Timer for UI updates
        self.timer = QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.update_ui)
        self.timer.start()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Video")
        if file_path:
            self.load_media(file_path)

    def load_media(self, file_path: str):
        media = self.instance.media_new_path(file_path)
        self.media_player.set_media(media)

        # Set video output
        if sys.platform.startswith('linux'):
            self.media_player.set_xwindow(self.video_frame.winId())
        elif sys.platform == "win32":
            self.media_player.set_hwnd(self.video_frame.winId())
        elif sys.platform == "darwin":
            self.media_player.set_nsobject(int(self.video_frame.winId()))

        self.media_player.play()
        QTimer.singleShot(1000, self.update_tracks)  # wait for tracks to be parsed

    def set_position(self, value):
        self.media_player.set_position(value / 1000.0)

    def update_ui(self):
        if self.media_player.is_playing():
            self.slider.blockSignals(True)
            self.slider.setValue(int(self.media_player.get_position() * 1000))
            self.slider.blockSignals(False)
        self.status_label.setText(f"Status: {self.media_player.get_state()}")

    def set_volume(self, value):
        self.media_player.audio_set_volume(value)

    def update_tracks(self):
        self.audio_track_box.clear()
        self.subtitle_track_box.clear()
        self.video_track_box.clear()

        # Audio tracks
        audio_tracks = self.media_player.audio_get_track_description()
        if audio_tracks:
            for track in audio_tracks:
                self.audio_track_box.addItem(track[1], track[0])
            self.audio_track_box.setCurrentIndex(
                self.audio_track_box.findData(self.media_player.audio_get_track())
            )

        # Subtitle tracks
        subtitle_tracks = self.media_player.video_get_spu_description()
        if subtitle_tracks:
            for track in subtitle_tracks:
                self.subtitle_track_box.addItem(track[1], track[0])
            self.subtitle_track_box.setCurrentIndex(
                self.subtitle_track_box.findData(self.media_player.video_get_spu())
            )

        # Video tracks (usually only one, but included for completeness)
        video_tracks = self.media_player.video_get_track_description()
        if video_tracks:
            for track in video_tracks:
                self.video_track_box.addItem(track[1], track[0])
            self.video_track_box.setCurrentIndex(
                self.video_track_box.findData(self.media_player.video_get_track())
            )

    def set_audio_track(self, index):
        track_id = self.audio_track_box.itemData(index)
        if track_id is not None:
            self.media_player.audio_set_track(track_id)

    def set_subtitle_track(self, index):
        track_id = self.subtitle_track_box.itemData(index)
        if track_id is not None:
            self.media_player.video_set_spu(track_id)

    def set_video_track(self, index):
        track_id = self.video_track_box.itemData(index)
        if track_id is not None:
            self.media_player.video_set_track(track_id)

    def play_from_memory(self, data: bytes):
        """Write to temp file and play from it."""
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mkv")
        temp.write(data)
        temp.flush()
        temp.close()
        self.load_media(temp.name)

        # temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mkv")
        # temp.write(self.video_data)
        # temp.flush()
        # temp.close()

        # # Play the temporary file
        # self.media_player.setSource(QUrl.fromLocalFile(temp.name))
        # self.media_player.play()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VLCVideoPlayer()
    player.show()
    sys.exit(app.exec())
