#MenuTitle: DrawBot Samples
# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
__doc__="""
Create effect for selected glyphs.
"""

import GlyphsApp

f = Glyphs.font # frontmost font
m = f.selectedFontMaster # active master
try:
	sel = f.selectedLayers # active layers of selected glyphs
	l0 = sel[0]
except:
	Glyphs.ShowMacroWindow()
	print("Please select a few glyphs for demo purpose.")

import drawBot as d
import subprocess # used for showing the saved PDF in Finder after exporting

paperSize = "Letter"
# Other sizes "A4" "A3Landscape"... are also available

d.newDrawing() # resets drawing so that the script doesn't inherit the previous run



# 1 Calling glyphs by name: capital A in the current master
try:
	d.newPage(paperSize)
	path = f.glyphs["A"].layers[m.id].completeBezierPath
	d.drawPath(path)
except:
	pass



d.newPage(paperSize) # blank page



# 2 draw selected glyphs
for l in sel:
	d.newPage(paperSize)
	path = l.completeBezierPath # outlines including paths and components
	d.drawPath(path)

	# draw every corner point
	corners = []
	for p in l.paths:
		for n in p.nodes:
			if n.type == GSLINE:
				corners.append(n)
			elif n.type == GSCURVE and n.connection == 0:
				corners.append(n)
	radius = 3
	d.fill(None)
	d.stroke(0,1,0,1)
	for c in corners:
		d.rect(c.x-radius, c.y-radius, radius*2, radius*2)

	# draw anchors as circles
	radius = 5
	d.fill(1, 0.5, 0, 1) # set orange colour for fill
	d.stroke(0, 0, 1, 0.5) # set semi-transparent blue for stroke
	d.fontSize(12)
	for a in l.anchors:
		d.oval(a.x-radius, a.y-radius, radius*2, radius*2)
		d.text(a.name, (a.x, a.y+10)) # anchor name while I'm at it



d.newPage(paperSize) # blank page



# 3 The size and position were probably wrong. Let's fix that by using the font metrics.
margin = 32 # it's in 0.5 mm increment. 32 = 16 mm
bodyHeightOnPaper = d.height() - margin * 2 # vertical size of the paper, minus top & bottom margin
scale = bodyHeightOnPaper / (m.ascender - m.descender)
for l in sel:
	d.newPage(paperSize)

	# get position and scale right
	d.translate(margin, margin)
	d.scale( scale ) # font scaled down to paper size
	d.translate(0, -m.descender) # move origin point of the paper to include descender

	# draw metric lines
	d.stroke(0,0,0,1) # black
	d.line((0,m.ascender), (l.width, m.ascender)) # draw ascender
	d.line((0,m.capHeight), (l.width, m.capHeight)) # draw descender
	d.line((0,m.xHeight), (l.width, m.xHeight)) # draw descender
	d.line((0,0), ((d.width()-margin*2)/scale, 0)) # draw baseline, all the way to the margin
	d.line((0,m.descender), (l.width, m.descender)) # draw descender

	d.stroke(None)
	d.fill(1,0,0,0.75)
	path = l.completeBezierPath # outlines including paths and components
	d.drawPath(path)



d.newPage(paperSize) # blank page



# 4 Typeset text using the glyphs file as if the instance is already installed
d.newPage(paperSize)
d.fill(0, 0, 0, 1)
tempFolder = os.path.expanduser("~/Library/Application Support/Glyphs/Temp")
ins = f.instances[0] # the index of the instance you want. First instance is 0.

f.instances[insIndex].generate(FontPath = tempFolder) # generates the instance in the "Temp" folder.

fontPath = "%s/%s" % (tempFolder, ins.fileName())
txt = d.FormattedString()
fontName = d.installFont(fontPath) # Drawbot installes the generated font temporalily. You need to uninstall later in the script.
txt.font(fontName)
string = """Mary had a little lamb,
Its fleece was white as snow,
And every where that Mary went
The lamb was sure to go."""
fontSize = 48
txt.fontSize(fontSize)
txt.lineHeight(fontSize*1.5)
txt.append(string)
d.textBox(txt, (margin, margin, d.width()-margin*2, d.height()-margin) ) 

d.uninstallFont(fontPath) # uninstalls the font from Drawbot


filePath = "~/Desktop/aaaaaaa.pdf"
d.saveImage(filePath)
subprocess.call(["open", "-R", os.path.expanduser(filePath)]) # show the PDF in the Finder