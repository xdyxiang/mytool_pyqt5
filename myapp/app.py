import sys,os
from PyQt5.QtWidgets import QApplication, QWidget,QMainWindow
from PyQt5.QtGui import QFont,QIcon
from myapp.mytool import Ui_MainWindow
import paramiko
from PyQt5.QtCore import QThread, pyqtSignal
import time
from myapp.signup import do_signup
from myapp.db_func import DB


class SSHtool:
    def __init__(self):
        self.sshclient = None
        self.trans = None

    def init_ssh(self):
        # 实例化SSHClient
        self.sshclient = paramiko.SSHClient()
        # 自动添加策略，保存服务器的主机名和密钥信息，如果不添加，那么不再本地know_hosts文件中记录的主机将无法连接
        self.sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接SSH服务端，以用户名和密码进行认证
        self.sshclient.connect(hostname='173.23', port=22, username='root', password='6')

    def init_trans(self):
        # 实例化SSHClient
        self.trans = paramiko.Transport(('17.23', 22))
        # 自动添加策略，保存服务器的主机名和密钥信息
        self.trans.connect(username="root", password='123456')

    def init_trans_web(self):
        # 实例化SSHClient
        self.trans = paramiko.Transport(('******', 22))
        # 自动添加策略，保存服务器的主机名和密钥信息
        private_key = paramiko.RSAKey.from_private_key_file('res/id_rsa_2048houduan',password='6')
        self.trans.connect(username="root",pkey=private_key)


    def close_ssh(self):
        self.sshclient.close()

    def close_trans(self):
        if self.trans.is_active():
            self.trans.close()



class WorkThread1(QThread):
    trigger = pyqtSignal(str)
    trigger1 = pyqtSignal()
    def __int__(self):
        super(WorkThread1, self).__init__()
        self.arg1 = None
        self.arg2 = None

    def run(self):
        # sshtool.init_trans()
        sshtool.init_trans_web()
        trans = sshtool.trans
        print("WorkThread1_id:%s",self.currentThreadId())
        # 连接SSH服务端，以用户名和密码进行认证
        chan = trans.open_session()
        chan.settimeout(30)
        chan.get_pty()
        chan.invoke_shell()
        time.sleep(1)
        print(self.arg1)
        print(self.arg2)
        chan.send('echo "start";python ********* {0} {1}  && echo "执行完成";exit || echo "执行失败";exit\n'.format(self.arg1,self.arg2))
        while True:
            time.sleep(1)
            results = chan.recv(99999).decode('utf8')
            print(results)
            self.trigger.emit(results)
            if chan.exit_status_ready():
                print(chan.exit_status_ready())
                self.trigger.emit("算力已经停止。。。")
                break
        self.trigger1.emit()

    def set_arg(self,arg1,arg2):
        self.arg1 = arg1
        self.arg2 = arg2


class WorkThread2(QThread):
    trigger = pyqtSignal(str)

    def __int__(self):
        super(WorkThread2, self).__init__()
        self.arg1 = None
        self.arg2 = None

    def run(self):
        resault = do_signup(self.arg1,self.arg2)
        self.trigger.emit(resault)

    def set_arg(self,arg1,arg2):
        self.arg1 = arg1
        self.arg2 = arg2


class WorkThread3(QThread):
    trigger = pyqtSignal(str)

    def __int__(self):
        super(WorkThread3, self).__init__()
        self.work_type = 0
        self.sqlstr = None
        self.sqlstr1 = None

    def run(self):
        if self.work_type ==1:
            resault = DB().execute_sql(self.sqlstr)
            if resault:
                code = resault[0][2]
            else:
                code = ""
            str = "邮箱验证码是：{0}".format(code)
            self.trigger.emit(str)
        elif self.work_type ==2:
            resault = DB().execute_sql(self.sqlstr)
            if resault:
                code = resault[0][3]
            else:
                code = ""
            str = "短信验证码是：{0}".format(code)
            self.trigger.emit(str)
        elif self.work_type ==3:
            resault = DB().execute_sql(self.sqlstr)
            resault1 = DB().execute_sql(self.sqlstr1)
            if resault:
                code = resault[0][3]
            else:
                code = ""
            if resault1:
                code1 = resault[0][3]
            else:
                code1 = ""
            str = "邮箱验证码是：{0}\n短信验证码是：{1}".format(code,code1)
            self.trigger.emit(str)

    def work1(self,email):
        self.work_type = 1
        self.sqlstr = "select * from email_captcha where email = '{0}' order by create_time desc".format(email)

    def work2(self,mobile):
        self.work_type = 2
        self.sqlstr = "select * from sms_captcha where mobile = '{0}' order by create_time desc".format(mobile)

    def work3(self,email):
        self.work_type = 3
        self.sqlstr = "select * from email_token where email = '{0}' and send_method = 'email' order by create_time desc".format(email)
        self.sqlstr1 = "select * from email_token where email = '{0}' and send_method = 'sms' order by create_time desc".format(email)


class Mytool(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Mytool, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.hash_start)
        self.pushButton_2.clicked.connect(self.hash_stop)
        self.pushButton_3.clicked.connect(self.signup)
        self.pushButton_4.clicked.connect(self.getcode_email)
        self.pushButton_5.clicked.connect(self.getcode_email_sms)
        self.pushButton_6.clicked.connect(self.getcode_mobile)



    def show_log(self,text):
        self.textBrowser.setText(text)



    def hash_start(self):
        arg1 = self.lineEdit.text()
        arg2 = self.lineEdit_2.text()
        if not arg1 or  not arg2:
            self.textBrowser.setText("请输入正确的跑算力参数...")
            return False
        else:
            self.textBrowser.setText("开始跑算力。。。\n账号:{0}\n币种:{1}\n-------".format(arg1,arg2))

        self.buttun_enable(self.pushButton, False, "跑算力中")
        workthread1 = WorkThread1(self)
        workthread1.set_arg(arg1,arg2)
        workthread1.start()
        workthread1.trigger.connect(self.show_log)
        workthread1.trigger1.connect(lambda :self.buttun_enable(self.pushButton,True,"开始"))



    def hash_stop(self):
        # self.textBrowser.clear()
        if not self.pushButton.isEnabled():
            sshtool.close_trans()


    def signup(self):
        arg1 = self.lineEdit_3.text()
        arg2 = self.lineEdit_4.text()
        if not arg1 or not arg2:
            self.textBrowser.setText("请输入正确的注册参数...")
            return False
        else:
            self.textBrowser.setText("开始注册。。。\nemail:{0}\naccount:{1}\n请稍后-------".format(arg1,arg2))

        self.buttun_enable(self.pushButton_3, False, "注册中")
        workthread2 = WorkThread2(self)
        workthread2.set_arg(arg1,arg2)
        workthread2.start()
        workthread2.trigger.connect(self.show_log)
        workthread2.trigger.connect(lambda :self.buttun_enable(self.pushButton_3,True,"注册"))

    def getcode_email(self):
        arg1 = self.lineEdit_5.text()
        if not arg1:
            self.textBrowser.setText("请输入参数...")
            return False
        else:
            self.textBrowser.setText("开始获取验证码。。。\nemail:{0}\n请稍后-------".format(arg1))

        self.buttun_enable(self.pushButton_4, False, "")
        workthread3 = WorkThread3(self)
        workthread3.work1(arg1)
        workthread3.start()
        workthread3.trigger.connect(self.show_log)
        workthread3.trigger.connect(lambda :self.buttun_enable(self.pushButton_4,True,""))

    def getcode_mobile(self):
        arg1 = self.lineEdit_6.text()
        if not arg1:
            self.textBrowser.setText("请输入参数...")
            return False
        else:
            self.textBrowser.setText("开始获取验证码。。。\nmobile:{0}\n请稍后-------".format(arg1))

        self.buttun_enable(self.pushButton_6, False, "")
        workthread3 = WorkThread3(self)
        workthread3.work2(arg1)
        workthread3.start()
        workthread3.trigger.connect(self.show_log)
        workthread3.trigger.connect(lambda :self.buttun_enable(self.pushButton_6,True,""))


    def getcode_email_sms(self):
        arg1 = self.lineEdit_7.text()
        if not arg1:
            self.textBrowser.setText("请输入参数...")
            return False
        else:
            self.textBrowser.setText("开始获取验证码。。。\nemail:{0}\n请稍后-------".format(arg1))

        self.buttun_enable(self.pushButton_5, False, "")
        workthread3 = WorkThread3(self)
        workthread3.work3(arg1)
        workthread3.start()
        workthread3.trigger.connect(self.show_log)
        workthread3.trigger.connect(lambda :self.buttun_enable(self.pushButton_5,True,""))



    def buttun_enable(self,btu,status,text):
        btu.setEnabled(status)
        if text:
            btu.setText(text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mytool = Mytool()
    mytool.setWindowTitle('my tool')  # 设置窗口标题
    # 获取据对路径
    mytool.setWindowIcon(QIcon('res/icon.ico'))
    sshtool = SSHtool()
    mytool.show()
    sys.exit(app.exec_())
