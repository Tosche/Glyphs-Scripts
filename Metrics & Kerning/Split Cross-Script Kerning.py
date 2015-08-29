#MenuTitle: Split Cross-Script Kerning
# -*- coding: utf-8 -*-
__doc__="""
Splits kerning groups of LGC (Latin, Greek, Cyrillic) and reconstructs kerning accordingly.
Kern once, split later.
"""

import GlyphsApp

font = Glyphs.font # frontmost font
fontMaster = font.selectedFontMaster # active master
selectedLayers = font.selectedLayers # active layers of selected glyphs
thisDoc = Glyphs.currentDocument

font.disableUpdateInterface() # suppresses UI updates in Font View
Glyphs.clearLog()

kernDic = font.kerningDict()				
newKernDic = {}
for thisMaster in font.masters:
	kernList = []
	for key1 in kernDic[thisMaster.id]:
		for key2 in kernDic[thisMaster.id][key1]:
			pairInList = [key1, key2, kernDic[thisMaster.id][key1][key2]]
			kernList.append(pairInList)
		newKernDic[thisMaster.id] = kernList

# dictionary of groups, each value containg a list of glyphs involved.
# groupsL/R[groupName][glyph, glyph, glyph...]
groupsL = {}
groupsR = {}
for thisGlyph in font.glyphs:
	if thisGlyph.category == "Letter":
		if thisGlyph.leftKerningGroupId() != None:
			if not thisGlyph.leftKerningGroupId() in groupsR:
				groupsR[thisGlyph.leftKerningGroupId()] = []
			groupsR[thisGlyph.leftKerningGroupId()].append(thisGlyph.name)
	
		if thisGlyph.rightKerningGroupId() != None:
			if not thisGlyph.rightKerningGroupId() in groupsL:
				groupsL[thisGlyph.rightKerningGroupId()] = []
			groupsL[thisGlyph.rightKerningGroupId()].append(thisGlyph.name)

groupsL_GCref = groupsL.copy()
groupsR_GCref = groupsR.copy()

def duplicateGroup(group, left):
	for key, item in group.iteritems():
#		print key
		groupCy = False
		groupCyName = ""
		groupGr = False
		groupGrName = ""
		for glyph in item:
			if font.glyphs[glyph].script == "greek":
				if groupGr == False:
					groupGrName = glyph
					groupGr = True
				if left:
					font.glyphs[glyph].setLeftKerningGroup_(groupGrName)
				else:
					font.glyphs[glyph].setRightKerningGroup_(groupGrName)
			elif font.glyphs[glyph].script == "cyrillic":
				if groupCy == False:
					groupCyName = glyph
					groupCy = True
				if left:
					font.glyphs[glyph].setLeftKerningGroup_(groupCyName)
				else:
					font.glyphs[glyph].setRightKerningGroup_(groupCyName)
		if left:
			groupsR_GCref[key] = ["@MMK_R_"+groupGrName, "@MMK_R_"+groupCyName]
		else:
			groupsL_GCref[key] = ["@MMK_L_"+groupGrName, "@MMK_L_"+groupCyName]

duplicateGroup(groupsL, False)
duplicateGroup(groupsR, True)

def splitToGC(givenPair, greek):
	if greek == True: # if Greek
		script = "greek"
		bin = 0
	else:
		script = "cyrillic"
		bin = 1
	try:
		if givenPair[0] in groupsL_GCref or givenPair[1] in groupsR_GCref: # if either one of the pair uses group
			pairL = ""
			pairR = ""
			if givenPair[0] in groupsL_GCref:
				if groupsL_GCref[givenPair[0]][bin] != "@MMK_L_":
					pairL = groupsL_GCref[givenPair[0]][bin]
				else:
					if font.glyphs[groupsL[givenPair[0]][0]].category != "Letter":
						pairL = givenPair[0]
			elif font.glyphs[givenPair[0]]:
				if font.glyphs[givenPair[0]].script == script or font.glyphs[givenPair[0]].category != "Letter":
					pairL = givenPair[0]
			else:
				pairL = givenPair[0]

			if givenPair[1] in groupsR_GCref:
				if groupsR_GCref[givenPair[1]][bin] != "@MMK_R_":
					pairR = groupsR_GCref[givenPair[1]][bin]
				else:
					if font.glyphs[groupsR[givenPair[1]][0]].category != "Letter":
						pairR = givenPair[1]
			elif font.glyphs[givenPair[1]]:
				if font.glyphs[givenPair[1]].script == script or font.glyphs[givenPair[1]].category != "Letter":
					pairR = givenPair[1]
			else:
				pairR = givenPair[1]

			if pairL != "" and pairR != "":
				return pairL, pairR
			else:
				return None, None
		else:
			return None, None
	except:
		return None, None

for key, item in newKernDic.iteritems():
	for thisPair in item:
		newPairGL, newPairGR = splitToGC(thisPair, True) #Greek
		newPairCL, newPairCR = splitToGC(thisPair, False) #Cyrillic
		if newPairGL != None:
			font.setKerningForPair(key, newPairGL, newPairGR, thisPair[2])
		if newPairCR != None:
			font.setKerningForPair(key, newPairCL, newPairCR, thisPair[2])
		# will remove unncessary pairs, like Latin-Greek
		necessityL = 0 # 0=Greek or Cyrillic, 1=non-letter, 2=Latin
		necessityR = 0
		if thisPair[0] in groupsL: # if left is some kind of letter group
			if font.glyphs[groupsL[thisPair[0]][0]].script == "latin":
				necessityL = 2 # definitely Lain
		elif font.glyphs[thisPair[0]]:
			if font.glyphs[thisPair[0]].category == "Letter":
				if font.glyphs[thisPair[0]].script == "latin":
					necessityL = 2 # definitely Latin here!
			elif font.glyphs[thisPair[0]].category != "Letter":
				necessityL = 1
		else: # non-letter kerning group
			necessityL = 1

		if thisPair[1] in groupsR: # if right is some kind of letter group
			if font.glyphs[groupsR[thisPair[1]][0]].script == "latin":
				necessityR = 2 
		elif font.glyphs[thisPair[1]]:
			if font.glyphs[thisPair[1]].category == "Letter":
				if font.glyphs[thisPair[1]].script == "latin":
					necessityR = 2
			elif font.glyphs[thisPair[1]].category != "Letter":
				necessityR = 1
		else:
			necessityR = 1

		if (necessityL == 0 or necessityR == 0) and (necessityL == 2 or necessityR == 2 ):
			font.removeKerningForPair(key, thisPair[0], thisPair[1])

font.enableUpdateInterface() # re-enables UI updates in Font View