from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtCore import QSize
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from DownloadPlaylist import DownloadPlaylist


# Класс для окна с входом в аккаунт
class ImportMusic(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('import_music.ui', self)

        self.pbt_back.setIcon(QtGui.QIcon('src/back.png'))
        self.pbt_back.setIconSize(QSize(40, 40))
        self.pbt_back.clicked.connect(self.back)

        self.pbt_import.setIcon(QtGui.QIcon('src/import_music.png'))
        self.pbt_import.setIconSize(QSize(200, 400))
        self.pbt_import.clicked.connect(self.get_account_info)

    # Получает и предаёт логин и пароль другому окну
    def get_account_info(self):
        login = self.inp_login.text()
        password = self.inp_password.text()
        if login != "" and password != "":
            self.second_form = DownloadPlaylist(login, password)
            self.second_form.show()

    def back(self):
        self.closeEvent()

    def closeEvent(self, event=None):
        self.close()
        self.destroy()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImportMusic()
    ex.show()
    sys.exit(app.exec())
