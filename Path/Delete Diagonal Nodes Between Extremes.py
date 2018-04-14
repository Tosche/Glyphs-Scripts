#MenuTitle: Delete Diagonal Nodes Between Extremes
# -*- coding: utf-8 -*-
__doc__="""
Good for cleaning TTF curve. It removes Diagonal Node Between Extremes, after placing the current outline in the background.
"""

import GlyphsApp
import math

f = Glyphs.font # frontmost font
sel = f.selectedLayers # active layers of selected glyphs

def deleteDiagonals( thisLayer ):
	for p in thisLayer.paths:
		numOfNodes = len(p.nodes)
		for i in range( -1, numOfNodes):
			try:
				hNode = p.nodes[i-1]
				iNode = p.nodes[i]
				jNode = p.nodes[i+1]
				if iNode.type != GSOFFCURVE: #if thisNode is on-curve
					if hNode.type == GSOFFCURVE and jNode.type == GSOFFCURVE:
						# on-curve now found
						# diagonal cleaner
						try:
							if p.nodes[i+2].x == p.nodes[i+3].x or p.nodes[i+2].y == p.nodes[i+3].y or p.nodes[i-2].x == p.nodes[i-3].x or p.nodes[i-2].y == p.nodes[i-3].y:
								if hNode.x == jNode.x or hNode.y == jNode.y:
									pass # because the node is extreme
								else:
									boolx1 = hNode.x < iNode.x < jNode.x
									boolx2 = hNode.x > iNode.x > jNode.x
									booly1 = hNode.y < iNode.y < jNode.y
									booly2 = hNode.y > iNode.y > jNode.y
									if (boolx1 or boolx2) and (booly1 or booly2):
										atan2hi = math.atan2(iNode.y-hNode.y,iNode.x-hNode.x)
										atan2ij = math.atan2(jNode.y-iNode.y,jNode.x-iNode.x)
										if abs(atan2ij-atan2hi) < 0.1:
											p.removeNodeCheckKeepShape_(iNode)
						except:
							pass
			except:
				pass

f.disableUpdateInterface() # suppresses UI updates in Font View

for l in sel:
	g = l.parent
	g.beginUndo() # begin undo grouping
	l.setBackground_(l)
	deleteDiagonals( l )
	deleteDiagonals( l ) # run the process again, just to make sure
	g.endUndo()   # end undo grouping

f.enableUpdateInterface() # re-enables UI updates in Font View
