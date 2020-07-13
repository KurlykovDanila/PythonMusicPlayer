from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from SongWidget import PlaylistWindow
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ImportMusic import ImportMusic
from MusicFromFolder import FolderView
import os


# Класс меню
class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('player_menu.ui', self)
        self.create_folder_for_music("/all_music")
        # Настраиваем все кнопки
        # Сначала задаём каждой кнопке иконку, а потом изменяем её размер
        self.pbt_my_music.setIcon(QtGui.QIcon('src/playlist.png'))
        self.pbt_my_music.setIconSize(QSize(200, 400))
        self.pbt_my_music.clicked.connect(self.go_to_playlist)

        self.pbt_import.setIcon(QtGui.QIcon('src/import_music.png'))
        self.pbt_import.setIconSize(QSize(200, 400))
        self.pbt_import.clicked.connect(self.go_to_import_music_from_yandex_music)

        self.pbt_add_music.setIcon(QtGui.QIcon('src/add_music.png'))
        self.pbt_add_music.setIconSize(QSize(200, 400))
        self.pbt_add_music.clicked.connect(self.add_files)

        self.pbt_setting.setIcon(QtGui.QIcon('src/settings.png'))
        self.pbt_setting.setIconSize(QSize(50, 50))
        self.pbt_setting.clicked.connect(self.go_to_settings)

    # Создаю папку для музыки
    def create_folder_for_music(self, dir_name):
        try:
            os.mkdir(dir_name)
        except FileExistsError:
            return

    # Открывает новые формы в зависимости от нажатой кнопки
    def go_to_playlist(self):
        self.second_form = PlaylistWindow()
        self.second_form.show()

    def go_to_import_music_from_yandex_music(self):
        self.second_form = ImportMusic()
        self.second_form.show()

    def add_files(self):
        FolderView(self).addFiles()

    def go_to_settings(self):
        pass

    # При закрытии окна вынуждаем приложение закрыться
    def closeEvent(self, event):
        qApp.quit()


app = QApplication(sys.argv)
ex = MenuWindow()
ex.show()
sys.exit(app.exec_())