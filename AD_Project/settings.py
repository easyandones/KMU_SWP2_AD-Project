# 게임 설정 메뉴 관련 기능들


class Settings():
    def __init__(self):
        self.keypadSize = 3

    def setKeypadSize(self, num):
        self.keypadSize = num

    def getKeypadSize(self):
        return self.keypadSize
