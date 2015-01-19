#MenuTitle: Regular Expression Glyph Renaming
# -*- coding: utf-8 -*-
__doc__="""
(GUI) Renames selected glyphs using regular expression, with case conversion options. You can use it as a normal renaming tool too.
"""

import vanilla
import GlyphsApp
import re

class RegularExpressionGlyphRenaming( object ):
	def __init__( self ):
		# Window 'self.w':
		editY = 22
		textY  = 17
		spaceX = 10
		spaceY = 10
		windowWidth  = spaceX*2+384
		windowHeight = spaceY*4+editY*2+50
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Regular Expression Glyph Renaming", # window title
			autosaveName = "com.Tosche.RegularExpressionGlyphRenaming.mainwindow" # stores last window position and size
		)
		
		# UI elements:
		self.w.text_1 = vanilla.TextBox( (spaceX, spaceY+2, 80, textY), "Search for:", sizeStyle='regular' )
		self.w.edit_1 = vanilla.EditText( (spaceX+80, spaceY, 300, editY), "", sizeStyle = 'regular')
		
		self.w.text_2 = vanilla.TextBox( (spaceX, spaceY*2+textY+7, 80, textY), "Replace by:", sizeStyle='regular' )
		self.w.edit_2 = vanilla.EditText( (spaceX+80, spaceY*2+editY, 300, editY), "", sizeStyle = 'regular')
		options = [ "ALL CAP", "Capitalise", "all lower", "No change" ]
		self.w.cases = vanilla.RadioGroup( (spaceX, spaceY*3+editY*2, 85*4, 20 ), options, isVertical =False, callback=self.SavePreferences, sizeStyle = 'small' )
		self.w.cases.set( 3 )
		
		# Run Button:
		self.w.runButton = vanilla.Button((-80-15, -20-15, -15, -15), "Run", sizeStyle='regular', callback=self.RegularExpressionGlyphRenamingMain )
		self.w.setDefaultButton( self.w.runButton )
		
		# Load Settings:
		if not self.LoadPreferences():
			print "Note: 'Regular Expression Glyph Renaming' could not load preferences. Will resort to defaults"
		
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()
		
	def SavePreferences( self, sender ):
		try:
			Glyphs.defaults["com.Tosche.RegularExpressionGlyphRenaming.edit_1"] = self.w.edit_1.get()
			Glyphs.defaults["com.Tosche.RegularExpressionGlyphRenaming.edit_2"] = self.w.edit_2.get()
		except:
			return False
			
		return True

	def LoadPreferences( self ):
		try:
			self.w.edit_1.set( Glyphs.defaults["com.Tosche.RegularExpressionGlyphRenaming.edit_1"] )
			self.w.edit_2.set( Glyphs.defaults["com.Tosche.RegularExpressionGlyphRenaming.edit_2"] )
		except:
			return False
			
		return True

	def RegularExpressionGlyphRenamingMain( self, sender ):
		try:
			font = Glyphs.font # frontmost font
			font.disableUpdateInterface() # suppresses UI updates in Font View
			listOfSelectedLayers = font.selectedLayers # active layers of currently selected glyphs
			for layer in listOfSelectedLayers: # loop through layers
				glyph = layer.parent
				glyph.beginUndo()
				newName = re.sub(self.w.edit_1.get(), self.w.edit_2.get(), glyph.name)
				case = self.w.cases.get()
				if case == 0:
					newName = newName.upper()
				elif case == 1:
					newName = newName[0].upper() + newName[1:]
				elif case == 2:
					newName = newName.lower()

				if font.glyphs[newName]:
					if glyph.name != newName:
						print "Skipped renaming of '%s' to '%s' because of name conflict." % (glyph.name, newName)
						Glyphs.showMacroWindow()
				else:
					glyph.name = newName
				


				glyph.endUndo()
			font.enableUpdateInterface() # re-enables UI updates in Font View

			if not self.SavePreferences( self ):
				print "Note: 'Regular Expression Glyph Renaming' could not write preferences."
			
		except Exception, e:
			# brings macro window to front and reports error:
			Glyphs.showMacroWindow()
			print "Regular Expression Glyph Renaming Error: %s" % e

RegularExpressionGlyphRenaming()