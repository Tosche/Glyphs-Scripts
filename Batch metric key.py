#MenuTitle: Batch metric key
# -*- coding: utf-8 -*-
__doc__="""
Applies the specified logic of metrics key to the selected glyphs.
"""

# User can customise presets here. Don't forget to add the comma at the end! (except when it's the last one)
presets = [
	"@base (No case change)",
	"@Base (Change to Upper)",
	"=@Base*0.9 (90% of Uppercase variant. Small cap intended.)",
	"=@base*0.7 (70% of the base letter. Super/subscript intended.)",
	"=@base.lf*0.7 (70% of .lf variant. Super/subscript from proportional lining figure intended.)"
	]

import vanilla
import GlyphsApp
import re

class BatchMetricKey( object ):
	def __init__( self ):
		windowWidth  = 400
		windowHeight = 280
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"ALL YOUR @BASE BELONG TO US.", # window title
			autosaveName = "com.Tosche.BatchMetricKey.mainwindow" # stores last window position and size
		)

		# UI elements:
		self.w.presetText = vanilla.TextBox( ( 12, 13, 55, 17), "Presets:", sizeStyle='regular' )
		self.w.presetPopup = vanilla.PopUpButton( (14+58, 13, -15, 17), [str(x) for x in presets], callback=self.setField, sizeStyle='regular' )
		self.w.keyTextField = vanilla.EditText( (14, 45, -15, 22), re.sub(" .*", "", presets[0]), sizeStyle = 'regular')
		self.w.setToText = vanilla.TextBox( ( 12, 78, 50, 17), "Set to:", sizeStyle='regular' )
		self.w.applyL = vanilla.CheckBox( ( 12+50, 78, 50, 22), "Left", value=True, sizeStyle='regular')
		self.w.applyR = vanilla.CheckBox( ( 12+50+50, 78, 56, 22), "Right", value=True, sizeStyle='regular')
		self.w.avoidNest = vanilla.CheckBox( ( 275, 78, 115, 22), "Adoid Nesting", value=True, sizeStyle='regular')
		self.w.radioQText = vanilla.TextBox( ( 12, 115, 100, 17), "If there is Q:", sizeStyle='regular' )
		self.w.radioQ = vanilla.RadioGroup( (100, 115, 350, 19), ["Use width of O (no key)", "Use RSB of Q"], sizeStyle='regular', isVertical=False)
		self.w.radioQ.set(0)
		self.w.line = HorizontalLine((12, 190, -10, 1))
		self.w.explain = vanilla.TextBox( ( 12, 200, 350, 80), "@base is a glyph without suffix of the selected glyph.\n@base of a.smcp is a\n@Base of hsuperior is H\n@base.smcp of one.numr is one.smcp", sizeStyle='regular' )
		# Run Button:
		self.w.setButton = vanilla.Button((290, 145, 90, 34), "Set", sizeStyle='regular', callback=self.BatchMetricKeyMain )
		self.w.setDefaultButton( self.w.setButton )
		
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()

	def setField( self, sender ):
		chosenKey = presets[self.w.presetPopup.get()]
		setFieldKey = re.sub(" .*", "", chosenKey)
		self.w.keyTextField.set(setFieldKey)

	def BatchMetricKeyMain( self, sender ):
		thisFont = Glyphs.font
		thisFontMaster = thisFont.selectedFontMaster
		listOfSelectedLayers = thisFont.selectedLayers
		fieldKey = self.w.keyTextField.get()
		flatFieldKey = re.sub("@Base", "@base", fieldKey)

		if "@base" in fieldKey or "@Base" in flatFieldKey:
			# Checks if a given layer has a metrics key of a glyph that has another key. Checks the glyph once and returns its name.
			def nestHuntL( targetGlyphName ):
				# Sees if the glyphName exists in the font
				if thisFont.glyphs[ targetGlyphName ]:
					# If exists, gets the left key of targetGlyph of the same layer
					targetGlyphL = thisFont.glyphs[ targetGlyphName ]
					targetLayerL = targetGlyphL.layers[ thisFontMaster.id ]
					targetLayerKeyL = targetLayerL.leftMetricsKey()
					a = ["=|", "+" "*", "/", "-1", "-2", "-3", "-4", "-5", "-6", "-7", "-8", "-9"]
					if targetLayerKeyL[0].isdigit() or any([ x in targetLayerKeyL for x in a]):
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
					print "Found invalid LSB key while checking the key of %s" % thisGlyph.name

			def nestHuntR( targetGlyphName ):
				# Sees if the glyphName exists in the font
				if thisFont.glyphs[ targetGlyphName ]:
					# If exists, gets the left key of targetGlyph of the same layer
					targetGlyphR = thisFont.glyphs[ targetGlyphName ]
					targetLayerR = targetGlyphR.layers[ thisFontMaster.id ]
					targetLayerKeyR = targetLayerR.rightMetricsKey()
					a = ["=|", "+" "*", "/", "-1", "-2", "-3", "-4", "-5", "-6", "-7", "-8", "-9"]
					if targetLayerKeyR[0].isdigit() or any([ x in targetLayerKeyR for x in a]):
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
					print "Found invalid RSB key while checking the key of %s" % thisGlyph.name

			# Set baseGlyphName for further nest hunting.
			for thisLayer in thisFont.selectedLayers:
				# Checks case of base glyph.
				thisGlyph = thisLayer.parent
				baseGlyphName = re.sub("\..*", "", thisGlyph.name)
				baseGlyphName = re.sub("superior", "", baseGlyphName)
				if "@Base" in fieldKey:
					baseGlyphName = baseGlyphName.capitalize()
					if thisGlyph.script == "Latin" and re.match("Ij|Ae|Oe", 	baseGlyphName):
						baseGlyphName = baseGlyphName[0:2].upper() + baseGlyphName[2:]

				# Detects ligatures and sets baseGlyphNameL and R
				if "_" in baseGlyphName:
					baseGlyphNameL = re.sub("_.*", "", baseGlyphName)
					baseGlyphNameR = re.sub(".*_", "", baseGlyphName)
				else:
					baseGlyphNameL = baseGlyphName
					baseGlyphNameR = baseGlyphName

				thisFont.disableUpdateInterface()
				thisGlyph.beginUndo()	

				# Runs nestHuntL multiple times until it finds the final glyph,
				# and then set the final left metrics key.
				if self.w.applyL:
					if self.w.avoidNest:
						dummyOldL = nestHuntL(baseGlyphNameL)
						dummyNewL = nestHuntL(dummyOldL)
						while dummyOldL != dummyNewL:
							dummyOldL = nestHuntL(dummyNewL)
							dummyNewL = nestHuntL(dummyOldL)
						finalKeyL = re.sub("@base", dummyNewL, flatFieldKey)
						for i in thisGlyph.layers:
							i.setLeftMetricsKey_(finalKeyL)

				# Runs nestHuntR multiple times until it finds the final glyph,
				# and then set the final right metrics key.
				if self.w.applyR:
					if self.w.avoidNest:
						dummyOldR = nestHuntR(baseGlyphNameR)
						dummyNewR = nestHuntR(dummyOldR)
						while dummyOldR != dummyNewR:
							dummyOldR = nestHuntR(dummyNewR)
							dummyNewR = nestHuntR(dummyOldR)
						finalKeyR = re.sub("@base", dummyNewR, flatFieldKey)
	
						for i in thisGlyph.layers:
							# Processes as normal
							if baseGlyphName != "Q":
								i.setRightMetricsKey_(finalKeyR)
							# Uses width of the width of O of the same group
							elif baseGlyphName == "Q" and self.w.radioQ.get() == 0:
								Qbefore = thisGlyph.name
								Qname = re.sub("Q", "O", Qbefore)
								Qname = re.sub("q", "o", Qbefore)
								glyphO = thisFont.glyphs[Qname]
								numOfMasters = len(thisFont.masters)
								for i in thisFont.masters:
									thisGlyphLayer = thisGlyph.layers[ i.id ]
									thisOLayer = glyphO.layers[ i.id ]
									thisOWidth = thisOLayer.width
									thisGlyphLayer.setWidth_(thisOWidth)
							# Uses RSB as normal
							elif baseGlyphName == "Q" and self.w.radioQ.get() == 1:
								i.setRightMetricsKey_(finalKeyR)

				thisGlyph.endUndo()
				thisFont.enableUpdateInterface()
			self.w.close()

		else:
			Glyphs.showMacroWindow()
			print "@base or @Base was not in the text field. Probably misspelling?"
BatchMetricKey()