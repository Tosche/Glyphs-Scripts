#MenuTitle: Copy Kerning Pairs
# -*- coding: utf-8 -*-
__doc__="""
(GUI) Copies kerning patterns to another. It supports pair-to-pair and preset group copying.
"""

import vanilla
import GlyphsApp
import re

try:
	thisFont = Glyphs.font
	# For Group validation in check text
	groups1 = []
	groups2 = []
	for thisGlyph in thisFont.glyphs:
		if thisGlyph.rightKerningGroup:
			if not "@"+thisGlyph.rightKerningGroup in groups1:
				groups1.append("@"+thisGlyph.rightKerningGroup)
		if thisGlyph.leftKerningGroup:
			if not "@"+thisGlyph.leftKerningGroup in groups2:
				groups2.append("@"+thisGlyph.leftKerningGroup)
except:
	pass

class CopyKerningPairs( object ):
	def __init__( self ):
		# Window 'self.w':
		editX = 180
		editY = 22
		textY  = 17
		spaceX = 10
		spaceY = 10
		buttonSizeX = 60
		windowWidth  = spaceX*3+editX*2+85
		windowHeight = 260
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Copy Kerning Pairs", # window title
			autosaveName = "com.Tosche.CopyKerningPairs.mainwindow" # stores last window position and size
		)
		
		# UI elements:
		self.w.tabs = vanilla.Tabs((10, 10, -10, -20-30), ["Pair", "Preset"])
		tab1 = self.w.tabs[0]
		tab1.text0 = vanilla.TextBox( (spaceX, 0, 260, textY), "Copy the kerning pair between...", sizeStyle='regular' )
		tab1.editL0 = vanilla.EditText( (spaceX, spaceY+textY, editX, editY), "", sizeStyle = 'regular', callback=self.checkField)
		tab1.editR0 = vanilla.EditText( (spaceX*3+editX+20, spaceY+textY, editX, editY), "", sizeStyle = 'regular', callback=self.checkField)
		tab1.checkL0 = vanilla.TextBox( (spaceX+editX+5, spaceY+textY+2, 40, textY), u"Any", sizeStyle='regular' )
		tab1.checkR0 = vanilla.TextBox( (spaceX*3+editX*2+25, spaceY+textY+2, 40, textY), u"Any", sizeStyle='regular' )
		tab1.text1 = vanilla.TextBox( (spaceX, spaceY*2+textY+editY, 200, textY), "...to this pair", sizeStyle='regular' )
		tab1.editL1 = vanilla.EditText( (spaceX, spaceY*3+textY*2+editY, editX, editY), "", sizeStyle = 'regular', callback=self.checkField)
		tab1.editR1 = vanilla.EditText( (spaceX*3+editX+20, spaceY*3+textY*2+editY, editX, editY), "", sizeStyle = 'regular', callback=self.checkField)
		tab1.checkL1 = vanilla.TextBox( (spaceX+editX+5, spaceY*3+textY*2+editY+2, 40, textY), u"Any", sizeStyle='regular')
		tab1.checkR1 = vanilla.TextBox( (spaceX*3+editX*2+25, spaceY*3+textY*2+editY+2, 40, textY), u"Any", sizeStyle='regular' )
		tab1.text2 = vanilla.TextBox( (spaceX, spaceY*5+textY*3+editY, 400, textY*2), "Groups will be automatically detected.\nYou can also type group name with @ prefix (e.g. @A)", sizeStyle='regular' )

		tab2 = self.w.tabs[1]
		tab2.radio = vanilla.RadioGroup((spaceX, 2, 80, 78), ["Letter", "Numeral"], isVertical = True, sizeStyle='regular', callback=self.checkRadio)
		tab2.popLetter = vanilla.PopUpButton( (spaceX+100, spaceY, 320, 20), ["Caps to Small Caps", "Caps & Lowercase to Superscript", "Caps & Lowercase to Subscript"], sizeStyle='regular' )
		tab2.popNum1 = vanilla.PopUpButton( (spaceX+100, spaceY+40, 140, 20), ["Lining Proportional", "Small Cap", "Numerator", "Denominator", "Superscript", "Subscript" ], sizeStyle='regular' )
		tab2.popNum2 = vanilla.PopUpButton( (spaceX+100+180, spaceY+40, 140, 20), ["Lining Proportional", "Small Cap", "Numerator", "Denominator", "Superscript", "Subscript" ], sizeStyle='regular' )
		tab2.textTo = vanilla.TextBox( (spaceX+100+151, spaceY+40, 20, textY), "to", sizeStyle='regular' )
		tab2.textScale = vanilla.TextBox( (spaceX, spaceY+80, 100, textY), "Scale\t\t%", sizeStyle='regular' )
		tab2.editScale = vanilla.EditText( (spaceX+40, spaceY+77, 40, editY), '100', sizeStyle = 'regular')
		tab2.textSkip = vanilla.TextBox( (spaceX+120, spaceY+80, 400, textY), "Ignore pair values smaller than         units", sizeStyle='regular' )
		tab2.editSkip = vanilla.EditText( (spaceX+321, spaceY+77, 30, editY), '10', sizeStyle = 'regular')
		tab2.textNote = vanilla.TextBox( (spaceX, spaceY*3+textY+76, 360, textY*2), "It only copies pairs between the groups.\nBut regular punctuations and symbols are taken care of.", sizeStyle='regular' )

		# Run Button:
		self.w.runButton = vanilla.Button((-80-15, -20-15, -15, -15), "Run", sizeStyle='regular', callback=self.CopyKerningPairsMain )

		# Load Settings:
		if not self.LoadPreferences():
			print "Note: 'Copy Kerning Pairs' could not load preferences. Will resort to defaults"
		
		# Open window and focus on it:
		self.w.open()
		tab2.radio.set(0)
		tab2.popNum1.enable(False)
		tab2.popNum2.enable(False)
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

	def checkField(self, sender):
		try:
			if thisFont.glyphs[self.w.tabs[0].editL0.get()] or self.w.tabs[0].editL0.get() in groups1:
				self.w.tabs[0].checkL0.set(u"✓")
			elif self.w.tabs[0].editL0.get() =="":
				self.w.tabs[0].checkL0.set(u"Any")
			else:
				self.w.tabs[0].checkL0.set("?")
				self.w.tabs[0].editL1.enable(True)
			if thisFont.glyphs[self.w.tabs[0].editR0.get()] or self.w.tabs[0].editR0.get() in groups2:
				self.w.tabs[0].checkR0.set(u"✓")
			elif self.w.tabs[0].editR0.get() =="":
				self.w.tabs[0].checkR0.set(u"Any")
			else:
				self.w.tabs[0].checkR0.set("?")
				self.w.tabs[0].editR1.enable(True)
			if thisFont.glyphs[self.w.tabs[0].editL1.get()] or self.w.tabs[0].editL1.get() in groups1:
				self.w.tabs[0].checkL1.set(u"✓")
			elif self.w.tabs[0].editL1.get() =="":
				self.w.tabs[0].checkL1.set(u"Any")
			else:
				self.w.tabs[0].checkL1.set("?")
			if thisFont.glyphs[self.w.tabs[0].editR1.get()] or self.w.tabs[0].editR1.get() in groups2:
				self.w.tabs[0].checkR1.set(u"✓")
			elif self.w.tabs[0].editR1.get() =="":
				self.w.tabs[0].checkR1.set(u"Any")
			else:
				self.w.tabs[0].checkR1.set("?")
		except Exception, e:
			Glyphs.showMacroWindow()
			print "Copy kerning Pairs Error (checkField): %s" % e
			print "No font open?"

	def checkRadio(self, sender):
		try:
			if self.w.tabs[1].radio.get() == 0:
				self.w.tabs[1].popLetter.enable(True)
				self.w.tabs[1].popNum1.enable(False)
				self.w.tabs[1].popNum2.enable(False)
			elif self.w.tabs[1].radio.get() == 1:
				self.w.tabs[1].popLetter.enable(False)
				self.w.tabs[1].popNum1.enable(True)
				self.w.tabs[1].popNum2.enable(True)
		except:
			print "except"
			pass

	def dupliKernPair(self, newKernDic, L0, R0, L1, R1):
		try:
			print "Following pairs have been added.\n"
			L0 = re.sub("@", "@MMK_L_", L0)
			R0 = re.sub("@", "@MMK_R_", R0)
			L1 = re.sub("@", "@MMK_L_", L1)
			R1 = re.sub("@", "@MMK_R_", R1)
			if not "@" in L0:
				try:
					L0 = "@MMK_L_" + thisFont.glyphs[L0].rightKerningGroup
				except:
					pass
			if not "@" in R0:
				try:
					R0 = "@MMK_R_" + thisFont.glyphs[R0].leftKerningGroup
				except:
					pass
			if not "@" in L1:
				try:
					L1 = "@MMK_L_" + thisFont.glyphs[L1].rightKerningGroup
				except:
					pass
			if not "@" in R1:
				try:
					R1 = "@MMK_R_" + thisFont.glyphs[R1].leftKerningGroup
				except:
					pass
			if L0 == "":
				for thisMaster in thisFont.masters:
					print thisMaster.name
					pairList = newKernDic[thisMaster.id]
					for i in range(len(pairList)):
						if pairList[i][1] == R0:
							print "\t%s,  %s,  %s" % (pairList[i][0], R1, pairList[i][2])
							thisFont.setKerningForPair(thisMaster.id, pairList[i][0], R1, pairList[i][2])
			elif R0 == "":
				for thisMaster in thisFont.masters:
					print thisMaster.name
					pairList = newKernDic[thisMaster.id]
					for i in range(len(pairList)):
						if pairList[i][0] == L0:
							print "\t%s,  %s,  %s" % (L1, pairList[i][1], pairList[i][2])
							thisFont.setKerningForPair(thisMaster.id, L1, pairList[i][1], pairList[i][2])
			else:
				for thisMaster in thisFont.masters:
					print thisMaster.name
					pairList = newKernDic[thisMaster.id]
					i = 0
					value = None
					while i != len(newKernDic[thisMaster.id]):
						if pairList[i][0] == L0 and pairList[i][1] == R0:
							value = pairList[i][2]
							print "\t%s,  %s,  %s" % (pairList[i][0], pairList[i][1], pairList[i][2])
							break
						i =i+1
					if value == None:
						print "The source pair does not exist."
					else:
						print "\t%s,  %s,  %s" % (L1, R1, pairList[i][2])
						thisFont.setKerningForPair(thisMaster.id, L1, R1, pairList[i][2])
		except Exception, e:
			Glyphs.showMacroWindow()
			print "Copy kerning Pairs Error (dupliKernPair): %s" % e

	def miscSymbolDic(self, miscType):
		miscSymbols = ["period", "comma", "minus", "plus","equal", "parenleft", "parenright"]
		miscSymbolDicNew ={}
		if miscType == "superscript":
			suffix1 = ".sups"
			suffix2 = "superior"
		elif miscType == "subscript":
			suffix1 = ".subs"
			suffix2 = "inferior"
		elif miscType == "smallcap":
			suffix1 = ".sc"
			suffix2 = ".smcp"
		for thisSymbol in miscSymbols:
			if thisFont.glyphs[thisSymbol + suffix1]:
				miscSymbolDicNew.update({thisSymbol:thisSymbol + suffix1})
			elif thisFont.glyphs[thisSymbol + suffix2]:
				miscSymbolDicNew.update({thisSymbol:thisSymbol + suffix2})
		return miscSymbolDicNew

	def numList(self, Suf):
		nums = [ "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
		if Suf == 0: #Lining Proportional (.lf)
			for i in range(len(nums)):
				nums[i] = nums[i]+".lf"
		elif Suf == 1: #Small Cap (.sc or .smcp)
			for i in range(len(nums)):
				if thisFont.glyphs[nums[i]+".sc"]:
					nums[i] = nums[i]+".sc"
				elif thisFont.glyphs[nums[i]+"smcp"]:
					nums[i] = nums[i]+"smcp"
		elif Suf == 2: #Numerator (.numr)
			for i in range(len(nums)):
				nums[i] = nums[i]+".numr"
		elif Suf == 3: #Denominator (.dnom)
			for i in range(len(nums)):
				nums[i] = nums[i]+".dnom"
		elif Suf == 4: #Superscript (.sups or superior)
			for i in range(len(nums)):
				if thisFont.glyphs[nums[i]+".sups"]:
					nums[i] = nums[i]+".sups"
				elif thisFont.glyphs[nums[i]+"superior"]:
					nums[i] = nums[i]+"superior"
		elif Suf == 5: #Subscript (.subs or inferior)
			for i in range(len(nums)):
				if thisFont.glyphs[nums[i]+".subs"]:
					nums[i] = nums[i]+".subs"
				elif thisFont.glyphs[nums[i]+"inferior"]:
					nums[i] = nums[i]+"inferior"
		return nums

	def dupliKernPreset(self, newKernDic, dic):
		print "Following pairs have been added.\n"
		try:
			dicL = {}
			dicR = {}
			for key, value in dic.iteritems():
				if thisFont.glyphs[key]:
					if thisFont.glyphs[key].rightKerningGroup:
						newKeyL = "@MMK_L_" + thisFont.glyphs[key].rightKerningGroup
					else:
						newKeyL = key
					if thisFont.glyphs[key].leftKerningGroup:
						newKeyR = "@MMK_R_" + thisFont.glyphs[key].leftKerningGroup
					else:
						newKeyR = key
				else:
					newKeyL = None
					newKeyR = None
				if thisFont.glyphs[value]:
					if thisFont.glyphs[value].rightKerningGroup:
						newValueL = "@MMK_L_" + thisFont.glyphs[value].rightKerningGroup
					else:
						newValueL = value
					if thisFont.glyphs[value].leftKerningGroup:
						newValueR = "@MMK_R_" + thisFont.glyphs[value].leftKerningGroup
					else:
						newValueR = value
				else:
					newValueL = None
					newValueR = None
				if newKeyL != None and newValueL != None:
					dicL.update({newKeyL:newValueL})
				if newKeyR != None and newValueR != None:
					dicR.update({newKeyR:newValueR})

			scale = float(self.w.tabs[1].editScale.get())/100
			skip = self.w.tabs[1].editSkip.get()
			for thisMaster in thisFont.masters:
				print thisMaster.name
				pairList = newKernDic[thisMaster.id]
				for keyL in dicL:
					for i in range(len(pairList)):
						if keyL in pairList[i][0]:
							for keyR in dicR:
								if keyR in pairList[i][1]:
									if int(abs(float(pairList[i][2])*scale)) >= int(skip):
										print "\t%s,  %s,  %s" % (dicL[keyL], dicR[keyR], float(pairList[i][2])*scale)
										thisFont.setKerningForPair(thisMaster.id, dicL[keyL], dicR[keyR], float(pairList[i][2])*scale)

		except Exception, e:
			Glyphs.showMacroWindow()
			print "Copy kerning Pairs Error (dupliKernPreset): %s" % e

	def CopyKerningPairsMain( self, sender ):
		try:
			kernDic = thisFont.kerningDict()				
			newKernDic = {}
			for thisMaster in thisFont.masters: # building newKernDic
				kernList = []
				for key1 in kernDic[thisMaster.id]:
					for key2 in kernDic[thisMaster.id][key1]:
						pairInList = [key1, key2, kernDic[thisMaster.id][key1][key2]]
						kernList.append(pairInList)
				newKernDic.update({thisMaster.id:kernList})
			if self.w.tabs.get()==0: # If it's an pair operation
				editList = [self.w.tabs[0].editL0.get(), self.w.tabs[0].editR0.get(), self.w.tabs[0].editL1.get(), self.w.tabs[0].editR1.get()]
				checkList = [self.w.tabs[0].checkL0.get(), self.w.tabs[0].checkR0.get(), self.w.tabs[0].checkL1.get(), self.w.tabs[0].checkR1.get()]
				if editList[0] == editList[1] == "":
					Glyphs.showMacroWindow()
					print 'Nothing happened. You cannot leave both sides of the pair as "Any."'
				elif (editList[0] =="" and editList[2] != "") or (editList[0] !="" and editList[2] == "") or (editList[1] =="" and editList[3] != "") or (editList[1] !="" and editList[3] == ""):
					Glyphs.showMacroWindow()
					print 'Nothing happened. "Any" should only be allowed on either side. And if the source pair consists of "Any", the same side of the destination should also be "Any".'
				elif "?" in checkList:
					print "Nothing happened. Please make sure the glyphs or groups exist."
				# When there's no problem in the font
				else:
					if editList[0] == editList[2] == "" or editList[1] == editList[3] == "":
						if editList[1] == editList[3] !="" or editList[0] == editList[2] !="":
							print "Nothing happened. Source and destination are the same."
						else:
							print "checkpoint. work on it."
							self.dupliKernPair(newKernDic, editList[0], editList[1], editList[2], editList[3])
					else:
						if editList[0] == editList[2] and editList[1] == editList[3]:
							print "Nothing happened. Source and destination are the same."
						else:
							self.dupliKernPair(newKernDic, editList[0], editList[1], editList[2], editList[3])

			elif self.w.tabs.get()==1: # If it's an preset operation
				if self.w.tabs[1].radio.get()==0: # If it's Letter preset
					if self.w.tabs[1].popLetter.get()==0: #Caps to Small Caps
						scList = []
						for thisGlyph in thisFont.glyphs:
							if thisGlyph.category =="Letter" and (".smcp" in thisGlyph.name or ".sc" in thisGlyph.name):
								scList.append(thisGlyph.name)
						capList = list(scList)
						for i in range(len(capList)):
							capList[i] = re.sub(".smcp", "", capList[i]).capitalize()
							capList[i] = re.sub(".sc", "", capList[i]).capitalize()
						print capList
						c2scDic={}
						for i in range(len(capList)):
							if thisFont.glyphs[capList[i]]:
								c2scDic.update({capList[i]:scList[i]})
						self.dupliKernPreset(newKernDic, c2scDic)

					else:
						if self.w.tabs[1].popLetter.get()==1: #Caps & Lowercase to Superscript
							suffix = ".sups"
							miscType = "superscript"
						elif self.w.tabs[1].popLetter.get()==2: #Caps & Lowercase to Subscript
							suffix = ".subs"
							miscType = "subscript"
						destiList = []
						for thisGlyph in thisFont.glyphs:
							if thisGlyph.category =="Letter" and suffix in thisGlyph.name:
								destiList.append(thisGlyph.name)
						print destiList
						sourceList = list(destiList)
						for i in range(len(sourceList)):
							sourceList[i] = re.sub(suffix, "", sourceList[i])
						letterDic={}
						for i in range(len(sourceList)):
							if thisFont.glyphs[sourceList[i]]:
								letterDic.update({sourceList[i]:destiList[i]})
						smallLetterDic = (letterDic.items() + self.miscSymbolDic(miscType).items())
						self.dupliKernPreset(newKernDic, smallLetterDic)

				else: # If it's an Number preset
					if self.w.tabs[1].popNum1.get() == self.w.tabs[1].popNum2.get():
						print "Nothing happened. You cannot set the same group as source and destination."
					else:
						numDic = {}
						miscDic = {}
						numList1 = self.numList(self.w.tabs[1].popNum1.get())
						numList2 = self.numList(self.w.tabs[1].popNum2.get())
						for i in range(len(numList1)):
							numDic.update({numList1[i]:numList2[i]})
						popNums = [self.w.tabs[1].popNum1.get(), self.w.tabs[1].popNum2.get()]
						if not (2 in popNums or 3 in popNums):
							if self.w.tabs[1].popNum1.get() == 1:
								miscDic = self.miscSymbolDic("smallcap")
							elif self.w.tabs[1].popNum1.get() == 4:
								miscDic = self.miscSymbolDic("superscript")
							elif self.w.tabs[1].popNum1.get() == 5:
								miscDic = self.miscSymbolDic("subscript")
							if self.w.tabs[1].popNum2.get() == 1:
								miscDic = self.miscSymbolDic("smallcap")
							elif self.w.tabs[1].popNum2.get() == 4:
								miscDic = self.miscSymbolDic("superscript")
							elif self.w.tabs[1].popNum2.get() == 5:
								miscDic = self.miscSymbolDic("subscript")
						numFinalDic = dict(numDic.items() + miscDic.items())
						# unfinished. at least the dictionary is done.
						# Careful! it hasn't done glyph validity check yet!
						self.dupliKernPreset(newKernDic, numFinalDic)

				if not self.SavePreferences( self ):
					print "Note: 'Copy Kerning Pairs' could not write preferences."
			
		except Exception, e:
			# brings macro window to front and reports error:
			Glyphs.showMacroWindow()
			print "Copy Kerning Pairs Error: %s" % e

CopyKerningPairs()