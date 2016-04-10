#MenuTitle: Duplicate Glyph with Component
# -*- coding: utf-8 -*-
__doc__="""
Duplicates selected glyphs but as components, giving them 001 suffix or above depending on availability.
"""

import GlyphsApp

Font = Glyphs.font
FirstMasterID = Font.masters[0].id

def removeDuplicate(seq):
	seen = set()
	seen_add = seen.add
	return [x for x in seq if not (x in seen or seen_add(x))]

selectedLayers = removeDuplicate(Font.selectedLayers)

def removeSuffix(glyphName):
	try:
		if glyphName[-4] == "." and glyphName[-3:].isdigit:
			return glyphName[:-4]
	except:
		return glyphName

def findSuffix( glyphName ):
	glyphName = removeSuffix(glyphName)
	nameIsFree = False
	suffixNumber = 0
	while nameIsFree is False:
		suffixNumber += 1
		suffix = ".%03d" % suffixNumber
		if Font.glyphs[ glyphName+suffix ] == None:
			nameIsFree = True
		if suffixNumber == 100:
			break
	return suffix
	
def process( sourceLayer ):
	sourceGlyphName = sourceLayer.parent.name
	sourceGlyphName = removeSuffix(sourceGlyphName)
	targetSuffix = findSuffix( sourceGlyphName )
	# append suffix, create glyph:
	targetGlyphName = sourceGlyphName + targetSuffix
	targetGlyph = GSGlyph( targetGlyphName )
	Font.glyphs.append( targetGlyph )
	# place component to all layers in the new glyph:
	sourceComponent = GSComponent( sourceGlyphName )
	for thisMaster in Font.masters:
		targetGlyph.layers[thisMaster.id].components.append(sourceComponent)
		targetGlyph.layers[thisMaster.id].width = Font.glyphs[sourceGlyphName].layers[thisMaster.id].width
	print "Added", targetGlyphName 
	return Font.glyphs[targetGlyphName].layers[Font.selectedFontMaster.id]

targetLayers =[]
for thisLayer in selectedLayers:
	targetLayers.append( process(thisLayer) )

if Font.currentTab != None:
	theTab = Font.currentTab
	theTabLayers = theTab.layers
	insertPos = theTab.textCursor + theTab.textRange
	for layer in targetLayers:
		theTabLayers.insert(insertPos, layer)
		insertPos += 1
	theTab.layers = theTabLayers