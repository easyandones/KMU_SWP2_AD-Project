import random
import time
import threading


class Game():
    # 최초 설정
    def __init__(self, window):
        self.clearData()
        self.window = window
        self.settings = self.window.settings

    # amount 길이의 새로운 답안 생성
    def getNewKeys(self, amount):
        self.answer = [random.randrange(self.settings.getKeypadSize() ** 2) for i in range(amount)]

    # UI에서 question패널 num번의 키패드 반짝이게
    def highlightKey(self, num):
        button = self.window.getButton("question", num)
        button.setStyleSheet('background:black')
        time.sleep(0.5)
        button.setStyleSheet('background:white')

    # order 순서대로 화면의 키패드 출력 - 0.5초 간격
    def showKeys(self, order):
        for key in order:
            self.highlightKey(key)
            time.sleep(0.5)

    # 키패드 입력 허용 및 차단 - 문제가 제시되는 동안은 입력 불가하게
    def blockKeypad(self, state):
        self.keypadBlock = state
        for i in range(self.settings.getKeypadSize() ** 2):
            self.window.getButton("answer", i).setDisabled(state)

    # attempt 순서의 답안이 key인지 확인
    def checkAttempt(self, attempt, key):
        return self.answer[attempt] == key

    # 답안 확인 ---- key는 해당 키패드 번호
    def checkAnswer(self, key):
        if self.keypadBlock:
            return
        if self.checkAttempt(self.attempt, key):
            self.attempt += 1
            if self.attempt == len(self.answer):
                gameController = threading.Thread(target=self.newLevel)
                gameController.start()
        else:
            self.gameOver()

    # 레벨 불러오기
    def newLevel(self):
        self.blockKeypad(True)
        self.level += 1
        self.attempt = 0
        self.getNewKeys(self.level)
        self.showKeys(self.answer)
        self.blockKeypad(False)

    # 게임 결과 불러오기 - 결과를 UI에 표시
    def getResult(self):
        self.window.total_score.setText(str(self.level))
        self.window.stackedWidget.setCurrentIndex(3)

    # 게임 데이터 초기화
    def clearData(self):
        self.keypadBlock = True
        self.level = 0
        self.answer = []
        self.attempt = 0

    # 게임 오버
    def gameOver(self):
        self.getResult()
        self.clearData()
