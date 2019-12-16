
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget,QLineEdit, QLCDNumber, QSlider,
                             QVBoxLayout, QApplication,QPushButton,QInputDialog,QTextEdit,QAction)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        lcd = QLCDNumber(self)
        sld = QSlider(Qt.Horizontal, self)
        vbox = QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(sld)
        sld.valueChanged.connect(lcd.display)

        self.btn = QPushButton('Dialog', self)
        vbox.addWidget(self.btn)
        self.btn.clicked.connect(self.showDialog)

        self.le = QLineEdit(self)
        vbox.addWidget(self.le)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Signal & slot')
        self.show()

    # 事件键盘事件处理
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog',
                                        'Enter your name:')
        if ok:
            self.le.setText(str(text))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
