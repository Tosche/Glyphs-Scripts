#MenuTitle: Check & Fix Metric Keys
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
		
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()

	def reportInvalid( self, sender ):
		thisFont = Glyphs.font

		def keyCleaner( keyValue ):
			newValue = re.sub("=", "", keyValue)
			newValue = re.sub(" .*", "", newValue)
			newValue = re.sub("\|", "", newValue)
			newValue = re.sub("[+\-\*/]\d.*", "", newValue)
			return newValue
		Glyphs.clearLog()
		thisFont.disableUpdateInterface()

		print 'Following glyphs use non-existent glyphs as their metric keys.\nPlease fix it manually, or use "Find and Replace in Metric Keys" script by https://github.com/mekkablue/Glyphs-Scripts\n'
		print "\nLeft Sidebearing\n"
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
						print "%s in %s: %s" % (thisGlyph.name, thisLayer.name, cleanKeyNameL)

		print "\nRight Sidebearing\n"
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
						print "%s in %s: %s" % (thisGlyph.name, thisLayer.name, cleanKeyNameR)
		print "Done."

		thisFont.enableUpdateInterface()
		Glyphs.showMacroWindow()

	def reportDifference( self, sender ):
		thisFont = Glyphs.font
		numberOfMasters = len(thisFont.masters)
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
		print "Following glyphs use different types or logics of metric key in each master. Note that this inconsistency is not necessarily a bad thing (you might have done so for a good reason). Also, Glyphs sometimes thinks that auto (component inheritance) is a plain value, therefore the script lists unnecessary glyphs. If you see this, just activate all masters once and re-run it. You can use my Batch Metric Key script to apply the same key to all masters.\n"
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
		thisFont = Glyphs.font
		numberOfMasters = len(thisFont.masters)
		thisFontMaster = thisFont.selectedFontMaster
		# Checks if a given layer has a metrics key of a glyph that has another key. Checks the glyph once and returns its name.
		def nestHuntL( targetGlyphName ):
			# Sees if the glyphName exists in the font
			if thisFont.glyphs[ targetGlyphName ]:
				# If exists, gets the left key of targetGlyph of the same layer
				targetGlyphL = thisFont.glyphs[ targetGlyphName ]
				targetLayerL = targetGlyphL.layers[ thisFontMaster.id ]
				targetLayerKeyL = targetLayerL.leftMetricsKey()
				# If it's a plain number or calculation, returns the original glyph name
				a = ["=|", "+", "*", "/", "-1", "-2", "-3", "-4", "-5", "-6", "-7", "-8", "-9"]
				if targetLayerKeyL[0].isdigit() or "-" in targetLayerKeyL[0] or any([ x in targetLayerKeyL for x in a]):
					return targetGlyphName

				# Finds the first component and returns its name
				elif "auto" in targetLayerKeyL:
					firstComponent = targetLayerL.components[0]
					return firstComponent.componentName

				# This is a single-letter key, so clean it up
				else:
					cleanGlyphName = re.sub( "=", "", targetLayerKeyL )
					cleanGlyphName = re.sub( " .*", "", cleanGlyphName )
					return cleanGlyphName

			# If the glyph doesn't exist:
			else:
				return "The above glyph doesn't exist."

		def nestHuntR( targetGlyphName ):
			# Sees if the glyphName exists in the font
			if thisFont.glyphs[ targetGlyphName ]:
				# If exists, gets the left key of targetGlyph of the same layer
				targetGlyphR = thisFont.glyphs[ targetGlyphName ]
				targetLayerR = targetGlyphR.layers[ thisFontMaster.id ]
				targetLayerKeyR = targetLayerR.rightMetricsKey()
				# If it's a plain number or calculation, returns the original glyph name
				a = ["=|", "+", "*", "/", "-1", "-2", "-3", "-4", "-5", "-6", "-7", "-8", "-9"]
				if targetLayerKeyR[0].isdigit() or "-" in targetLayerKeyR[0] or any([ x in targetLayerKeyR for x in a]):
					return targetGlyphName

				# Finds the last "Letter" component and returns its name
				elif "auto" in targetLayerKeyR:
					allCompornents = thisLayer.components 
					numOfCompornents = len(allCompornents)
					lastCompornent = allCompornents[numOfCompornents]
					lastCompornentName = lastCompornent.componentName
					lastCompornentGlyph = thisFont.glyphs[lastCompornentName]
					while lastCompornentGlyph.category != "Letter":
						numOfCompornents = numOfCompornents-1
						lastCompornent = allCompornents[numOfCompornents]
						lastCompornentName = lastCompornent.componentName
						lastCompornentGlyph = thisFont.glyphs[lastCompornentName]
					return lastCompornentName

				# This is a single-letter key, so clean it up
				else:
					cleanGlyphName = re.sub( "=", "", targetLayerKeyR )
					cleanGlyphName = re.sub( " .*", "", cleanGlyphName )
					return cleanGlyphName

			# If the glyph doesn't exist:
			else:
				return "The above glyph doesn't exist."

		thisFont.disableUpdateInterface()
		Glyphs.clearLog()

		print "Following glyphs has at least one nesting of sidebearing keys in the current layer (it doesn't check all layers). Nesting should be avoided as much as possible, because Update Metrics command only checks the key once, and you have to update as many times as you nest. Nested calculation, however, cannot be easily simplified, so you might have to change it or leave it and don't forget to update metrics several times.\n\nTo fix this, click Clean Up button of this script (again, it doesn't remove calculation).\n"
		print "\nLeft Sidebearing\n"
		for thisGlyph in thisFont.glyphs:
			thisGlyphNameL = thisGlyph.name
			thisGlyphLayerL = thisGlyph.layers[ thisFontMaster.id ]
			thisGlyphKeyL = thisGlyphLayerL.leftMetricsKey()
			if thisGlyphKeyL[0].isdigit() or "-" in thisGlyphKeyL[0] or re.match("auto", thisGlyphKeyL):
				pass
			else:
				dummyOldL = nestHuntL(thisGlyphNameL)
				dummyNewL = nestHuntL(dummyOldL)
				if dummyOldL != dummyNewL:
					print thisGlyphNameL
					indent = "\t> "
					print indent+dummyOldL
					indent = indent + "> "
					print indent+dummyNewL
					while dummyOldL != dummyNewL:
						dummyOldL = nestHuntL(dummyNewL)
						if dummyOldL != dummyNewL:
							indent = indent + "> "
							print indent + dummyOldL
							indent = indent + "> "
						dummyNewL = nestHuntL(dummyOldL)
						if dummyOldL != dummyNewL:
							print indent + dummyNewL
						if len(indent) >= 10:
							print indent + "> The reporter gave up. You probably have a loop. Naughty you."
							break

		print "\nRight Sidebearing\n"
		for thisGlyph in thisFont.glyphs:
			thisGlyphNameR = thisGlyph.name
			thisGlyphLayerR = thisGlyph.layers[ thisFontMaster.id ]
			thisGlyphKeyR = thisGlyphLayerR.rightMetricsKey()
			if thisGlyphKeyR[0].isdigit() or "-" in thisGlyphKeyR[0] or re.match("auto", thisGlyphKeyR):
				pass
			else:
				dummyOldR = nestHuntR(thisGlyphNameR)
				dummyNewR = nestHuntR(dummyOldR)
				if dummyOldR != dummyNewR:
					print thisGlyphNameR
					indent = "\t> "
					print indent+dummyOldR
					indent = indent + "> "
					print indent+dummyNewR
					while dummyOldR != dummyNewR:
						dummyOldR = nestHuntR(dummyNewR)
						if dummyOldR != dummyNewR:
							indent = indent + "> "
							print indent + dummyOldR
							indent = indent + "> "
						dummyNewR = nestHuntR(dummyOldR)
						if dummyOldR != dummyNewR:
							print indent + dummyNewR
						if len(indent) >= 10:
							print indent + "> The reporter gave up. You probably have a loop. Naughty you."
							break
		Glyphs.showMacroWindow()
	def clearNest( self, sender ):
		pass


CheckAndFixMetricKeys()