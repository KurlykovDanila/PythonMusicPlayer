import sqlite3
from yandex_music.client import Client


# Класс для работы с БД и Яндекс апи
class MusicToDB():
    def __init__(self, login, password, db_name="Music.db"):
        super().__init__()
        self.account = {"login": str(login), "password": str(password)}
        self.db_name = db_name
        self.con = sqlite3.connect(self.db_name)
        self.cur = self.con.cursor()

    # Вход в аккаунт Яндекс Музыки
    def login(self):
        try:
            self.client = Client.from_credentials(self.account["login"], self.account["password"])
            return True
        except:
            return False

    # Возвращает список понравивщихся песен
    def return_list_of_music(self):
        list_of_music_in_yandex_account = list()
        if not self.login():
            return False
        for ind, track in enumerate(self.client.users_likes_tracks()):
            song_name = track.track["title"].replace("'", '"')
            author_name = track.track["artists"][0]["name"].replace("'", '"')
            list_of_music_in_yandex_account.append({"title": song_name, "author": author_name, "index": ind})
        return list_of_music_in_yandex_account

    # Основная функция, скачивает песни по их индексам с Яндекс Музыки
    def run(self, list_music):
        self.con = sqlite3.connect(self.db_name)
        self.cur = self.con.cursor()
        self.yandex_music_tracks = self.client.users_likes_tracks()
        for i in list_music:
            track = self.yandex_music_tracks[i]
            print(track.track)
            song_name = track.track["title"].replace("'", '"')
            author_name = track.track["artists"][0]["name"].replace("'", '"')
            year = str(track.track["albums"][0]["year"])
            self.add_track_in_db(song_name, author_name, year)
            track_id = self.get_track_id(song_name, author_name)
            track.track.download("all_music/" + str(track_id) + ".mp3")
        self.con.close()
        return True

    # Возвращает id песни из БД
    def get_track_id(self, song_name, author_name):
        return str(self.cur.execute(("""SELECT song_id FROM songs WHERE song_name = '{0}' 
                    and author_id = (SELECT author_id FROM authors 
                    WHERE author_name = '{1}')""").format(song_name, author_name)).fetchall()[0][0])

    # Объединяет функции по работе с БД, в результате добавляет информацию о песне в БД
    def add_track_in_db(self, song_name, author_name, year):
        self.add_to_db_authors(author_name)
        self.add_to_db_year(year)
        self.add_to_db_songs(song_name, author_name, year)
        self.con.commit()

    # Добавляет автора в БД
    def add_to_db_authors(self, author_name):
        if self.cur.execute(("""SELECT author_id FROM authors 
                            WHERE author_name = '{0}'""").format(author_name)).fetchall() == []:
            try:
                self.cur.execute(("""INSERT INTO authors(author_name) VALUES('{0}')""").format(author_name))
            except:
                pass

    # Добавляет имя песни, id автора и id года
    def add_to_db_songs(self, song_name, author_name, year):
        if self.cur.execute(("""SELECT song_id FROM songs 
                                WHERE song_name = '{0}' and author_id = (SELECT author_id FROM authors
                                WHERE author_name = '{1}')""").format(song_name, author_name)).fetchall() == []:
            try:
                self.cur.execute(("""INSERT INTO songs(song_name, author_id, year_id) VALUES('{0}', 
                            (SELECT author_id FROM authors 
                            WHERE author_name = '{1}'), (SELECT year_id FROM years 
                            WHERE year = '{2}'))""").format(song_name, author_name, year))
            except:
                pass

    # Добавляет год песни
    def add_to_db_year(self, year):
        if self.cur.execute(("""SELECT year_id FROM years 
        WHERE year = '{0}'""").format(year)).fetchall() == []:
            try:
                self.cur.execute(("""INSERT INTO years(year) VALUES('{0}')""").format(year))
            except:
                pass