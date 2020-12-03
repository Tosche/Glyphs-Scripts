#MenuTitle: Delete Diagonal Nodes Between Extremes
# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
__doc__="""
Good for cleaning TTF curve. It removes Diagonal Node Between Extremes, after placing the current outline in the background.
"""

import GlyphsApp
import math

f = Glyphs.font # frontmost font
sel = f.selectedLayers # active layers of selected glyphs

def deleteDiagonals( thisLayer ):
	for pathindex, p in enumerate(thisLayer.paths):
		for nodeindex, n in enumerate(p.nodes):
			try:
				nPrev1 = n.prevNode
				nPrev2 = nPrev1.prevNode
				nPrev3 = nPrev2.prevNode
				nNext1 = n.nextNode
				nNext2 = nNext1.nextNode
				nNext3 = nNext2.nextNode

				if n.type != GSOFFCURVE: #if thisNode is on-curve
					if nPrev1.type == GSOFFCURVE and nNext1.type == GSOFFCURVE: # if n is sandwiched by off-curves
						try:
							if nNext2.x == nNext3.x or nNext2.y == nNext3.y or nPrev2.x == nPrev3.x or nPrev2.y == nPrev3.y:
								if nPrev1.x == nNext1.x or nPrev1.y == nNext1.y:
									pass # because n is extreme
								else:
									boolx1 = nPrev1.x < n.x < nNext1.x
									boolx2 = nPrev1.x > n.x > nNext1.x
									booly1 = nPrev1.y < n.y < nNext1.y
									booly2 = nPrev1.y > n.y > nNext1.y
									if (boolx1 or boolx2) and (booly1 or booly2):
										atan2hi = math.atan2(n.y-nPrev1.y,n.x-nPrev1.x)
										atan2ij = math.atan2(nNext1.y-n.y,nNext1.x-n.x)

										# check if n is an inflection point
										if abs(atan2ij-atan2hi) < 0.1:
											dupLayer = thisLayer.copy()
											dupPath = dupLayer.paths[pathindex]
											dupNode = dupPath.nodes[nodeindex]
											dupPath.removeNodeCheckKeepShape_(dupNode)
											nodesBefore = len(dupPath.nodes)
											dupLayer.addInflectionPoints()
											nodesAfter = len(dupPath.nodes)
											
											if (nodesBefore == nodesAfter):
												p.removeNodeCheckKeepShape_(n)
						except:
							pass
			except:
				pass

f.disableUpdateInterface() # suppresses UI updates in Font View

for l in sel:
	g = l.parent
	g.beginUndo() # begin undo grouping
	l.setBackground_(l)
	deleteDiagonals(l)
	deleteDiagonals(l) # run the process again, just to make sure
	g.endUndo()   # end undo grouping

f.enableUpdateInterface() # re-enables UI updates in Font View
