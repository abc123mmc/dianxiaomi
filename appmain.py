from PyQt5.QtCore import QRect,QCoreApplication,QMetaObject
from PyQt5.QtWidgets import QCheckBox,QPushButton,QApplication,QWidget
import automatic_shunt
import threading #线程
import ctypes


class weiThreading:
    def t_start(self,fun,*args):
        '''传入函数名和参数，启动函数线程'''
        try:
            self.t1 = threading.Thread(target=lambda:fun(*args))
            self.t1.start()
        except:
            print('出错了,详情查看日志')
            weiLog().l_error('error_log')
    def t_close(self):
        '''终止线程'''
        xcid=self.t1.ident#线程id[线程标识符]
        ctypes.c_long(xcid)#tid对应的C中的类型，返回c_long(xcid)
        #pythonapi是一个预定义的符号用来访问python C api.
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(xcid, ctypes.py_object(SystemExit))#结束线程
        if res == 0:
            print('无效线程')
            #raise ValueError('无效的线程')#抛出类型为ValueError的异常，异常内容为invalid thread id(无效的线程)
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(xcid, None)
            raise SystemError('Py线程状态设置异步Exc失败了')#Py线程状态设置异步Exc失败了,PyThreadState_SetAsyncExc failed

class Ui_Form(automatic_shunt.automaticShunt,object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(306, 149)
        self.checkBox = QCheckBox(Form)
        self.checkBox.setGeometry(QRect(30, 10, 141, 31))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QCheckBox(Form)
        self.checkBox_2.setGeometry(QRect(30, 42, 141, 31))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QCheckBox(Form)
        self.checkBox_3.setGeometry(QRect(30, 74, 141, 31))
        self.checkBox_3.setObjectName("checkBox_3")
        self.pushButton = QPushButton(Form)
        self.pushButton.setGeometry(QRect(200, 13, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QPushButton(Form)
        self.pushButton_2.setGeometry(QRect(200, 64, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QPushButton(Form)
        self.pushButton_3.setGeometry(QRect(200, 114, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.checkBox_4 = QCheckBox(Form)
        self.checkBox_4.setGeometry(QRect(30, 108, 141, 31))
        self.checkBox_4.setObjectName("checkBox_4")

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(self.slot1)
        self.pushButton_2.clicked.connect(lambda:xc.t_start(self.slot2))
        self.pushButton_3.clicked.connect(self.slot3)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "店小蜜自动分流"))
        self.checkBox.setText(_translate("Form", "分流下单未付款名单"))
        self.checkBox_2.setText(_translate("Form", "分流未下单高意愿名单"))
        self.checkBox_3.setText(_translate("Form", "分流其他未下单名单"))
        self.pushButton.setText(_translate("Form", "打开浏览器"))
        self.pushButton_2.setText(_translate("Form", "开始分流"))
        self.pushButton_3.setText(_translate("Form", "停止分流"))
        self.checkBox_4.setText(_translate("Form", "全部分流"))

    def slot1(self):
        try:
            self.panduan001
            print('浏览器已经打开，无需重复操作')
        except:
            self.star_driver()
            self.panduan001=1

    def slot2(self):
        try:
            self.panduan002
            print('分流已经执行，无需重复操作')
        except:
            self.panduan002=1
            latest_date=''
            self.new_page()#调用打开新页面
            while 1:
                try:
                    x1=self.checkBox.isChecked()
                    x2=self.checkBox_2.isChecked()
                    x3=self.checkBox_3.isChecked()
                    x4=self.checkBox_4.isChecked()
                    automatic_shunt.currency.time.sleep(3)
                    if not self.panduan002:
                        continue
                    try:latest_date2=self.go_dianxiaomi(latest_date='')#调用打开店小蜜
                    except:pass
                    if latest_date!=latest_date2:
                        self.run(x1,x2,x3,x4)
                        latest_date=latest_date2
                except:
                    automatic_shunt.currency.Ri_zhi()
            

    def slot3(self):
        if self.panduan002:self.panduan002=0
        else:self.panduan002=1

if __name__ == "__main__":
    import sys
    xc=weiThreading()
    app = QApplication(sys.argv)
    Form = QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
