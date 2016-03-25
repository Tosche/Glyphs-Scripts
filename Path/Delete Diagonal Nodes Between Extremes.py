#MenuTitle: Delete Diagonal Nodes Between Extremes
# -*- coding: utf-8 -*-
__doc__="""
Good for cleaning TTF curve. It removes Diagonal Node Between Extremes, after placing the current outline in the background.
"""

import GlyphsApp
import math

thisFont = Glyphs.font # frontmost font
thisFontMaster = thisFont.selectedFontMaster # active master
listOfSelectedLayers = thisFont.selectedLayers # active layers of selected glyphs
selection = listOfSelectedLayers[0].selection # node selection in edit mode
thisDoc = Glyphs.currentDocument

def process( thisLayer ):
	for thisPath in thisLayer.paths:
		numOfNodes = len(thisPath.nodes)
		for i in range( -1, numOfNodes):
			try:
				hNode = thisPath.nodes[i-1]
				iNode = thisPath.nodes[i]
				jNode = thisPath.nodes[i+1]
				if iNode.type != GSCURVE: #if thisNode is on-curve
					if hNode.type == GSCURVE and jNode.type==GSCURVE:
						#diagonal cleaner
						try:
							if thisPath.nodes[i+3].x == thisPath.nodes[i+4].x or thisPath.nodes[i+3].y == thisPath.nodes[i+4].y or thisPath.nodes[i-3].x == thisPath.nodes[i-4].x or thisPath.nodes[i-3].y == thisPath.nodes[i-4].y:
								if hNode.x == jNode.x or hNode.y == jNode.y:
									pass
								else:
									boolx1 = hNode.x < iNode.x < jNode.x
									boolx2 = hNode.x > iNode.x > jNode.x
									booly1 = hNode.y < iNode.y < jNode.y
									booly2 = hNode.y > iNode.y > jNode.y
									if (boolx1 or boolx2) and (booly1 or booly2):
										atan2hi = math.atan2(iNode.y-hNode.y,iNode.x-hNode.x)
										atan2ij = math.atan2(jNode.y-iNode.y,jNode.x-iNode.x)
										if abs(atan2ij-atan2hi) < 0.1:
											thisPath.removeNodeCheckKeepShape_(iNode)
						except:
							pass

						#diagonal cleaner, exactly the same again
						try:
							if thisPath.nodes[i+3].x == thisPath.nodes[i+4].x or thisPath.nodes[i+3].y == thisPath.nodes[i+4].y or thisPath.nodes[i-3].x == thisPath.nodes[i-4].x or thisPath.nodes[i-3].y == thisPath.nodes[i-4].y:
								if hNode.x == jNode.x or hNode.y == jNode.y:
									pass
								else:
									boolx1 = hNode.x < iNode.x < jNode.x
									boolx2 = hNode.x > iNode.x > jNode.x
									booly1 = hNode.y < iNode.y < jNode.y
									booly2 = hNode.y > iNode.y > jNode.y
									if (boolx1 or boolx2) and (booly1 or booly2):
										atan2hi = math.atan2(iNode.y-hNode.y,iNode.x-hNode.x)
										atan2ij = math.atan2(jNode.y-iNode.y,jNode.x-iNode.x)
										if abs(atan2ij-atan2hi) < 0.1:
											thisPath.removeNodeCheckKeepShape_(iNode)
						except:
							pass

			except:
				pass

thisFont.disableUpdateInterface() # suppresses UI updates in Font View

for thisLayer in listOfSelectedLayers:
	thisGlyph = thisLayer.parent
	thisGlyph.beginUndo() # begin undo grouping
	for thisMaster in thisFont.masters:
		layer = thisGlyph.layers[thisMaster.id]
		layer.setBackground_(layer)
		process( layer )
	thisGlyph.endUndo()   # end undo grouping

thisFont.enableUpdateInterface() # re-enables UI updates in Font View
