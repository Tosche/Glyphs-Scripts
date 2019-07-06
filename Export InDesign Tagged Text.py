#MenuTitle: Export InDesign Tagged Text with All Glyphs...
# -*- coding: utf-8 -*-
__doc__="""
Saves InDesign tagged text file that contains all glyphs for typesetting a specimen, using glyph ID. This is a better solution than generating ss20 feature.
"""

import GlyphsApp
import os.path
import vanilla
import subprocess

class ExportInDesignTaggedText( object ):
	def __init__( self ):
		# Window 'self.w':
		edY = 22
		sp = 10
		btnX = 80
		btnY = 22
		windowWidth  = 300
		windowHeight = 340
		windowWidthResize  = 100 # user can resize width by this value
		windowHeightResize = 0   # user can resize height by this value
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Export InDesign Tagged Text", # window title
			autosaveName = "com.Tosche.ExportInDesignTaggedText.mainwindow" # stores last window position and size
		)
		f = Glyphs.font
		try:
			os.path.dirname(f.filepath)
			location = "the same folder as the Glyphs source file"
		except:
			location = "Documents folder"

		instruction = u'''Instruction:

1. Export button will save the text file(s) in %s (overwites existing ones).

2. You also need to generate the font and make it available in InDesign.

3. In InDesign, have a document open. Go to "File > Place", choose the exported text file, and place it somewhere in the document. Et voilà!''' % location

		instancePopupItems = []
		for ins in f.instances:
			familyName = ins.customParameters["familyName"] if ins.customParameters["familyName"] else f.familyName
			instancePopupItems.append( "%s %s" % (familyName, ins.name) )
		instancePopupItems += ["All instances"]

		# UI elements:
		self.w.instancesText = vanilla.TextBox( (sp, sp+5, 75, edY), "Export for", sizeStyle='small' )
		self.w.instancesList = vanilla.PopUpButton( (sp*2+55, sp, -sp, edY), instancePopupItems, sizeStyle='small' )
		self.w.tabCheck = vanilla.CheckBox( (sp, sp*2+edY*1, -sp, edY), "Tab-separated", sizeStyle = 'small', callback = self.checkBoxes)
		self.w.unicodeCheck = vanilla.CheckBox( (sp, sp*2+edY*2, -sp, edY), "Unicode characters first, un-encoded later", sizeStyle = 'small', callback = self.checkBoxes)
		self.w.breakCheck = vanilla.CheckBox( (sp, sp*2+edY*3, -sp, edY), "Break up the unicode part by category", sizeStyle = 'small')
		self.w.runButton = vanilla.Button((sp, sp*3+edY*4, -sp, btnY), "Export", sizeStyle='regular', callback=self.ExportInDesignTaggedTextMain )
		self.w.setDefaultButton( self.w.runButton )
		self.w.border = vanilla.HorizontalLine((0, sp*4+edY*5, -0, 1))
		self.w.instructionText = vanilla.TextBox( (sp, sp*5+edY*5, -sp, 200), instruction, sizeStyle='small' )
		
		# Load Settings:
		if not self.LoadPreferences():
			print "Note: 'Export InDesign Tagged Text.py' could not load preferences. Will resort to defaults"
		
		self.checkBoxes(self.w.unicodeCheck)

		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()
		
	def SavePreferences( self, sender ):
		try:
			Glyphs.defaults["com.Tosche.ExportInDesignTaggedText.tabCheck"] = self.w.tabCheck.get()
			Glyphs.defaults["com.Tosche.ExportInDesignTaggedText.unicodeCheck"] = self.w.unicodeCheck.get()
			Glyphs.defaults["com.Tosche.ExportInDesignTaggedText.breakCheck"] = self.w.breakCheck.get()
		except:
			return False
			
		return True

	def LoadPreferences( self ):
		try:
			self.w.tabCheck.set( Glyphs.defaults["com.Tosche.ExportInDesignTaggedText.tabCheck"] )
			self.w.unicodeCheck.set( Glyphs.defaults["com.Tosche.ExportInDesignTaggedText.unicodeCheck"] )
			self.w.breakCheck.set( Glyphs.defaults["com.Tosche.ExportInDesignTaggedText.breakCheck"] )
		except:
			return False
			
		return True

	def checkBoxes( self, sender ):
		if sender == self.w.unicodeCheck:
			if sender.get():
				self.w.breakCheck.enable(True)
			else:
				self.w.breakCheck.enable(False)
				self.w.breakCheck.set(False)
		if not self.SavePreferences( self ):
			print "Note: 'Export InDesign Tagged Text' could not write preferences."

	def ExportInDesignTaggedTextMain( self, sender ):
		try:
			f = Glyphs.font # frontmost font
			insChoice = self.w.instancesList.get()
			insList = [ins for ins in f.instances if ins.active]
			glyphCount = len([g for g in f.glyphs if g.export])

			if self.w.instancesList.getItem() != "All instances": # choose one instance if "All" is not selected
				insList = [insList[insChoice]]

			tab = "\t" if self.w.tabCheck.get() else ""

			for ins in insList:
				familyName = ins.customParameters["familyName"] if ins.customParameters["familyName"] else f.familyName
				paraStyleName = "%s %s 12pt" % (f.familyName, ins.name)

				header = '''<ASCII-MAC>
<Version:7.5><FeatureSet:InDesign-Roman><ColorTable:=<Black:COLOR:CMYK:Process:0,0,0,1>>
<DefineParaStyle:%s=<cSize:12.000000><cTypeface:%s><cFont:%s><cOTFContAlt:0>>
''' % (paraStyleName, ins.name, familyName)

				line = ""
				lineUni = ""
				if self.w.unicodeCheck.get(): # unicode + GID solutions
					line += """\n\nUnencoded Glyphs\n"""
					gPrev = None
					for g in f.glyphs:
						if g.export:

							if self.w.breakCheck.get(): # break up table by character set
								if gPrev:
									if g.category != gPrev.category:
										if g.category == "Letter" and g.script is not None:
											lineUni += "\n\n%s\n" % g.script.capitalize()
										else:
											lineUni += "\n\n%ss\n" % g.category
									elif g.category == "Letter":
										if g.script != gPrev.script:
											if g.script:
												lineUni += "\n\n%s\n" % g.script.capitalize()
											else:
												lineUni += "\n\n%s\n" % g.category
										elif g.subCategory != gPrev.subCategory:
											lineUni += "\n"
								else: # if it's the first glyph
									if g.script:
										lineUni += "<ParaStyle:%s>%s\n" % (paraStyleName, g.script.capitalize())
									else:
										lineUni += "<ParaStyle:%s>%s\n" % (paraStyleName, g.category)
								gPrev = g

							if g.unicode:
								if g.unicode not in ["0000", "000D", "003C", "003E", "005C"]: # null, CR, less, greater, backslash
									char = "<0x%s>" % g.unicode
								else: # I need to type these literally
									if g.unicode == "003C": # less
										char = "\\<"
									elif g.unicode == "003E": # greater
										char = "\\>"
									elif g.unicode == "005C": # backslash
										char = "\\\\"
								lineUni += "<ParaStyle:%s>%s%s" % (paraStyleName, char, tab) # Add unicode character
							else: # non-unicode glyph
								line += "<ParaStyle:%s><cSpecialGlyph:%s><0xFFFD>%s" % (paraStyleName, g.glyphId(), tab) # Add GID character

				else: # entirely GID
					for g in f.glyphs:
						if g.export:
							line += "<ParaStyle:%s><cSpecialGlyph:%s><0xFFFD>%s" % (paraStyleName, g.glyphId(), tab)
				try:
					dirPath = os.path.dirname(f.filepath)
				except:
					dirPath = os.path.abspath(os.path.expanduser("~/") + '/Documents')
				filePath = os.path.abspath(dirPath+"/InDesign Tagged Text - %s %s.txt" % (familyName, ins.name))
				with open(filePath, 'w') as thisFile:
					thisFile.write(header+lineUni+line)
					thisFile.close()

			subprocess.call(["open", "-R", filePath]) # show the tagged text in the Finder

			if not self.SavePreferences( self ):
				print "Note: 'Export InDesign Tagged Text' could not write preferences."
			
			self.w.close()
		except Exception, e:
			Glyphs.showMacroWindow()
			print "Export InDesign Tagged Text .py Error: %s" % e

ExportInDesignTaggedText()