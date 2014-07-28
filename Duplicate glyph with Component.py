#MenuTitle: Duplicate with Component
# -*- coding: utf-8 -*-
__doc__="""
Duplicates selected glyphs but as components, giving them 001 suffix or above, depending on availability. Modified from Mekkablue's "Create .ssXX glyph from current layer" script.
"""

import GlyphsApp

Font = Glyphs.font
FirstMasterID = Font.masters[0].id
allGlyphNames = [ x.name for x in Font.glyphs ]
selectedLayers = Font.selectedLayers

def findSuffix( glyphName ):
	nameIsFree = False
	duplicateNumber = 0
	
	while nameIsFree is False:
		duplicateNumber += 1
		targetSuffix = ".0%.2d" % duplicateNumber
		targetGlyphName = glyphName + targetSuffix
		if allGlyphNames.count( targetGlyphName ) == 0:
			nameIsFree = True

	return targetSuffix

	
def process( sourceLayer ):
	# find suffix
	sourceGlyphName = sourceLayer.parent.name
	targetSuffix = findSuffix( sourceGlyphName )
	
	# append suffix, create glyph:
	targetGlyphName = sourceGlyphName + targetSuffix
	targetGlyph = GSGlyph( targetGlyphName )
	Font.glyphs.append( targetGlyph )

	# place component to all layers in the new glyph:
	sourceComponent = GSComponent( sourceGlyphName )
	for thisMaster in Font.masters:
		targetGlyph.layers[thisMaster.id].components.append(sourceComponent)
	print "Created", targetGlyphName 
	

for thisLayer in selectedLayers:
	process( thisLayer )

