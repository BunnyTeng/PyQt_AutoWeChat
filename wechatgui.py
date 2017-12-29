#coding: UTF-8
import sys
import itchat
from itchat.content import *
from PyQt4 import QtGui, QtCore

###################################回复内容#######################################
@itchat.msg_register(TEXT, isGroupChat = True)#group into this
def text_reply(msg):
    print 'intoone'
    if msg['isAt']:
        if busy:
            return 'Sorry,I\'m busy at the moment'
        elif sleep:
            return 'Sorry,I\'m sleeping now'
        elif leave:#
            return 'Sorry,I\'m not at home now'

@itchat.msg_register([TEXT, MAP, CARD, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO])#single chat into this
def text_reply(msg):
    print ('leave = %d'%leave)
    if busy:
        return 'Sorry,I\'m busy at the moment'
    elif sleep:
        return 'Sorry,I\'m sleeping now'
    elif leave:#
        return 'Sorry,I\'m not at home now'
##################################回复API##########################################
class Reply(QtCore.QThread):
    def __init__(self, parent=None):
        super(Reply, self).__init__(parent)

    def run(self):
        global busy
        global sleep
        global leave
        if self.busy == 1:
            busy = 1
            sleep = 0
            leave = 0
        if self.sleep == 1:
            busy = 0
            sleep = 1
            leave = 0
        if self.leave == 1:
            busy = 0
            sleep = 0
            leave = 1
        itchat.run()

    def busy_status(self):
        self.busy = 1
        self.sleep = 0
        self.leave = 0
    def sleep_status(self):
        self.busy = 0
        self.sleep = 1
        self.leave = 0
    def leave_status(self):
        self.busy = 0
        self.sleep = 0
        self.leave = 1
        print 'leave'

class Login(QtCore.QThread):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)

    def run(self):
        itchat.auto_login()
###################################new一个主窗口#########################################
class Createwindow(QtGui.QWidget):
    def __init__(self):
        super(Createwindow, self).__init__()

        self.init()
    def init(self):
###################################按键#########################################
        bt_set = QtGui.QPushButton('设置'.decode('utf8'), self)
        bt_set.resize(bt_set.sizeHint())
        bt_set.move(5, 120)
        #需要建立新线程

        self.connect(bt_set, QtCore.SIGNAL("clicked()"), self.bt_setfunction)

        bt_login = QtGui.QPushButton('登录'.decode('utf8'), self)
        bt_login.resize(bt_login.sizeHint())
        bt_login.move(89, 120)
        self.loginthread = Login()
        self.connect(bt_login, QtCore.SIGNAL("clicked()"), self.loginthread.start)

        bt_exit = QtGui.QPushButton('退出'.decode('utf8'), self)
        bt_exit.resize(bt_exit.sizeHint())
        bt_exit.move(171, 120)
        #退出
        bt_exit.clicked.connect(QtCore.QCoreApplication.instance().quit)
##################################单选框##########################################
        self.ck_leave = QtGui.QRadioButton('离开'.decode('utf8'), self)#将‘忙碌’解码为utf8
        self.ck_leave.resize(self.ck_leave.sizeHint())
        self.ck_leave.move(5, 10)

        self.ck_busy = QtGui.QRadioButton('忙碌'.decode('utf8'), self)
        self.ck_busy.resize(self.ck_busy.sizeHint())
        self.ck_busy.move(5, 50)

        self.ck_sleep = QtGui.QRadioButton('睡觉'.decode('utf8'),self)
        self.ck_sleep.resize(self.ck_sleep.sizeHint())
        self.ck_sleep.move(5,90)
##################################主窗口显示##########################################
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('WeChat AutoReply')
        self.show()

    def bt_setfunction(self):
        self.replythread = Reply()
        if(self.ck_leave.isChecked()):
            self.replythread.leave_status()
        if(self.ck_busy.isChecked()):
            self.replythread.busy_status()
        if(self.ck_sleep.isChecked()):
            self.replythread.sleep_status()
        self.replythread.start()

def appstart():
    app = QtGui.QApplication(sys.argv)
    win = Createwindow()
    sys.exit(app.exec_())

if __name__=='__main__':
    appstart()