import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog
from pyowm import OWM
from pyowm.utils.config import get_default_config
import sqlite3
#from datetime import datetime
'''не удалось реализовать задание заметкам звукового напоминания,
поэтому куски кода, отвечающие за данный функционал,
закомментированы с целью дальнейшего улучшения'''
from playsound import playsound


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('test.ui', self)
        self.setWindowTitle('Notes')

        #дизайн
        self.setStyleSheet("background-image: url(bluebg.png);")
        self.label.setStyleSheet("background-image: url(cat1.png);")
        self.createnew.setStyleSheet("background: #6a87ed; border-radius: 45px; color: rgb(255, 255, 255);")
        self.notes.setStyleSheet("background: #363636; border-radius: 5px; color: rgb(255, 255, 255);")
        self.showNote.setStyleSheet("background: #363636; border-radius: 5px; color: rgb(255, 255, 255);")
        self.deleteNote.setStyleSheet("background: #363636; border-radius: 30px; color: rgb(255, 255, 255);")
        self.setcall.setStyleSheet("background: #363636; border-radius: 30px; color: rgb(255, 255, 255);")
        self.deletecall.setStyleSheet("background: #363636; border: 2px solid #ffffff; "
                                      "border-radius: 10px; color: red;")
        self.readycall.setStyleSheet("background: #363636; border: 2px solid #ffffff; "
                                     "border-radius: 10px; color: green;")
        self.saveNote.setStyleSheet("background: #363636; border-radius: 30px; color: rgb(255, 255, 255);")
        self.update.setStyleSheet("background: #363636; border-radius: 5px; color: rgb(255, 255, 255);")
        self.cities.setStyleSheet("background: #6a87ed; border-radius: 5px; color: rgb(255, 255, 255);")
        self.notnamline.setStyleSheet("background: #ffffff; border-radius: 5px;")
        self.nottextline.setStyleSheet("background: #ffffff; border-radius: 5px;")
        self.weather.setStyleSheet("color: rgb(255, 255, 255);")
        self.temp.setStyleSheet("color: rgb(255, 255, 255);")

        #привязка кнопок к функциям
        self.update.clicked.connect(self.update_weather)
        self.createnew.clicked.connect(self.create_new_one)
        self.saveNote.clicked.connect(self.save_note)
        self.setcall.clicked.connect(self.note_call)
        self.deletecall.clicked.connect(self.delete_note_call)
        self.readycall.clicked.connect(self.ready_note_call)
        self.showNote.clicked.connect(self.show_note)
        self.deleteNote.clicked.connect(self.delete_note)
        """self.showNote.clicked.connect(self.is_time_to_call())"""

        #начальное отображение виджетов редактирования/создания заметки
        self.notesName.hide()
        self.notnamline.hide()
        self.notesText.hide()
        self.nottextline.hide()
        self.timeline.hide()
        self.deleteNote.hide()
        self.saveNote.hide()
        self.deletecall.hide()
        self.setcall.hide()
        self.readycall.hide()

        #список городов
        self.cities.addItem('Moscow')
        self.cities.addItem('Krasnodar')
        self.cities.addItem('Saint Petersburg')
        self.cities.addItem('Rostov')
        self.cities.addItem('Novosibirsk')

        #список существующих заметок
        con = sqlite3.connect("Заметки.sqlite")
        cur = con.cursor()
        result = cur.execute("""SELECT name FROM notelist """).fetchall()
        con.close()
        for elem in result:
            for i in elem:
                self.notes.addItem(i)

    #функция отображения выбранной заметки на экране
    def show_note(self):
        con = sqlite3.connect("Заметки.sqlite")
        cur = con.cursor()
        result = cur.execute("""SELECT text FROM notelist 
        WHERE name = '{nm}'""".format(**{'nm': self.notes.currentText()})).fetchall()
        con.close()
        self.notnamline.setText(self.notes.currentText())
        self.nottextline.setText(result[0][0])
        self.notesName.show()
        self.notnamline.show()
        self.notesText.show()
        self.nottextline.show()
        self.deleteNote.show()
        self.saveNote.show()
        self.setcall.show()

    #функция удаления заметки
    def delete_note(self):
        #удаление уже существующей заметки
        con = sqlite3.connect("Заметки.sqlite")
        cur = con.cursor()
        result = cur.execute("""SELECT name FROM notelist """).fetchall()
        con.close()
        s = []
        for elem in result:
            for i in elem:
                s.append(i)
        if self.notnamline.text() in s:
            con = sqlite3.connect("Заметки.sqlite")
            cur = con.cursor()
            result = cur.execute("""SELECT text FROM notelist 
            WHERE name = '{nm}'""".format(**{'nm': self.notnamline.text()})).fetchall()
            con.close()
            #проверка, что сейчас не редактируется ещё несохранённая заметка
            #с таким же именем, как у уже существующей
            if self.nottextline.toPlainText() == result[0][0]:
                con = sqlite3.connect("Заметки.sqlite")
                cur = con.cursor()
                result = cur.execute("""DELETE FROM notelist
                                WHERE name = '{nm}'""".format(**{'nm': self.notnamline.text()}))
                con.commit()
                con.close()
                self.notnamline.setText('')
                self.nottextline.setText('')
                self.notesName.hide()
                self.notnamline.hide()
                self.notesText.hide()
                self.nottextline.hide()
                self.timeline.hide()
                self.deleteNote.hide()
                self.saveNote.hide()
                self.deletecall.hide()
                self.setcall.hide()
                self.readycall.hide()
                self.notes.removeItem(self.notes.currentIndex())
            else:
                self.notnamline.setText('')
                self.nottextline.setText('')
                self.notesName.hide()
                self.notnamline.hide()
                self.notesText.hide()
                self.nottextline.hide()
                self.timeline.hide()
                self.deleteNote.hide()
                self.saveNote.hide()
                self.deletecall.hide()
                self.setcall.hide()
                self.readycall.hide()
        else: #удаление ещё несохранённой заметки
            self.notnamline.setText('')
            self.nottextline.setText('')
            self.notesName.hide()
            self.notnamline.hide()
            self.notesText.hide()
            self.nottextline.hide()
            self.timeline.hide()
            self.deleteNote.hide()
            self.saveNote.hide()
            self.deletecall.hide()
            self.setcall.hide()
            self.readycall.hide()

    #функция добавления новой заметки
    def create_new_one(self):
        self.notnamline.setText('')
        self.nottextline.setText('')
        #включение отображения виджетов редактирования/создания заметки
        self.notesName.show()
        self.notnamline.show()
        self.notesText.show()
        self.nottextline.show()
        self.deleteNote.show()
        self.saveNote.show()
        self.setcall.show()

    #функция сохранения заметки
    def save_note(self):
        #проверка на пустоту строки названия заметки с выводом диалогового окна
        if self.notnamline.text() == '' or self.notnamline.text() == ' ':
            text, ok = QInputDialog.getText(self, 'Error', 'Enter note name:')
            if ok:
                self.notnamline.setText(str(text))
        else:
            #проверка на существование заметки с таким же именем
            con = sqlite3.connect("Заметки.sqlite")
            cur = con.cursor()
            result = cur.execute("""SELECT name FROM notelist """).fetchall()
            con.close()
            s = []
            for elem in result:
                for i in elem:
                    s.append(i)
            if self.notnamline.text() in s:
                text, ok = QInputDialog.getItem(self, "Error",
                                                "A note with that name already exists. What do you want to do?",
                                                ("Enter new name.", "Edit note."), 1, False)
                if ok:
                    #если пользователь решил ввести новое имя для заметки:
                    cur_value = str(text)
                    if cur_value == "Enter new name.":
                        text, ok = QInputDialog.getText(self, 'Error', 'Enter note name:')
                        if ok:
                            self.notnamline.setText(str(text))
                    #если пользователь решил редактировать заметку с введённым именем:
                    elif cur_value == "Edit note.":
                        con = sqlite3.connect("Заметки.sqlite")
                        cur = con.cursor()
                        result = cur.execute("""UPDATE notelist
                            SET text = ?
                            WHERE name = ?""", (self.nottextline.toPlainText(), self.notnamline.text())).fetchall()
                        con.commit()
                        con.close()
            else:
                #добавление заметки в базу данных
                con = sqlite3.connect("Заметки.sqlite")
                cur = con.cursor()
                result = cur.execute("""INSERT INTO notelist(name,text) 
                VALUES ('{nm}', '{t}') """.format(**{'nm': self.notnamline.text(),
                                                     't': self.nottextline.toPlainText()}))
                con.commit()
                self.notes.clear()
                result = cur.execute("""SELECT name FROM notelist """).fetchall()
                con.close()
                for elem in result:
                    for i in elem:
                        self.notes.addItem(i)
                con.close()

    def note_call(self):
        self.deletecall.show()
        self.readycall.show()
        self.timeline.show()

    def delete_note_call(self):
        self.deletecall.hide()
        self.readycall.hide()
        self.timeline.hide()

    def ready_note_call(self):
        con = sqlite3.connect("Заметки.sqlite")
        cur = con.cursor()
        result = cur.execute("""SELECT name FROM notelist """).fetchall()
        con.close()
        s = []
        for elem in result:
            for i in elem:
                s.append(i)
        if self.notnamline.text() in s:
            con = sqlite3.connect("Заметки.sqlite")
            cur = con.cursor()
            result = cur.execute("""SELECT text FROM notelist 
            WHERE name = '{nm}'""".format(**{'nm': self.notnamline.text()})).fetchall()
            con.close()
            # проверка, что сейчас не редактируется ещё несохранённая заметка
            # с таким же именем, как у уже существующей
            if self.nottextline.toPlainText() == result[0][0]:
                con = sqlite3.connect("Заметки.sqlite")
                cur = con.cursor()
                dtcall = self.timeline.dateTime()
                result = cur.execute("""UPDATE notelist SET date = '{d}'
                        WHERE name = '{nm}'""".format(**{'nm': self.notnamline.text(),
                        'd': ' '.join(str(dtcall).replace('PyQt5.QtCore.QDateTime(', '')[:-1].split(', '))})).fetchall()
                con.commit()
                con.close()

    """def is_time_to_call(self):
        while True:
            con = sqlite3.connect("Заметки.sqlite")
            cur = con.cursor()
            result = cur.execute("""'SELECT date FROM notelist'""").fetchall()
            con.close()
            dtnow = datetime.now()
            if str(dtnow.strftime("%H")).startswith('0'):
                current_hour = int(str(dtnow.strftime("%H"))[1:])
            else:
                current_hour = int(dtnow.strftime("%H"))
            if str(dtnow.strftime("%H")).startswith('0'):
                current_min = int(str(dtnow.strftime("%M"))[1:])
            else:
                current_min = int(dtnow.strftime("%M"))
            if str(dtnow.strftime("%H")).startswith('0'):
                current_year = int(str(dtnow.strftime("%Y"))[1:])
            else:
                current_year = int(dtnow.strftime("%Y"))
            if str(dtnow.strftime("%H")).startswith('0'):
                current_month = int(str(dtnow.strftime("%m"))[1:])
            else:
                current_month = int(dtnow.strftime("%m"))
            if str(dtnow.strftime("%H")).startswith('0'):
                current_day = int(str(dtnow.strftime("%e"))[1:])
            else:
                current_day = int(dtnow.strftime("%e"))
            for elem in result:
                for i in elem:
                    if i is None:
                        pass
                    else:
                        if int(i[0:4]) == current_year and int(i[5]) == current_month and\
                                int(i[7]) == current_day and 
                                int(i[9]) == int(current_hour) and int(i[11]) == current_min:
                            playsound('Alarm.wav')"""

    #функция определения текущей погоды
    def update_weather(self):
        config_dict = get_default_config()
        config_dict['language'] = 'ru'
        owm = OWM('ваш ключ', config_dict)
        mgr = owm.weather_manager()
        city = self.cities.currentText()
        observation = mgr.weather_at_place(city + ', RU')
        w = observation.weather
        weathernow = w.detailed_status
        self.weather.setText(weathernow.capitalize())
        self.temp.setText(str(w.temperature('celsius')['temp']) + 'C')
        if 'снег' in weathernow:
            self.label.setStyleSheet("background-image: url(снег.png);")
        elif 'дождь' in weathernow:
            self.label.setStyleSheet("background-image: url(дождь.png);")
        else:
            self.label.setStyleSheet("background-image: url(cat1.png);")
        playsound('minecraft-cat-meloboom.wav')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
