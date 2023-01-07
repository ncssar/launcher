import os
import sys
import glob

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

qtDesignerSubDir='designer' # subdir containing Qt Designer source files (*.ui)
qtUiPySubDir='ui' # target subdir for compiled ui files (*_ui.py)
qtQrcSubDir='.' # subdir containing Qt qrc resource files (*.qrc)
qtRcPySubDir='.' # target subdir for compiled resource files
iconsSubDir='icons'

installDir=os.path.dirname(os.path.realpath(__file__))
qtDesignerDir=os.path.join(installDir,qtDesignerSubDir)
qtUiPyDir=os.path.join(installDir,qtUiPySubDir)
qtQrcDir=os.path.join(installDir,qtQrcSubDir)
qtRcPyDir=os.path.join(installDir,qtRcPySubDir)
iconsDir=os.path.join(installDir,iconsSubDir)

def rprint(t):
	print(t)
	
# rebuild all _ui.py files from .ui files in the same directory as this script as needed
#   NOTE - this will overwrite any edits in _ui.py files
for ui in glob.glob(os.path.join(qtDesignerDir,'*.ui')):
	uipy=os.path.join(qtUiPyDir,os.path.basename(ui).replace('.ui','_ui.py'))
	if not (os.path.isfile(uipy) and os.path.getmtime(uipy) > os.path.getmtime(ui)):
		cmd='pyuic5 -o '+uipy+' '+ui
		rprint('Building GUI file from '+os.path.basename(ui)+':')
		rprint('  '+cmd)
		os.system(cmd)

# rebuild all _rc.py files from .qrc files in the same directory as this script as needed
#   NOTE - this will overwrite any edits in _rc.py files
for qrc in glob.glob(os.path.join(qtQrcDir,'*.qrc')):
	rcpy=os.path.join(qtRcPyDir,os.path.basename(qrc).replace('.qrc','_rc.py'))
	if not (os.path.isfile(rcpy) and os.path.getmtime(rcpy) > os.path.getmtime(qrc)):
		cmd='pyrcc5 -o '+rcpy+' '+qrc
		rprint('Building Qt Resource file from '+os.path.basename(qrc)+':')
		rprint('  '+cmd)
		os.system(cmd)

from ui.launcher_ui import Ui_launcher

# Tried MANY methods to allow the image to scale up on mouse enter, and down on mouse leave;
#  it was surprisingly tricky.  The method below uses a pushbutton widget, and a plain widget with
#  the same geometry.  These overlapping widgets are possible if they are not inside a layout structure,
#  or, if they are in the same cell of a QGridLayout.  There's no need to use a layout structure
#  in this case.
# When the pushbutton is entered, we want to increase the size of the plain widget, and vice versa.
# Since mouse actions only go to one widget, mouseMoveEvent at the top dialog level checks to
#  see if either the pushbutton or the plain widget are under the mouse, and compares to the previous
#  state.  If there is a change from previous state, the plain widget (with the foreground image) is
#  grown or shrunk as appropriate.
class MyWindow(QDialog,Ui_launcher):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.setWindowFlags(self.windowFlags()|Qt.WindowMinMaxButtonsHint)
		self.parent=parent
		self.ui=Ui_launcher()
		self.ui.setupUi(self)
		self.ui.caltopoButtonWidget.setStyleSheet('image:url(:/launcher/icons/caltopo_logo.svg);')
		self.um=False
		growBy=20 # per side
		self.cbwSmallGeom=self.ui.caltopoButtonWidget.geometry()
		bigX=self.cbwSmallGeom.x()-growBy
		bigY=self.cbwSmallGeom.y()-growBy
		bigW=self.cbwSmallGeom.width()+2*growBy
		bigH=self.cbwSmallGeom.height()+2*growBy
		self.cbwBigGeom=QRect(bigX,bigY,bigW,bigH)
	
	def mouseMoveEvent(self,e):
		um1=self.ui.caltopoButton.underMouse()
		um2=self.ui.caltopoButtonWidget.underMouse()
		um=um1 or um2
		if um and not self.um: # enter
			self.ui.caltopoButtonWidget.setGeometry(self.cbwBigGeom) # works
			# animation=QPropertyAnimation(self.ui.caltopoButtonWidget,b'geometry')
			# animation.setDuration(1000)
			# animation.setStartValue(self.cbwSmallGeom)
			# animation.setEndValue(self.cbwBigGeom)
			# animation.start()
			rprint('entering: cbw pos='+str(self.ui.caltopoButtonWidget.pos()))
			self.um=um
		elif self.um and not um: # leave
			self.ui.caltopoButtonWidget.setGeometry(self.cbwSmallGeom)
			rprint(' leaving')
			self.um=um


class AnimatedHoverButton(QPushButton):
	# clicked=pyqtSignal()
	def __init__(self,parent,*args,**kwargs):
		self.parent=parent
		QPushButton.__init__(self,parent)
		self.w=self.size().width()
		self.h=self.size().height()
		rprint('w='+str(self.w)+' h='+str(self.h))
		self.inner=False
		# self.pressed=False

	# def enterEvent(self,e):
	# 	rprint('in')
	# 	# self.setIconSize(QSize(160,160))
	# 	# self.setIconSize(QSize(self.w-20,self.h-20))
	# 	# QCoreApplication.processEvents()
	# 	# self.setIconSize(self.big)
	# 	# self.parent.ui.caltopoButtonWidget.setFixedSize(self.big)
	# 	# animation=QPropertyAnimation(self,b'iconSize') # iconSize is not a valid property, apparently
	# 	# animation=QPropertyAnimation(self.icon(),b'size') # QIcon is not a QObject - throws TypeError
	# 	# animation=QPropertyAnimation(self.parent.ui.caltopoButtonWidget,b'geometry')
	# 	# animation.setDuration(1000)
	# 	# animation.setStartValue(self.smallRect)
	# 	# animation.setEndValue(self.bigRect)
	# 	# animation.start()
	# 	self.setStyleSheet('border: 10px outset blue; padding: 30px;')
	# 	self.parent.ui.caltopoButtonWidget.setContentsMargins(10,10,10,10)

	# def leaveEvent(self,e):
	# 	# if self.parent.ui.caltopoButtonWidget.underMouse():
	# 	# 	return
	# 	# if self.inner:
	# 	# 	return
	# 	rprint('out')
	# 	# self.setIconSize(self.small)
	# 	# self.parent.ui.caltopoButtonWidget.setFixedSize(self.small)
	# 	# self.setIconSize(QSize(self.w-60,self.h-60))
	# 	# QCoreApplication.processEvents()
	# 	# animation=QPropertyAnimation(self,b'iconSize')
	# 	# animation.setDuration(1000)
	# 	# animation.setStartValue(self.iconSize())
	# 	# animation.setEndValue(QSize(50,50))
	# 	# animation.start()
	# 	self.setStyleSheet('border: 20px inset blue; padding: 40px;')
	# 	self.parent.ui.caltopoButtonWidget.setContentsMargins(20,20,20,20)
	# 	# animation=QPropertyAnimation(self.parent.ui.caltopoButtonWidget,b'geometry')
	# 	# animation.setDuration(1000)
	# 	# animation.setStartValue(self.bigRect)
	# 	# animation.setEndValue(self.smallRect)
	# 	# animation.start()


def main():
	app = QApplication(sys.argv)
	# eFilter=customEventFilter()
	# app.installEventFilter(eFilter)
	w = MyWindow(app)
	w.show()
	sys.exit(app.exec_())

if __name__ == "__main__":
	# sys.excepthook = handle_exception
	main()