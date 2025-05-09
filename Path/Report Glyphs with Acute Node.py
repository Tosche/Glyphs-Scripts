#MenuTitle: Report Glyphs with Acute-angled Node
# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
__doc__ = """
Reports glyphs that have nodes with very acute angle (default: less than 15 degrees).
"""

from GlyphsApp import Glyphs
import math

# The user can change this value.
checkAngle = 15

thisFont = Glyphs.font  # frontmost font
thisFontMaster = thisFont.selectedFontMaster  # active master
listOfSelectedLayers = thisFont.selectedLayers  # active layers of selected glyphs
selection = listOfSelectedLayers[0].selection()  # node selection in edit mode
thisDoc = Glyphs.currentDocument


def compareAngle(node1, node2, node3):
	x1 = node1.x - node2.x
	y1 = node1.y - node2.y
	x2 = node3.x - node2.x
	y2 = node3.y - node2.y
	if x1 == 0.0 and x2 == 0.0 and any(s < 0 for s in [y1, y2]):
		return False
	elif y1 == 0.0 and y2 == 0.0 and any(s < 0 for s in [x1, x2]):
		return False
	innerProduct = x1 * x2 + y1 * y2
	len1 = math.hypot(x1, y1)
	len2 = math.hypot(x2, y2)
	try:
		acosine = math.acos(innerProduct / (len1 * len2))
	except:
		return False
	ang = abs(acosine * 180 / math.pi)
	if ang >= 180:
		ang = 360 - ang
	if ang < checkAngle:
		return True
	else:
		return False


Glyphs.clearLog()
print("Following glyphs have a very acute corner point, at less than %s degrees:" % checkAngle)


def process(thisLayer):
	for thisPath in thisLayer.paths:
		for thisPath in thisLayer.paths:
			numOfNodes = len(thisPath.nodes)
			for i in range(numOfNodes):
				node = thisPath.nodes[i]
				if node.type != 65:
					nodeBefore = thisPath.nodes[i - 1]
					nodeAfter = thisPath.nodes[i + 1]
					if compareAngle(nodeBefore, node, nodeAfter):
						print("%s in %s" % (thisLayer.parent.name, thisMaster.name))
						return


for thisGlyph in thisFont.glyphs:
	for thisMaster in thisFont.masters:
		process(thisGlyph.layers[thisMaster.id])

Glyphs.showMacroWindow()
