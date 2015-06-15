#MenuTitle: Display Unlocked Kerning Pairs
# -*- coding: utf-8 -*-
__doc__="""
Shows unlocked kerning pairs (exceptions) in the edit view.
String part done by Ben Jones, display part done by Toshi Omagari and Georg Seifert
"""

import GlyphsApp

Glyphs.clearLog()

font = Glyphs.font 

kernDict = font.kerningDict()
leftGroups = {}
rightGroups = {}
for g in font.glyphs:
	if g.rightKerningGroup:
		group_name = g.rightKerningGroupId()
		try:
			leftGroups[group_name].append(g.name)
		except:
			leftGroups[group_name] = [g.name]

	if g.leftKerningGroup:
		group_name = g.leftKerningGroupId()
		try:
			rightGroups[group_name].append(g.name)
		except:
			rightGroups[group_name] = [g.name]

# make glyphname:groupname dictionaries
left_members = dict((item, group) for group,sublist in leftGroups.items() for item in sublist)
right_members = dict((item, group) for group,sublist in rightGroups.items() for item in sublist)

editString = NSMutableAttributedString.alloc().init()
for m in font.masters:
	pairs = set()
	for left in kernDict[m.id].allKeys():
		rights = kernDict[m.id][left]
		for gn in rights:
			if left in left_members.keys():
				try:
					pairs.add('/{0}/{1}'.format(left, rightGroups[gn][0]))
				except KeyError:
					pairs.add('/{0}/{1}'.format(left, gn))
			elif gn in right_members.keys():
				try:
					pairs.add('/{0}/{1}'.format(leftGroups[left][0], gn))
				except KeyError:
					pairs.add('/{0}/{1}'.format(left, gn))
	string = '  '.join(sorted(pairs))
	charString = font.charStringFromDisplayString_(string)
	string  = NSString.stringWithFormat_('%@\n%@\n\n', m.name, charString)
	attribString = NSMutableAttributedString.alloc().initWithString_attributes_(string, { "GSLayerIdAttrib" : m.id })
	editString.appendAttributedString_(attribString)

if editString.length() > 0:
	try:
		Glyphs.currentDocument.windowController().activeEditViewController().graphicView().textStorage().setText_(editString)
	except:
		Glyphs.currentDocument.windowController().addTabWithString_("")
		Glyphs.currentDocument.windowController().activeEditViewController().graphicView().textStorage().setText_(editString)
