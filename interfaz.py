__all__ = ('Gauge',)

__title__ = 'interfaz'
__version__ = '1.0'


import kivy
kivy.require('1.7.1')
from kivy.config import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.properties import BoundedNumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.scatter import Scatter
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
import random


class Componentes(Widget):
	"""docstring for Compnentes"""

	unit = NumericProperty(1.8)
	rpm = BoundedNumericProperty(0, min=0, max=100, errorvalue=0)
	fuel = BoundedNumericProperty(0, min=0, max=100, errorvalue=0)
	speedcar = BoundedNumericProperty(0, min=0, max=100, errorvalue=0)
	file_gauge = StringProperty("imagenes/RPM.png")
	file_needle = StringProperty("imagenes/needle.png")
	file_gmail = StringProperty("imagenes/gmail.png");
	file_facebook = StringProperty("imagenes/facebook.png");
	file_whatsApp = StringProperty("imagenes/whatsApp.png");
	size_gauge = BoundedNumericProperty(128, min=128, max=256, errorvalue=128)
	size_text = NumericProperty(10)


	def __init__(self, **kwargs):
		super(Componentes, self).__init__(**kwargs)

#---------------Inicializacion-----------------------

		self._gauge = Scatter(
			size=(self.size_gauge, self.size_gauge),
			do_rotate=False, 
			do_scale=False,
			do_translation=False
			)

		_img_gauge = Image(source=self.file_gauge, size=(self.size_gauge, 
			self.size_gauge))

		self._needle = Scatter(
			size=(self.size_gauge/7*6, self.size_gauge),
#			size=(self.size_gauge, self.size_gauge),
			do_rotate=False,
			do_scale=False,
			do_translation=False
			)

		_img_needle = Image(source=self.file_needle, size=(self.size_gauge/7*6, 
			self.size_gauge))
		
#redes sociales Iconos
		
		# self._gmail = Scatter(
		# 	size=(30, 30),
		# 	do_rotate=False, 
		# 	do_scale=False,
		# 	do_translation=False
		# 	)

		# _img_gmail = Image(source=self.file_gmail,size=(30,30))

		# self._facebook = Scatter(
		# 	size=(30, 30),
		# 	do_rotate=False, 
		# 	do_scale=False,
		# 	do_translation=False
		# 	)

		# _img_facebook = Image(source=self.file_facebook,size=(30,30))

		# self._whatsApp = Scatter(
		# 	size=(50, 50),
		# 	do_rotate=False, 
		# 	do_scale=False,
		# 	do_translation=False
		# 	)

		# _img_whatsApp = Image(source=self.file_whatsApp,size=(30,30))

#Fin redes sociales Iconos

		#_img_needle = Image(source=self.file_needle, size=(self.size_gauge, 
		#	self.size_gauge))

		self._glab = Label(font_size=100, markup=True)
		
		self._progress = ProgressBar(max=100, height=500, value=self.fuel)

		self._gauge.add_widget(_img_gauge)
		self._needle.add_widget(_img_needle)
		# self._gmail.add_widget(_img_gmail)
		# self._facebook.add_widget(_img_facebook)
		# self._whatsApp.add_widget(_img_whatsApp)

		self.add_widget(self._gauge)
		self.add_widget(self._needle)
		# self.add_widget(self._gmail)
		# self.add_widget(self._facebook)
		# self.add_widget(self._whatsApp)
		self.add_widget(self._glab)
		self.add_widget(self._progress)

		self.bind(pos=self._update)
		self.bind(size=self._update)
		self.bind(rpm=self._changeRPM)
		self.bind(fuel=self._changeFuel)
		self.bind(speedcar=self._changeSpeed)

	def _update(self, *args):
		'''
		Update gauge and needle positions after sizing or positioning.

		'''
		self._gauge.pos = (250,50)
		print self._gauge.pos
		print "gauge"
		self._needle.pos = (250, 50)
		print self._needle.pos
		print "needle"
		# self._gmail.pos =(300,250)
		# self._facebook.pos =(340,250)
		# self._whatsApp.pos =(380,250)
		self._needle.center = self._gauge.center
		self._glab.center_x = self._gauge.center_x
		self._glab.center_y = self._gauge.center_y
		self._progress.x = self._gauge.x
		self._progress.y = self._gauge.y + (self.size_gauge / 4)
		self._progress.width = self.size_gauge

#-----------------Update Info


	def _changeRPM(self, *args):

		self._needle.center_x = self._gauge.center_x + self.size_gauge/32
		self._needle.center_y = self._gauge.center_y - self.size_gauge/32
#		self._needle.center_x = self._gauge.center_x 
#		self._needle.center_y = self._gauge.center_y  

		self._needle.rotation = (50  - self.rpm ) * self.unit + 50
#		self._needle.rotation = -self.rpm  * self.unit 

	def _changeFuel(self, *args):
		'''
		Turn needle, 1 degree = 1 unit, 0 degree point start on 50 value.

		'''
		self._progress.value = self.fuel

	def _changeSpeed(self, *args):
		'''
		Turn needle, 1 degree = 1 unit, 0 degree point start on 50 value.

		'''
		self._glab.text = "[i][b]{0:.0f}[/b][/i]".format(self.speedcar)



rpmMax = False
fuelMax = False
speedMax = False

class GaugeApp(App):

	def build(self):
		from kivy.uix.slider import Slider
		from kivy.clock import Clock
		from functools import partial
		import serial

		box = BoxLayout(orientation='horizontal', spacing=10, padding=10)

		gauge = Componentes(rpm=0,speedcar=0,fuel=100,size_gauge=256, size_text=15)	
		
		box.add_widget(gauge)
		

		#global rpmMax = False
		#global fuelMax = False
		#global speedMax = False

		def setRPM(sender, value):
			#if (gauge.rpm == 99):
			#self.rpmMax = True

			#if (self.rpmMax):
			#gauge.rpm -= value
			#else:
			gauge.rpm += value

		def setFuel(sender, value):
			gauge.fuel += value

		def setSpeed(sender,value):
			gauge.speedcar += value

			   # def rpmValues(sender,incr):
			   #	 ser.write("01 0C \r")
			   #	 rpm_hex = ser.readline().split(' ')
			   #	 rpm = float( ((256 * int(speed[4] , 16)) + int(speed[5] ,16 ) )/4  )
		 	  #	 rpm/=800
			   #	 setgauge(0,int(rpm))
			
		def readRPM(sender,incr):
			setRPM(0,1)
			
		def readFuel(sender,incr):
			setFuel(0,-1)

		def readSpeed(sender,incr):
			setSpeed(0,1)
		

		Clock.schedule_interval(partial(readRPM,1),0.05)
		Clock.schedule_interval(partial(readFuel,1),1)
		Clock.schedule_interval(partial(readSpeed,1),0.5)

		return box

if __name__ == '__main__':
	GaugeApp().run() 
