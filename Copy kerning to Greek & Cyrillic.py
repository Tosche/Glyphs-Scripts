#MenuTitle: Copy kerning to Greek & Cyrillic (GUI)
# -*- coding: utf-8 -*-
__doc__="""
Copies your Latin kerning to the common shapes of Greek and Cyrillic, including small caps, using predefined dictionary. Exceptions and absent glyphs are skipped. It's best used after finishing Latin kerning and before starting Cyrillic and Greek.
"""

import vanilla
import GlyphsApp

GrkUC = {"A":"Alpha", "B":"Beta", "E":"Epsilon", "H":"Eta", "I":"Iota", "K":"Kappa", "M":"Mu", "N":"Nu", "O":"Omicron", "P":"Rho", "T":"Tau", "X":"Chi", "Y":"Upsilon", "Z":"Zeta"}

CyrUC = {"A":"A-cy", "B":"Ve-cy", "C":"Es-cy", "E":"Ie-cy", "H":"En-cy", "I":"I-cy", "K":"Ka-cy", "M":"Em-cy", "O":"O-cy", "P":"Er-cy", "S":"Dze-cy", "T":"Te-cy", "W":"We-cy", "X":"Ha-cy", "Y":"Ustrait-cy"}

CyrLCUpright = {"a": "a-cy", "abreve": "abreve-cy", "adieresis": "adieresis-cy", "e": "ie-cy", "egrave": "iegrave-cy", "edieresis": "io-cy", "o": "o-cy", "p": "er-cy", "c": "es-cy", "y": "u-cy", "ydieresis": "udieresis-cy", "x": "ha-cy", "s": "dze-cy", "h": "shha-cy", "l": "palochka-cy", "i": "i-cy", "idieresis": "yi-cy", "j": "je-cy", "w": "we-cy"}

CyrLCCursive = {"a": "a-cy", "abreve": "abreve-cy", "adieresis": "adieresis-cy", "e": "ie-cy", "egrave": "iegrave-cy", "edieresis": "io-cy", "ebreve": "iebreve-cy", "u": "ii-cy", "ubreve": "iishort-cy", "ugrave": "iigrave-cy", "o": "o-cy", "n": "pe-cy", "p": "er-cy", "c": "es-cy", "m": "te-cy", "y": "u-cy", "ydieresis": "udieresis-cy", "x": "ha-cy", "s": "dze-cy", "h": "shha-cy", "l": "palochka-cy", "idieresis": "yi-cy", "i": "i-cy", "j": "je-cy", "w":"we-cy"}


class CopyKerningToGreekCyrillic( object ):
	def __init__( self ):
		spaceX = 10
		buttonSizeX = 60
		Y = 16
		spaceY = 10
		windowWidth  = 360
		windowHeight = spaceY*2+(Y+spaceY)*6
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Copy kerning to Greek & Cyrillic", # window title
			autosaveName = "com.Tosche.CopyKerningToGreekCyrillic.mainwindow" # stores last window position and size
		)
		
		# UI :
		self.w.instruction = vanilla.TextBox((spaceX, spaceY, 340, 87), "This script copies your Latin kerning to the common shapes of Greek and Cyrillic, including small caps.\nExceptions and absent glyphs are skipped.\nIt's best used after finishing Latin kerning and before starting Cyrillic and Greek.")
		self.w.CursiveBox = vanilla.CheckBox( (spaceX, spaceY+90+spaceY, 270, Y), 'Cyrillic Lowercase is "cursive"', value=False)
		self.w.runButton = vanilla.Button((-80-15, spaceY+(Y+spaceY)*5, -15, Y), "Copy", sizeStyle='regular', callback=self.CopyKerningToGreekCyrillicMain )
		self.w.setDefaultButton( self.w.runButton )

		# Load Settings:
		if not self.LoadPreferences():
			print "Note: 'Copy kerning to Greek & Cyrillic (GUI)' could not load preferences. Will resort to defaults"
		
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()
		
	def SavePreferences( self, sender ):
		try:
			pass
		except:
			return False
			
		return True

	def LoadPreferences( self ):
		try:
			pass
		except:
			return False
			
		return True

	# duplication of Latin letter-to-letter pairs to the given dictionary
	def dupliKern(self, thisFont, kernDic, nonLetterGroupsL, nonLetterGroupsR, dic):
		# add small cap to the newDic if it exists:
		if thisFont.glyphs["a.sc"] or thisFont.glyphs["a.smcp"]:
			if thisFont.glyphs["a.sc"]:
				suffix = ".sc"
			elif thisFont.glyphs["a.smcp"]:
				suffix = ".smcp"
			scDic = {}
			for key, value in dic.iteritems():
				if str(key)[0].isupper():
					if thisFont.glyphs[value.lower()+suffix]:
						scDic.update({key.lower()+suffix : value.lower()+suffix})
			dic.update(scDic)
		# update dic with group names where necessary. newDicL is for the left of the GLYPHS, not pairs.
		newDicL = {}
		newDicR = {}
		for key, value in dic.iteritems():
			try:
				if thisFont.glyphs[key].leftKerningGroup:
					newKeyL = "@MMK_R_"+thisFont.glyphs[key].leftKerningGroup
				else:
					newKeyL = key
				if thisFont.glyphs[value].leftKerningGroup:
					newValueL = "@MMK_R_"+thisFont.glyphs[value].leftKerningGroup
				else:
					newValueL = value
				newDicL.update({newKeyL:newValueL})

				if thisFont.glyphs[key].rightKerningGroup:
					newKeyR = "@MMK_L_"+thisFont.glyphs[key].rightKerningGroup
				else:
					newKeyR = key
				if thisFont.glyphs[value].rightKerningGroup:
					newValueR = "@MMK_L_"+thisFont.glyphs[value].rightKerningGroup
				else:
					newValueR = value
				newDicR.update({newKeyR:newValueR})
			except:
				pass

		for thisMaster in thisFont.masters:
			for rightKey in kernDic[thisMaster.id]:
				isLeftLetter = False
				isRightLetter = False
				if rightKey in newDicR or rightKey in nonLetterGroupsR or (thisFont.glyphs[rightKey] and thisFont.glyphs[rightKey].category != "Letter"):
					if rightKey in newDicR:
						leftOfPair = newDicR[rightKey]
						isLeftLetter = True
					elif rightKey in nonLetterGroupsR or (thisFont.glyphs[rightKey] and thisFont.glyphs[rightKey].category != "Letter"):
						leftOfPair = rightKey
					for leftKey in kernDic[thisMaster.id][rightKey].keys():
						if leftKey in newDicL or leftKey in nonLetterGroupsL or (thisFont.glyphs[leftKey] and thisFont.glyphs[leftKey].category != "Letter"):
							if leftKey in newDicL:
								rightOfPair = newDicL[leftKey]
								isRightLetter = True
							elif leftKey in nonLetterGroupsL or (thisFont.glyphs[leftKey] and thisFont.glyphs[leftKey].category != "Letter"):
								rightOfPair = leftKey
							if isLeftLetter == True or isRightLetter == True:
								print "  %s   %s   %s   %s" % (thisMaster.name, leftOfPair, rightOfPair, kernDic[thisMaster.id][rightKey][leftKey])
								thisFont.setKerningForPair(thisMaster.id, leftOfPair, rightOfPair, kernDic[thisMaster.id][rightKey][leftKey])

	def CopyKerningToGreekCyrillicMain( self, sender ):
		try:
			thisFont = Glyphs.font
			kernDic=thisFont.kerningDict()
			thisFont.disableUpdateInterface()
			Glyphs.clearLog()
			print "Following pairs have been added or updated.\n"
			# list of non-Letter kerning groups in a font.
			nonLetterGroupsL = []
			nonLetterGroupsR = []
			for thisGlyph in thisFont.glyphs:
				if thisGlyph.category != "Letter":
					if thisGlyph.leftKerningGroup:
						if not "@MMK_R_"+thisGlyph.leftKerningGroup in nonLetterGroupsL:
							nonLetterGroupsL.append("@MMK_R_"+thisGlyph.leftKerningGroup)
					if thisGlyph.rightKerningGroup:
						if not "@MMK_L_"+thisGlyph.rightKerningGroup in nonLetterGroupsR:
							nonLetterGroupsR.append("@MMK_L_"+thisGlyph.rightKerningGroup)
			print "Greek"
			self.dupliKern(thisFont, kernDic, nonLetterGroupsL, nonLetterGroupsR, GrkUC)
			if self.w.CursiveBox.get():
				CyrDic = dict( CyrUC.items() + CyrLCCursive.items() )
			else:
				CyrDic = dict( CyrUC.items() + CyrLCUpright.items() )
			print "Cyrillic"
			self.dupliKern(thisFont, kernDic, nonLetterGroupsL, nonLetterGroupsR, CyrDic)

			thisFont.enableUpdateInterface()
			Glyphs.showMacroWindow()

			if not self.SavePreferences( self ):
				print "Note: 'Copy kerning to Greek & Cyrillic (GUI)' could not write preferences."
			
			self.w.close() # delete if you want window to stay open
		except Exception, e:
			# brings macro window to front and reports error:
			Glyphs.showMacroWindow()
			print "Copy kerning to Greek & Cyrillic (GUI) Error: %s" % e

CopyKerningToGreekCyrillic()