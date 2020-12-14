import sys
import threading

from PyQt5.QtWidgets import QApplication, QMainWindow, QToolButton, QSizePolicy
from PyQt5 import uic

from game import Game
from settings import Settings

main_ui = uic.loadUiType('MainWindow.ui')[0]


class Button(QToolButton):
    def __init__(self, key, callback):
        super().__init__()
        self.setStyleSheet('background:white')
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.key = key

        if callback is not None:
            self.clicked.connect(callback)
        else:
            self.setDisabled(True)


class MainWindow(QMainWindow, main_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.settings = Settings()

        self.setupPanels()

        self.start.clicked.connect(self.game_page)
        self.level.clicked.connect(self.setting_page)
        self.back.clicked.connect(self.main_page)
        self.back_2.clicked.connect(self.main_page)
        self.toMain.clicked.connect(self.main_page)
        self.restart.clicked.connect(self.game_page)

        # 키패드 수 최소 2X2부터 시작
        self.size.setMinimum(2)
        self.size.valueChanged.connect(self.spinBoxChanged)

        self.main_page()
        self.show()

    # 초기화면
    def main_page(self):
        self.stackedWidget.setCurrentIndex(0)

    # 난이도 조절
    def setting_page(self):
        self.stackedWidget.setCurrentIndex(1)

    def game_page(self):
        game.clearData()
        self.generatePanel()
        self.stackedWidget.setCurrentIndex(2)
        gameController = threading.Thread(target=game.newLevel)
        gameController.start()

    # 버튼 객체 삭제 및 패널 초기화
    def setupPanels(self):
        self.panel = {"question": {}, "answer": {}}
        self.clearLayout(self.Question)
        self.clearLayout(self.Answer)

    def clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

    def generateButton(self, layout, layout_name, x, y, callback):
        key = x * self.settings.getKeypadSize() + y
        button = Button(key, callback)
        self.panel[layout_name][key] = button
        layout.addWidget(button, x, y, 1, 1)

    def getButton(self, layout_name, key):
        return self.panel[layout_name][key]

    def generatePanel(self):
        self.setupPanels()
        for i in range(self.settings.getKeypadSize()):
            for j in range(self.settings.getKeypadSize()):
                self.generateButton(self.Question, "question", i, j, None)
                self.generateButton(self.Answer, "answer", i, j, self.buttonClick)

    def buttonClick(self):
        game.checkAnswer(self.sender().key)

    def spinBoxChanged(self):
        self.settings.setKeypadSize(self.size.value())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    game = Game(ex)
    ex.resize(900, 600)
    sys.exit(app.exec_())
