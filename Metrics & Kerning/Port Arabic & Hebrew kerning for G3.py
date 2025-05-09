#MenuTitle: Port Arabic & Hebrew kerning for G3
# -*- coding: utf-8 -*-
__doc__ = """
Ports Arabic kerning data of G2 to G3 now that the kerning tables are separate.
Run only once on a file.
"""

from GlyphsApp import Glyphs

f = Glyphs.font

f.disableUpdateInterface()

RTLs = ('arabic', 'hebrew')

# Switch kerning group's sides and catalog them
RTLGroups = []
for g in f.glyphs:
	if g.category == 'Letter':
		if g.script in RTLs:
			oldL = g.rightKerningGroup
			oldR = g.leftKerningGroup
			oldLID = g.rightKerningGroupId()
			oldRID = g.leftKerningGroupId()
			g.rightKerningGroup = oldR
			g.leftKerningGroup = oldL
			if g.rightKerningGroupId() != None:
				RTLGroups.append(g.rightKerningGroupId())
			if g.leftKerningGroupId() != None:
				RTLGroups.append(g.leftKerningGroupId())

			if oldR != None:
				RTLGroups.append(oldRID)
			if oldL != None:
				RTLGroups.append(oldLID)

RTLGroups = set(RTLGroups)
# print(RTLGroups)


def verifyRTL(name):
	if name[0] == '@':
		if name in RTLGroups:
			return True
		else:
			return False
	elif f.glyphs[name].category == 'Letter':
		if f.glyphs[name].script in RTLs:
			return True
		return False
	else:
		return False


kd = Glyphs.font.kerningDictForDirection_(0)
pairsToRemove = []
for mas, firsts in kd.items():
	for fir, seconds in firsts.items():
		RTLFirst = verifyRTL(fir)
		for sec, val in seconds.items():
			RTLSecond = verifyRTL(sec)
			if any((RTLFirst, RTLSecond)) is True:
				newFir = fir.replace('_L', '_R') if fir[0] == '@' else f.glyphs[fir].id
				newSec = sec.replace('_R', '_L') if sec[0] == '@' else f.glyphs[sec].id
				# print(mas,newFir, newSec, val)
				f.setKerningForFontMasterID_LeftKey_RightKey_Value_direction_(mas, newFir, newSec, val, 2)
				pairsToRemove.append((mas, fir, sec))

for p in pairsToRemove:
	f.removeKerningForPair(p[0], p[1], p[2])

f.enableUpdateInterface()
