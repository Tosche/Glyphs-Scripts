#MenuTitle: Copy Kerning to Greek & Cyrillic...
# -*- coding: utf-8 -*-
__doc__="""
(GUI) Copies your Latin kerning to the common shapes of Greek and Cyrillic, including small caps, using predefined dictionary. Exceptions and absent glyphs are skipped. It's best used after finishing Latin kerning and before starting Cyrillic and Greek.
"""

import vanilla
import GlyphsApp

#Stores a Latin glyph name as key and G/C glyph as unicode value, because glyph name may differ
Grk = {"A": "0391", "B": "0392", "E": "0395", "H": "0397", "I": "0399", "K": "039A", "M": "039C", "N": "039D", "O": "039F", "P": "03A1", "T": "03A4", "X": "03A7", "Y": "03A5", "Z": "0396", "o": "03BF"}

CyrUC = {"A": "0410", "B": "0412", "C": "0421", "E": "0415", "H": "041D", "I": "0406", "J": "0408", "K": "041A", "M": "041C", "O": "041E", "P": "0420", "S": "0405", "T": "0422", "W": "051C", "X": "0425", "Y": "04AE", "Schwa": "04D8"}

CyrLCNormal = {"a": "0430", "abreve": "04D1", "adieresis": "04D3", "e": "0435", "egrave": "0450", "edieresis": "0451", "o": "043E", "p": "0440", "c": "0441", "y": "0443", "ydieresis": "04F1", "x": "0445", "s": "0455", "h": "04BB", "l": "04CF", "i": "0456", "idieresis": "0457", "j": "0458", "w": "051D", "schwa": "04D9", "v": "04AF"}

CyrLCCursive = {"a": "0430", "abreve": "04D1", "adieresis": "04D3", "e": "0435", "egrave": "0450", "edieresis": "0451", "ebreve": "04D7", "u": "0438", "ubreve": "0439", "ugrave": "045D", "o": "043E", "n": "043F", "p": "0440", "c": "0441", "m": "0442", "y": "0443", "ydieresis": "04F1", "x": "0445", "s": "0455", "h": "04BB", "l": "04CF", "idieresis": "0457", "i": "0456", "j": "0458", "w": "051D", "schwa": "04D9"}


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
		self.w.AllCapBox = vanilla.CheckBox( (spaceX, spaceY+87+spaceY, 270, Y), "ALL CAP (skip lowercase)", callback=self.triggerCursive, value=False)
		self.w.CursiveBox = vanilla.CheckBox( (spaceX, spaceY+87+spaceY+Y+spaceY, 270, Y), 'Cyrillic lowercase is "cursive"', value=False)
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

	def triggerCursive(self, sender):
		if self.w.AllCapBox.get() == True:
			self.w.CursiveBox.enable(False)
			self.w.CursiveBox.set(False)
		elif self.w.AllCapBox.get() == False:
			self.w.CursiveBox.enable(True)
			self.w.CursiveBox.set(False)

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
			for key1, value1 in Grk.iteritems():
				try:
					Grk[key1] = thisFont.glyphForUnicode_(value1).name
				except:
					pass
			self.dupliKern(thisFont, kernDic, nonLetterGroupsL, nonLetterGroupsR, Grk)
			print "Cyrillic"
			if self.w.AllCapBox.get() == False:
				if self.w.CursiveBox.get():
					CyrDic = dict( CyrUC.items() + CyrLCCursive.items() )
				else:
					CyrDic = dict( CyrUC.items() + CyrLCNormal.items() )

			elif self.w.AllCapBox.get() == True:
				CyrDic = CyrUC.copy
			for key2, value2 in CyrDic.iteritems():
				try:
					CyrDic[key2] = thisFont.glyphForUnicode_(value2).name
				except:
					pass

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