#MenuTitle: Create .case alternate
# -*- coding: utf-8 -*-
__doc__="""
Duplicates selected glyphs but as components, giving them .case suffix and the sidebearings. Modified from Mekkablue's "Create .ssXX glyph from current layer" script.
"""

import GlyphsApp

Font = Glyphs.font
FirstMasterID = Font.masters[0].id
allGlyphNames = [ x.name for x in Font.glyphs ]
selectedLayers = Font.selectedLayers

def findSuffix( glyphName ):
	nameIsFree = False
	duplicateNumber = -1
	
	while nameIsFree is False:
		duplicateNumber += 1
		targetSuffix = "case.0%.2d" % duplicateNumber
		targetGlyphName = glyphName + targetSuffix
		if allGlyphNames.count( targetGlyphName ) == 0:
			nameIsFree = True
	if targetSuffix == "case.000";
		targetSuffix = "case"
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
		targetGlyph.layers[thisMaster.id].setLeftMetricsKey_(sourceGlyphName)
		targetGlyph.layers[thisMaster.id].setRightMetricsKey_(sourceGlyphName)
	print "Created", targetGlyphName 
	
for thisLayer in selectedLayers:
	process( thisLayer )

