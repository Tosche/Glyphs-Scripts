#MenuTitle: Decomposed Components By Type in Selected Layers...
# -*- coding: utf-8 -*-
__doc__="""
Decomposes specific types of components from selected layers and more.
"""

import vanilla
import GlyphsApp

class DecomposeComponentsInSelectedLayers( object ):
	def __init__( self ):
		# Window 'self.w':
		edY = 22
		txY = 17
		sp = 10
		btnX = 160
		btnY = 22
		self.w = vanilla.FloatingWindow(
			( 300, sp*13+txY*8+btnY ), # default window size
			"Clear Backgrounds in Selected Layers...", # window title
			autosaveName = "com.Tosche.ClearBackgroundsInSelectedLayersmainwindow" # stores last window position and size
		)
		
		# UI elements:
		self.w.text_1 = vanilla.TextBox( (sp, sp, -sp, txY), "Where?", sizeStyle='regular' )
		self.w.radio = vanilla.RadioGroup((sp*2, sp*2+txY, -sp, txY*4+sp*3), ["Current master layers only", "All master & special layers", "All backup layers", "All layers"])
		self.w.text_2 = vanilla.TextBox( (sp, sp*6+txY*5, -sp, txY), "What to decompose?", sizeStyle='regular' )
		self.w.compoCheck = vanilla.CheckBox((sp*2, sp*7+txY*6, -sp, txY), "Regular Components", value=True)
		self.w.cornerCheck = vanilla.CheckBox((sp*2, sp*8+txY*7, -sp, txY), "Corner/Cap/Segment Components", value=True)
		self.w.smartCheck = vanilla.CheckBox((sp*2, sp*9+txY*8, -sp, txY), "Smart/Part Components", value=True)

		# Run Button:
		self.w.runButton = vanilla.Button((-sp-btnX, -sp-btnY, -sp, btnY), "Clear", sizeStyle='regular', callback=self.DecomposeComponentsInSelectedLayersMain )
		self.w.setDefaultButton( self.w.runButton )

		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()

	def Decomp(self, layer):
		try:
			if self.w.compoCheck.get():
				if Glyphs.versionNumber >= 3.0:
					compos = [s for s in layer.shapes if type(s) == GSComponent]
					compos = [c for c in compos if c.name[:5] not in ('_smar', '_part')]
					print(compos)
				else: # if G2 and below
					compos = [c for c in layer.components if c.smartComponentValues == None]
					compos = [c for c in compos if c.name[:5] not in ('_smar', '_part')]
				for c in compos:
					layer.decomposeComponent_(c)

		except Exception as e:
			print("Decomp error:", e)
		try:
			if self.w.cornerCheck.get():
				layer.decomposeCorners()
		except Exception as e:
			print("Decomp error:", e)
		try:
			if self.w.smartCheck.get():
				if Glyphs.versionNumber >= 3.0:
					compos = [s for s in layer.shapes if type(s) == GSComponent]
					compos = [c for c in compos if c.name[:5] in ('_smar', '_part')]
				else: # if G2 and below
					compos = [c for c in layer.components if c.smartComponentValues == None]
					compos = [c for c in compos if c.name[:5] in ('_smar', '_part')]
				for c in compos:
					layer.decomposeComponent_(c)
		except Exception as e:
			print("Decomp error:", e)

	def DecomposeComponentsInSelectedLayersMain( self, sender ):
		try:
			f = Glyphs.font # frontmost font
			sel = f.selectedLayers # active layers of currently selected glyphs
			where = self.w.radio.get()
			for l in sel: # loop through layers
				if where == 0: # current master only
					self.Decomp(l)
				else:
					for gl in l.parent.layers:
						if where == 1: # all master & special layers
							if gl.isMasterLayer or gl.isSpecialLayer:
								self.Decomp(gl)
						elif where == 2: # all backup layers
							if gl.isMasterLayer + gl.isSpecialLayer == 0:
								self.Decomp(gl)
						else: # all layers
							self.Decomp(gl)

			self.w.close() # delete if you want window to stay open
		except Exception as e:
			print(e)

DecomposeComponentsInSelectedLayers()