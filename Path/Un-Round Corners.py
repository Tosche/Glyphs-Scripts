#MenuTitle: Un-Round Corners
# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
__doc__ = """
Removes corners of outlines of the selected letters (current master only).
1. It doesn't do perfect job at curved segments, but does keep the original in the background. Please fine-tune by hand.
2. If it creates really funny results, try changing start node position.
3. It might miss corners with big round radius. You can change the roundness at line 16.
4. The script assumes there is no extreme point in the corner.
"""

from GlyphsApp import Glyphs, GSCURVE, GSOFFCURVE, GSLINE, GSSHARP

thisFont = Glyphs.font  # frontmost font
listOfSelectedLayers = thisFont.selectedLayers  # active layers of selected glyphs

roundness = 30

thisFont.disableUpdateInterface()  # suppresses UI updates in Font View


def line(p1, p2):
	A = (p1[1] - p2[1])
	B = (p2[0] - p1[0])
	C = (p1[0] * p2[1] - p2[0] * p1[1])
	return A, B, -C


def intersection(L1, L2):
	D = L1[0] * L2[1] - L1[1] * L2[0]
	Dx = L1[2] * L2[1] - L1[1] * L2[2]
	Dy = L1[0] * L2[2] - L1[2] * L2[0]
	if D != 0:
		x = Dx / D
		y = Dy / D
		return x, y
	else:
		return False


def nudge(oncurveMv, offcurve1, offcurve2, oncurveSt, offsetX, offsetY):
	distanceX = oncurveMv.x - oncurveSt.x
	distanceX1 = oncurveMv.x - offcurve1.x
	distanceX2 = offcurve2.x - oncurveSt.x
	if distanceX1 != 0:
		offcurve1.x += (1 - distanceX1 / distanceX) * offsetX
	else:
		offcurve1.x += offsetX

	if distanceX2 != 0:
		offcurve2.x += (distanceX2 / distanceX) * offsetX

	distanceY = oncurveMv.y - oncurveSt.y
	distanceY1 = oncurveMv.y - offcurve1.y
	distanceY2 = offcurve2.y - oncurveSt.y
	if distanceY1 != 0:
		offcurve1.y += (1 - distanceY1 / distanceY) * offsetY
	else:
		offcurve1.y += offsetY

	if distanceY2 != 0:
		offcurve2.y += (distanceY2 / distanceY) * offsetY

	oncurveMv.x += offsetX
	oncurveMv.y += offsetY


def sharpen(path, n):
	if path.nodes[n + 4]:
		node0 = path.nodes[n - 1]
		node1 = path.nodes[n]
		node2 = path.nodes[n + 1]
		node3 = path.nodes[n + 2]
		node4 = path.nodes[n + 3]
		node5 = path.nodes[n + 4]
		# node2 and 3 should be the offcurve points in question.
		# if it starts from straight segment to straight
		if node0.type != GSOFFCURVE and node1.type == GSLINE and node2.type == GSOFFCURVE and node3.type == GSOFFCURVE and node4.type != GSOFFCURVE and node5.type == GSLINE:
			if abs(node1.x - node4.x) <= roundness and abs(node1.y - node4.y) <= roundness:
				L1 = line(node0.position, node1.position)
				L2 = line(node4.position, node5.position)
				R = intersection(L1, L2)
				path.removeNodeAtIndex_(n + 1)
				path.removeNodeAtIndex_(n + 1)
				path.removeNodeAtIndex_(n + 1)
				node1.position = R
				node1.type = GSLINE
				node1.connection = GSSHARP
				return True
		# if it starts from curved segment to straight
		elif node0.type == GSOFFCURVE and node1.type != GSOFFCURVE and node2.type == GSOFFCURVE and node3.type == GSOFFCURVE and node4.type != GSOFFCURVE and node5.type == GSLINE:
			if abs(node1.x - node4.x) <= roundness and abs(node1.y - node4.y) <= roundness:
				L1 = line(node0.position, node1.position)
				L2 = line(node4.position, node5.position)
				R = intersection(L1, L2)
				path.removeNodeAtIndex_(n + 1)
				path.removeNodeAtIndex_(n + 1)
				path.removeNodeAtIndex_(n + 1)
				offsetX = R[0] - path.nodes[n].x
				offsetY = R[1] - path.nodes[n].y
				nudge(path.nodes[n], path.nodes[n - 1], path.nodes[n - 2], path.nodes[n - 3], offsetX, offsetY)
				path.nodes[n].type = GSCURVE
				path.nodes[n].connection = GSSHARP
				return True
		# if it starts from straight segemt to curve
		elif node0.type == GSCURVE and node1.type == GSLINE and node2.type == GSOFFCURVE and node3.type == GSOFFCURVE and node4.type == GSCURVE and node5.type == GSOFFCURVE:
			if abs(node1.x - node4.x) <= roundness and abs(node1.y - node4.y) <= roundness:
				L1 = line(node0.position, node1.position)
				L2 = line(node4.position, node5.position)
				R = intersection(L1, L2)
				path.nodes[n - 1].type = GSCURVE
				path.nodes[n - 1].connection = GSSHARP
				path.removeNodeAtIndex_(n)
				path.removeNodeAtIndex_(n)
				path.removeNodeAtIndex_(n)
				path.nodes[n].type = GSLINE
				path.nodes[n].connection = GSSHARP
				offsetX = R[0] - path.nodes[n].x
				offsetY = R[1] - path.nodes[n].y
				nudge(path.nodes[n], path.nodes[n + 1], path.nodes[n + 2], path.nodes[n + 3], offsetX, offsetY)
				return True
		else:
			return False


def unRound(thisLayer):
	try:
		thisLayer.setBackground_(thisLayer)
		for thisPath in thisLayer.paths:
			nodeTotal = len(thisPath.nodes)
			for i in range(len(thisPath.nodes)):
				if i >= nodeTotal - 1:  # it's weird, but this is the way to avoid first node error.
					sharpen(thisPath, -1)
					break
				elif sharpen(thisPath, i):
					nodeTotal -= 3

	except Exception as e:
		Glyphs.showMacroWindow()
		print("Un-Round Corners Error (unRound): %s" % e)


for thisLayer in listOfSelectedLayers:
	thisGlyph = thisLayer.parent
	thisGlyph.beginUndo()  # begin undo grouping
	thisGlyph.name
	unRound(thisLayer)
	thisGlyph.endUndo()   # end undo grouping

# brings macro window to front and clears its log:

thisFont.enableUpdateInterface()  # re-enables UI updates in Font View
