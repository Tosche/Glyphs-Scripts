#MenuTitle: Analyse Manuscript
# -*- coding: utf-8 -*-
__doc__="""
(GUI) Calculates the minimal character set required for the pasted text.
Ideal for starting a font for specific text (e.g. book).
"""

import vanilla
import GlyphsApp

class AnalyseManuscript( object ):
	def __init__( self ):
		# Window 'self.w':
		edY = 200
		txY  = 14
		spX = 10
		spY = 5
		btnX = 260
		btnY = 20
		windowWidth  = 350
		windowHeight = edY*2+spY*6+txY*2+btnY+14
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Analyse Manuscript", # window title
			autosaveName = "com.Tosche.AnalyseManuscript.mainwindow" # stores last window position and size
		)
		
		# UI elements:
		self.w.text1 = vanilla.TextBox((spX, spY, -spX, txY), 'Paste your text below...', sizeStyle='small')
		self.w.dump = vanilla.TextEditor( (spX, spY*2+txY, -spX, edY), "", callback=self.updateChar)
		self.w.text2 = vanilla.TextBox((spX, spY*3+txY+edY, -spX, txY), "0 Unicode characters", sizeStyle='small')
		self.w.chars = vanilla.TextEditor( (spX, spY*4+txY*2+edY, -spX, edY), "", readOnly=True)
		self.w.chars._textView.setFont_( NSFont.fontWithName_size_("Menlo", 12) )
		self.w.dump._textView.setAutomaticSpellingCorrectionEnabled_(False)
		self.w.dump._textView.setAutomaticTextReplacementEnabled_(False)
		self.w.dump._textView.setContinuousSpellCheckingEnabled_(False)
		self.w.dump._textView.setGrammarCheckingEnabled_(False)

		# Run Button:
		self.w.runButton = vanilla.Button((-btnX-spX, -btnY-spY-7, -spX, -spY-7), "Add missing characters to the Font", sizeStyle='regular', callback=self.AnalyseManuscriptMain )
		self.w.setDefaultButton( self.w.runButton )
		
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()
	
	def updateChar( self, sender ):
		try:
			cleanUpDict = dict.fromkeys(range(32))
			cleanStr = self.w.dump.get().translate(cleanUpDict)
			charList = sorted(set(cleanStr))
			niceNameList = [Glyphs.niceGlyphName(char) for char in charList]
			if sender == self.w.dump:
				self.w.chars.set(' '.join(niceNameList))
				plural = "s" if len(niceNameList) != 1 else ""
				self.w.text2.set("%s Unicode character%s" % (len(niceNameList), plural) )
			elif sender == self.w.runButton:
				return niceNameList

		except Exception, e:
			# brings macro window to front and reports error:
			Glyphs.showMacroWindow()
			print "Analyse Manuscript Error (updateChar): %s" % e

	def AnalyseManuscriptMain( self, sender ):
		try:
			niceNameList = self.updateChar(sender)
			font = Glyphs.font
			for niceName in niceNameList:
				if not font.glyphs[niceName]:
					font.glyphs.append(GSGlyph(niceName))

		except Exception, e:
			# brings macro window to front and reports error:
			Glyphs.showMacroWindow()
			print "Analyse Manuscript Error (AnalyseManuscriptMain): %s" % e

AnalyseManuscript()