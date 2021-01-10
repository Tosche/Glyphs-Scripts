 #MenuTitle: New Tab With Unlocked Kerning Pairs
# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
__doc__="""
Shows unlocked kerning pairs (exceptions) in the edit view.
String part done by Ben Jones, display part done by Toshi Omagari and Georg Seifert
"""

import GlyphsApp
from AppKit import NSAffineTransform, NSString, NSMutableAttributedString

Glyphs.clearLog()

f = Glyphs.font

if Glyphs.versionNumber >= 3.0:
	kernDict = f.kerning
else:
	kernDict = f.kerningDict()

# make groupname:glyphname dictionaries.
leftGroups = {}
rightGroups = {}
for g in f.glyphs:
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
for m in f.masters:
	pairs = set()
	for L in kernDict[m.id].keys():
		rights = kernDict[m.id][L]
		if Glyphs.versionNumber >= 3.0 and L[0] != '@': # it's likely this is a glyph ID
			L = f.glyphForId_(L).name # Glyphs 3 uses glyph ID for single glyphs, whereas 2 uses names
		for R in rights.keys():
			if Glyphs.versionNumber >= 3.0 and R[0] != '@':
				R = f.glyphForId_(R).name
			if L in left_members.keys(): # if left is a single glyph
				try:
					pairs.add('/{0}/{1}'.format(L, rightGroups[R][0]))
				except KeyError:
					pairs.add('/{0}/{1}'.format(L, R))
			elif R in right_members.keys():
				try:
					pairs.add('/{0}/{1}'.format(leftGroups[L][0], R))
				except KeyError:
					pairs.add('/{0}/{1}'.format(L, R))

	string = '  '.join(sorted(pairs))
	charString = f.charStringFromDisplayString_(string)
	string  = NSString.stringWithFormat_('%@\n%@\n\n', m.name, charString)
	attribString = NSMutableAttributedString.alloc().initWithString_attributes_(string, { "GSLayerIdAttrib" : m.id })
	editString.appendAttributedString_(attribString)

if editString.length() > 0:
	try:
		Glyphs.currentDocument.windowController().activeEditViewController().graphicView().textStorage().setText_(editString)
	except:
		Glyphs.currentDocument.windowController().addTabWithString_("")
		Glyphs.currentDocument.windowController().activeEditViewController().graphicView().textStorage().setText_(editString)
