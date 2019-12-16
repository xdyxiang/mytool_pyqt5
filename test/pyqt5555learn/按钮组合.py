import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QGroupBox, QRadioButton, QLabel, QHBoxLayout, QVBoxLayout


class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.groupbox_1 = QGroupBox('On and Off', self)  # 1
        self.groupbox_2 = QGroupBox('Change Color', self)

        self.red = QRadioButton('Red', self)  # 2
        self.blue = QRadioButton('Blue', self)
        self.green = QRadioButton('Green', self)
        self.yellow = QRadioButton('Yellow', self)
        self.color_list = [self.red, self.blue, self.green, self.yellow]

        self.on = QRadioButton('On', self)  # 3
        self.off = QRadioButton('Off', self)

        self.pic_label = QLabel(self)  # 4

        self.h1_layout = QHBoxLayout()
        self.h2_layout = QHBoxLayout()
        self.h3_layout = QHBoxLayout()
        self.all_v_layout = QVBoxLayout()

        self.layout_init()
        self.radiobutton_init()
        self.label_init()

    def layout_init(self):
        self.h1_layout.addWidget(self.on)
        self.h1_layout.addWidget(self.off)
        self.groupbox_1.setLayout(self.h1_layout)

        self.h2_layout.addWidget(self.red)
        self.h2_layout.addWidget(self.blue)
        self.h2_layout.addWidget(self.green)
        self.h2_layout.addWidget(self.yellow)
        self.groupbox_2.setLayout(self.h2_layout)

        self.h3_layout.addWidget(self.groupbox_1)
        self.h3_layout.addWidget(self.groupbox_2)

        self.all_v_layout.addWidget(self.pic_label)
        self.all_v_layout.addLayout(self.h3_layout)

        self.setLayout(self.all_v_layout)

    def radiobutton_init(self):
        self.yellow.setChecked(True)  # 5
        for btn in self.color_list:
            btn.clicked.connect(self.change_color_func)

        self.off.setChecked(True)  # 6
        self.off.toggled.connect(self.on_and_off_func)

    def label_init(self):  # 7
        self.pic_label.setPixmap(QPixmap('images/Off.png'))
        self.pic_label.setAlignment(Qt.AlignCenter)

    def change_color_func(self):
        if self.on.isChecked():
            path = 'images/{}.png'.format([btn.text() for btn in self.color_list if btn.isChecked()][0])
            self.pic_label.setPixmap(QPixmap(path))

    def on_and_off_func(self):
        if self.on.isChecked():
            path = 'images/{}.png'.format([btn.text() for btn in self.color_list if btn.isChecked()][0])
            self.pic_label.setPixmap(QPixmap(path))
        else:
            self.pic_label.setPixmap(QPixmap('images/Off.png'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
