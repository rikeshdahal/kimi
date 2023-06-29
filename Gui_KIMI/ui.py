from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(640, 495)
        self.avatar = QtWidgets.QLabel(Form)
        self.avatar.setGeometry(QtCore.QRect(0, 50, 641, 441))
        self.avatar.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.avatar.setStyleSheet("font: 63 10pt \"Segoe UI Variable Small Semibol\";\n"
                                  "color: rgb(0, 85, 0);\n"
                                  "border-color: rgb(255, 255, 255);;\n"
                                  "border-radius:10px;\n"
                                  "border-style:solid;\n"
                                  "border-width:2.5px 2.5px 2.5px 2.5px;\n"
                                  "padding:10px;\n"
                                  "background-color:transparent;\n"
                                  "")
        self.avatar.setScaledContents(True)
        self.avatar.setObjectName("avatar")
        self.Welcome = QtWidgets.QLabel(Form)
        self.Welcome.setGeometry(QtCore.QRect(90, -10, 491, 61))
        self.Welcome.setStyleSheet("font: 30pt \"Roman\";\n"
                                   "background-color:transparent;\n"
                                   "color: rgb(255, 255, 255);\n"
                                   "border-color: rgb(0, 85, 0);")

        self.Welcome.setObjectName("Welcome")
        self.debug = QtWidgets.QPushButton(Form)
        self.debug.setGeometry(QtCore.QRect(600, 260, 31, 31))
        self.debug.setStyleSheet("background-color:transparent;")
        self.debug.setIcon(QIcon("media\\debug.png"))
        self.debug.setObjectName("debug")
        self.screen = QtWidgets.QPushButton(Form)
        self.screen.setGeometry(QtCore.QRect(600, 65, 31, 31))
        self.screen.setStyleSheet("background-color:transparent;\n")
        self.screen.setIcon(QIcon("media\\halfscreen.png"))
        self.screen.setObjectName("screen")
        self.output = QtWidgets.QPlainTextEdit(Form)
        self.output.setGeometry(QtCore.QRect(440, 170, 201, 211))
        self.output.setStyleSheet("font: 63 10pt \"Segoe UI Variable Small Semibol\";\n"
                                  "color: rgb(255, 255, 255);\n"
                                  "border-color: rgb(255, 255, 255);\n"
                                  "border-radius:10px;\n"
                                  "border-style:solid;\n"
                                  "border-width:2.5px 2.5px 2.5px 2.5px;\n"
                                  "padding:10px;\n"
                                  "background-color:transparent;\n"
                                  "")
        self.output.setReadOnly(True)
        self.output.setObjectName("output")
        self.camera = QtWidgets.QPushButton(Form)
        self.camera.setGeometry(QtCore.QRect(600, 460, 31, 31))
        self.camera.setStyleSheet("background-color:transparent;")
        self.camera.setObjectName("camera")
        self.mic = QtWidgets.QPushButton(Form)
        self.camera.setIcon(QIcon("media\\camera.png"))
        self.mic.setGeometry(QtCore.QRect(0, 460, 31, 31))
        self.mic.setStyleSheet("background-color:transparent;\n")
        self.mic.setIcon(QIcon("media\\mic.png"))
        self.mic.setObjectName("mic")
        self.sound = QtWidgets.QPushButton(Form)
        self.sound.setGeometry(QtCore.QRect(0, 65, 31, 31))
        self.sound.setStyleSheet("background-color:transparent;")
        self.sound.setIcon(QIcon("media\\sound.png"))
        self.sound.setObjectName("sound")
        self.input = QtWidgets.QLineEdit(Form)
        self.input.setGeometry(QtCore.QRect(130, 420, 401, 51))
        self.input.setStyleSheet("font: 63 10pt \"Segoe UI Variable Small Semibol\";\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "border-color: rgb(255, 255, 255);\n"
                                 "border-radius:10px;\n"
                                 "border-style:solid;\n"
                                 "border-width:2.5px 2.5px 2.5px 2.5px;\n"
                                 "padding:10px;\n"
                                 "background-color:transparent;\n"
                                 "")
        self.input.setObjectName("input")
        self.cam = QtWidgets.QLabel(Form)
        self.cam.setGeometry(QtCore.QRect(0, 170, 201, 211))
        self.cam.setStyleSheet("font: 63 10pt \"Segoe UI Variable Small Semibol\";\n"
                               "color: rgb(255, 255, 255);\n"
                               "border-color: rgb(255, 255, 255);\n"
                               "border-radius:10px;\n"
                               "border-style:solid;\n"
                               "border-width:2.5px 2.5px 2.5px 2.5px;\n"
                               "padding:10px;\n"
                               "background-color:transparent;\n"
                               "")
        self.cam.setObjectName("cam")
        self.close = QtWidgets.QPushButton(Form)
        self.close.setGeometry(QtCore.QRect(600, 10, 31, 31))
        self.close.setStyleSheet("background-color:transparent;")
        self.close.setIcon(QIcon("media\\x.png"))
        self.close.setObjectName("close")
        self.footer = QtWidgets.QLabel(Form)
        self.footer.setGeometry(QtCore.QRect(170, 455, 375, 50))
        self.footer.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.footer.setStyleSheet("color: rgb(88,161,221);\n"
                                  "font: 75 10pt \"MS Shell Dlg 2\";\n"
                                  "background-color:transparent;\n"
                                  "border:none;")

        self.footer.setText(
            "@2023 Kimi AI Assistant | Designed BY RIKESH & PIYUSH")
        self.footer.setScaledContents(True)
        self.footer.setObjectName("footer")
        self.avatar.raise_()
        self.Welcome.raise_()
        self.screen.raise_()
        self.output.raise_()
        self.camera.raise_()
        self.mic.raise_()
        self.sound.raise_()
        self.input.raise_()
        self.cam.raise_()
        self.close.raise_()
        self.debug.raise_()
        self.footer.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Welcome.setText(_translate(
            "Form", "Welcome To KRIPI Technology"))
        self.output.setPlaceholderText(
            _translate("Form", "Terminal Output Goes Here"))
        self.input.setPlaceholderText(_translate("Form", "Enter Your Command"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
