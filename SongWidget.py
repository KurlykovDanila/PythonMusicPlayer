from PyQt5 import uic
from PyQt5 import QtCore, QtMultimedia, QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import os
import sqlite3
from Player import PlayerWindow
from PlaylistWidget import PlaylistWidget


class PlaylistWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Переменная для определения текущего плейлиста
        self.playlist_from_author = False
        # Все файлы из папки с музыкой
        self.music = os.listdir("all_music/")

        self.player = QtMultimedia.QMediaPlayer()
        # Инициализация следующего окна
        self.Player_in_new_window = PlayerWindow()
        # Три словоря для получения информации по нажатой кнопке
        # Вид dict() ~ key = sender(), item = соответствует названию dict
        self.song_id = dict()
        self.author_id = dict()
        self.delete_song_id = dict()
        self.db_name = "Music.db"
        self.con = sqlite3.connect(self.db_name)
        self.cur = self.con.cursor()
        self.playlist_widget = QWidget()
        self.add_widget = PlaylistWidget()
        uic.loadUi('playlist_bar.ui', self)
        # Label над виджетом
        self.head.setStyleSheet('QLabel {color: #ffffff}')
        # Вызов функции, которая создаёт плейлист из всей музыки
        self.create_playlist_from_all_music()
        self.playlist_widget.setLayout(self.add_widget.playlist)
        self.playlist.setWidget(self.playlist_widget)
        # Настройка кнопки
        self.pbt_back.setIcon(QtGui.QIcon('src/back.png'))
        self.pbt_back.setIconSize(QSize(40, 40))
        self.pbt_back.clicked.connect(self.back)

    # Нахождение имени песни по её id
    def find_names_by_song_id(self, song_id):
        song_name = self.cur.execute(("""SELECT song_name FROM songs
                                    WHERE song_id = {0}""").format(song_id)).fetchall()[0][0]
        author_name = self.cur.execute(("""SELECT author_name FROM authors
                                    WHERE author_id = (SELECT author_id FROM songs
                                    WHERE song_id = {0})""").format(song_id)).fetchall()[0][0]
        return {"song_name": song_name, "author_name": author_name}

    # Добавление виджета песни в плейлист и заполнение dict'ов
    def information_about_widget(self, names, song_id):
        # Создание кнопки play
        pbt_play = QPushButton(self.add_widget)
        pbt_play.resize(50, 50)
        pbt_play.setIcon(QtGui.QIcon('src/play.png'))
        pbt_play.setIconSize(QSize(25, 25))
        sp_play = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sp_play.setHorizontalStretch(1)
        pbt_play.setSizePolicy(sp_play)
        pbt_play.clicked.connect(self.play_in_this_window)
        # Создание кнопки delete
        pbt_del = QPushButton("del", self.add_widget)
        pbt_del.setStyleSheet('QPushButton {color: #ffffff}')
        pbt_del.resize(50, 50)
        sp_del = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sp_del.setHorizontalStretch(1)
        pbt_del.setSizePolicy(sp_del)
        pbt_del.clicked.connect(self.delete_song)

        widget_information = self.add_widget.add_widget(names["song_name"][:22], names["author_name"][:22],
                                                        pbt_play,
                                                        self.play_in_new_window,
                                                        self.author_id_this_song,
                                                        pbt_del)
        self.song_id[widget_information["play"]] = song_id
        self.song_id[widget_information["song"]] = song_id
        self.author_id[widget_information["author"]] = self.cur.execute(("""SELECT author_id FROM authors
                                        WHERE author_name = '{0}'""").format(names["author_name"])).fetchall()[0][0]
        self.delete_song_id[widget_information["delete"]] = song_id

    # Проходим в цикле по всем песням и добавляем их в плейлист-виджет
    def create_playlist_from_all_music(self):
        for song in self.music:
            song_id = int(song[:-4])
            names = self.find_names_by_song_id(song_id)
            self.information_about_widget(names, song_id)
        self.playlist_from_author = False

    # Функция кнопки для проигрывания музыки в этом окне
    def play_in_this_window(self):
        self.player.stop()
        media = QtCore.QUrl.fromLocalFile("all_music/" + str(self.song_id[str(self.sender())]) + ".mp3")
        content = QtMultimedia.QMediaContent(media)

        self.player.setMedia(content)
        self.player.play()

    # Создание плейлиста из одного автора по sender()
    def author_id_this_song(self):
        self.create_playlist_from_songs_by_one_author(int(self.author_id[str(self.sender())]))

    # Проигрывание музыки в новом окне
    def play_in_new_window(self):
        self.player.stop()
        song_id = self.song_id[str(self.sender())]
        self.Player_in_new_window = PlayerWindow()
        self.Player_in_new_window.song_ind_now = self.music.index(str(song_id) + ".mp3")
        self.Player_in_new_window.show()

    # Очистить информацию о плейлисте
    def reset_playlist(self):
        self.author_id = dict()
        self.song_id = dict()
        for ind in range(self.add_widget.playlist.count()):
            self.add_widget.playlist.itemAt(ind).widget().close()

    # Процесс создания плейлиста по id автора
    def create_playlist_from_songs_by_one_author(self, author_id):
        self.reset_playlist()
        for song_id in self.cur.execute(("""SELECT song_id FROM songs
                                WHERE author_id = {0}""").format(author_id)).fetchall():
            song_id = song_id[0]
            names = self.find_names_by_song_id(song_id)
            self.information_about_widget(names, song_id)
        self.playlist_from_author = True

    # Обновить все виджеты в плейлистеб одно и то же, что пересоздать плейлист
    def update_playlist(self):
        self.music = os.listdir("all_music/")
        self.playlist_widget = QWidget()
        self.create_playlist_from_all_music()

    # Удаление песни и вызов окна подтверждения
    def delete_song(self):
        message = QMessageBox(self)
        message.setStyleSheet("QMessageBox {color: #ffffff}")
        reply = message.question(self, 'Delete song', 'Pres Yes to Delete.', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.Yes)
        if reply != QMessageBox.Yes:
            return
        song_id = self.delete_song_id[str(self.sender())]
        self.delete_song_from_db(song_id)
        os.remove("all_music/" + str(song_id) + ".mp3")
        self.reset_playlist()
        self.update_playlist()

    # Удаление всей информации о песне из БД
    def delete_song_from_db(self, song_id):
        if len(self.cur.execute(("""SELECT song_name FROM songs 
        WHERE song_id = '{0}'""").format(str(song_id))).fetchall()) == 1:
            author_id = self.cur.execute(("""SELECT author_id FROM songs 
                        WHERE song_id = '{0}'""").format(str(song_id))).fetchall()[0][0]
            year_id = self.cur.execute(("""SELECT year_id FROM songs 
                                    WHERE song_id = '{0}'""").format(str(song_id))).fetchall()[0][0]
            self.cur.execute(("""DELETE FROM songs WHERE song_id = '{0}'""").format(str(song_id)))
            if len(self.cur.execute(("""SELECT author_id FROM songs 
                    WHERE author_id = '{0}'""").format(str(author_id))).fetchall()) == 0:
                self.cur.execute(("""DELETE FROM authors WHERE author_id = '{0}'""").format(str(author_id)))
            if len(self.cur.execute(("""SELECT year_id FROM songs 
                                WHERE author_id = '{0}'""").format(str(year_id))).fetchall()) == 0:
                self.cur.execute(("""DELETE FROM years WHERE year_id = '{0}'""").format(str(year_id)))
            self.con.commit()

    # Возврат к предыдущему плейлисту или закрытие окна
    def back(self):
        if self.playlist_from_author is True:
            self.reset_playlist()
            self.create_playlist_from_all_music()
        else:
            self.closeEvent()

    # Корректное закрытие плеера и окна
    def closeEvent(self, event=None):
        if self.player.state() in [QtMultimedia.QMediaPlayer.PlayingState, QtMultimedia.QMediaPlayer.PausedState]:
            self.player.stop()
        self.close()
        self.destroy()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlaylistWindow()
    ex.show()
    sys.exit(app.exec())