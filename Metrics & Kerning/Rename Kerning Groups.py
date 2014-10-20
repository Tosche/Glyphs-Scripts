#MenuTitle: Rename Kerning Groups
# -*- coding: utf-8 -*-
__doc__="""
(GUI) Lets you rename kerning names and pairs associated with them. 
"""

import vanilla
import GlyphsApp

thisFont = Glyphs.font
# builing a more accessible kerning dictionary
# it's a dictionary of lists. newKernDic[master.id][left, right, value]
kernDic = thisFont.kerningDict()				
newKernDic = {}
for thisMaster in thisFont.masters:
	kernList = []
	for key1 in kernDic[thisMaster.id]:
		for key2 in kernDic[thisMaster.id][key1]:
			pairInList = [key1, key2, kernDic[thisMaster.id][key1][key2]]
			kernList.append(pairInList)
		newKernDic[thisMaster.id] = kernList

# building popup list
# each value contains a list of glyphs involved. groupsL/R[groupName][glyph, glyph, glyph...]
groupsL = {}
groupsR = {}
for thisGlyph in thisFont.glyphs:
	if thisGlyph.leftKerningGroup != None:
		if not thisGlyph.leftKerningGroup in groupsL:
			groupsL[thisGlyph.leftKerningGroup] = []
		groupsL[thisGlyph.leftKerningGroup].append(thisGlyph.name)

	if thisGlyph.rightKerningGroup != None:
		if not thisGlyph.rightKerningGroup in groupsR:
			groupsR[thisGlyph.rightKerningGroup] = []
		groupsR[thisGlyph.rightKerningGroup].append(thisGlyph.name)

class RenameKerningGroups( object ):
	def __init__( self ):
		# Window 'self.w':
		editX = 180
		editY = 22
		textY  = 17
		spaceX = 10
		spaceY = 10
		windowWidth  = spaceX*3+editX*2+85
		windowHeight = 150

		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Rename Kerning Groups", # window title
			minSize = ( windowWidth, windowHeight ), # minimum size (for resizing)
			maxSize = ( windowWidth + 100, windowHeight ), # maximum size (for resizing)
			autosaveName = "com.Tosche.RenameKerningGroups.mainwindow" # stores last window position and size
		)
		
		# UI elements:
		self.w.radio = vanilla.RadioGroup( (spaceX+130, spaceY, 120, textY), ["Left", "Right"], isVertical = False, sizeStyle='regular', callback=self.switchList)
		self.w.radio.set(0)
		self.w.text1 = vanilla.TextBox( (spaceX, spaceY*2+textY, 120, textY), "Rename this Group", sizeStyle='regular' )
		self.w.text2 = vanilla.TextBox( (spaceX, spaceY*3+editY+textY, 120, textY), "to this", sizeStyle='regular' )
		self.w.popup = vanilla.PopUpButton( (spaceX+130, spaceY*2+textY, -15, editY), [str(x) for x in sorted(groupsL)], sizeStyle='regular' )
		self.w.newName = vanilla.EditText( (spaceX+130, spaceY*3+editY+textY, -15, editY), "", sizeStyle = 'regular' )
		# Run Button:
		self.w.runButton = vanilla.Button((-80-15, spaceY*4+editY*3, -15, -15), "Run", sizeStyle='regular', callback=self.RenameKerningGroupsMain )
		self.w.setDefaultButton( self.w.runButton )
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()

	def switchList(self, sender):
		try:
			if self.w.radio.get() == 0:
				self.w.popup.setItems(sorted(groupsL))
			elif self.w.radio.get() == 1:
				self.w.popup.setItems(sorted(groupsR))
		except Exception, e:
			print "Rename Kerning Group Error (switchList): %s" % e

	def RenameKerningGroupsMain( self, sender ):
		try:
			newName = self.w.newName.get()
			popupNum = self.w.popup.get()
			if self.w.radio.get() == 0: # it it's a left group
				popup = sorted(groupsL)[popupNum]
				for thisGlyphName in groupsL[popup]:
					thisFont.glyphs[thisGlyphName].leftKerningGroup = newName
				for thisMaster in thisFont.masters:
					for thisPair in newKernDic[thisMaster.id]:
						if "@MMK_R_"+popup in thisPair[1]:
							thisFont.setKerningForPair(thisMaster.id, thisPair[0], "@MMK_R_"+newName, thisPair[2])
							thisFont.removeKerningForPair( thisMaster.id, thisPair[0], "@MMK_R_"+popup)
				# updating groupsL popup
				groupsL[newName] = groupsL.pop(popup)
				self.w.popup.setItems(sorted(groupsL))
				self.w.popup.set(sorted(groupsL).index(newName))
				# updating newKernDic
				for thisMaster in thisFont.masters:
					for thisPair in newKernDic[thisMaster.id]:
						if thisPair[1] == "@MMK_R_"+popup:
							thisPair[1] = "@MMK_R_"+newName

			if self.w.radio.get() == 1: # it it's a right group
				popup = sorted(groupsR)[popupNum]
				for thisGlyphName in groupsR[popup]:
					thisFont.glyphs[thisGlyphName].rightKerningGroup = newName
				for thisMaster in thisFont.masters:
					for thisPair in newKernDic[thisMaster.id]:
						if "@MMK_L_"+popup in thisPair[0]:
							thisFont.setKerningForPair(thisMaster.id, "@MMK_L_"+newName, thisPair[1], thisPair[2])
							thisFont.removeKerningForPair(thisMaster.id, "@MMK_L_"+popup, thisPair[1])
				# updating groupsR popup
				groupsR[newName] = groupsR.pop(popup)
				self.w.popup.setItems(sorted(groupsR))
				self.w.popup.set(sorted(groupsR).index(newName))
				# updating newKernDic
				for thisMaster in thisFont.masters:
					for thisPair in newKernDic[thisMaster.id]:
						if thisPair[0] == "@MMK_L_"+popup:
							thisPair[0] = "@MMK_L_"+newName
	
		except Exception, e:
			# brings macro window to front and reports error:
			Glyphs.showMacroWindow()
			print "Rename Kerning Group Error (RenameKerningGroupsMain): %s" % e

RenameKerningGroups()