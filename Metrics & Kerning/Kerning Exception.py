#MenuTitle: Kerning Exception...
# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
__doc__ = """
(GUI) Makes an kerning exception of the current pair. Note: Current glyph is considered the RIGHT side of the glyph.
"""

import vanilla
from GlyphsApp import Glyphs


class KerningException(object):
	def __init__(self):
		# Window 'self.w':
		spaceX = 10
		spaceY = 10
		buttonSizeX = 220
		buttonSizeY = 20
		windowWidth = spaceX * 2 + buttonSizeX
		windowHeight = spaceY * 5 + buttonSizeY * 4
		self.w = vanilla.FloatingWindow(
			(windowWidth, windowHeight),  # default window size
			"Kerning Exception",  # window title
			autosaveName="com.Tosche.Kerning Exception.mainwindow"  # stores last window position and size
		)


		# Run Button:
		self.w.runButton1 = vanilla.Button((spaceX, spaceY, buttonSizeX, buttonSizeY), "1 🔒 🔓 Unlock Right (Ta→Tà)", sizeStyle='regular', callback=self.KerningExceptionMain)
		self.w.runButton2 = vanilla.Button((spaceX, spaceY * 2 + buttonSizeY, buttonSizeX, buttonSizeY), "2 🔓 🔒 Unlock Left (aT→áT)", sizeStyle='regular', callback=self.KerningExceptionMain)
		self.w.runButton3 = vanilla.Button((spaceX, spaceY * 3 + buttonSizeY * 2, buttonSizeX, buttonSizeY), "3 🔓 🔓 Unlock Both ", sizeStyle='regular', callback=self.KerningExceptionMain)
		self.w.runButton4 = vanilla.Button((spaceX, spaceY * 4 + buttonSizeY * 3, buttonSizeX, buttonSizeY), "4 🔒 🔒 Lock Both ", sizeStyle='regular', callback=self.KerningExceptionMain)

		# Assign keyboard shortcuts
		self.w.runButton1.bind('1', [])
		self.w.runButton2.bind('2', [])
		self.w.runButton3.bind('3', [])
		self.w.runButton4.bind('4', [])

		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()

	def KerningExceptionMain(self, sender):
		try:
			def validLayer(layer):
				if (layer == None) or (layer.name == None):
					return False
				else:
					return True

			f = Glyphs.font  # frontmost font
			View = Glyphs.currentDocument.windowController().activeEditViewController().graphicView()
			activeLayer = View.activeLayer()
			prevLayer = View.cachedGlyphAtIndex_(View.activeIndex() - 1)
			mID = activeLayer.associatedMasterId

			prevGlyph = prevLayer.parent
			activeGlyph = activeLayer.parent
			prevGroup = "@MMK_L_" + prevLayer.parent.rightKerningGroup
			activeGroup = "@MMK_R_" + activeLayer.parent.leftKerningGroup
			# value1, value2, value3, value4 = None, None, None, None

			# if Glyphs.versionNumber >= 3.0:
			# # kerning exception functions have been removed, so I need to check on my own
			# # check the current state of kerning
			# # maybe not necessary for now
			# 	try:
			# 		value1 = f.kerningForPair(mID, prevGroup, activeLayer)
			# 	except:
			# 		pass
			# 	try:
			# 		value2 = f.kerningForPair(m.id, prevLayer, activeGroup)
			# 	except:
			# 		pass
			# 	try:
			# 		value3 = f.kerningForPair(m.id, prevLayer, activeLayer)
			# 	except:
			# 		pass
			# 	try:
			# 		value4 = f.kerningForPair(m.id, prevGroup, activeGroup)
			# 	except:
			# 		pass

			if validLayer(activeLayer) and validLayer(prevLayer):
				if sender == self.w.runButton1:  # Unlock Right
					if Glyphs.versionNumber >= 3.0:
						print(mID, prevGroup, activeGroup)
						f.setKerningForPair(mID, prevGroup, activeGlyph.name, 0)
					else:
						activeLayer.setLeftKerningExeption_forLayer_(True, prevLayer)
						prevLayer.setRightKerningExeption_forLayer_(False, activeLayer)
				elif sender == self.w.runButton2:  # Unlock Left
					if Glyphs.versionNumber >= 3.0:
						f.setKerningForPair(mID, prevGlyph.name, activeGroup, 0)
					else:
						activeLayer.setLeftKerningExeption_forLayer_(False, prevLayer)
						prevLayer.setRightKerningExeption_forLayer_(True, activeLayer)
				elif sender == self.w.runButton3:  # Unock Both
					if Glyphs.versionNumber >= 3.0:
						f.setKerningForPair(mID, prevGlyph.name, activeGlyph.name, 0)
					else:
						activeLayer.setLeftKerningExeption_forLayer_(True, prevLayer)
						prevLayer.setRightKerningExeption_forLayer_(True, activeLayer)
				else:  # Lock Both
					if Glyphs.versionNumber >= 3.0:
						# Not sure which kern state, so try all
						f.removeKerningForPair(mID, prevGroup, activeGlyph.name)
						f.removeKerningForPair(mID, prevGlyph.name, activeGroup)
						f.removeKerningForPair(mID, prevGlyph.name, activeGlyph.name)
					else:
						activeLayer.setLeftKerningExeption_forLayer_(False, prevLayer)
						prevLayer.setRightKerningExeption_forLayer_(False, activeLayer)
			else:
				if Glyphs.versionNumber >= 3.0:
					Glyphs.showNotification('Kerning Exception Error', 'Text cursor should be placed between two glyphs.')
				else:
					Glyphs.displayDialog('Text cursor should be placed between two glyphs.')

			self.w.close()  # delete if you want window to stay open
		except Exception as e:
			# brings macro window to front and reports error:
			Glyphs.showMacroWindow()
			print("Kerning Exception Error: %s" % e)


KerningException()
