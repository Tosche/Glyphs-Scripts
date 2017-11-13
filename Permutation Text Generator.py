#MenuTitle: Permutation Text Generator...
# -*- coding: utf-8 -*-
__doc__="""
(GUI) Outputs glyph permutation text for kerning.
"""

import vanilla
import GlyphsApp
import re

surrogate_pairs = re.compile(u'[\ud800-\udbff][\udc00-\udfff]', re.UNICODE)
surrogate_start = re.compile(u'[\ud800-\udbff]', re.UNICODE)
emoji_variation_selector = re.compile(u'[\ufe00-\ufe0f]', re.UNICODE)

class PermutationTextGenerator( object ):
	def __init__( self ):
		# Window 'self.w':
		edY = 22
		txY  = 17
		sp = 10
		btnX = 120
		btnY = 20
		windowWidth = 430
		windowHeight = sp*8+edY*3+txY*2+btnY+20
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
		self.w.text_A = vanilla.TextBox( (sp, sp+2, 70, txY), "List A", sizeStyle='regular' )
		self.w.edit_A = vanilla.EditText( (sp*2+70, sp, -15, edY), "", sizeStyle = 'small')
		self.w.text_C = vanilla.TextBox( (sp, sp*2+edY+2, 70, txY), "between c", sizeStyle='regular' )
		self.w.edit_C = vanilla.EditText( (sp*2+70, sp*2+edY, -15, edY), "", sizeStyle = 'small')
		self.w.text_B = vanilla.TextBox( (sp, sp*3+edY*2+2, 70, txY), "List B", sizeStyle='regular' )
		self.w.edit_B = vanilla.EditText( (sp*2+70, sp*3+edY*2, -15, edY), "", sizeStyle = 'small')
		self.w.text_3 = vanilla.TextBox( (sp, sp*4+edY*3, 85, txY), "Pattern:", sizeStyle='regular' )
		self.w.radio  = vanilla.RadioGroup((sp*2+70, sp*4+edY*3, 320, txY), ["BABABAB", "AcB AcB AcB", "BcA BcA BcA"], isVertical = False, sizeStyle='regular', callback=self.dupeControl)
		self.w.edit_3 = vanilla.EditText( (sp*2+70, sp*5+edY*3+txY-2, 40, edY), "0", sizeStyle = 'regular')
		self.w.text_4 = vanilla.TextBox( (sp*2+115, sp*5+edY*3+txY, 200, txY), "pairs per line", sizeStyle='regular' )
		self.w.dupe = vanilla.CheckBox( (sp*3+210, sp*5+edY*3+txY, 200, txY), "Remove Duplicates", sizeStyle='regular', value=False)

		# Run Button:
		self.w.outputButton = vanilla.Button((sp*2+70, -sp*2-btnY, btnX, btnY), "Macro Panel", sizeStyle='regular', callback=self.Main )
		self.w.viewButton = vanilla.Button((sp*3+70+btnX, -sp*2-btnY, btnX, btnY), "Edit View", sizeStyle='regular', callback=self.Main )
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
			Glyphs.defaults["com.Tosche.PermutationTextGenerator.edit_1"] = self.w.edit_A.get()
			Glyphs.defaults["com.Tosche.PermutationTextGenerator.edit_C"] = self.w.edit_C.get()
			Glyphs.defaults["com.Tosche.PermutationTextGenerator.edit_2"] = self.w.edit_B.get()
			Glyphs.defaults["com.Tosche.PermutationTextGenerator.radio"] = self.w.radio.get()
			Glyphs.defaults["com.Tosche.PermutationTextGenerator.edit_3"] = self.w.edit_3.get()
			Glyphs.defaults["com.Tosche.PermutationTextGenerator.dupe"] = self.w.dupe.get()
		except:
			return False
			
		return True

	def LoadPreferences( self ):
		try:
			self.w.edit_A.set( Glyphs.defaults["com.Tosche.PermutationTextGenerator.edit_1"] )
			self.w.edit_C.set( Glyphs.defaults["com.Tosche.PermutationTextGenerator.edit_C"] )
			self.w.edit_B.set( Glyphs.defaults["com.Tosche.PermutationTextGenerator.edit_2"] )
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
			if newList:
				filtered = []
				skip = 0
				for i, c in enumerate(newList):
					if i < skip:
						continue
					if surrogate_start.match(c):
						codepoint = surrogate_pairs.findall(c+newList[i+1])[0]
						# skip over emoji skin tone modifiers
						if codepoint in [u'🏻', u'🏼', u'🏽', u'🏾', u'🏿']:
							continue
						filtered.append(codepoint)
					elif surrogate_start.match(newList[i-1]):
						continue
					elif emoji_variation_selector.match(newList[i]):
						continue
					else:
						if c == "/":
							if i+1 > len(newList)-1:
								filtered.append(c)
								continue
							j = i
							longest = ''.join(newList[i+1:])
							while True:
								if Glyphs.font.glyphs[longest]:
									filtered.append(longest)
									skip = j + len(longest) + 1
									break
								longest = longest[:-1]
								if len(longest) <= 1:
									break
						else:
							filtered.append(c)

			return filtered

		except Exception, e:
			Glyphs.showMacroWindow()
			print "Permutation Text Generator Error (MakeList): %s" % e

	def Main( self, sender ):
		try:
			stringA = self.w.edit_A.get()
			stringB = self.w.edit_B.get()
			insert = self.w.edit_C.get()
			if stringA == "" or stringB == "":
				Glyphs.showMacroWindow()
				print "There needs to be something in both fields."
			else:
				newListA = self.makeList(stringA)
				newListB = self.makeList(stringB)
				finalRow = []
				itemBpast = []
				for itemB in newListB:
					if itemB[0] == "/":
						itemB += " "
					row = ""

					if self.w.radio.get() ==1: # if AB AB AB
						if int(self.w.edit_3.get()) != 0: # pairs per line
							i = 1
							for itemA in newListA:
								if itemA[0] == "/":
									itemA += " "
								if i == int(self.w.edit_3.get()): # line break at every 'i'th pair
									row += itemA + insert + itemB + "\n"
									i = 0
								else:
									row += itemA + insert + itemB + " "
								i = i+1
						else:
							for itemA in newListA:
								if itemA[0] == "/":
									itemA += " "
								row += itemA + insert + itemB + " "
						row=re.sub(r"\n$", "", row)
						finalRow.append(row)

					elif self.w.radio.get() ==2: # if BA BA BA
						if int(self.w.edit_3.get()) != 0: # pairs per line
							i = 0
							for itemA in newListA:
								if itemA[0] == "/":
									itemA += " "
								if i == int(self.w.edit_3.get()): # line break at every 'i'th pair
									row += "\n" + itemB + insert + itemA
									i = 0
								else:
									row += " " + itemB + insert + itemA
								i = i+1
						else:
							for itemA in newListA:
								if itemA[0] == "/":
									itemA += " "
								row += " " + itemB + insert + itemA
						row = row[1:]
						finalRow.append(row)

					else: # if BABABAB
						itemBpast.append(itemB)
						if int(self.w.edit_3.get()) != 0: # pairs per line
							i = 1
							row = row + itemB
							for itemA in newListA:
								if itemA[0] == "/":
									itemA += " "
								if i == int(self.w.edit_3.get()): # line break at every 'i'th pair
									row += itemA + itemB+ "\n" + itemB
									i = 0
								else:
									if self.w.dupe.get() == True: # if duplicates are forbidden
										if not itemA in itemBpast or itemA == itemB:
											row += itemA + itemB
									else:
										row += itemA + itemB
								i = i+1
						else:
							row += itemB
							for itemA in newListA:
								if itemA[0] == "/":
									itemA += " "
								row += itemA + itemB
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
			print "Permutation Text Generator Error (Main): %s" % e

PermutationTextGenerator()