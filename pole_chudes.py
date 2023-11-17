import sys

from PyQt5 import uic, QtCore, QtMultimedia
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap, QTransform
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QInputDialog
from random import randint, randrange

PLAYERS = []
COMPLEXITY = ['Детские', 'Школьные', 'Эрудит']
ANSWERS = {'Банкрот': f'Увы! Вы БАНКРОТ. Следующий игрок, вращайте барабан!',
           '1000': '1000 очков, буква?',
           '100': '100 очков, буква?',
           'x2': 'Если вы угадаете букву, ваши очки удвоятся! Буква?',
           '600': '600 очков, буква?',
           '800': '800 очков, буква?',
           '+1': 'Открылась одна буква в слове! Вращайте барабан!',
           '400': '400 очков, буква?',
           '900': '900 очков, буква?',
           '0': 'Увы, 0 очков на барабане. Следующий игрок, вращайте барабан!',
           'Приз': 'Вам достаётся приз: 1000 очков! Вращайте барабан!',
           '500': '500 очков, буква?',
           '300': '300 очков, буква?',
           '200': '200 очков, буква?',
           'x3': 'Если вы угадаете букву, ваши очки утроятся! Буква?',
           '700': '700 очков, буква?'}
RUS_ALPHABET = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'.lower()


class Start(QMainWindow):
    def __init__(self):
        super(Start, self).__init__()
        uic.loadUi('Поле чудес.ui', self)
        self.setWindowTitle('Поле Чудес!')
        self.load_mp3('music.mp3')
        self.music_player.play()
        self.button_rules.clicked.connect(self.game_rules)
        self.button_exit.clicked.connect(self.game_exit)
        self.button_setting.clicked.connect(self.music_setting)
        self.button_settings.clicked.connect(self.game_settings)

        self.game_rules_window = AboutGame()
        self.game_settings_window = GameSettings()

    def load_mp3(self, filename):
        media = QtCore.QUrl.fromLocalFile(filename)
        content = QtMultimedia.QMediaContent(media)
        self.music_player = QtMultimedia.QMediaPlayer()
        self.music_player.setMedia(content)

    def game_rules(self):
        self.game_rules_window.show()

    def music_setting(self):
        value, ok_pressed = QInputDialog.getItem(self, "Выберите громкость музыки", "Настройки музыки",
                                                 ("100", "75", "50", "25", "0"), self.music_player.volume(), False)
        if ok_pressed:
            self.music_player.setVolume(int(value))

    def game_settings(self):
        self.hide()
        self.game_rules_window.hide()
        self.game_settings_window.show()

    def game_exit(self):
        self.close()


class AboutGame(QWidget):
    def __init__(self):
        super(AboutGame, self).__init__()

        self.setWindowTitle('Об игре')
        self.setLayout(QVBoxLayout(self))
        self.setFixedSize(1420, 100)
        self.info = QLabel(self)
        self.info.setText('Игроки по очереди вращают барабан и предлагают свои варианты букв или слов.  Как только '
                          'игрок открывает все буквы или называет слово верно - он побеждает в игре.')
        self.setStyleSheet("background-color: rgb(35, 211, 255); font: 14pt 'Times New Roman'")
        self.layout().addWidget(self.info)


class GameSettings(QWidget):
    def __init__(self):
        super(GameSettings, self).__init__()
        uic.loadUi('Настройки игры.ui', self)
        self.setWindowTitle('Настройки игры')
        self.button_start.setIcon(QIcon('1265142.jpeg'))
        self.complexity_box.addItems(COMPLEXITY)
        PLAYERS.append(self.player_1_name.text())
        PLAYERS.append(self.player_2_name.text())
        PLAYERS.append(self.player_3_name.text())
        self.button_start.clicked.connect(self.game)

        self.game_window = Game()

    def game(self):
        self.hide()
        self.game_window.show()


class Game(QWidget):
    def __init__(self):
        super(Game, self).__init__()
        uic.loadUi('Поле чудес(игра).ui', self)
        self.drum.setAlignment(Qt.AlignCenter)
        self.setWindowTitle('Поле чудес!')
        media = QtCore.QUrl.fromLocalFile('music.mp3')
        content = QtMultimedia.QMediaContent(media)
        self.music_player = QtMultimedia.QMediaPlayer()
        self.music_player.setMedia(content)
        self.question_label.setWordWrap(True)
        self.answer_label.setWordWrap(True)
        self.pixmap_drum = QPixmap('baraban.png')
        self.drum.setPixmap(self.pixmap_drum)
        self.drum.resize(self.pixmap_drum.width(), self.pixmap_drum.height())
        self.arrow.setStyleSheet('image: url("стрелка.png");')
        self.player_name_1.setText(PLAYERS[0])
        self.player_name_2.setText(PLAYERS[1])
        self.player_name_3.setText(PLAYERS[2])
        self.player = 0
        self.background_label.setStyleSheet('image: url("Фон для игры");')
        self.talk_label.setText(f'Добро пожаловать! {PLAYERS[self.player % 3]}, вращайте барабан!')
        self.players = [self.player_1_points, self.player_2_points, self.player_3_points]
        self.buttons = [self.pushButton, self.pushButton_2, self.pushButton_3, self.pushButton_4,
                        self.pushButton_5, self.pushButton_6, self.pushButton_7, self.pushButton_8,
                        self.pushButton_9, self.pushButton_10, self.pushButton_11, self.pushButton_12,
                        self.pushButton_13, self.pushButton_14, self.pushButton_15, self.pushButton_16,
                        self.pushButton_17, self.pushButton_18, self.pushButton_19, self.pushButton_20,
                        self.pushButton_21, self.pushButton_22, self.pushButton_23, self.pushButton_24,
                        self.pushButton_25, self.pushButton_26, self.pushButton_27, self.pushButton_28,
                        self.pushButton_29, self.pushButton_30, self.pushButton_31, self.pushButton_32,
                        self.pushButton_33]
        for s in self.buttons:
            s.clicked.connect(self.letter)
        self.music_button.clicked.connect(self.music)
        self.spin_the_rell.clicked.connect(self.run)
        self.all_word_button.clicked.connect(self.all_word)
        self.get_question()

    def get_question(self):
        with open('questions.txt', 'r', encoding='utf-8') as f:
            question_list = f.read().splitlines()
        number_question = randrange(0, len(question_list))
        question_answer = str(question_list[number_question])
        for i in range(len(question_answer)):
            if question_answer[i] == ';':
                self.question = question_answer[:i]
                self.answer = question_answer[i + 1:len(question_answer)].lower()
        self.curent_view = []
        for _ in self.answer:
                self.curent_view.append('*')
        self.question_label.setText(self.question)
        self.answer_label.setText(''.join(self.curent_view))

    def run(self):
        angel = 1
        a = randint(1, 360)
        for _ in range(a):
            self.drum.setPixmap(self.pixmap_drum.transformed(QTransform().rotate(angel)))
            angel += 1
        if angel <= 12 or angel > 349:
            self.talk_label.setText(f"{PLAYERS[self.player % 3]}, {ANSWERS['Банкрот']}")
            self.players[self.player % 3].display(0)
            self.player += 1
        elif 12 < angel <= 33:
            self.talk_label.setText(f"{PLAYERS[self.player % 3]}, {ANSWERS['1000']}")
            self.spin_the_rell.setEnabled(False)
        elif 33 < angel <= 56:
            self.talk_label.setText(ANSWERS['100'])
            self.spin_the_rell.setEnabled(False)
        elif 56 < angel <= 81:
            self.talk_label.setText(ANSWERS['x2'])
            self.spin_the_rell.setEnabled(False)
        elif 81 < angel <= 102:
            self.talk_label.setText(ANSWERS['600'])
            self.spin_the_rell.setEnabled(False)
        elif 102 < angel <= 125:
            self.talk_label.setText(ANSWERS['800'])
            self.spin_the_rell.setEnabled(False)
        elif 125 < angel <= 147:
            self.talk_label.setText(ANSWERS['+1'])
            self.curent_view.clear()
            for s in self.answer_label.text():
                self.curent_view.append(s)
            for i in range(len(self.answer)):
                if self.curent_view[i] == '*':
                    self.curent_view[i] = self.answer[i]
                    self.answer_label.setText(''.join(self.curent_view))
                    break
            if self.answer == self.answer_label.text():
                self.talk_label.setText(f'Победил(а) {PLAYERS[self.player % 3]}. Поздравляем! '
                                        f'Итог: {self.players[self.player % 3].intValue()} очков')
                self.spin_the_rell.setEnabled(False)
        elif 147 < angel <= 170:
            self.talk_label.setText(ANSWERS['400'])
            self.spin_the_rell.setEnabled(False)
        elif 170 < angel <= 191:
            self.talk_label.setText(ANSWERS['900'])
            self.spin_the_rell.setEnabled(False)
        elif 191 < angel <= 212:
            self.talk_label.setText(ANSWERS['0'])
            self.players[self.player % 3].display(self.players[self.player % 3].intValue())
            self.player += 1
        elif 212 < angel <= 235:
            self.talk_label.setText(ANSWERS['Приз'])
            self.players[self.player % 3].display(self.players[self.player % 3].intValue() + 1000)
        elif 235 < angel <= 259:
            self.talk_label.setText(ANSWERS['500'])
            self.spin_the_rell.setEnabled(False)
        elif 259 < angel <= 281:
            self.talk_label.setText(ANSWERS['300'])
            self.spin_the_rell.setEnabled(False)
        elif 281 < angel <= 303:
            self.talk_label.setText(ANSWERS['200'])
            self.spin_the_rell.setEnabled(False)
        elif 303 < angel <= 325:
            self.talk_label.setText(ANSWERS['x3'])
            self.spin_the_rell.setEnabled(False)
        elif 325 < angel <= 348:
            self.talk_label.setText(ANSWERS['700'])
            self.spin_the_rell.setEnabled(False)

    def letter(self):
        self.spin_the_rell.setEnabled(True)
        if 'вращайте барабан' in self.talk_label.text().lower():
            pass
        else:
            if self.sender().text() in self.answer:
                sum = 0
                for s in self.answer:
                    if s == self.sender().text():
                        sum += 1
                if self.talk_label.text() == ANSWERS['1000']:
                    self.player_1_points.display(self.player_1_points.intValue() + 1000)
                elif self.talk_label.text() == ANSWERS['100']:
                    self.players[self.player % 3].display(self.players[self.player % 3].intValue() + (100 * sum))
                elif self.talk_label.text() == ANSWERS['x2']:
                    self.players[self.player % 3].display(self.players[self.player % 3].intValue() * 2)
                elif self.talk_label.text() == ANSWERS['600']:
                    self.players[self.player % 3].display(self.players[self.player % 3].intValue() + (600 * sum))
                elif self.talk_label.text() == ANSWERS['800']:
                    self.players[self.player % 3].display(self.players[self.player % 3].intValue() + (800 * sum))
                elif self.talk_label.text() == ANSWERS['400']:
                    self.players[self.player % 3].display(self.players[self.player % 3].intValue() + (400 * sum))
                elif self.talk_label.text() == ANSWERS['900']:
                    self.players[self.player % 3].display(self.players[self.player % 3].intValue() + (900 * sum))
                elif self.talk_label.text() == ANSWERS['500']:
                    self.players[self.player % 3].display(self.players[self.player % 3].intValue() + (500 * sum))
                elif self.talk_label.text() == ANSWERS['300']:
                    self.players[self.player % 3].display(self.players[self.player % 3].intValue() + (300 * sum))
                elif self.talk_label.text() == ANSWERS['200']:
                    self.players[self.player % 3].display(self.players[self.player % 3].intValue() + (200 * sum))
                elif self.talk_label.text() == ANSWERS['x3']:
                    self.players[self.player % 3].display(self.players[self.player % 3].intValue() * 3)
                elif self.talk_label.text() == ANSWERS['700']:
                    self.players[self.player % 3].display(self.players[self.player % 3].intValue() + (700 * sum))
                self.talk_label.setText(f'Есть такая буква! {PLAYERS[self.player % 3]}, вращайте барабан!')
                self.sender().setEnabled(False)
                self.sender().setStyleSheet('color: rgb(255, 0, 0)')

                for i in range(len(self.answer)):
                    if self.answer[i] == self.sender().text():
                        self.curent_view[i] = self.sender().text()
            else:
                self.talk_label.setText(f'Такой буквы нет! {PLAYERS[(self.player + 1) % 3]}, вращайте барабан!')
                self.sender().setEnabled(False)
                self.sender().setStyleSheet('color: rgb(255, 0, 0)')
                self.player += 1
            self.answer_label.setText(''.join(self.curent_view))
            if self.answer == self.answer_label.text():
                self.talk_label.setText(f'Победил(а) {PLAYERS[self.player % 3]}. Поздравляем! '
                                        f'Итог: {self.players[self.player % 3].intValue()} очков')
                self.spin_the_rell.setEnabled(False)

    def all_word(self):
        word, ok_pressed = QInputDialog.getText(self, "Введите слово", "Ввод всего слова")
        if ok_pressed:
            if word == self.answer:
                self.talk_label.setText(f'Победил(а) {PLAYERS[self.player % 3]}. Поздравляем! '
                                        f'Итог: {self.players[self.player % 3].intValue()} очков')
                self.answer_label.setText(self.answer)
                self.spin_the_rell.setEnabled(False)
            else:
                self.talk_label.setText(f'{PLAYERS[self.player % 3]}, ваши очки онулированы. '
                                        f'{PLAYERS[(self.player + 1) % 3]}, вращайте барабан!')
                self.players[self.player % 3].display(0)
                self.player += 1

    def music(self):
        self.music_player.stop()
        self.music_player.play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = Start()
    wnd.show()
    sys.exit(app.exec())
