from PyQt5 import uic
from PyQt5.QtWidgets import *
from db import MusicToDB
from PlaylistWidget import PlaylistWidget
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import QSize


# Класс для окна скачивания музыки
class DownloadPlaylist(QMainWindow):
    def __init__(self, login, password):
        super().__init__()
        # Создаю словарь для сопоставления checkbox и id песни
        self.what_was_chosen = dict()
        self.add_widget = PlaylistWidget()
        # Список песен которые хотим скачать
        self.what_user_want_download = []
        self.account = {"login": str(login), "password": str(password)}
        self.yandex_music = MusicToDB(self.account["login"], self.account["password"])
        # Список всех песен в Аккаунте Яндекс Музыка
        self.list_of_music_in_yandex = self.yandex_music.return_list_of_music()

        self.playlist_widget = QWidget()
        self.create_playlist_form_all_yandex_music()

        uic.loadUi('playlist_bar.ui', self)

        self.playlist_widget.setLayout(self.add_widget.playlist)
        self.playlist.setWidget(self.playlist_widget)
        # Настройка кнопки download
        self.pbt_download = QPushButton("Download", self)
        self.pbt_download.resize(170, 80)
        self.pbt_download.move(150, 10)
        self.pbt_download.clicked.connect(self.download)
        self.pbt_download.setStyleSheet('QPushButton {color: #ffffff}')
        # Настройка кнопки back
        self.pbt_back.setIcon(QtGui.QIcon('src/back.png'))
        self.pbt_back.setIconSize(QSize(40, 40))
        self.pbt_back.clicked.connect(self.back)

    # Запуск скачивания выбраных песен
    def download(self):
        self.yandex_music.run(self.what_user_want_download)

    # Создаю список виджетов всех песен
    def create_playlist_form_all_yandex_music(self):
        for sing_info in self.list_of_music_in_yandex:
            cb = QCheckBox('', self)
            cb.stateChanged.connect(self.chose_song)
            self.what_was_chosen[str(cb)] = sing_info["index"]
            self.add_widget.add_widget(sing_info["title"], sing_info["author"], cb, self.nothing, self.nothing, None)

    # Функция кнопки back
    def back(self):
        self.closeEvent()

    # Закрываю окно
    def closeEvent(self, event=None):
        self.close()
        self.destroy()

    # Определяет выбрана ли песня
    def chose_song(self, state):
        index_music = self.what_was_chosen[str(self.sender())]
        if bool(state) is True:
            self.what_user_want_download.append(index_music)
        else:
            self.what_user_want_download.remove(index_music)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DownloadPlaylist("danilakurlykov", "danila2003")
    ex.show()
    sys.exit(app.exec())