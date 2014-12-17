#MenuTitle: Export InDesign Tagged Text with All Glyphs
# -*- coding: utf-8 -*-
__doc__="""
Saves InDesign tagged text file that contains all glyphs for typesetting a specimen, using glyph ID. This is a better solution than generating ss20 feature.
"""

import GlyphsApp
import os.path

thisFont = Glyphs.font # frontmost font
thisFontMaster = thisFont.selectedFontMaster # active master
selectedLayers = thisFont.selectedLayers # active layers of selected glyphs
thisDoc = Glyphs.currentDocument



instanceList = []
for thisInstance in thisFont.instances:
	if thisInstance.active:
		instanceList.append(thisInstance.name)

glyphCount = 0
for glyph in thisFont.glyphs:
	if glyph.export:
		glyphCount += 1


for instance in instanceList:
	paraStyleName = "%s %s 12pt" % (thisFont.familyName, instance)

	header = "<ASCII-MAC>\n<Version:7.5><FeatureSet:InDesign-Roman><ColorTable:=<Black:COLOR:CMYK:Process:0,0,0,1>>\n<DefineParaStyle:%s=<cSize:12.000000><cTypeface:%s><cFont:%s><cOTFContAlt:0>>\n" % (paraStyleName, instance, thisFont.familyName)

	line = ""
	for i in range(glyphCount-1):
		line += "<ParaStyle:%s><cSpecialGlyph:%s><0xFFFD>" % (paraStyleName, i+1)

	try:
		directory = "the same folder as the working file"
		dirPath = os.path.dirname(thisFont.filepath)
	except:
		directory = "the Documents folder, because the source is not a saved Glyphs file"
		dirPath = filepath = os.path.abspath(expanduser("~/") + '/Documents')
	filePath = os.path.abspath(dirPath+"/InDesign Tagged Text - %s %s.txt" % (thisFont.familyName, instance))
	with open(filePath, 'w') as thisFile:
		thisFile.write(header+line)
		thisFile.close

Glyphs.displayDialog_(u'Tagged text files saved in %s (overwitten existing tagged texts if they exist). Please follow the instruction:\n\n1. Generate the font and make it available in InDesign (okay to do it before running this script).\n\n2. In InDesign, have a document open. Go to "File > Place", choose the generated text file, and place it somewhere in the document.\n\n3. Voilà! Now you have all glyphs, referred to in Glyph ID.' % directory)