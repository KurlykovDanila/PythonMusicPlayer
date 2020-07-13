from os.path import expanduser
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
from db import MusicToDB
import os


# Класс для добавления музыки из папки
class FolderView:
    def __init__(self, window):
        self.window = window
        self.music_db = MusicToDB("login", "password")
        self.path_to_music_folder = os.path.abspath(os.path.dirname(sys.argv[0])) + "\\all_music\\"

    # Функция для добавления всех .mp3 файлов из папки в БД и в основную папку с музыкой all_music
    def addFiles(self):
        folderChoosen = QFileDialog.getExistingDirectory(self.window, 'Open Music Folder', expanduser('~'))
        if folderChoosen != None:
            it = QDirIterator(folderChoosen)
            it.next()
            while it.hasNext():
                if it.fileInfo().isDir() is False and it.filePath() != '.':
                    fInfo = it.fileInfo()
                    if fInfo.suffix() == 'mp3':
                        song_name = fInfo.fileName()[:-4]
                        author_name = "Автор неизвестен"
                        year = 0
                        self.music_db.add_track_in_db(song_name, author_name, year)
                        track_id = self.music_db.get_track_id(song_name, author_name)
                        try:
                            os.rename(it.filePath(), self.path_to_music_folder + str(track_id) + ".mp3")
                        except:
                            pass
                it.next()