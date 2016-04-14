#MenuTitle: Transform Images with Proper Maths...
# -*- coding: utf-8 -*-
__doc__="""
(GUI) Batch scale and move images in selected layers, using the maths you learned at school. Based on mekkablue's Transform Images script.
"""

import vanilla
import GlyphsApp
import traceback

class TransformImages( object ):
	def __init__( self ):
		editX = 55
		editY = 22
		textY  = 17
		spaceX = 10
		spaceY = 10
		buttonSizeX = 60
		windowWidth  = spaceX*2+editX*2+160
		windowHeight = 150
		self.w = vanilla.FloatingWindow( (windowWidth, windowHeight), "Transform Images with Proper Maths", autosaveName="com.Tosche.TransformImagesWithRealMaths.mainwindow" )
		self.w.checkAbsolute = vanilla.CheckBox( (spaceX, spaceY, 75, textY), "Absolute", sizeStyle='regular', callback=self.changeAbsolute )
		self.w.move_text1 = vanilla.TextBox( (spaceX,  spaceY*2+editY+2, 100, textY), "Move x/y to:", sizeStyle='regular' )
		self.w.move_X = vanilla.EditText( (spaceX+88,    spaceY*2+editY, editX, editY), "0", sizeStyle = 'regular')
		self.w.move_Y = vanilla.EditText( (spaceX+88+editX+5, spaceY*2+editY, editX, editY), "0", sizeStyle = 'regular')
		self.w.move_text2 = vanilla.TextBox( (spaceX+88+editX*2+10,  spaceY*2+editY+2, -15, textY), "units", sizeStyle='regular' )

		self.w.scale_text1 = vanilla.TextBox( (spaceX, spaceY*3+editY*2+2, 100, textY), "Scale x/y to:", sizeStyle='regular' )
		self.w.scale_X = vanilla.EditText( (spaceX+88,    spaceY*3+editY*2, editX, editY), "100", sizeStyle = 'regular')
		self.w.scale_Y = vanilla.EditText( (spaceX+88+editX+5, spaceY*3+editY*2, editX, editY), "100", sizeStyle = 'regular')
		self.w.scale_text2 = vanilla.TextBox( (spaceX+88+editX*2+10, spaceY*3+editY*2+2, -15, textY), "%", sizeStyle='regular' )
		
		self.w.runButton   = vanilla.Button((-60-15, -20-15, -15, -15), "Go", sizeStyle='regular', callback=self.TransformImagesMain )
		self.w.setDefaultButton( self.w.runButton )
		
		try:
			self.LoadPreferences( )
		except:
			pass
		self.w.checkAbsolute.set(True)
		self.w.open()
		
	def SavePreferences( self, sender ):
		try:
			Glyphs.defaults["com.Tosche.TransformImagesWithRealMaths.scaleX"] = self.w.scale_X.get()
			Glyphs.defaults["com.Tosche.TransformImagesWithRealMaths.scaleY"] = self.w.scale_Y.get()
			Glyphs.defaults["com.Tosche.TransformImagesWithRealMaths.moveX"]  = self.w.move_X.get()
			Glyphs.defaults["com.Tosche.TransformImagesWithRealMaths.moveY"]  = self.w.move_Y.get()
		except:
			return False
			
		return True

	def LoadPreferences( self ):
		try:
			self.w.scale_X.set( Glyphs.defaults["com.Tosche.TransformImagesWithRealMaths.scaleX"] )
			self.w.scale_Y.set( Glyphs.defaults["com.Tosche.TransformImagesWithRealMaths.scaleY"] )
			self.w.move_X.set( Glyphs.defaults["com.Tosche.TransformImagesWithRealMaths.moveX"] )
			self.w.move_Y.set( Glyphs.defaults["com.Tosche.TransformImagesWithRealMaths.moveY"] )
		except:
			return False
			
		return True
	def changeAbsolute(self, sender):
		try:
			if self.w.checkAbsolute.get()==False:
				self.w.scale_text1.set("Scale x/y by:")
				self.w.move_text1.set("Move x/y by:")
			else:
				self.w.scale_text1.set("Scale x/y to:")
				self.w.move_text1.set("Move x/y to:")
		except:
			pass

	def TransformImagesMain( self, sender ):
		try:
			Font = Glyphs.font
			selectedLayers = Font.selectedLayers
			for thisLayer in selectedLayers:
				thisImage = thisLayer.backgroundImage
				if thisImage:
					curPosX, curPosY, curSclX, curSclY = thisImage.transformStruct()[4], thisImage.transformStruct()[5], thisImage.transformStruct()[0], thisImage.transformStruct()[3]
					print curPosX, curPosY, curSclX, curSclY

					moveXfix, moveYfix, scaleXfix, scaleYfix  = self.w.move_X.get(), self.w.move_Y.get(), self.w.scale_X.get(), self.w.scale_Y.get()
					if moveXfix == "": moveXfix = 0
					if moveYfix == "": moveYfix = 0
					if scaleXfix == "": scaleXfix = 0
					if scaleYfix == "": scaleYfix = 0

					if self.w.checkAbsolute.get() == True:
						moveX, moveY = float(moveXfix), float(moveYfix)
						scaleX, scaleY = float(scaleXfix)/100, float(scaleYfix)/100
					else:
						moveX, moveY = curPosX+float(moveXfix), curPosY+float(moveYfix)
						scaleX, scaleY = curSclX+float(scaleXfix)/100, curSclY+float(scaleYfix)/100
					print moveX, moveY, scaleX, scaleY
					thisImage.setTransformStruct_( (scaleX, 0.0, 0.0, scaleY, moveX, moveY) )

			if not self.SavePreferences( self ):
				print "Note: could not write preferences."
			
			# self.w.close()
		except Exception, e:
			print traceback.format_exc()

TransformImages()
