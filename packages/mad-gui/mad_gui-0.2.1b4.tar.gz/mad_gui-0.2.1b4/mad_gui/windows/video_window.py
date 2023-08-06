import pandas as pd
from PySide2.QtCore import QObject, Qt, QUrl
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist

from mad_gui.qt_designer.ui_video import Ui_VideoWindow
from mad_gui.state_keeper import StateKeeper


class VideoWindow(Ui_VideoWindow, QObject):
    """Display a video that can be synchronised with sensor data.

    Interacts with :class:`mad_gui.plot_tools.SensorPlot`"""

    def __init__(self, parent=None):  # MainWindow
        super().__init__()
        self.parent = parent
        if parent:
            self.setWindowIcon(self.parent.windowIcon())
            self.setPalette(self.parent.palette())
        self.fps = None
        self.sync_info = None
        self.slider.sliderPressed.connect(self.slider_pressed)
        self.slider.sliderReleased.connect(self.slider_released)
        self.slider.sliderMoved.connect(self.slider_moved)
        self.slider.valueChanged.connect(self.slider_changed)
        self.player.positionChanged.connect(self.frame_changed)
        self.player.durationChanged.connect(self.set_slider_range)
        self.btn_play_pause.clicked.connect(self.toggle_play)
        self.setStyleSheet(parent.styleSheet())
        self.setWindowFlag(Qt.WindowStaysOnTopHint)

    def _init_position(self):
        """Move the window to the center of the parent window."""

        x = self.parent.pos().x() + self.parent.size().width() / 2 - self.size().width() / 2
        y = self.parent.pos().y() + self.parent.size().height() / 2 - self.size().height() / 2
        self.move(x, y)

    def toggle_play(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def start_video(self, video_file: str):
        self.playlist.clear()
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(video_file)))
        self.playlist.setCurrentIndex(0)
        self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
        self.player.setPlaylist(self.playlist)
        self.player.mediaStatusChanged.connect(self.set_rate)
        self.player.setVideoOutput(self.view_video)
        self.player.setNotifyInterval(10)
        self.player.setPlaybackRate(1.0)
        self.player.setVolume(0)
        # trigger mediaStatusChanged event, such that self.fps is set in self.set_rate
        self.player.play()
        self.player.pause()
        self._init_position()

    def set_rate(self):
        if self.fps:
            # the signal that calls this will occasionally be called during playing the video but we simply assume
            # that fps is constant
            return
        if "VideoFrameRate" not in self.player.availableMetaData():
            return
        self.fps = self.player.metaData("VideoFrameRate")

        StateKeeper.video_duration_available.emit(self.player.metaData("Duration") / 1000, self.fps)
        # Not sure yet why this is, but we need the following commands to make sure switching to sync mode directly
        # after loading the video works
        self.player.play()
        self.player.pause()

    def set_sync(self, start_frame: float, end_frame: float):
        self.sync_info = pd.Series(data=[start_frame, end_frame], index=[["start", "end"]])

    def key_press_event(self, **args):  # noqa (unused argument)
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        elif self.player.state() == QMediaPlayer.PausedState:
            self.player.play()

    def slider_pressed(self):
        self.player.pause()
        self.slider_is_pressed = True

    def slider_released(self):
        self.set_video_position()
        self.slider_is_pressed = False

    def slider_changed(self):
        if self.player.state() == QMediaPlayer.PausedState:
            self.set_video_position()
            self.frame_changed()

    def slider_moved(self):
        if self.player.state() == QMediaPlayer.PausedState:
            self.set_video_position()
            self.frame_changed()

    def set_slider_range(self, duration):
        self.slider.setRange(0, duration)

    def set_slider_position(self):
        if not self.slider_is_pressed:
            self.slider.setValue(self.player.position())

    def set_video_position(self):
        if self.player.state() == QMediaPlayer.PausedState:
            self.player.setPosition(self.slider.value())

    def frame_changed(self):
        if (
            self.player.mediaStatus() == QMediaPlayer.MediaStatus.LoadedMedia
            or self.player.metaData("Duration") is None
        ):
            return
        if not self.player.state() == QMediaPlayer.PausedState:
            self.set_slider_position()
        # if self.sync_info is not None and self.fps:
        #    stream_length = self.sync_info["end"][0] - self.sync_info["start"][0]
        #    start = self.sync_info["start"][0]
        # else:
        if self.sync_info is None:
            start = 0
            end = self.player.metaData("Duration")
        else:
            start = self.sync_info["start"] / self.fps * 1000
            end = self.sync_info["end"] / self.fps * 1000

        stream_length = end - start
        pos = self.slider.value()
        percent_since_start = (pos - start) / stream_length * 100
        try:
            StateKeeper.data_position_changed.emit(percent_since_start)
        except RuntimeError:
            # application already closed
            pass

    def closeEvent(self, event):  # noqa
        # comment "noqa" suppresses pep8 error N802: function name 'closeEvent' should be lowercase
        self.player.pause()
        StateKeeper.video_window_closed.emit()
