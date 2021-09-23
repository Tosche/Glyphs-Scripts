#MenuTitle: Make .case alternates from selected glyphs
# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
__doc__="""
Duplicates selected glyphs but as components, giving them .case suffix and the sidebearings, also centering at the cap height.
"""

import GlyphsApp

f = Glyphs.font
allGlyphNames = [ g.name for g in f.glyphs ]
sel = f.selectedLayers

f.disableUpdateInterface()
for l in sel:
	# find suffix
	g = l.parent
	newGlyphName = '%s.case' % g.name

	if f.glyphs[newGlyphName] is None:
		newGlyph = GSGlyph( newGlyphName )
		f.glyphs.append( newGlyph )

	ng = f.glyphs[newGlyphName]

	ng.leftMetricsKey = g.leftMetricsKey if g.leftMetricsKey else g.name
	ng.rightMetricsKey = g.rightMetricsKey if g.rightMetricsKey else g.name

	for m in f.masters:
		ngl = ng.layers[m.id]
		ngl.shapes = []
		newComp = GSComponent( g )
		ngl.shapes.append(newComp)
		ngl.shapes[0].alignment = False
		currentCentre = ngl.bounds[0][1] + ngl.bounds[1][1]/2
		targetCentre = m.capHeight/2
		ngl.shapes[0].y += (targetCentre - currentCentre)
		ngl.syncMetrics()

f.enableUpdateInterface()