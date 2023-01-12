import os
import sys
import glob
import winreg
import enum
import subprocess
import json

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

# ADAPTED FROM https://gist.github.com/asissuthar/1470a3080c276ac0caf0ab237d91afcd

sources = [
    [
        winreg.HKEY_LOCAL_MACHINE,
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
    ],
    [
        winreg.HKEY_LOCAL_MACHINE,
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
    ],
    [
        winreg.HKEY_CURRENT_USER,
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
    ],
]

class HKEYEnum(enum.Enum):
	HKEY_LOCAL_MACHINE=winreg.HKEY_LOCAL_MACHINE
	HKEY_CURRENT_USER=winreg.HKEY_CURRENT_USER

class ReadMode(enum.Enum):
   KEY = 1
   VALUE = 2

def read(key, mode):
    i = 0
    while True:
        try:
            if mode == ReadMode.KEY:
                yield winreg.EnumKey(key, i)
            elif mode == ReadMode.VALUE:
                yield winreg.EnumValue(key, i)
            i += 1
        except OSError:
            break

def readRegistery(keyType, registryKeyPath):
    registry = winreg.ConnectRegistry(None, keyType)
    access=winreg.KEY_READ
    if 'WOW6432' not in registryKeyPath: # disable redirection, so that non-WOW actually opens non-WOW
        access=winreg.KEY_READ|winreg.KEY_WOW64_64KEY
    registryKey = winreg.OpenKey(registry, registryKeyPath,0,access)
    for subKeyName in read(registryKey, ReadMode.KEY):
        # rprint('subkey:'+subKeyName)
        subKey = winreg.OpenKey(registry, f"{registryKeyPath}\\{subKeyName}",0,access)
        values = {}
        for subKeyValue in read(subKey, ReadMode.VALUE):
            values[subKeyValue[0]] = subKeyValue[1]
        yield values

# getAppData
#  argument: beginning of the application name to search for
#  return: list of application data from the registry: [InstalledLocation,DisplayVersion]
def getAppData(appNameStart):
	for source in sources:
		# rprint('Source:'+HKEYEnum(source[0]).name+'\\'+source[1])
		for data in readRegistery(source[0], source[1]):
			# rprint(json.dumps(data,indent=3))
			if 'DisplayName' in data and data['DisplayName'].startswith(appNameStart):
				return [data.get('InstallLocation'),data.get('DisplayVersion')]



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

		self.ui.caltopoButtonWidget.setGraphicsEffect(QGraphicsOpacityEffect())
		self.ui.radiologButtonWidget.setGraphicsEffect(QGraphicsOpacityEffect())
		self.ui.iapbButtonWidget.setGraphicsEffect(QGraphicsOpacityEffect())
		# self.ui.sliderWidget.setGraphicsEffect(QGraphicsOpacityEffect())

		with open('launcher.html','r') as file:
			self.launcherHTML=file.read()

		with open('caltopo.html','r') as file:
			self.caltopoHTML=file.read()

		with open('radiolog.html','r') as file:
			self.radiologHTML=file.read()

		with open('iapb.html','r') as file:
			self.iapbHTML=file.read()

		self.radiologAppData=getAppData('RadioLog')
		self.radiologHTML+='<br><h2>Installed version: '+str(self.radiologAppData[1]+'</h2>')

		self.ctdAppData=getAppData('CalTopo')
		rprint('ctd:'+str(self.ctdAppData))

		self.sartopoLANURL='https://microsoft.com'

		# caltopo button was the only one for which click signal was getting sent... why?
		# noticed that it was the only button with a .raise_() command in _ui.py... why?
		# not sure, but, raise them all here.  This might simplify other parts of the code too...
		self.ui.caltopoButton.raise_()
		self.ui.radiologButton.raise_()
		self.ui.iapbButton.raise_()

		self.ui.caltopoButtonWidget.setStyleSheet('image:url(:/launcher/icons/caltopo_logo.svg);')
		self.um1=False
		self.um2=False
		self.um3=False

		self.opacityList=[0.7,1]

		growBy=10 # per side

		self.cbwSmallGeom=self.ui.caltopoButtonWidget.geometry()
		self.cbwBigGeom=QRect(
			self.cbwSmallGeom.x()-growBy,
			self.cbwSmallGeom.y()-growBy,
			self.cbwSmallGeom.width()+2*growBy,
			self.cbwSmallGeom.height()+2*growBy)
		
		self.rbwSmallGeom=self.ui.radiologButtonWidget.geometry()
		self.rbwBigGeom=QRect(
			self.rbwSmallGeom.x()-growBy,
			self.rbwSmallGeom.y()-growBy,
			self.rbwSmallGeom.width()+2*growBy,
			self.rbwSmallGeom.height()+2*growBy)
	
		self.ibwSmallGeom=self.ui.iapbButtonWidget.geometry()
		self.ibwBigGeom=QRect(
			self.ibwSmallGeom.x()-growBy,
			self.ibwSmallGeom.y()-growBy,
			self.ibwSmallGeom.width()+2*growBy,
			self.ibwSmallGeom.height()+2*growBy)

		self.mouseMoveEvent(None) # initially set all opacities to 1

	def mouseMoveEvent(self,e):
		um1a=self.ui.caltopoButton.underMouse()
		um1b=self.ui.caltopoButtonWidget.underMouse()
		um2a=self.ui.radiologButton.underMouse()
		um2b=self.ui.radiologButtonWidget.underMouse()
		um3a=self.ui.iapbButton.underMouse()
		um3b=self.ui.iapbButtonWidget.underMouse()
		umTray=self.ui.caltopoTrayWidget.underMouse()
		umT1=self.ui.caltopoWebButton.underMouse()
		umT2=self.ui.caltopoLANButton.underMouse()
		umT3=self.ui.caltopoLocalhostButton.underMouse()
		umT=umTray or umT1 or umT2 or umT3
		# even though the button is raised, button.underMouse becomes false when moving inwards
		# rprint(str(int(um1a))+' '+str(int(um1b))+' '+str(int(umTray))+' '+str(int(umT1))+' '+str(int(umT2))+' '+str(int(umT3)))
		um1=um1a or um1b or umT
		um2=um2a or um2b
		um3=um3a or um3b
		umNone=not(um1 or um2 or um3)
		self.ui.caltopoButtonWidget.graphicsEffect().setOpacity(self.opacityList[int(um1 or umNone)])
		self.ui.radiologButtonWidget.graphicsEffect().setOpacity(self.opacityList[int(um2 or umNone)])
		self.ui.iapbButtonWidget.graphicsEffect().setOpacity(self.opacityList[int(um3 or umNone)])
		if um1 and not self.um1: # enter caltopo
			# self.ui.caltopoButtonWidget.setGeometry(self.cbwBigGeom) # works
			# rprint('entering: cbw pos='+str(self.ui.caltopoButtonWidget.pos()))
			# animation objects must be object attributes so that they persist after this function is done
			self.caltopoAnimation=QPropertyAnimation(self.ui.caltopoButtonWidget,b'geometry')
			self.caltopoAnimation.setEndValue(self.cbwBigGeom)
			self.caltopoAnimation.setDuration(100)
			self.caltopoAnimation.start()
			# self.sliderOpacityAnimation=QPropertyAnimation(self.ui.sliderWidget.graphicsEffect(),b'opacity')
			# self.sliderOpacityAnimation.setEndValue(1)
			# self.sliderOpacityAnimation.start()
			# self.sliderAnimation=QPropertyAnimation(self.ui.sliderWidget,b'size')
			# self.sliderAnimation.setEndValue(QSize(600,140))
			# self.sliderAnimation.start()
			self.trayAnimation=QPropertyAnimation(self.ui.caltopoTrayWidget,b'pos')
			self.trayAnimation.setEndValue(QPoint(130,39))
			self.trayAnimation.start()
			self.ui.textEdit.setHtml(self.caltopoHTML)
			self.um1=um1
		elif self.um1 and not um1: # leave caltopo
			# self.ui.caltopoButtonWidget.setGeometry(self.cbwSmallGeom)
			self.caltopoAnimation=QPropertyAnimation(self.ui.caltopoButtonWidget,b'geometry')
			self.caltopoAnimation.setEndValue(self.cbwSmallGeom)
			self.caltopoAnimation.setDuration(100)
			self.caltopoAnimation.start()
			# self.sliderOpacityAnimation=QPropertyAnimation(self.ui.sliderWidget.graphicsEffect(),b'opacity')
			# self.sliderOpacityAnimation.setEndValue(0)
			# self.sliderOpacityAnimation.start()
			# self.sliderAnimation=QPropertyAnimation(self.ui.sliderWidget,b'size')
			# self.sliderAnimation.setEndValue(QSize(20,140))
			# self.sliderAnimation.start()
			self.trayAnimation=QPropertyAnimation(self.ui.caltopoTrayWidget,b'pos')
			self.trayAnimation.setEndValue(QPoint(-470,39))
			self.trayAnimation.start()
			# rprint(' leaving')
			self.um1=um1
		if um2 and not self.um2: # enter radiolog
			# self.ui.radiologButtonWidget.setGeometry(self.rbwBigGeom)
			self.radiologAnimation=QPropertyAnimation(self.ui.radiologButtonWidget,b'geometry')
			self.radiologAnimation.setEndValue(self.rbwBigGeom)
			self.radiologAnimation.setDuration(100)
			self.radiologAnimation.start()
			self.ui.textEdit.setHtml(self.radiologHTML)
			self.um2=um2
		elif self.um2 and not um2: # leave radiolog
			# self.ui.radiologButtonWidget.setGeometry(self.rbwSmallGeom)
			self.radiologAnimation=QPropertyAnimation(self.ui.radiologButtonWidget,b'geometry')
			self.radiologAnimation.setEndValue(self.rbwSmallGeom)
			self.radiologAnimation.setDuration(100)
			self.radiologAnimation.start()
			self.um2=um2
		if um3 and not self.um3: # enter IAP builder
			# self.ui.iapbButtonWidget.setGeometry(self.ibwBigGeom)
			self.iapbAnimation=QPropertyAnimation(self.ui.iapbButtonWidget,b'geometry')
			self.iapbAnimation.setEndValue(self.ibwBigGeom)
			self.iapbAnimation.setDuration(100)
			self.iapbAnimation.start()
			self.ui.textEdit.setHtml(self.iapbHTML)
			self.um3=um3
		elif self.um3 and not um3: # leave IAP builder
			# self.ui.iapbButtonWidget.setGeometry(self.ibwSmallGeom)
			self.iapbAnimation=QPropertyAnimation(self.ui.iapbButtonWidget,b'geometry')
			self.iapbAnimation.setEndValue(self.ibwSmallGeom)
			self.iapbAnimation.setDuration(100)
			self.iapbAnimation.start()
			self.um3=um3
		if umNone:
			self.ui.textEdit.setHtml(self.launcherHTML)
		if umT1:
			rprint('umT1')

 	# since a quick move of the mouse could exit the window without mouseMoveEvent being called
	#  on a location that would reset icon opacities and sizes, do it here manually
	def leaveEvent(self,e):
		self.mouseMoveEvent(None)

	def caltopoClicked(self):
		rprint('caltopo clicked')

	def radiologClicked(self):
		rprint('radiolog clicked')
		self.ui.textEdit.append('<br><h2>Launching RadioLog...</h2>')
		QCoreApplication.processEvents()
		QTimer.singleShot(5000,lambda:self.ui.textEdit.setHtml(self.radiologHTML))
		# os.system('"'+os.path.join(self.radiologAppData[0],'RadioLog.exe')+'"')
		subprocess.Popen('"'+os.path.join(self.radiologAppData[0],'RadioLog.exe')+'"')
		
	def iapbClicked(self):
		rprint('IAP builder clicked')
		shutil.copyfile(template,dst)

	def caltopoWebClicked(self):
		rprint('caltopo web clicked')
		self.ui.textEdit.append('<br><h2>Opening sartopo.com in a new browser tab...</h2>')
		QCoreApplication.processEvents()
		QTimer.singleShot(2000,lambda:self.ui.textEdit.setHtml(self.caltopoHTML))
		os.system('start https://sartopo.com')
		
	def caltopoLANClicked(self):
		rprint('caltopo LAN clicked')
		self.ui.textEdit.append('<br><h2>Opening '+self.sartopoLANURL+' in a new browser tab...</h2>')
		QCoreApplication.processEvents()
		QTimer.singleShot(2000,lambda:self.ui.textEdit.setHtml(self.caltopoHTML))
		os.system('start '+self.sartopoLANURL)

	def caltopoLocalhostClicked(self):
		rprint('caltopo localhost clicked')

# class AnimatedHoverButton(QPushButton):
# 	# clicked=pyqtSignal()
# 	def __init__(self,parent,*args,**kwargs):
# 		self.parent=parent
# 		QPushButton.__init__(self,parent)
# 		self.w=self.size().width()
# 		self.h=self.size().height()
# 		rprint('w='+str(self.w)+' h='+str(self.h))
# 		self.inner=False
# 		# self.pressed=False

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