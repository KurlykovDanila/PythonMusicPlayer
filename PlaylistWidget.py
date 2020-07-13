from PyQt5.QtWidgets import *


# Класс для создания плейлистов
class PlaylistWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Виджет плейлиста
        self.playlist = QVBoxLayout()

    # Добавляет все кнопки в один горизонтальеый виджет, а потом добавляет его в виджет плейлиста
    def add_widget(self, song_name, author_name, first_widget, first_fun, second_fun, second_widget):
        new_widget = QWidget(self)
        # Виджет одной песни
        box = QHBoxLayout()
        # Настройка кнопки песни, её иконка, выполняемая функция
        pbt_song = QPushButton(self)
        pbt_song.resize(50, 10)
        pbt_song.setText(song_name)
        # Задаю отношение в котором кнопки будут относительно друг друга, в данный момент 3/3
        sp_song = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sp_song.setHorizontalStretch(3)
        pbt_song.setSizePolicy(sp_song)
        pbt_song.clicked.connect(first_fun)
        pbt_song.setStyleSheet('QPushButton {color: #ffffff}')

        pbt_author = QPushButton(self)
        pbt_author.resize(50, 100)
        pbt_author.setText(author_name)
        sp_author = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sp_author.setHorizontalStretch(3)
        pbt_author.setSizePolicy(sp_author)
        pbt_author.clicked.connect(second_fun)
        pbt_author.setStyleSheet('QPushButton {color: #ffffff}')
        # Добавляю все кнопки в виджет
        box.addWidget(first_widget)
        box.addWidget(pbt_song)
        box.addWidget(pbt_author)
        if second_widget is not None:
            box.addWidget(second_widget)
        new_widget.setLayout(box)
        self.playlist.addWidget(new_widget, -1)
        # Возвращаю все виджеты песни
        return {"play": str(first_widget),
                "song": str(pbt_song),
                "author": str(pbt_author),
                "delete": str(second_widget)}

    # Очищаю плейлист
    def clear_playlist(self):
        self.playlist = QVBoxLayout()