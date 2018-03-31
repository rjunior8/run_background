from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from threading import Thread
import sys
import time
from multiprocessing import Queue, Process

class Test(QMainWindow):
    counter = pyqtSignal(str)
    counting = False

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Test")
        self.setFixedSize(150, 150)

        self.lbl = QLabel("", self)
        self.lbl.move(70, 50)

        self.btn = QPushButton("Start", self)
        self.btn.move(25, 90)
        self.btn.clicked.connect(self.count)

        self.counter.connect(self.lbl.setText)

        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def count(self):
        if not self.counting:
            self.counting = True
            t1 = Thread(target=self.s)
            t1.setDaemon(True)
            t1.start()

    def s(self):
        for x in range(10):
            self.counter.emit(str(x))
            time.sleep(0.99)
        self.counting = False

def background():
    for i in range(10):
        print(i)
        time.sleep(0.99)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Test()

    q = Queue()
    p = Process(target=background)
    p.start()
    p.join()

    sys.exit(app.exec_())