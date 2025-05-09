#MenuTitle: Split Lat-Grk-Cyr Kerning
# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
__doc__ = """
Splits kerning groups of LGC (Latin, Greek, Cyrillic) and reconstructs kerning accordingly.
Kern once, split later.
"""

from GlyphsApp import Glyphs
# import traceback

f = Glyphs.font  # frontmost f

f.disableUpdateInterface()  # suppresses UI updates in f View
Glyphs.clearLog()

kernDic = f.kerningDictForDirection_(0)
newKernDic = {}
for m in f.masters:
	kernList = []
	for l, rs in kernDic[m.id].items():
		for r, v in rs.items():
			pairInList = [l, r, v]
			kernList.append(pairInList)
		newKernDic[m.id] = kernList

# dictionary of groups, each value containg a list of glyphs involved.
# groupsL/R[groupName][glyph, glyph, glyph...]
groupsL = {}
groupsR = {}
for g in f.glyphs:
	if g.category == "Letter":
		if g.leftKerningGroupId() != None:
			if not g.leftKerningGroupId() in groupsR:
				groupsR[g.leftKerningGroupId()] = []
			groupsR[g.leftKerningGroupId()].append(g.name)

		if g.rightKerningGroupId() != None:
			if not g.rightKerningGroupId() in groupsL:
				groupsL[g.rightKerningGroupId()] = []
			groupsL[g.rightKerningGroupId()].append(g.name)

groupsL_GCref = groupsL.copy()
groupsR_GCref = groupsR.copy()


def duplicateGroup(group, left):
	for groupName, glyphNames in group.items():
		groupCy = False
		groupCyName = ""
		groupGr = False
		groupGrName = ""
		for gn in glyphNames:
			if f.glyphs[gn].script == "greek":
				if groupGr == False:
					groupGrName = gn
					groupGr = True
				if left:
					f.glyphs[gn].setLeftKerningGroup_(groupGrName)
				else:
					f.glyphs[gn].setRightKerningGroup_(groupGrName)
			elif f.glyphs[gn].script == "cyrillic":
				if groupCy == False:
					groupCyName = gn
					groupCy = True
				if left:
					f.glyphs[gn].setLeftKerningGroup_(groupCyName)
				else:
					f.glyphs[gn].setRightKerningGroup_(groupCyName)
		if left:
			groupsR_GCref[groupName] = ["@MMK_R_" + groupGrName, "@MMK_R_" + groupCyName]
		else:
			groupsL_GCref[groupName] = ["@MMK_L_" + groupGrName, "@MMK_L_" + groupCyName]


duplicateGroup(groupsL, False)
duplicateGroup(groupsR, True)


def splitToGC(thePair, greek):
	if greek == True:  # if Greek
		script = "greek"
		bin = 0
	else:
		script = "cyrillic"
		bin = 1
	try:
		if thePair[0] in groupsL_GCref or thePair[1] in groupsR_GCref:  # if either one of the pair uses group
			pairL = ""
			pairR = ""
			if thePair[0] in groupsL_GCref:
				if groupsL_GCref[thePair[0]][bin] != "@MMK_L_":
					pairL = groupsL_GCref[thePair[0]][bin]
				else:
					if f.glyphs[groupsL[thePair[0]][0]].category != "Letter":
						pairL = thePair[0]
			elif f.glyphs[thePair[0]]:
				if f.glyphs[thePair[0]].script == script or f.glyphs[thePair[0]].category != "Letter":
					pairL = thePair[0]
			else:
				pairL = thePair[0]

			if thePair[1] in groupsR_GCref:
				if groupsR_GCref[thePair[1]][bin] != "@MMK_R_":
					pairR = groupsR_GCref[thePair[1]][bin]
				else:
					if f.glyphs[groupsR[thePair[1]][0]].category != "Letter":
						pairR = thePair[1]
			elif f.glyphs[thePair[1]]:
				if f.glyphs[thePair[1]].script == script or f.glyphs[thePair[1]].category != "Letter":
					pairR = thePair[1]
			else:
				pairR = thePair[1]

			if pairL != "" and pairR != "":
				return pairL, pairR
			else:
				return None, None
		else:
			return None, None
	except:
		return None, None


for mID, pairs in newKernDic.items():
	for thisPair in pairs:
		newPairGL, newPairGR = splitToGC(thisPair, True)  # Greek
		newPairCL, newPairCR = splitToGC(thisPair, False)  # Cyrillic
		if newPairGL != None:
			f.setKerningForPair(mID, newPairGL, newPairGR, thisPair[2])
		if newPairCR != None:
			f.setKerningForPair(mID, newPairCL, newPairCR, thisPair[2])
		# will remove unncessary pairs, like Latin-Greek
		necessityL = 0  # 0=Greek or Cyrillic, 1=non-letter, 2=Latin
		necessityR = 0
		if thisPair[0] in groupsL:  # if left is some kind of letter group
			if f.glyphs[groupsL[thisPair[0]][0]].script == "latin":
				necessityL = 2  # definitely Lain
		elif f.glyphs[thisPair[0]]:
			if f.glyphs[thisPair[0]].category == "Letter":
				if f.glyphs[thisPair[0]].script == "latin":
					necessityL = 2  # definitely Latin here!
			elif f.glyphs[thisPair[0]].category != "Letter":
				necessityL = 1
		else:  # non-letter kerning group
			necessityL = 1

		if thisPair[1] in groupsR:  # if right is some kind of letter group
			if f.glyphs[groupsR[thisPair[1]][0]].script == "latin":
				necessityR = 2
		elif f.glyphs[thisPair[1]]:
			if f.glyphs[thisPair[1]].category == "Letter":
				if f.glyphs[thisPair[1]].script == "latin":
					necessityR = 2
			elif f.glyphs[thisPair[1]].category != "Letter":
				necessityR = 1
		else:
			necessityR = 1

		if (necessityL == 0 or necessityR == 0) and (necessityL == 2 or necessityR == 2):
			f.removeKerningForPair(mID, thisPair[0], thisPair[1])

f.enableUpdateInterface()  # re-enables UI updates in f View
