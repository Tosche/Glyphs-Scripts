#MenuTitle: Report Metric Keys...
# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
__doc__ = """
(GUI) Reports possibly wrong keys. It reports non-existent glyphs in the keys, glyphs using different keys in each layer, and nested keys. Vanilla required.
"""

import vanilla
from GlyphsApp import Glyphs
import re
from collections import namedtuple
nestReturn = namedtuple("nestReturn", ["type", "key", "cleanKey"])
thisFont = Glyphs.font


class ReportMetricKeys(object):
	def __init__(self):
		# Window 'self.w':
		left = 14
		top = 14
		leading = 36
		textW = 220
		textH = 20
		xSpace = 10
		buttonW = 100
		buttonTop = top - 5
		buttonH = 30
		windowWidth = left + textW + xSpace + buttonW + left
		windowHeight = top + leading + leading + leading
		self.w = vanilla.FloatingWindow(
			(windowWidth, windowHeight),  # default window size
			"Report Metric Keys",  # window title
		)

		# UI elements:
		self.w.textInvalid = vanilla.TextBox((left, top, textW, textH), "Invalid glyphs in sidebearing keys", sizeStyle='regular')
		self.w.textDifferent = vanilla.TextBox((left, top + leading, textW, textH), "Different keys in each master", sizeStyle='regular')
		self.w.textNesting = vanilla.TextBox((left, top + leading + leading, textW, textH), "Nested sidebearing keys", sizeStyle='regular')

		# Run Button:
		self.w.reportInvalid = vanilla.Button((left + textW + xSpace, buttonTop, buttonW, buttonH), "Report", sizeStyle='regular', callback=self.reportInvalid)
		self.w.reportDifference = vanilla.Button((left + textW + xSpace, buttonTop + leading, buttonW, buttonH), "Report", sizeStyle='regular', callback=self.reportDifference)
		self.w.reportNest = vanilla.Button((left + textW + xSpace, buttonTop + leading + leading, buttonW, buttonH), "Report", sizeStyle='regular', callback=self.reportNest)

		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()

	def reportInvalid(self, sender):
		#thisFont = Glyphs.font

		def keyCleaner(keyValue):
			newValue = re.sub("=", "", keyValue)
			newValue = re.sub(" .*", "", newValue)
			newValue = re.sub(r"\|", "", newValue)
			newValue = re.sub(r"[+\-\*/]\d.*", "", newValue)
			return newValue
		Glyphs.clearLog()
		thisFont.disableUpdateInterface()

		print('Following glyphs use non-existent glyphs as their metric keys.\nPlease fix it manually, or use "Find and Replace in Metric Keys" script by https://github.com/mekkablue/Glyphs-Scripts\n')
		print("\nLeft Sidebearing\n")
		try:
			for thisGlyph in thisFont.glyphs:
				for thisLayer in thisGlyph.layers:
					thisLayerKeyL = thisLayer.leftMetricsKeyUI()
					if thisLayerKeyL[0].isdigit() or "-" in thisLayerKeyL[0]:
						pass
					elif re.match("auto", thisLayerKeyL):
						pass
					else:
						cleanKeyNameL = keyCleaner(thisLayerKeyL)
						if not thisFont.glyphs[cleanKeyNameL]:
							print("%s in %s: %s" % (thisGlyph.name, thisLayer.name, cleanKeyNameL))

			print("\nRight Sidebearing\n")
			for thisGlyph in thisFont.glyphs:
				for thisLayer in thisGlyph.layers:
					thisLayerKeyR = thisLayer.rightMetricsKeyUI()
					if thisLayerKeyR[0].isdigit() or "-" in thisLayerKeyR[0]:
						pass
					elif re.match("auto", thisLayerKeyR):
						pass
					else:
						cleanKeyNameR = keyCleaner(thisLayerKeyR)
						if not thisFont.glyphs[cleanKeyNameR]:
							print("%s in %s: %s" % (thisGlyph.name, thisLayer.name, cleanKeyNameR))

			print("\nWidth\n")
			for thisGlyph in thisFont.glyphs:
				for thisLayer in thisGlyph.layers:
					thisLayerKeyW = thisLayer.widthMetricsKeyUI()
					if thisLayerKeyW[0].isdigit() or "-" in thisLayerKeyW[0]:
						pass
					elif re.match("auto", thisLayerKeyW):
						pass
					else:
						cleanKeyNameW = keyCleaner(thisLayerKeyW)
						if not thisFont.glyphs[cleanKeyNameW]:
							print("%s in %s: %s" % (thisGlyph.name, thisLayer.name, cleanKeyNameW))

			print("Done.")
		except Exception as e:
			print("reportInvalid error", e)

		thisFont.enableUpdateInterface()
		Glyphs.showMacroWindow()

	def reportDifference(self, sender):
		#thisFont = Glyphs.font
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
		print("Following glyphs use different types or logics of metric key in each master. Note that this inconsistency is not necessarily a bad thing (you might have done so for a good reason).\n")
		print("\nLeft Sidebearing\n")
		try:
			for thisGlyph in thisFont.glyphs:
				thisGlyphKeyCategoryL = []
				for thisLayer in thisGlyph.layers:
					thisLayerKeyL = thisLayer.leftMetricsKeyUI()
					keyCategoryL = categoryCheck(thisLayerKeyL)
					thisGlyphKeyCategoryL.append(keyCategoryL)
				# Removing non-master layers. A bit inefficient, but I don't know how to improve yet.
				del thisGlyphKeyCategoryL[numberOfMasters:]
				if not listCheck(thisGlyphKeyCategoryL):
					print(thisGlyph.name)
					j = 0
					for i in thisGlyphKeyCategoryL:
						thisMaster = thisFont.masters[j]
						print("\t%s:\t\t%s" % (thisMaster.name, i))
						j = j + 1

			print("\nRight Sidebearing\n")
			for thisGlyph in thisFont.glyphs:
				thisGlyphKeyCategoryR = []
				for thisLayer in thisGlyph.layers:
					thisLayerKeyR = thisLayer.rightMetricsKeyUI()
					keyCategoryR = categoryCheck(thisLayerKeyR)
					thisGlyphKeyCategoryR.append(keyCategoryR)
				# Removing non-master layers. A bit inefficient, but I don't know how to improve yet.
				del thisGlyphKeyCategoryR[numberOfMasters:]
				if not listCheck(thisGlyphKeyCategoryR):
					print(thisGlyph.name)
					j = 0
					for i in thisGlyphKeyCategoryR:
						thisMaster = thisFont.masters[j]
						print("\t%s:\t\t%s" % (thisMaster.name, i))
						j = j + 1

			print("\nWidth\n")
			for thisGlyph in thisFont.glyphs:
				thisGlyphKeyCategoryW = []
				for thisLayer in thisGlyph.layers:
					thisLayerKeyW = thisLayer.widthMetricsKeyUI()
					keyCategoryW = categoryCheck(thisLayerKeyW)
					thisGlyphKeyCategoryW.append(keyCategoryW)
				# Removing non-master layers. A bit inefficient, but I don't know how to improve yet.
				del thisGlyphKeyCategoryW[numberOfMasters:]
				if not listCheck(thisGlyphKeyCategoryW):
					print(thisGlyph.name)
					j = 0
					for i in thisGlyphKeyCategoryW:
						thisMaster = thisFont.masters[j]
						print("\t%s:\t\t%s" % (thisMaster.name, i))
						j = j + 1

			print("Done.")
		except Exception as e:
			print("reportDifference error", e)
		thisFont.enableUpdateInterface()
		Glyphs.showMacroWindow()

	def reportNest(self, sender):
		try:
			# numberOfMasters = len(thisFont.masters)

			def nestCheck(targetGlyphName, side):
				calc = ["|", "+", "*", "/", "-1", "-2", "-3", "-4", "-5", "-6", "-7", "-8", "-9"]
				# Sees if the glyphName exists in the font
				thisFontMaster = thisFont.selectedFontMaster
				if thisFont.glyphs[targetGlyphName]:
					# If exists, gets the left key of targetGlyph of the same layer
					thisGlyph = thisFont.glyphs[targetGlyphName]
					thisLayer = thisGlyph.layers[thisFontMaster.id]
					if side == "left":
						targetLayerKey = thisLayer.leftMetricsKeyUI()
					elif side == "right":
						targetLayerKey = thisLayer.rightMetricsKeyUI()
					else:
						targetLayerKey = thisLayer.widthMetricsKeyUI()
					# plain number
					if targetLayerKey[0].isdigit() or "-" in targetLayerKey[0]:
						return nestReturn("stop", targetLayerKey, 0)
					elif "auto" in targetLayerKey and side == "left":
						firstComponent = thisLayer.components[0]
						return nestReturn("care", firstComponent.componentName, firstComponent.componentName)
					elif "auto" in targetLayerKey and side == "right":
						allComponents = thisLayer.components
						numOfComponents = len(allComponents)
						lastComponent = allComponents[numOfComponents - 1]
						lastComponentName = lastComponent.componentName
						lastComponentGlyph = thisFont.glyphs[lastComponentName]
						while lastComponentGlyph.category != "Letter":
							numOfComponents = numOfComponents - 1
							lastComponent = allComponents[numOfComponents]
							lastComponentName = lastComponent.componentName
							lastComponentGlyph = thisFont.glyphs[lastComponentName]
						return nestReturn("care", lastComponentName, lastComponentName)
					# Single, calculation, or absent
					else:
						targetLayerKey = re.sub("=", "", targetLayerKey)
						targetLayerKey = re.sub(" .*", "", targetLayerKey)
						if thisFont.glyphs[targetLayerKey]:
							return nestReturn("care", targetLayerKey, targetLayerKey)
						elif any([x in targetLayerKey for x in calc]):
							clean = re.sub(r"[\*+-/].*", "", targetLayerKey)
							clean = re.sub(r"\|", "", clean)
							printString = targetLayerKey + " (Calculation)"
							return nestReturn("care", printString, clean)
						# If keyed glyph is absent
						else:
							return nestReturn("not", targetLayerKey, 0)

			# Checks if a given layer has a metrics key of a glyph that has another key. Checks the glyph once and returns its name.
			thisFont.disableUpdateInterface()
			Glyphs.clearLog()

			print("Following glyphs has at least one nesting of sidebearing keys in the current layer (it doesn't check all layers). Nesting should be avoided as much as possible, because Update Metrics command does not go all the way to the origin of the nest, and you have to update as many times as its depth. To fix this, it's advisable to use the last glyph that shows up in each nest.\n\nNested calculation, however, cannot be simplified when different operator types are involved (i.e. when [+-] and [*/] are mixed in the nest), so you might have to change it depending on the situation, or leave it and don't forget to update metrics several times.\n")
			print("\nLeft Sidebearing\n")
			for thisGlyph in thisFont.glyphs:
				thisGlyphKeyResultL = nestCheck(thisGlyph.name, "left")
				if thisGlyphKeyResultL[0] == "care" and "Component" not in thisGlyphKeyResultL[1]:
					resultL = nestCheck(thisGlyphKeyResultL[2], "left")
					if resultL[0] == "care":
						print(thisGlyph.name)
						indent = "  > "
						print(indent + thisGlyphKeyResultL[1])
						indent += "> "
						print(indent + resultL[1])
						resultL = nestCheck(resultL[2], "left")
						if resultL[0] == "not":
							print("%s%s (does not exist)" % (indent, resultL[1]))
						while resultL[0] == "care":
							indent += "> "
							print("%s%s" % (indent, resultL[1]))
							resultL = nestCheck(resultL[2], "left")
							if resultL[0] == "not":
								print("%s%s (does not exist)" % (indent, resultL[1]))
								break
							if len(indent) >= 12:
								print("  The reporter gave up. You probably have a loop.")
								break

			print("\nRight Sidebearing\n")
			for thisGlyph in thisFont.glyphs:
				thisGlyphKeyResultR = nestCheck(thisGlyph.name, "right")
				if thisGlyphKeyResultR[0] == "care" and "Component" not in thisGlyphKeyResultR[1]:
					resultR = nestCheck(thisGlyphKeyResultR[2], "right")
					if resultR[0] == "care":
						print(thisGlyph.name)
						indent = "  > "
						print(indent + thisGlyphKeyResultR[1])
						indent += "> "
						print(indent + resultR[1])
						resultR = nestCheck(resultR[2], "right")
						if resultR[0] == "not":
							print("%s%s (does not exist)" % (indent, resultR[1]))
						while resultR[0] == "care":
							indent += "> "
							print("%s%s" % (indent, resultR[1]))
							resultR = nestCheck(resultR[2], "right")
							if resultR[0] == "not":
								print("%s%s (does not exist)" % (indent, resultR[1]))
								break
							if len(indent) >= 12:
								print("  The reporter gave up. You probably have a loop.")
								break

			print("\nWidth\n")
			for thisGlyph in thisFont.glyphs:
				thisGlyphKeyResultW = nestCheck(thisGlyph.name, "width")
				if thisGlyphKeyResultW[0] == "care" and "Component" not in thisGlyphKeyResultW[1]:
					resultW = nestCheck(thisGlyphKeyResultW[2], "width")
					if resultW[0] == "care":
						print(thisGlyph.name)
						indent = "  > "
						print(indent + thisGlyphKeyResultW[1])
						indent += "> "
						print(indent + resultW[1])
						resultW = nestCheck(resultW[2], "width")
						if resultW[0] == "not":
							print("%s%s (does not exist)" % (indent, resultW[1]))
						while resultW[0] == "care":
							indent += "> "
							print("%s%s" % (indent, resultW[1]))
							resultW = nestCheck(resultW[2], "width")
							if resultW[0] == "not":
								print("%s%s (does not exist)" % (indent, resultW[1]))
								break
							if len(indent) >= 12:
								print("  The reporter gave up. You probably have a loop.")
								break
		except Exception as e:
			print("reportNest error", e)

		Glyphs.showMacroWindow()


ReportMetricKeys()
