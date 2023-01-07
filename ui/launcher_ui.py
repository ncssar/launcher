# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\caver\Documents\GitHub\launcher\designer\launcher.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_launcher(object):
    def setupUi(self, launcher):
        launcher.setObjectName("launcher")
        launcher.resize(778, 629)
        launcher.setMouseTracking(True)
        self.caltopoButton = AnimatedHoverButton(launcher)
        self.caltopoButton.setGeometry(QtCore.QRect(30, 10, 180, 180))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.caltopoButton.sizePolicy().hasHeightForWidth())
        self.caltopoButton.setSizePolicy(sizePolicy)
        self.caltopoButton.setMinimumSize(QtCore.QSize(180, 180))
        self.caltopoButton.setMaximumSize(QtCore.QSize(180, 180))
        self.caltopoButton.setBaseSize(QtCore.QSize(180, 180))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.caltopoButton.setFont(font)
        self.caltopoButton.setMouseTracking(True)
        self.caltopoButton.setText("")
        self.caltopoButton.setIconSize(QtCore.QSize(20, 20))
        self.caltopoButton.setFlat(True)
        self.caltopoButton.setObjectName("caltopoButton")
        self.caltopoButton_2 = QtWidgets.QPushButton(launcher)
        self.caltopoButton_2.setGeometry(QtCore.QRect(30, 210, 181, 171))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.caltopoButton_2.setFont(font)
        self.caltopoButton_2.setObjectName("caltopoButton_2")
        self.caltopoButton_3 = QtWidgets.QPushButton(launcher)
        self.caltopoButton_3.setGeometry(QtCore.QRect(30, 390, 181, 171))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.caltopoButton_3.setFont(font)
        self.caltopoButton_3.setObjectName("caltopoButton_3")
        self.textEdit = QtWidgets.QTextEdit(launcher)
        self.textEdit.setGeometry(QtCore.QRect(260, 10, 501, 211))
        self.textEdit.setObjectName("textEdit")
        self.caltopoButtonWidget = QtWidgets.QWidget(launcher)
        self.caltopoButtonWidget.setGeometry(QtCore.QRect(30, 20, 180, 180))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.caltopoButtonWidget.sizePolicy().hasHeightForWidth())
        self.caltopoButtonWidget.setSizePolicy(sizePolicy)
        self.caltopoButtonWidget.setMinimumSize(QtCore.QSize(150, 150))
        self.caltopoButtonWidget.setMouseTracking(True)
        self.caltopoButtonWidget.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.caltopoButtonWidget.setAutoFillBackground(False)
        self.caltopoButtonWidget.setStyleSheet("image: url(:/launcher/icons/caltopo_logo.svg);")
        self.caltopoButtonWidget.setObjectName("caltopoButtonWidget")

        self.retranslateUi(launcher)
        QtCore.QMetaObject.connectSlotsByName(launcher)

    def retranslateUi(self, launcher):
        _translate = QtCore.QCoreApplication.translate
        launcher.setWindowTitle(_translate("launcher", "NCSSAR Application Launcher"))
        self.caltopoButton_2.setText(_translate("launcher", "RadioLog"))
        self.caltopoButton_3.setText(_translate("launcher", "IAP Builder"))
        self.textEdit.setHtml(_translate("launcher", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">SARTopo - Web, Trailer Server, or Localhost</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Web</span><span style=\" font-size:8pt;\"> - sartopo.com - if you expect to have very reliable and reasonably fast internet for the entire operation</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Trailer Server</span><span style=\" font-size:8pt;\"> - NCSSAR uses this most of the time- if you want to use an online map, but, your internet connection is not fast or is unreliable</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Localhost</span><span style=\" font-size:8pt;\"> - if you need to use this computer without internet or trailer server connection</span></p></body></html>"))
from launcher import AnimatedHoverButton
import launcher_rc
