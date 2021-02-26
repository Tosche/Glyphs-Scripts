#MenuTitle: Clear Backgrounds in Selected Layers...
# -*- coding: utf-8 -*-
__doc__="""
Deletes stuff from selected layers and more.
"""

import vanilla
import GlyphsApp

class ClearBackgroundsInSelectedLayers( object ):
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
		self.w.text_2 = vanilla.TextBox( (sp, sp*6+txY*5, -sp, txY), "What to delete?", sizeStyle='regular' )
		self.w.pathCheck = vanilla.CheckBox((sp*2, sp*7+txY*6, -sp, txY), "Paths (incl. corner & cap components)", value=True)
		self.w.compoCheck = vanilla.CheckBox((sp*2, sp*8+txY*7, -sp, txY), "Components", value=True)
		self.w.anchorCheck = vanilla.CheckBox((sp*2, sp*9+txY*8, -sp, txY), "Anchors", value=True)

		# Run Button:
		self.w.runButton = vanilla.Button((-sp-btnX, -sp-btnY, -sp, btnY), "Clear", sizeStyle='regular', callback=self.ClearBackgroundsInSelectedLayersMain )
		self.w.setDefaultButton( self.w.runButton )
		
		# Load Settings:
		# if not self.LoadPreferences():
		# 	print("Note: 'Clear Backgrounds in Selected Layers...' could not load preferences. Will resort to defaults")
		
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()
		
	# def SavePreferences( self, sender ):
	# 	try:
	# 		Glyphs.defaults["com.Tosche.ClearBackgroundsInSelectedLayerspopup_1"] = self.w.popup_1.get()
	# 	except:
	# 		return False
			
	# 	return True

	# def LoadPreferences( self ):
	# 	try:
	# 		self.w.popup_1.set( Glyphs.defaults["com.Tosche.ClearBackgroundsInSelectedLayerspopup_1"] )
	# 	except:
	# 		return False
			
	# 	return True

	def clearBackground(self, layer):
		try:
			if self.w.pathCheck.get():
				paths = [s for s in layer.background.shapes if type(s) == GSPath]
				layer.background.removeShapes_(paths)
		except Exception as e:
			print("clearBackground error:", e)
		try:
			if self.w.compoCheck.get():
				compos = [s for s in layer.background.shapes if type(s) == GSComponent]
				layer.background.removeShapes_(compos)
		except Exception as e:
			print("clearBackground error:", e)
		try:
			if self.w.anchorCheck.get():
				layer.background.anchors = []
		except Exception as e:
			print("clearBackground error:", e)

	def ClearBackgroundsInSelectedLayersMain( self, sender ):
		try:
			f = Glyphs.font # frontmost font
			sel = f.selectedLayers # active layers of currently selected glyphs
			where = self.w.radio.get()
			for l in sel: # loop through layers
				if where == 0: # current master only
					self.clearBackground(gl)
				else:
					for gl in l.parent.layers:
						if where == 1: # all master & special layers
							if gl.isMasterLayer or gl.isSpecialLayer:
								self.clearBackground(gl)
						elif where == 2: # all backup layers
							if gl.isMasterLayer + gl.isSpecialLayer == 0:
								self.clearBackground(gl)
						else: # all layers
							self.clearBackground(gl)
						
			# if not self.SavePreferences( self ):
			# 	print("Note: 'Clear Backgrounds in Selected Layers...' could not write preferences.")
			
			self.w.close() # delete if you want window to stay open
		except Exception as e:
			print(e)
			# brings macro window to front and reports error:
			# Glyphs.showMacroWindow()/

ClearBackgroundsInSelectedLayers()