#MenuTitle: Close Tabs with Few Glyphs...
# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
__doc__="""
(GUI) Closes the tabs that have certain number of glyphs or fewer.
"""

import vanilla
import GlyphsApp

class CloseTabswithFewGlyphs( object ):
	def __init__( self ):
		# Window 'self.w':
		edY = 22
		txY = 17
		sp = 8
		btnX = 100
		btnY = 22
		windowWidth  = 230
		windowHeight = 100
		windowWidthResize  = 100 # user can resize width by this value
		windowHeightResize = 0   # user can resize height by this value
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Close Tabs with Few Glyphs", # window title
			autosaveName = "com.Tosche.CloseTabswithFewGlyphs.mainwindow" # stores last window position and size
		)

		# UI elements:
		self.w.text = vanilla.TextBox( (sp, sp, 230, txY), "Close tabs with 3 glyphs or fewer")
		self.w.glyphsCount = vanilla.Slider( (sp, sp*2+edY, -sp, edY),
				tickMarkCount = 10,
				stopOnTickMarks = True,
				minValue = 1,
				maxValue = 10,
				value = 3,
				callback = self.updateText)

		# Run Button:
		self.w.runButton = vanilla.Button((-sp-btnX, sp*3+edY*2, -sp, btnY), "Close", sizeStyle='regular', callback=self.CloseTabs )
		self.w.setDefaultButton( self.w.runButton )

		# Load Settings:
		if not self.LoadPreferences():
			print("Note: 'Close Tabs with Few Glyphs' could not load preferences. Will resort to defaults")
		
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()
		
	def SavePreferences( self, sender ):
		try:
			Glyphs.defaults["com.Tosche.CloseTabswithFewGlyphs.glyphsCount"] = self.w.glyphsCount.get()
		except:
			return False
			
		return True

	def LoadPreferences( self ):
		try:
			self.w.glyphsCount.set( Glyphs.defaults["com.Tosche.CloseTabswithFewGlyphs.glyphsCount"] )
			self.updateText(self.w.glyphsCount)
		except:
			self.w.glyphsCount.set( 3 )
			
		return True

	def updateText(self, sender):
		try:
			glyphs = int(self.w.glyphsCount.get())

			if glyphs < 10:
				plural = "s" if glyphs > 1 else ""
				self.w.text.set( "Close tabs with %s glyph%s or fewer" % (glyphs, plural) )
			else:
				self.w.text.set( "Send ALL tabs to heaven" )
		except:
			pass

	def CloseTabs( self, sender ):
		try:
			glyphs = self.w.glyphsCount.get()
			f = Glyphs.font # frontmost font
			tabsToClose = []
			if glyphs < 10:
				for t in f.tabs:
					if len(t.layers) <= glyphs:
						tabsToClose.append(t)
				for t in tabsToClose:
					t.close()
			else:
				while len(f.tabs) > 0:
					f.tabs[-1].close()
			
			if not self.SavePreferences( self ):
				print("Note: 'Close Tabs with Few Glyphs' could not write preferences.")
			
			self.w.close() # delete if you want window to stay open
		except Exception as e:
			# brings macro window to front and reports error:
			Glyphs.showMacroWindow()
			print("Close Tabs with Few Glyphs Error (CloseTabs): %s" % e)

CloseTabswithFewGlyphs()