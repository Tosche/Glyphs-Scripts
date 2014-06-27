#MenuTitle: Generate ss20 for All-Glyph Access
# -*- coding: utf-8 -*-
__doc__="""
Writes OpenType ss20 feature for all glyphs in the font. Copy glyphs names with slashes (e.g. /Aringacute) and paste it to an OpenType-savvy application, and activate ss20 to see the glyphs.
"""

import GlyphsApp

thisFont = Glyphs.font # frontmost font
featureLineList = []
fontFeatures = thisFont.features

nonLetter = {"_":"underscore", "-":"hyphen", ".":"period", "0":"zero", "1":"one", "2":"two", "3":"three", "4":"four", "5":"five", "6":"six", "7":"seven", "8":"eight", "9":"nine"}

def replaceNonLetter(text, dictionary):
	for key in dictionary:
		text = text.replace(key, dictionary[key])
	return text

thisFont.disableUpdateInterface() # suppresses UI updates in Font View

for thisGlyph in thisFont.glyphs:
	if thisGlyph.export:
		thisGlyphName = thisGlyph.name
		spacedThisGlyphName = " ".join(thisGlyphName)
		if any(x in nonLetter.keys() for x in spacedThisGlyphName):
			spacedThisGlyphName = replaceNonLetter(spacedThisGlyphName, nonLetter)
		featureLine = "sub slash " + spacedThisGlyphName + " by %s;" % thisGlyphName
		featureLineList.append(featureLine)

featureLineList.sort(key = len)
featureLineList.reverse()

if "ss20" in [f.name for f in fontFeatures]:
	ss20Feature = thisFont.features["ss20"]
	ss20Feature.code = "\n".join(featureLineList)
else:
	ss20Feature = GSFeature()
	ss20Feature.name = "ss20"
	ss20Feature.code = "\n".join(featureLineList)
	thisFont.features.append(ss20Feature)

thisFont.enableUpdateInterface() # re-enables UI updates in Font View
