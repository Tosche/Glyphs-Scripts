#MenuTitle: Report Compatibility by Numbers
# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
__doc__="""
Outputs path count, node count, anchor count etc. of selected glyphs in the Macro Window.
"""

import GlyphsApp

font = Glyphs.font # frontmost font
fontMaster = font.selectedFontMaster # active master
selectedLayers = font.selectedLayers # active layers of selected glyphs
thisDoc = Glyphs.currentDocument

font.disableUpdateInterface() # suppresses UI updates in Font View
Glyphs.clearLog()

for layer in selectedLayers:
	glyph = layer.parent
	print(glyph.name)
	for l in glyph.layers:
		if l.pathCount() == 1:
			pathCount = "1 path"
		else:
			pathCount = str(l.pathCount()) + " paths"
		nCount = 0
		for p in l.paths:
			nCount += len(p.nodes)
		print("\t%s\n\t\t%s, %s nodes, %s components, %s anchors" % (l.name, pathCount, nCount, l.componentCount(), len(l.anchors)))
		for i in range(len(l.paths)):
			nodeCount = len(l.paths[i].nodes)
			offcurveCount = 0
			for n in l.paths[i].nodes:
				if n.type == 65:
					offcurveCount += 1
			print("\t\tpath %s: %s nodes (%s on-curve, %s off-curve)" % (i+1, nodeCount, nodeCount-offcurveCount, offcurveCount))
	print
font.enableUpdateInterface() # re-enables UI updates in Font View
Glyphs.showMacroWindow()