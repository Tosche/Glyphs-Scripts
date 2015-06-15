#MenuTitle: Kerning Exception
# -*- coding: utf-8 -*-
__doc__="""
(GUI) Makes an kerning exception of the current pair. Note: Current glyph is considered the RIGHT side of the glyph.
"""

import vanilla
import GlyphsApp

class KerningException( object ):
	def __init__( self ):
		# Window 'self.w':
		spaceX = 10
		spaceY = 10
		buttonSizeX = 220
		buttonSizeY = 20
		windowWidth  = spaceX*2+buttonSizeX
		windowHeight = spaceY*5+buttonSizeY*4
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Kerning Exception", # window title
			autosaveName = "com.Tosche.Kerning Exception.mainwindow" # stores last window position and size
		)
		

		# Run Button:
		self.w.runButton1 = vanilla.Button((spaceX, spaceY, buttonSizeX, buttonSizeY), u"1 🔒 🔓 Unlock Right (Ta→Tà)", sizeStyle='regular', callback=self.KerningExceptionMain )
		self.w.runButton2 = vanilla.Button((spaceX, spaceY*2+buttonSizeY, buttonSizeX, buttonSizeY), u"2 🔓 🔒 Unlock Left (aT→áT)", sizeStyle='regular', callback=self.KerningExceptionMain )
		self.w.runButton3 = vanilla.Button((spaceX, spaceY*3+buttonSizeY*2, buttonSizeX, buttonSizeY), u"3 🔓 🔓 Unlock Both ", sizeStyle='regular', callback=self.KerningExceptionMain )
		self.w.runButton4 = vanilla.Button((spaceX, spaceY*4+buttonSizeY*3, buttonSizeX, buttonSizeY), u"4 🔒 🔒 Lock Both ", sizeStyle='regular', callback=self.KerningExceptionMain )

		# Assign keyboard shortcuts
		self.w.runButton1.bind('1', [])
		self.w.runButton2.bind('2', [])
		self.w.runButton3.bind('3', [])
		self.w.runButton4.bind('4', [])
		
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()

	def KerningExceptionMain( self, sender ):
		try:
			def validLayer(layer):
				if (layer == None) or (layer.name == None):
					return False
				else:
					return True

			font = Glyphs.font # frontmost font
			View = Glyphs.currentDocument.windowController().activeEditViewController().graphicView()
			ActiveLayer = View.activeLayer()
			PrevLayer = View.cachedGlyphAtIndex_(View.activeIndex() - 1)
#			HasExeption = ActiveLayer.leftKerningExeptionForLayer_(PrevLayer) # Returns 0 or 1

			if validLayer(ActiveLayer) and validLayer(PrevLayer):
				if sender == self.w.runButton1: #Unlock Right
					ActiveLayer.setLeftKerningExeption_forLayer_(True, PrevLayer)
					PrevLayer.setRightKerningExeption_forLayer_(False, ActiveLayer)
				elif sender == self.w.runButton2: #Unlock Left
					ActiveLayer.setLeftKerningExeption_forLayer_(False, PrevLayer)
					PrevLayer.setRightKerningExeption_forLayer_(True, ActiveLayer)
				elif  sender == self.w.runButton3: #Unock Both
					ActiveLayer.setLeftKerningExeption_forLayer_(True, PrevLayer)
					PrevLayer.setRightKerningExeption_forLayer_(True, ActiveLayer)
				else: #Lock Both
					ActiveLayer.setLeftKerningExeption_forLayer_(False, PrevLayer)
					PrevLayer.setRightKerningExeption_forLayer_(False, ActiveLayer)
			else:
				Glyphs.displayDialog_('Text cursor should be between the pair you want to make an exception!')

			self.w.close() # delete if you want window to stay open
		except Exception, e:
			# brings macro window to front and reports error:
			Glyphs.showMacroWindow()
			print "Kerning Exception Error: %s" % e

KerningException()