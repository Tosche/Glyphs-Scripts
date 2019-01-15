#MenuTitle: Search Glyph In Class Features
# -*- coding: utf-8 -*-
__doc__="""
Create effect for selected glyphs.
"""

import vanilla
import GlyphsApp

class SearchGlyphInClassFeatures( object ):
	def __init__( self ):
		# Window 'self.w':
		edY = 22
		txY = 17
		sp = 10
		btnX = 100
		btnY = 22
		windowWidth  = 300
		windowHeight = sp*5+edY*2+edY+btnY+sp
		# windowWidthResize  = 100 # user can resize width by this value
		# windowHeightResize = 0   # user can resize height by this value
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Search Glyph In Class Features", # window title
			# minSize = ( windowWidth, windowHeight ), # minimum size (for resizing)
			# maxSize = ( windowWidth, windowHeight ), # maximum size (for resizing)
			autosaveName = "com.Tosche.SearchGlyphInClassFeatures.mainwindow" # stores last window position and size
		)
		
		listOfOptions = [ "Check which alternates are unused", "Check if/where the selected glyph is used", "Same as the above, but by name" ]
		self.w.radioButtons = vanilla.RadioGroup( (sp, sp, -sp, edY*len(listOfOptions) ), listOfOptions, sizeStyle = 'regular', callback=self.radio )
		self.w.edit_1 = vanilla.EditText( (sp+20, sp*1.5+edY*len(listOfOptions), -sp, edY), "", sizeStyle = 'regular')
		
		# Run Button:
		self.w.runButton = vanilla.Button((-sp-btnX, sp*5+edY*2+edY, -sp, btnY), "Check", sizeStyle='regular', callback=self.Search )
		self.w.setDefaultButton( self.w.runButton )
				
		# Open window and focus on it:
		self.w.radioButtons.set( 0 )
		self.w.edit_1.enable(False)
		self.w.open()
		self.w.makeKey()

	def radio( self, sender ):
		if sender.get() == 2:
			self.w.edit_1.enable(True)
		else:
			self.w.edit_1.enable(False)

	def showMacro(self, theText):
		Glyphs.clearLog()
		print theText
		Glyphs.showMacroWindow()

	def Search( self, sender ):
		try:
			f = Glyphs.font # frontmost font
			option = self.w.radioButtons.get()
			if option == 0: # check all glyphs
				unusedGlyphs = []
				for g in f.glyphs:
					used = False
					if "." in g.name:
						for cla in f.classes:
							if g.name in cla.code:
								used = True
								break
						for fea in f.features:
							if g.name in fea.code:
								used = True
								break
						if used == False:
							unusedGlyphs.append(g.name)
				if len(unusedGlyphs) > 0:
					self.showMacro("The following alternate glyphs are not used in any OpenType classes or features:\n"+"\n".join([g for g in unusedGlyphs]) )
				else:
					self.showMacro("All alternates are being used!")

			else:
				proceed = False
				if option == 1:
					if len(f.selectedLayers) != 0:
						proceed = True
						gname = f.selectedLayers[0].parent.name # active layers of currently selected glyphs
					else:
						Glyphs.showAlert_message_OKButton_("SEARCH ERROR", "Nothing is selected.", "OK")
				else:
					gname = self.w.edit_1.get()
					if f.glyphs[gname]:
						proceed = True
					else:
						Glyphs.showAlert_message_OKButton_("SEARCH ERROR", "There is no glyph with that name.", "OK")

				if proceed:
					usedFeas = []
					for cla in f.classes:
						if gname in cla.code:
							usedFeas.append("@"+cla.name)
					for fea in f.features:
						if gname in fea.code:
							usedFeas.append(fea.name)

					if len(usedFeas) != 0:
						self.showMacro("The glyph is used in the follwing classes and features:\n"+"\n".join([fea for fea in usedFeas]))
					else:
						self.showMacro("The glyph is not being used anywhere!")


		except Exception, e:
			# brings macro window to front and reports error:
			Glyphs.showMacroWindow()
			print "Search Glyph In Class Features Error: %s" % e

SearchGlyphInClassFeatures()