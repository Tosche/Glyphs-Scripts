#MenuTitle: Check & Fix Metric keys
# -*- coding: utf-8 -*-
__doc__="""
(GUI) Reports possibly wrong keys and cleans up some, if you wish. It checks non-existent glyphs in the keys, glyphs using different keys in each layer, and nested keys.
"""

import vanilla
import GlyphsApp
import re

# Needs to report different keys in the same glyph.
# Needs to report invalid keys.
# Needs to report nesting.

thisFont = Glyphs.font
numberOfMasters = len(thisFont.masters)

class CheckAndFixMetricKeys( object ):
	def __init__( self ):
		# Window 'self.w':
		left = 14
		top = 14
		leading = 36
		textW = 220
		textH = 20
		xSpace = 10
		buttonW = 100
		buttonTop = top-5
		buttonH = 30
		windowWidth  = left+textW+xSpace+buttonW+xSpace+buttonW+left
		windowHeight = top+leading+leading+leading+leading
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Check & Fix Metric Keys", # window title
			autosaveName = "com.Tosche.MetricKeyChecker.mainwindow" # stores last window position and size
		)
		
		# UI elements:
		self.w.textInvalid = vanilla.TextBox( (left, top, textW, textH), "Invalid glyphs in sidebearing keys", sizeStyle='regular' )
		self.w.textDifferent = vanilla.TextBox( (left, top+leading, textW, textH), "Different keys in each master", sizeStyle='regular' )
		self.w.textNesting = vanilla.TextBox( (left, top+leading+leading, textW, textH), "Nested sidebearing keys", sizeStyle='regular' )
		self.w.textNestUnavailable = vanilla.TextBox( (left, top+leading+leading+leading, textW, textH), "Nest Buttons are not working yet for now. Watch this space.", sizeStyle='small' )
		
		# Run Button:
		self.w.reportInvalid = vanilla.Button((left+textW+xSpace, buttonTop, buttonW, buttonH), "Report", sizeStyle='regular', callback=self.reportInvalid )
		self.w.reportDifference = vanilla.Button((left+textW+xSpace, buttonTop+leading, buttonW, buttonH), "Report", sizeStyle='regular', callback=self.reportDifference )
		self.w.reportNest = vanilla.Button((left+textW+xSpace, buttonTop+leading+leading, buttonW, buttonH), "Report", sizeStyle='regular', callback=self.reportNest )
		self.w.clearNest = vanilla.Button((left+textW+xSpace+buttonW+xSpace, buttonTop+leading+leading, buttonW, buttonH), "Clean Up", sizeStyle='regular', callback=self.clearNest )

		# Load Settings:
		if not self.LoadPreferences():
			print "Note: 'Metric Key Checker' could not load preferences. Will resort to defaults"
		
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()
		
	def SavePreferences( self, sender ):
		try:
			Glyphs.defaults["com.Tosche.MetricKeyChecker.popup_1"] = self.w.popup_1.get()
		except:
			return False
			
		return True

	def LoadPreferences( self ):
		try:
			self.w.popup_1.set( Glyphs.defaults["com.Tosche.MetricKeyChecker.popup_1"] )
		except:
			return False
			
		return True

	def reportInvalid( self, sender ):
		def keyCleaner( keyValue ):
			newValue = re.sub("=", "", keyValue)
			newValue = re.sub(" .*", "", newValue)
			newValue = re.sub("\|", "", newValue)
			newValue = re.sub("[+\-\*/]\d.*", "", newValue)
			return newValue
		Glyphs.clearLog()
		thisFont.disableUpdateInterface()

		print 'Following glyphs use non-existent glyphs as their metric keys.\nPlease fix it manually, or use "Find and Replace in Metric Keys" script by https://github.com/mekkablue/Glyphs-Scripts'
		print "\nLeft Sidebearing"
		for thisGlyph in thisFont.glyphs:
			for thisLayer in thisGlyph.layers:
				thisLayerKeyL = thisLayer.leftMetricsKey()
				if thisLayerKeyL[0].isdigit() or "-" in thisLayerKeyL[0]:
					pass
				elif re.match("auto", thisLayerKeyL):
					pass
				else:
					cleanKeyNameL = keyCleaner(thisLayerKeyL)
					if not thisFont.glyphs[ cleanKeyNameL ]:
						print "%s in %s uses: %s" % (thisGlyph.name, thisLayer.name, cleanKeyNameL)

		print "\nRight Sidebearing"
		for thisGlyph in thisFont.glyphs:
			for thisLayer in thisGlyph.layers:
				thisLayerKeyR = thisLayer.rightMetricsKey()
				if thisLayerKeyR[0].isdigit() or "-" in thisLayerKeyR[0]:
					pass
				elif re.match("auto", thisLayerKeyR):
					pass
				else:
					cleanKeyNameR = keyCleaner(thisLayerKeyR)
					if not thisFont.glyphs[ cleanKeyNameR ]:
						print "%s in %s uses: %s" % (thisGlyph.name, thisLayer.name, cleanKeyNameR)
		print "Done."

		thisFont.enableUpdateInterface()
		Glyphs.showMacroWindow()

	def reportDifference( self, sender ):
		def categoryCheck(keyValue):
			if keyValue[0].isdigit() or "-" in keyValue[0]:
				return "Numerical value"
			elif re.match("auto", keyValue):
				return "Auto (Component)"
			else:
				keyValue = re.sub(" .*", "", keyValue)
				return "Glyph Key (%s)" % keyValue

		def listCheck(thisList):
		   return thisList[1:] == thisList[:-1]

		thisFont.disableUpdateInterface()
		Glyphs.clearLog()
		print "Following glyphs use different types or logics of metric key in each master. Note that this inconsistency is not necessarily a bad thing (you might have done so for a good reason). Also, Glyphs sometimes thinks that auto (component inheritance) is a plain value, therefore the script lists unnecessary glyphs. If you see this, just activate all masters once and re-run it. If you see You can use my Batch Metric Key script to apply the same key to all masters.\n"
		print "\nLeft Sidebearing\n"
		for thisGlyph in thisFont.glyphs:
			thisGlyphKeyCategoryL = []
			for thisLayer in thisGlyph.layers:
				thisLayerKeyL = thisLayer.leftMetricsKey()
				keyCategoryL = categoryCheck(thisLayerKeyL)
				thisGlyphKeyCategoryL.append(keyCategoryL)
			# Removing non-master layers. A bit inefficient, but I don't know how to improve yet.
			del thisGlyphKeyCategoryL[numberOfMasters:]
			if not listCheck(thisGlyphKeyCategoryL):
				print thisGlyph.name
				j=0
				for i in thisGlyphKeyCategoryL:
					thisMaster = thisFont.masters[j]
					print "\t%s:\t\t%s" %( thisMaster.name, i)
					j = j+1

		print "\nRight Sidebearing\n"
		for thisGlyph in thisFont.glyphs:
			thisGlyphKeyCategoryR = []
			for thisLayer in thisGlyph.layers:
				thisLayerKeyR = thisLayer.rightMetricsKey()
				keyCategoryR = categoryCheck(thisLayerKeyR)
				thisGlyphKeyCategoryR.append(keyCategoryR)
			# Removing non-master layers. A bit inefficient, but I don't know how to improve yet.
			del thisGlyphKeyCategoryR[numberOfMasters:]
			if not listCheck(thisGlyphKeyCategoryR):
				print thisGlyph.name
				j=0
				for i in thisGlyphKeyCategoryR:
					thisMaster = thisFont.masters[j]
					print "\t%s:\t\t%s" %( thisMaster.name, i)
					j = j+1
		print "Done."
		thisFont.enableUpdateInterface()
		Glyphs.showMacroWindow()

	def reportNest( self, sender ):
		pass

	def clearNest( self, sender ):
		pass


CheckAndFixMetricKeys()