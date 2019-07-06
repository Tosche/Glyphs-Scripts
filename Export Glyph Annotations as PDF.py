#MenuTitle: Export Glyph Annotations as PDF
# -*- coding: utf-8 -*-
__doc__="""
Create effect for selected glyphs.
"""

import drawBot as d
import GlyphsApp
from datetime import date
today = date.today()
f = Glyphs.font
sf = 1000/f.upm
paperSize = "A4Landscape"
annoThickness = 3

d.newDrawing()
# Title page
d.newPage(paperSize)
margin = 20
d.font(".SF Compact Display Thin", 36)
creationDate = "%s %s %s" % (today.day,today.strftime("%B"),today.year)
d.text("%s\nPer-glyph Comments" % f.familyName, (margin*3, d.height()/2))

d.font(".SF Compact Display Regular", 10)
d.text(creationDate, margin, margin)

def new(layer, totalPages):
	d.newPage(paperSize)
	w,h = d.width(), d.height()

	m = l.associatedFontMaster()
	d.font(".SF Compact Text", 10)
	d.text("%s    %s" % (layer.parent.name, layer.name),(margin, margin))
	d.text("%s/%s" % (d.pageCount(), totalPages-1), (w-margin, margin), align="right")
	ma, md, mx, mc = m.ascender, m.descender, m.xHeight, m.capHeight
	zones = [az.position+az.size for az in m.alignmentZones]
	if len(zones) == 0:
		boundsTop, boundsBtm = ma, md
	else:
		boundsTop, boundsBtm = max(zones), min(zones)
	sf = float(h-margin*3)/(boundsTop-boundsBtm) #scalefactor
	d.scale(sf)
	wNew = w/sf # scaled paper size
	d.translate((margin/sf), -boundsBtm+(margin*2)/sf)

	# drawing metrics lines
	d.stroke(0,0,0,0.5)
	d.strokeWidth(0.5/sf)
	d.fill(None)
	lw = layer.width
	d.rect(0, md, lw, ma-md)
	d.line((0,mc), (lw,mc)) # x-height
	d.line((0,mx), (lw,mx)) # x-height
	d.line((0,0), (lw,0)) # baseline

	# alignment zones
	d.stroke(None)
	d.fill(0.7,0.3,0,0.1)
	for az in m.alignmentZones:
		d.rect(0, az.position, lw, az.size)

	# drawing nodes
	offcurves = []
	smooths = []
	sharps = []
	for p in layer.paths:
		smooths += [n for n in p.nodes if n.connection == GSSMOOTH]
		sharps += [n for n in p.nodes if n.type != OFFCURVE and n.connection != GSSMOOTH]
		offcurves += [n for n in p.nodes if n.type == OFFCURVE]
		d.stroke(0,0,0,0.2)
		for n in p.nodes:
			if n.type == OFFCURVE:
				if n.nextNode.type != OFFCURVE:
					d.line((n.x,n.y), (n.nextNode.x, n.nextNode.y))
				elif n.prevNode.type != OFFCURVE:
					d.line((n.prevNode.x,n.prevNode.y), (n.x, n.y))
	d.stroke(None)
	nodeSize = 3/sf
	hf = nodeSize/2 #half
	d.fill(0,0,1,0.5)
	for n in sharps:
		d.rect(n.x-hf, n.y-hf, nodeSize, nodeSize)
	d.fill(0,0.7,0,0.5)
	for n in smooths:
		d.oval(n.x-hf, n.y-hf, nodeSize, nodeSize)
	d.fill(0,0,0,0.2)
	for n in offcurves:
		d.oval(n.x-hf, n.y-hf, nodeSize, nodeSize)
	
	# drawing anchors
	d.stroke(None)
	d.fill(0.7,0.25,0.0,0.75)
	nodeSize = 4/sf
	hf = nodeSize * 0.7
	for a in layer.anchors:
		# print a, (ma, md, mc, mx, 0)
		if a.y in (ma, md, mc, mx, 0):
			d.polygon((a.x-hf, a.y),(a.x, a.y-hf),(a.x+hf,a.y), (a.x,a.y+hf), close=True)
		else:
			d.oval(a.x-hf, a.y-hf, nodeSize, nodeSize)
		
	# glyph outline
	d.fill(0,0,0,0.3)
	d.stroke(0,0,0,1)
	d.drawPath(layer.completeBezierPath)
	
	return sf, ma, md

def drawText(sf, ma, md, texts):
	if len(texts) != 0:
		columnX = (texts[0].parent().width+20/sf)
		d.stroke(None)
		d.fill(1,0,0,1)
		d.font(".SF Compact Text", 10/sf)
		columnText = ""
		for i, a in enumerate(texts):
			x, y, wid = a.x, a.y, a.width
			d.text(str(i+1), (x, y))
			columnText += "%s\t%s\n\n" % (i+1, a.text)
		t = d.FormattedString()
		t.fill(1,0,0,1)
		t.font(".SF Compact Text", 10/sf)
		t.firstLineIndent(-10/sf)
		t.tabs((10, "left"))
		t += columnText
		columnW = min(250/sf, (d.width()-margin)/sf-a.layer.bounds[1][0])
		d.textBox(t, (columnX, md, columnW, ma-md))

def drawArrow(sf, a):
	x, y, ang = a.x, a.y, a.angle
	path = d.BezierPath()
	path.moveTo((50,40))
	path.lineTo((0,0))
	path.lineTo((50,-40))
	path.moveTo((0,0))
	path.lineTo((120,0))
	path.closePath()
	# path.scale(sf)
	d.lineCap("round")
	d.lineJoin("round")
	path.rotate(ang, center=(0,0))
	path.translate(x,y)
	d.fill(None)
	d.stroke(1,0,0,0.5)
	d.strokeWidth(annoThickness/sf)
	d.drawPath(path)

def drawCircle(sf, a):
	x, y, wid = a.x, a.y, a.width
	d.fill(None)
	d.stroke(1,0,0,0.5)
	d.strokeWidth(annoThickness/sf)
	d.oval(x-wid,y-wid,wid*2,wid*2)

def drawPlusMinus(sf, a):
	x, y = a.x, a.y
	x, y, ang = a.x, a.y, a.angle
	path = d.BezierPath()
	path.moveTo((-50,0))
	path.lineTo((50,0))
	if a.type == PLUS:
		path.moveTo((0,50))
		path.lineTo((0,-50))
	path.closePath()
	# path.scale(1/sf)
	d.lineCap("round")
	d.lineJoin("round")
	path.translate(x,y)
	d.fill(None)
	d.stroke(1,0,0,0.5)
	d.strokeWidth(annoThickness/sf)
	d.drawPath(path)

totalPages = 0
for g in f.glyphs:
	totalPages += sum([1 for l in g.layers if l.annotations])

for g in f.glyphs:
	for l in g.layers:
		if l.annotations:
			sf, ma, md = new(l, totalPages) # draw new page and get scalefactor
			texts = []
			for a in l.annotations:
				if a.type == TEXT:
					texts += [a]
				elif a.type == ARROW:
					drawArrow(sf, a)
				elif a.type == CIRCLE:
					drawCircle(sf, a)
				elif a.type in (PLUS, MINUS):
					drawPlusMinus(sf, a)
			drawText(sf, ma, md, texts)

d.saveImage(["~/Desktop/A.pdf"])
d.endDrawing()