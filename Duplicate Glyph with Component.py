#MenuTitle: Duplicate Glyph with Component
# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
__doc__="""
Duplicates selected glyphs but as components, giving them 001 suffix or above depending on availability.
"""

import GlyphsApp

f = Glyphs.font

# returns the base glyph name without ".00X" suffix.
# I'm doing it just in case the selected glyph already has such suffix.
def removeSuffix(glyphName):
	try:
		if glyphName[-4] == "." and glyphName[-3:].isdigit:
			return glyphName[:-4]
	except: # glyph name too short, passes the test without removal
		return glyphName

# returns the smallest available suffix number. Tries up to .100
def findSuffix( glyphName ):
	glyphName = removeSuffix(glyphName)
	for i in range(1, 100):
		suffix =".%03d" % i
		# if glyph name available, stop loop early
		if f.glyphs[ glyphName + suffix ] == None:
			break
	return suffix

newGlyphs = []
# make set first before iteration to avoid running multiple times
# on the same glyph (that can happen if ran from Edit View)
for l in set(f.selectedLayers):
	originGlyph = l.parent

	# prepare new glyph name
	newGlyphNameBase = removeSuffix( originGlyph.name )
	newSuffix = findSuffix( newGlyphNameBase )
	newGlyphName = newGlyphNameBase + newSuffix

	# add new glyph
	newGlyph = GSGlyph( newGlyphName )
	f.glyphs.append( newGlyph )

	# newGlyph is currently empty.
	# Place component to all layers in it.
	for m in f.masters:
		c = GSComponent( originGlyph.name )
		c.alignment = True
		newGlyph.layers[m.id].components.append( c )
		# Setting width may be unncessary since component is auto-aligned
		newGlyph.layers[m.id].width = originGlyph.layers[m.id].width
	print("Added", newGlyphName )
	newGlyphs.append( newGlyph )

# if the script was ran from Edit view, show the added glyphs
if f.currentTab != None:
	masterID = f.selectedFontMaster.id
	theTab = f.currentTab
	theTabLayers = list(theTab.layers)
	insertPos = theTab.textCursor + theTab.textRange
	for g in newGlyphs:
		layer = g.layers[masterID]
		theTabLayers.insert(insertPos, layer)
		insertPos += 1
	theTab.layers = theTabLayers