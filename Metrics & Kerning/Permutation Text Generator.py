#MenuTitle: Permutation Text Generator...
# -*- coding: utf-8 -*-
__doc__="""
(GUI) Outputs glyph permutation text for kerning.
"""

import vanilla
import GlyphsApp
import re

class PermutationTextGenerator( object ):
	def __init__( self ):
		# Window 'self.w':
		edY = 22
		txY  = 17
		spX = 10
		spY = 10
		btnX = 120
		btnY = 20
		windowWidth = 400
		windowHeight = spY*7+edY*2+txY*2+btnY+20
		windowWidthResize  = 600 # user can resize width by this value
		windowHeightResize = 0   # user can resize height by this value
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Permutation Text Generator", # window title
			minSize = ( windowWidth, windowHeight ), # minimum size (for resizing)
			maxSize = ( windowWidth + windowWidthResize, windowHeight + windowHeightResize ), # maximum size (for resizing)
			autosaveName = "com.Tosche.PermutationTextGenerator.mainwindow" # stores last window position and size
		)
		
		# UI elements:
		self.w.text_1 = vanilla.TextBox( (spX, spY+2, 40, txY), "List A", sizeStyle='regular' )
		self.w.edit_1 = vanilla.EditText( (spX*2+40, spY, -15, edY), "", sizeStyle = 'small')
		self.w.text_2 = vanilla.TextBox( (spX, spY*2+edY+2, 40, txY), "List B", sizeStyle='regular' )
		self.w.edit_2 = vanilla.EditText( (spX*2+40, spY*2+edY, -15, edY), "", sizeStyle = 'small')
		self.w.text_3 = vanilla.TextBox( (spX*2+40, spY*3+edY*2, 85, txY), "Pattern:", sizeStyle='regular' )
		self.w.radio  = vanilla.RadioGroup((spX*2+100, spY*3+edY*2, 260, txY), ["BABABAB", "AB AB AB", "BA BA BA"], isVertical = False, sizeStyle='regular', callback=self.dupeControl)
		self.w.edit_3 = vanilla.EditText( (spX*2+40, spY*4+edY*2+txY-2, 40, edY), "0", sizeStyle = 'regular')
		self.w.text_4 = vanilla.TextBox( (spX*2+85, spY*4+edY*2+txY, 200, txY), "pairs per line", sizeStyle='regular' )
		self.w.dupe = vanilla.CheckBox( (spX*3+180, spY*4+edY*2+txY, 200, txY), "Remove Duplicates", sizeStyle='regular', value=False)

		# Run Button:
		self.w.outputButton = vanilla.Button((spX*2+40, spY*6+edY*2+txY*2, btnX, btnY), "Macro Panel", sizeStyle='regular', callback=self.PermutationTextGeneratorMain )
		self.w.viewButton = vanilla.Button((spX*3+40+btnX, spY*6+edY*2+txY*2, btnX, btnY), "Edit View", sizeStyle='regular', callback=self.PermutationTextGeneratorMain )
		self.w.setDefaultButton( self.w.viewButton )
		
		# Load Settings:
		if not self.LoadPreferences():
			print "Note: 'Permutation Text Generator' could not load preferences. Will resort to defaults"
			
		
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()
		self.dupeControl(self.w.radio)
		
	def SavePreferences( self, sender ):
		try:
			Glyphs.defaults["com.Tosche.PermutationTextGenerator.edit_1"] = self.w.edit_1.get()
			Glyphs.defaults["com.Tosche.PermutationTextGenerator.edit_2"] = self.w.edit_2.get()
			Glyphs.defaults["com.Tosche.PermutationTextGenerator.radio"] = self.w.radio.get()
			Glyphs.defaults["com.Tosche.PermutationTextGenerator.edit_3"] = self.w.edit_3.get()
			Glyphs.defaults["com.Tosche.PermutationTextGenerator.dupe"] = self.w.dupe.get()
		except:
			return False
			
		return True

	def LoadPreferences( self ):
		try:
			self.w.edit_1.set( Glyphs.defaults["com.Tosche.PermutationTextGenerator.edit_1"] )
			self.w.edit_2.set( Glyphs.defaults["com.Tosche.PermutationTextGenerator.edit_2"] )
			self.w.radio.set( Glyphs.defaults["com.Tosche.PermutationTextGenerator.radio"] )
			self.w.edit_3.set( Glyphs.defaults["com.Tosche.PermutationTextGenerator.edit_3"] )
			self.w.dupe.set( Glyphs.defaults["com.Tosche.PermutationTextGenerator.dupe"] )
		except:
			return False
			
		return True

	def dupeControl( self, sender ):
		try:
			if self.w.radio.get() == 0:
				self.w.dupe.enable(True)
			else:
				self.w.dupe.enable(False)
				self.w.dupe.set(False)
		except Exception, e:
			Glyphs.showMacroWindow()
			print "Permutation Text Generator Error (dupeControl): %s" % e

	def makeList(self, string):
		try:
			newList=[]
			while string !="":
				if string[0] == "/":
					name = ""
					while string != "" or (string[0] != "/" and string[0] !=" "):
						name = name + string[0]
						if string != "":
							try:
								string = string[1:]
							except:
								pass
						if string =="" or string[0] == "/" or string[0] == " ":
							break
					newList.append(name)
				elif string[0] == " ":
					string = string[1:]
				else:
					newList.append(string[0])
					string = string[1:]
			return newList

		except Exception, e:
			Glyphs.showMacroWindow()
			print "Permutation Text Generator Error: %s" % e

	def PermutationTextGeneratorMain( self, sender ):
		try:
			string1 = self.w.edit_1.get()
			string2 = self.w.edit_2.get()
			if string1 == "" or string2 == "":
				Glyphs.showMacroWindow()
				print "There needs to be something in both fields."
			else:
				newList1 = self.makeList(string1)
				newList2 = self.makeList(string2)
				finalRow = []
				item2past = []
				for item2 in newList2:
					if item2[0] == "/":
						item2 = item2 + " "
					row = ""

					if self.w.radio.get() ==1: # if AB AB AB
						if int(self.w.edit_3.get()) != 0: # pairs per line
							i = 1
							for item1 in newList1:
								if item1[0] == "/":
									item1 = item1 + " "
								if i == int(self.w.edit_3.get()): # line break at every 'i'th pair
									row = row + item1 + item2+ "\n"
									i = 0
								else:
									row = row + item1 + item2 + " "
								i = i+1
						else:
							for item1 in newList1:
								if item1[0] == "/":
									item1 = item1 + " "
								row = row + item1 + item2 + " "
						row=re.sub(r"\n$", "", row)
						finalRow.append(row)

					elif self.w.radio.get() ==2: # if BA BA BA
						if int(self.w.edit_3.get()) != 0: # pairs per line
							i = 0
							for item1 in newList1:
								if item1[0] == "/":
									item1 = item1 + " "
								if i == int(self.w.edit_3.get()): # line break at every 'i'th pair
									row = row + "\n" + item2 + item1
									i = 0
								else:
									row = row + " " + item2 + item1
								i = i+1
						else:
							for item1 in newList1:
								if item1[0] == "/":
									item1 = item1 + " "
								row = row + " "+ item2 + item1
						row = row[1:]
						finalRow.append(row)

					else: # if BABABAB
						item2past.append(item2)
						if int(self.w.edit_3.get()) != 0: # pairs per line
							i = 1
							row = row + item2
							for item1 in newList1:
								if item1[0] == "/":
									item1 = item1 + " "
								if i == int(self.w.edit_3.get()): # line break at every 'i'th pair
									row = row + item1 + item2+ "\n" + item2
									i = 0
								else:
									if self.w.dupe.get() == True: # if duplicates are forbidden
										if not item1 in item2past or item1 == item2:
											row = row + item1 + item2
									else:
										row = row + item1 + item2
								i = i+1
						else:
							row = row + item2
							for item1 in newList1:
								if item1[0] == "/":
									item1 = item1 + " "
								row = row + item1 + item2
						row=re.sub(r"\n.$", "", row)
						finalRow.append(row)

				if sender == self.w.outputButton: # Show in Macro Window
					Glyphs.showMacroWindow()
					for thisRow in finalRow:
						print thisRow

				else:
					if int(self.w.edit_3.get()) != 0:
						finalText="\n".join(finalRow)
						finalText=re.sub(" \n", "\n", finalText)
					else:
						finalText=row
					
					try:
						Glyphs.currentDocument.windowController().activeEditViewController().graphicView().setDisplayString_(finalText)
					except:
						Glyphs.currentDocument.windowController().addTabWithString_(finalText)
			
			if not self.SavePreferences( self ):
				print "Note: 'Permutation Text Generator' could not write preferences."
			
			
		except Exception, e:
			# brings macro window to front and reports error:
			Glyphs.showMacroWindow()
			print "Permutation Text Generator Error: %s" % e

PermutationTextGenerator()