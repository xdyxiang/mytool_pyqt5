import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
                             QHBoxLayout, QVBoxLayout, QApplication,QGridLayout,QLabel,QLineEdit,QTextEdit)
from PyQt5.QtGui import QIcon

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('这是一个标题')
        # 设置窗口的图标，引用当前目录下的web.png图片
        self.setWindowIcon(QIcon('../static/picture/houzi.ico'))
        self.initUI()

    # 绝对定位
    # def initUI(self):
    #     lbl1 = QLabel('Zetcode', self)
    #     lbl1.move(15, 10)
    #
    #     lbl2 = QLabel('tutorials', self)
    #     lbl2.move(35, 40)
    #
    #     lbl3 = QLabel('for programmers', self)
    #     lbl3.move(55, 70)
    #
    #     self.setGeometry(300, 300, 250, 150)
    #     self.setWindowTitle('Absolute')
    #     self.show()



    # 框布局
    # def initUI(self):
    #     okButton = QPushButton("OK")
    #     cancelButton = QPushButton("Cancel")
    #
    #     hbox = QHBoxLayout()
    #     hbox.addStretch(1)
    #     hbox.addWidget(okButton)
    #     hbox.addWidget(cancelButton)
    #
    #     vbox = QVBoxLayout()
    #     vbox.addStretch(1)
    #     vbox.addLayout(hbox)
    #
    #     self.setLayout(vbox)
    #
    #     self.setGeometry(300, 300, 300, 150)
    #     self.setWindowTitle('Buttons')
    #     self.show()


    # def initUI(self):
    #
    #     grid = QGridLayout()
    #     self.setLayout(grid)
    #
    #     names = ['Cls', 'Bck', '', 'Close',
    #              '7', '8', '9', '/',
    #              '4', '5', '6', '*',
    #              '1', '2', '3', '-',
    #              '0', '.', '=', '+']
    #
    #     positions = [(i, j) for i in range(5) for j in range(4)]
    #
    #     for position, name in zip(positions, names):
    #
    #         if name == '':
    #             continue
    #         button = QPushButton(name)
    #         grid.addWidget(button, *position)
    #
    #     self.move(300, 150)
    #     self.setWindowTitle('Calculator')
    #     self.show()

    def initUI(self):
        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')

        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()

        grid = QGridLayout()
        # 设置周边宽度
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(review, 3, 0)
        # 设置占行占列
        grid.addWidget(reviewEdit, 3, 1, 10, 1)

        self.setLayout(grid)

        self.setGeometry(300, 300, 350, 300)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

