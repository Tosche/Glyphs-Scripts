#MenuTitle: Copy Kerning to Greek & Cyrillic...
# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
__doc__="""
(GUI) Copies your Latin kerning to the common shapes of Greek and Cyrillic, including small caps, using predefined dictionary. Exceptions and absent glyphs are skipped. It's best used after finishing Latin kerning and before starting Cyrillic and Greek.
"""

import vanilla
import GlyphsApp
import traceback

#Stores a Latin glyph name as key and G/C glyph as unicode value, because glyph name may differ
Grk = {"A":"0391", "B":"0392", "E":"0395", "H":"0397", "I":"0399", "K":"039A", "M":"039C", "N":"039D", "O":"039F", "P":"03A1", "T":"03A4", "X":"03A7", "Y":"03A5", "Z":"0396", "o":"03BF"}

CyrUC = {"A":"0410", "B":"0412", "C":"0421", "E":"0415", "H":"041D", "I":"0406", "J":"0408", "K":"041A", "M":"041C", "O":"041E", "P":"0420", "S":"0405", "T":"0422", "W":"051C", "X":"0425", "Y":"04AE", "Schwa":"04D8"}

CyrLCNormal = {"a":"0430", "abreve":"04D1", "adieresis":"04D3", "e":"0435", "egrave":"0450", "edieresis":"0451", "o":"043E", "p":"0440", "c":"0441", "y":"0443", "ydieresis":"04F1", "x":"0445", "s":"0455", "h":"04BB", "l":"04CF", "i":"0456", "idieresis":"0457", "j":"0458", "w":"051D", "schwa":"04D9", "v":"04AF"}

CyrLCCursive = {"a":"0430", "abreve":"04D1", "adieresis":"04D3", "e":"0435", "egrave":"0450", "edieresis":"0451", "ebreve":"04D7", "u":"0438", "ubreve":"0439", "ugrave":"045D", "o":"043E", "n":"043F", "p":"0440", "c":"0441", "m":"0442", "y":"0443", "ydieresis":"04F1", "x":"0445", "s":"0455", "h":"04BB", "l":"04CF", "idieresis":"0457", "i":"0456", "j":"0458", "w":"051D", "schwa":"04D9"}


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
			print("Note: 'Copy kerning to Greek & Cyrillic (GUI)' could not load preferences. Will resort to defaults")
		
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

	def appliablePairKey(self, f, keyName):
		if keyName[0] == '@':
			return keyName
		else: # if keyName is glyph ID
			return f.glyphForId_(keyName).name

	# duplication of Latin letter-to-letter pairs to the given dictionary
	def dupliKern(self, f, kernDic, nonLetterGroupsL, nonLetterGroupsR, dic):
		try:
			# add small cap to the kernKeysDic if it exists:
			if f.glyphs["a.sc"] or f.glyphs["a.smcp"]:
				suffix = ".sc" if f.glyphs["a.sc"] else ".smcp"
				scDic = {}
				for key, value in dic.items():
					if str(key)[0].isupper():
						if f.glyphs[value.lower()+suffix]:
							scDic.update({key.lower()+suffix : value.lower()+suffix})
				dic.update(scDic)

			# update dic with group names where necessary.
			# kerning keys are group name or glyph id.
			kernKeysDicL = {}
			kernKeysDicR = {}
			for key, value in dic.items():
				# key = Latin glyph name
				# value = Greek / Cyrillic glyph name
				# newKeys & newValues = Latin kerning key and Grk/Cyr kerning key.
				try:
					if f.glyphs[key].leftKerningGroup:
						newKeyR = "@MMK_R_"+f.glyphs[key].leftKerningGroup
					else:
						newKeyR = key
					if f.glyphs[value].leftKerningGroup:
						newValueR = "@MMK_R_"+f.glyphs[value].leftKerningGroup
					else:
						newValueR = value
					kernKeysDicR.update({newKeyR:newValueR})

					if f.glyphs[key].rightKerningGroup:
						newKeyL = "@MMK_L_"+f.glyphs[key].rightKerningGroup
					else:
						newKeyL = key
					if f.glyphs[value].rightKerningGroup:
						newValueL = "@MMK_L_"+f.glyphs[value].rightKerningGroup
					else:
						newValueL = value
					kernKeysDicL.update({newKeyL:newValueL})
				except:
					pass

			for m in f.masters:
				for l, rightKeys in kernDic[m.id].items():
					isLeftLetter = False
					leftOfPair = None
					l = self.appliablePairKey(f, l) # cleanup. glyph key becomes name

					if l in kernKeysDicL:
						leftOfPair = kernKeysDicL[l]
						isLeftLetter = True
					elif (l in nonLetterGroupsL): # if non-Letter in a group
						leftOfPair = l
					elif l[0]!='@': # if l is a glyph id = single glyph
						try:
							if l.category != "Letter":
								leftOfPair = l
								
								# print('L', leftOfPair)
								# leftOfPair = None
							else: # single glyph and a letter that's irrelevant
								pass
						except: # glyph does not exist
							pass
					# non-Latin letters will be skipped

					if leftOfPair is not None:
						# print('yay', leftOfPair, rightKeys)
						for r, value in rightKeys.items():
							isRightLetter = False
							rightOfPair = None
							r = self.appliablePairKey(f, r)
							if r in kernKeysDicR:
								rightOfPair = kernKeysDicR[r]
								isRightLetter = True
							elif r in nonLetterGroupsR:
								rightOfPair = r
							elif r[0]!='@': # if l is a glyph id = single glyph
								try:
									if f.glyphForId_(r).category != "Letter":
										rightOfPair = r
										# print('R', rightOfPair)
										# rightOfPair = None
								except: # glyph does not exist
									pass
							# non-Latin letters will be skipped

							if leftOfPair and rightOfPair: # both sides are not None
								if isLeftLetter or isRightLetter: # if at least one side is Letter
									try:
										# this print function conflicts with glyph name/key
										print("  %s   %s   %s   %s" % (m.name, leftOfPair, rightOfPair, value))
										f.setKerningForPair(m.id, leftOfPair, rightOfPair, value)
									except:
										print('dupliKern error: ', traceback.format_exc())

		except Exception as e:
			Glyphs.showMacroWindow()
			print("Copy kerning to Greek & Cyrillic... Error (dupliKern): %s" % e)

	def CopyKerningToGreekCyrillicMain( self, sender ):
		try:
			f = Glyphs.font
			kernDic = f.kerning
			f.disableUpdateInterface()
			Glyphs.clearLog()
			print("Following pairs have been added or updated.\n")
			# list of non-Letter kerning groups in a font.
			nonLetterGroupsL = []
			nonLetterGroupsR = []
			for g in f.glyphs:
				if g.category != "Letter":
					if g.leftKerningGroup:
						if not "@MMK_R_"+g.leftKerningGroup in nonLetterGroupsR:
							nonLetterGroupsR.append("@MMK_R_"+g.leftKerningGroup)
					if g.rightKerningGroup:
						if not "@MMK_L_"+g.rightKerningGroup in nonLetterGroupsL:
							nonLetterGroupsL.append("@MMK_L_"+g.rightKerningGroup) 

			print("Greek")
			for key1, value1 in Grk.items():
				try:
					Grk[key1] = f.glyphForUnicode_(value1).name
				except:
					pass
			self.dupliKern(f, kernDic, nonLetterGroupsL, nonLetterGroupsR, Grk)

			print("Cyrillic")
			if self.w.AllCapBox.get(): # if all-caps
				CyrDic = CyrUC.copy
			else: # if not all caps
				if self.w.CursiveBox.get(): # if lowercase cursive
					CyrDic = CyrUC | CyrLCCursive # this merging syntax works from Py3.9
				else: # if normal lowercase
					CyrDic = CyrUC | CyrLCNormal

			for key2, value2 in CyrDic.items():
				try:
					CyrDic[key2] = f.glyphForUnicode_(value2).name
				except:
					pass
			self.dupliKern(f, kernDic, nonLetterGroupsL, nonLetterGroupsR, CyrDic)

			f.enableUpdateInterface()
			Glyphs.showMacroWindow()

			if not self.SavePreferences( self ):
				print("Note: 'Copy kerning to Greek & Cyrillic...' could not write preferences.")
			
			self.w.close() # delete if you want window to stay open
		except Exception as e:
			Glyphs.showMacroWindow()
			print("Copy kerning to Greek & Cyrillic... Error: %s" % e)

CopyKerningToGreekCyrillic()