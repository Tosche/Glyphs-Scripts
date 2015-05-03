#MenuTitle: Guideline Locker
# -*- coding: utf-8 -*-
__doc__="""
(GUI) Locks selected guidelines and unlocks all guidelines. It’s convenient for un/locking multiple selected guidelines.
"""

import vanilla
import GlyphsApp

class GuidelineLocker( object ):
	def __init__( self ):
		# Window 'self.w':
		spaceX = 10
		spaceY = 10
		buttonSizeX = 250
		buttonSizeY = 20
		windowWidth  = spaceX*2+buttonSizeX
		windowHeight = spaceY*4+buttonSizeY*3+25
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Guideline Locker", # window title
			autosaveName = "com.Tosche.GuidelineLocker.mainwindow" # stores last window position and size
		)
		
		# Run Button:
		self.w.runButton0 = vanilla.Button((spaceX, spaceY, buttonSizeX, buttonSizeY), "Lock selected guidelines", sizeStyle='regular', callback=self.GuidelineLockerMain )
		self.w.runButton1 = vanilla.Button((spaceX, spaceY*2+buttonSizeY, buttonSizeX, buttonSizeY), "Unlock all global guidelines", sizeStyle='regular', callback=self.GuidelineLockerMain )
		self.w.runButton2 = vanilla.Button((spaceX, spaceY*3+buttonSizeY*2, buttonSizeX, buttonSizeY), "Unlock all local guidelines*", sizeStyle='regular', callback=self.GuidelineLockerMain )
		self.w.text_1 = vanilla.TextBox( (spaceX, spaceY*3+buttonSizeY*3+10, buttonSizeX, 15), "* Only in the current layer of current glyph", sizeStyle='small' )
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()
		self.w.setDefaultButton( self.w.runButton0 )

	def GuidelineLockerMain( self, sender ):
		try:
			font = Glyphs.font
			fontMaster = font.selectedFontMaster
			listOfSelectedLayers = font.selectedLayers
			thisGlyph = font.selectedLayers[0].parent

			font.disableUpdateInterface()

			if sender == self.w.runButton0:
				for glGuideToLock in fontMaster.guideLines:
					if glGuideToLock in font.selectedLayers[0].selection():
						glGuideToLock.makeLocked()
				thisGlyph.beginUndo()
				for lcGuideToLock in font.selectedLayers[0].guideLines:
					if lcGuideToLock in font.selectedLayers[0].selection():
						lcGuideToLock.makeLocked()
				thisGlyph.endUndo()

			elif sender == self.w.runButton1:
				for glGuideToUnlock in fontMaster.guideLines:
					glGuideToUnlock.makeUnlocked()

			elif sender == self.w.runButton2:
				for lcGuideToUnlock in font.selectedLayers[0].guideLines:
					thisGlyph.beginUndo()
					lcGuideToUnlock.makeUnlocked()
					thisGlyph.endUndo()
					
			font.enableUpdateInterface()
						
		except Exception, e:
			# brings macro window to front and reports error:
			Glyphs.showMacroWindow()
			print "GuidelineLocker Error: %s" % e

GuidelineLocker()