from PyQt5 import uic
from PyQt5 import QtCore, QtMultimedia, QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QSlider
from mutagen.mp3 import MP3
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *
import sys
import os


# Класс воспроизведения песни в отдельном окне
class PlayerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # длительность песни
        self.duration_this_song = 0
        uic.loadUi('play_music.ui', self)
        # Список музыки в папке all_music
        self.Music = os.listdir("all_music/")
        # Номер песни с которой начинается воспроизведение
        self.song_ind_now = 0
        # Состояния пользователя -1 = Неактивен, 1 = музыка играла
        self.user_session = -1
        # Переменная для определения, нужно ли повторять этот трек или начинать играть следующий
        self.repeat_this_song = False
        # Настройка кнопки play
        self.pbt_play.setIcon(QtGui.QIcon('src/play.png'))
        self.pbt_play.setIconSize(QSize(70, 70))
        self.pbt_play.clicked.connect(self.play)
        self.pbt_play.setToolTip("Clicked here for start listening")
        self.pbt_play.resize(self.pbt_play.sizeHint())
        self.pbt_play.move(50, 50)

        self.pbt_next.setIcon(QtGui.QIcon('src/next.png'))
        self.pbt_next.setIconSize(QSize(50, 50))
        self.pbt_next.clicked.connect(self.next)

        self.pbt_last.setIcon(QtGui.QIcon('src/last.png'))
        self.pbt_last.setIconSize(QSize(50, 50))
        self.pbt_last.clicked.connect(self.last)
        # Настройка ползунка для перематывания
        self.duration.setMinimum(0)
        self.duration.setMaximum(100)
        self.duration.sliderReleased.connect(self.player_position)
        self.duration.setPageStep(0)
        self.duration.setSingleStep(0)

        self.pbt_back.setIcon(QtGui.QIcon('src/back.png'))
        self.pbt_back.setIconSize(QSize(40, 40))
        self.pbt_back.clicked.connect(self.back)

        self.pbt_repeat.clicked.connect(self.repeat)

    # Функция кнопки repeat
    def repeat(self):
        self.repeat_this_song = not self.repeat_this_song

    # Изменить состояние кнопки play, изменить иконку
    def change_btn_play_state(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.pbt_play.setIcon(QtGui.QIcon('src/pause.png'))
        elif self.player.state() == QMediaPlayer.PausedState:
            self.pbt_play.setIcon(QtGui.QIcon('src/play.png'))
        self.pbt_play.setIconSize(QSize(70, 70))

    # Переключить на предыдущую песню
    def last(self):
        if self.song_ind_now - 1 < 0:
            return
        self.song_ind_now -= 1
        if self.user_session != -1:
            self.player.stop()
        else:
            self.play()
        file_name = "all_music/" + self.Music[self.song_ind_now - 1]
        self.load_mp3(file_name)
        self.song_ind_now -= 1
        self.player.play()
        self.change_btn_play_state()
        self.duration_this_song = MP3(file_name).info.length
        self.duration.setMaximum(self.duration_this_song)

    # Переключить на следующую песню
    def next(self):
        if self.song_ind_now + 1 == len(self.Music):
            return
        self.song_ind_now += 1
        if self.user_session != -1:
            self.player.stop()
        else:
            self.play()
        file_name = "all_music/" + self.Music[self.song_ind_now + 1]
        self.load_mp3(file_name)

        self.player.play()
        self.change_btn_play_state()
        self.duration_this_song = MP3(file_name).info.length
        self.duration.setMaximum(self.duration_this_song)

    # Начать воспроизведение песни, либо поставить её на паузу
    def play(self):
        if self.user_session == -1:
            file_name = "all_music/" + self.Music[self.song_ind_now]
            self.load_mp3(file_name)
            self.duration_this_song = MP3(file_name).info.length
            self.duration.setMaximum(self.duration_this_song)
        self.user_session = 1
        if self.player.state() == QMediaPlayer.StoppedState:
            self.player.play()
        elif self.player.state() == QMediaPlayer.PausedState:
            self.player.play()
        elif self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        self.change_btn_play_state()

    # Загрузить .mp3 в MediaPlayer
    def load_mp3(self, filename):
        media = QtCore.QUrl.fromLocalFile(filename)
        content = QtMultimedia.QMediaContent(media)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)
        self.player.positionChanged.connect(self.change_slider)

    # Изменение положения слайдера в зависимости от текущего времени песни
    def change_slider(self, position, senderType=False):
        if senderType == False:
            self.duration.setValue(position // 1000)
        if self.user_session == 1 and self.duration_this_song - 1 < position // 1000:
            if self.repeat_this_song is True:
                self.player.stop()
                self.player.play()
            else:
                self.next()

    # При изменении слайдера изменяем время песни
    def player_position(self):
        sender = self.sender()
        if isinstance(sender, QSlider):
            if self.user_session != -1 and self.player.isSeekable():
                self.player.setPosition(self.duration.value() * 1000)

    def back(self):
        self.closeEvent()

    def closeEvent(self, event=None):
        if self.user_session != -1:
            self.player.stop()
        self.close()
        self.destroy()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlayerWindow()
    ex.show()
    sys.exit(app.exec())