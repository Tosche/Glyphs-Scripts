#MenuTitle: Export Tagged Text with All Glyphs for InDesign
# -*- coding: utf-8 -*-
__doc__="""
Saves tagged Text file that contains all glyphs for typesetting a specimen in InDesign, using glyph ID. This is a better solution than generating ss20 feature.
"""

import GlyphsApp
import os.path

thisFont = Glyphs.font # frontmost font
thisFontMaster = thisFont.selectedFontMaster # active master
selectedLayers = thisFont.selectedLayers # active layers of selected glyphs
thisDoc = Glyphs.currentDocument

paraStyleName = thisFont.familyName + " 12pt"

instanceList = []
for thisInstance in thisFont.instances:
	if thisInstance.active:
		instanceList.append(thisInstance.name)

line = ""
for i in range(len(thisFont.glyphs)):
	line += "<ParaStyle:%s><cSpecialGlyph:%s><0xFFFD>" % (styleName, i+1)

for item in instanceList:
	header = "<ASCII-MAC>\n<Version:7.5><FeatureSet:InDesign-Roman><ColorTable:=<Black:COLOR:CMYK:Process:0,0,0,1>>\n<DefineParaStyle:%s=<cSize:12.000000>%s<cFont:%s><cOTFContAlt:0>>\n" % (paraStyleName, item, thisFont.familyName)
	try:
		directory = "the same folder as the working file"
		dirPath = os.path.dirname(thisFont.filepath)
	except:
		directory = "the Documents folder, because the source is not a saved Glyphs file"
		dirPath = filepath = abspath(expanduser("~/") + '/Documents')
	filePath = abspath(dirPath+"/Tagged Text - %s %s.txt" % (thisFont.familyName, item))
	with open(filePath, 'w') as thisFile:
		thisFile.write(header+line)
		thisFile.close

Glyphs.displayDialog_(u'Tagged text file(s) saved in %s. Please follow the instruction:\n\n1. Generate the font and make it available in InDesign (okay to do it before running this script).\n\n2. In InDesign, have a document open. Go to "File > Place", choose the generated text file, and place it somewhere in the document.\n\n3. Voilà! Now you have all glyphs, referred to in Glyph ID.' % directory)