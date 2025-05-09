#MenuTitle: Analyse Manuscript...
# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
__doc__ = """
(GUI) Calculates the minimal character set required for the pasted text.
Ideal for starting a font for specific text (e.g. book).
"""

import vanilla
from GlyphsApp import Glyphs, GSGlyph
from AppKit import NSFont, NSMenuItem


class AnalyseManuscript(object):
	def __init__(self):
		# Window 'self.w':
		edY = 200
		txY = 14
		spX = 10
		spY = 5
		btnX = 250
		btnY = 20
		windowWidth = 350
		windowHeight = edY * 2 + spY * 6 + txY * 2 + btnY + 14
		self.w = vanilla.FloatingWindow(
			(windowWidth, windowHeight),  # default window size
			"Analyse Manuscript",  # window title
			autosaveName="com.Tosche.AnalyseManuscript.mainwindow"  # stores last window position and size
		)

		# UI elements:
		self.w.text1 = vanilla.TextBox((spX, spY, -spX, txY), 'Paste your text below...', sizeStyle='small')
		self.w.dump = vanilla.TextEditor((spX, spY * 2 + txY, -spX, edY), "", callback=self.updateChar)
		self.w.text2 = vanilla.TextBox((spX, spY * 3 + txY + edY, -spX, txY), "0 Unicode characters", sizeStyle='small')
		self.w.chars = vanilla.TextEditor((spX, spY * 4 + txY * 2 + edY, -spX, edY), "", readOnly=True)
		self.w.chars._textView.setFont_(NSFont.fontWithName_size_("Menlo", 12))
		self.w.dump._textView.setAutomaticSpellingCorrectionEnabled_(False)
		self.w.dump._textView.setAutomaticTextReplacementEnabled_(False)
		self.w.dump._textView.setContinuousSpellCheckingEnabled_(False)
		self.w.dump._textView.setGrammarCheckingEnabled_(False)
		self.w.dump._textView.setAutomaticQuoteSubstitutionEnabled_(False)

		# Run Button:
		self.w.markPopup = vanilla.PopUpButton(
			(spX, -btnY - spY - 7, 70, -spY - 7),
			["Mark", "Red", "Orange", "Brown", "Yellow", "Light Green", "Dark Green", "Cyan", "Blue", "Purple", "Pink", "Light Grey", "Dark Grey"],
			callback=self.markGlyphs
		)
		self.w.runButton = vanilla.Button((-btnX - spX, -btnY - spY - 7, -spX, -spY - 7), "Add missing characters", sizeStyle='regular', callback=self.AnalyseManuscriptMain)
		self.w.setDefaultButton(self.w.runButton)

		# Open window and focus on it:
		self.w.open()
		menu = self.w.markPopup._nsObject.menu()
		menu.setAutoenablesItems_(False)
		menu.itemAtIndex_(0).setEnabled_(False)
		divider = NSMenuItem.separatorItem()
		menu.insertItem_atIndex_(divider, 1)
		self.w.makeKey()

	def updateChar(self, sender):
		try:
			# Strip off control characters
			cleanUpDict = dict.fromkeys(range(32))
			cleanStr = self.w.dump.get().translate(cleanUpDict)
			# Make unique set
			charList = sorted(set(cleanStr))
			niceNameList = [Glyphs.niceGlyphName(char) for char in charList]
			if sender == self.w.dump:
				self.w.chars.set(' '.join(niceNameList))
				plural = "s" if len(niceNameList) != 1 else ""
				self.w.text2.set("%s Unicode character%s" % (len(niceNameList), plural))
			elif sender == self.w.runButton or sender == self.w.markPopup:
				return niceNameList

		except Exception as e:
			Glyphs.showMacroWindow()
			print("Analyse Manuscript Error (updateChar): %s" % e)

	def markGlyphs(self, sender):
		try:
			codeList = [Glyphs.glyphInfoForName(a).unicode for a in self.updateChar(sender)]
			#niceNameList = self.updateChar(sender)
			font = Glyphs.font
			colour = self.w.markPopup.get() - 2
			self.w.markPopup.set(0)
			for g in font.glyphs:
				if g.unicode in codeList:
					g.color = colour
		except Exception as e:
			Glyphs.showMacroWindow()
			print("Analyse Manuscript Error (markGlyphs): %s" % e)

	def AnalyseManuscriptMain(self, sender):
		try:
			niceNameList = self.updateChar(sender)
			font = Glyphs.font
			for niceName in niceNameList:
				if not font.glyphs[niceName]:
					font.glyphs.append(GSGlyph(niceName))

		except Exception as e:
			Glyphs.showMacroWindow()
			print("Analyse Manuscript Error (AnalyseManuscriptMain): %s" % e)


AnalyseManuscript()
