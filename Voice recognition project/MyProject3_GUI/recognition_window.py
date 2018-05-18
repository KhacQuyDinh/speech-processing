# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'recognition_window.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QDialog
import record_audio_training as recorder
import train_models as trainer
import test_speaker as recognizer
import os 
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_recognition_window(object):
    def record_audio(self):
        cmd = self.tv_record_cmd.toPlainText()
        if cmd != "":
            recorder.record(self.tv_record_cmd.toPlainText())

    def train_model(self):
        trainer.train()

    def test_recognizer(self):
        recognizer.recognize()

    def setupUi(self, recognition_window):
        recognition_window.setObjectName(_fromUtf8("recognition_window"))
        recognition_window.resize(797, 641)
        recognition_window.setWindowTitle(_fromUtf8("recognition_window"))
        self.widget = QtGui.QWidget(recognition_window)
        self.widget.setGeometry(QtCore.QRect(0, 0, 801, 641))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.tv_record_cmd = QtGui.QTextEdit(self.widget)
        self.tv_record_cmd.setGeometry(QtCore.QRect(190, 510, 581, 51))
        font = QtGui.QFont()
        font.setItalic(False)
        self.tv_record_cmd.setFont(font)
        self.tv_record_cmd.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.tv_record_cmd.setObjectName(_fromUtf8("tv_record_cmd"))
        self.btn_record = QtGui.QPushButton(self.widget)
        self.btn_record.setGeometry(QtCore.QRect(60, 510, 99, 51))
        self.btn_record.setObjectName(_fromUtf8("btn_record"))
        self.btn_test = QtGui.QPushButton(self.widget)
        self.btn_test.setEnabled(True)
        self.btn_test.setGeometry(QtCore.QRect(430, 580, 99, 51))
        self.btn_test.setObjectName(_fromUtf8("btn_test"))
        self.btn_train = QtGui.QPushButton(self.widget)
        self.btn_train.setGeometry(QtCore.QRect(60, 580, 99, 51))
        self.btn_train.setObjectName(_fromUtf8("btn_train"))
        self.lv_available_cmd = QtGui.QListWidget(self.widget)
        self.lv_available_cmd.setGeometry(QtCore.QRect(0, 0, 791, 231))
        self.lv_available_cmd.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.lv_available_cmd.setObjectName(_fromUtf8("lv_available_cmd"))
        self.lv_log_info = QtGui.QListWidget(self.widget)
        self.lv_log_info.setGeometry(QtCore.QRect(0, 250, 791, 241))
        self.lv_log_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.lv_log_info.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.lv_log_info.setObjectName(_fromUtf8("lv_log_info"))

        #---------------------------------
        self.btn_record.clicked.connect(self.record_audio)
        self.btn_train.clicked.connect(self.train_model)
        self.btn_test.clicked.connect(self.test_recognizer)                          
	
	modelpath = "word_training_set"        
        words = [f_name for f_name in os.listdir(modelpath)]        
        for i, word in enumerate(words):
	    cmd = str(i + 1) + ". " + word
            self.lv_available_cmd.addItem(cmd.decode('utf-8'))
        #---------------------------------

        self.retranslateUi(recognition_window)
        QtCore.QMetaObject.connectSlotsByName(recognition_window)

    def retranslateUi(self, recognition_window):
        self.tv_record_cmd.setHtml(_translate("recognition_window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Enter the name of command you want to record...</p></body></html>", None))
        self.btn_record.setText(_translate("recognition_window", "Record", None))
        self.btn_test.setText(_translate("recognition_window", "Test", None))
        self.btn_train.setText(_translate("recognition_window", "Train", None))

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    recognition_window = QtGui.QDialog()
    ui = Ui_recognition_window()
    ui.setupUi(recognition_window)    
    recognition_window.show()
    sys.exit(app.exec_())
