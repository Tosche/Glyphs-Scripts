#MenuTitle: Instance Slider...
# -*- coding: utf-8 -*-
__doc__="""
(GUI) Lets you define interpolation values of instances more graphically, using sliders and preview.
"""

import vanilla
import GlyphsApp
from vanilla.dialogs import askYesNo
from robofab.interface.all.dialogs import AskString
from AppKit import NSNoBorder

font = Glyphs.font
insList = []
for ins in font.instances:
	insParameters = {
		"Instance" : "%s %s" % (ins.familyName, ins.name),
		"Weight" : int(ins.interpolationWeight()),
		"Width" : int(ins.interpolationWidth()),
		"Custom" : int(ins.interpolationCustom()),
		"WeightY" : ins.customParameters["InterpolationWeightY"]
		}
	insList.append(insParameters)

masterWeights = [x.weightValue for x in font.masters]
masterWidths = [x.widthValue for x in font.masters]
masterCustoms = [x.customValue for x in font.masters]
weMin = sorted(masterWeights)[0]
weMax = sorted(masterWeights)[-1]
wiMin = sorted(masterWidths)[0]
wiMax = sorted(masterWidths)[-1]
csMin = sorted(masterCustoms)[0]
csMax = sorted(masterCustoms)[-1]

slider1Min = weMin-(weMax-weMin)/2
slider1Max = weMax+(weMax-weMin)/2
slider2Min = wiMin-(wiMax-wiMin)/2
slider2Max = wiMax+(wiMax-wiMin)/2
slider3Min = csMin-(csMax-csMin)/2
slider3Max = csMax+(csMax-csMin)/2

class InstanceSlider( object ):
	def __init__( self ):
		
		edX = 40
		txX  = 70
		sliderY = 18
		spX = 10
		windowWidth  = 350
		windowHeight = 260
		windowWidthResize  = 3000          # user can resize width by this value
		windowHeightResize = 3000          # user can resize height by this value
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Instance Slider",             # window title
			minSize = ( windowWidth, windowHeight ), # minimum size (for resizing)
			maxSize = ( windowWidth + windowWidthResize, windowHeight + windowHeightResize ), # maximum size (for resizing)
			autosaveName = "com.Tosche.InstanceSlider.mainwindow" # stores last window position and size
		)
		
		# UI elements:
		
		YOffset = 27
		self.w.add = vanilla.Button((6, -YOffset, 24, 20), "+", callback=self.addDelButtons)
		self.w.delete = vanilla.Button((34, -YOffset, 24, 20), u"–", callback=self.addDelButtons)
		self.w.revert = vanilla.Button((62, -YOffset, 60, 20), "Revert", callback=self.revert )
		
		LineHeight = 26
		YOffset += LineHeight
		
		if slider1Min != slider1Max:
			self.w.textY = vanilla.TextBox( (spX, -YOffset, txX, 14), "WeightY", sizeStyle='small' )
			self.w.checkY = vanilla.CheckBox((txX-spX, -YOffset-3, -10, 18), "", sizeStyle='small', callback=self.checkboxY, value=False)
			self.w.sliderY = vanilla.Slider((spX+txX, -YOffset, -spX*2-edX, sliderY), minValue=slider1Min, maxValue=slider1Max, tickMarkCount=5, sizeStyle="small", callback=self.slide, continuous=True)
			self.w.editY = vanilla.EditText( (-spX-edX, -YOffset, edX, sliderY), "0", sizeStyle = 'small', callback=self.typeValue)
			YOffset += LineHeight
		
		if slider3Min != slider3Max:
			self.w.text3 = vanilla.TextBox( (spX, -YOffset, txX, 14), "Custom", sizeStyle='small' )
			self.w.slider3 = vanilla.Slider((spX+txX, -YOffset, -spX*2-edX, sliderY), minValue=slider3Min, maxValue=slider3Max, tickMarkCount=5, sizeStyle="small", callback=self.slide, continuous=True)
			self.w.edit3 = vanilla.EditText( (-spX-edX, -YOffset, edX, sliderY), "0", sizeStyle = 'small', callback=self.typeValue)
			YOffset += LineHeight
		
		if slider2Min != slider2Max:
			self.w.text2 = vanilla.TextBox( (spX, -YOffset, txX, 14), "Width", sizeStyle='small' )
			self.w.slider2 = vanilla.Slider((spX+txX, -YOffset, -spX*2-edX, sliderY), minValue=slider2Min, maxValue=slider2Max, tickMarkCount=5, sizeStyle="small", callback=self.slide, continuous=True)
			self.w.edit2 = vanilla.EditText( (-spX-edX, -YOffset, edX, sliderY), "0", sizeStyle = 'small', callback=self.typeValue)
			YOffset += LineHeight
			
		if slider1Min != slider1Max:
			self.w.text1 = vanilla.TextBox( (spX, -YOffset, txX, 14), "Weight", sizeStyle='small' )
			self.w.slider1 = vanilla.Slider((spX+txX, -YOffset, -spX*2-edX, sliderY), minValue=slider1Min, maxValue=slider1Max,  tickMarkCount=5, sizeStyle="small", callback=self.slide, continuous=True)
			self.w.edit1 = vanilla.EditText( (-spX-edX, -YOffset, edX, sliderY), "0", sizeStyle = 'small', callback=self.typeValue)
			YOffset += LineHeight
		
		self.w.list = vanilla.List( (0, 0, -0, -(YOffset - 18)), insList, selectionCallback=self.listClick, allowsMultipleSelection=False, allowsEmptySelection=False,
			columnDescriptions=[
				{"title":"Instance", "width":self.w.getPosSize()[2]-215},
				{"title":"Weight", "width":50},
				{"title":"Width", "width":50},
				{"title":"Custom", "width":50},
				{"title":"WeightY", "width":50}
				]
			)
		self.w.list._nsObject.setBorderType_(NSNoBorder)
		tableView = self.w.list._tableView
		tableView.setAllowsColumnReordering_(False)
		tableView.unbind_("sortDescriptors") # Disables sorting by clicking the title bar
		tableView.tableColumns()[0].setResizingMask_(1)
		tableView.tableColumns()[1].setResizingMask_(0)
		tableView.tableColumns()[2].setResizingMask_(0)
		tableView.tableColumns()[3].setResizingMask_(0)
# setResizingMask_() 0=Fixed, 1=Auto-Resizable (Not user-resizable). There may be more options?
		tableView.setColumnAutoresizingStyle_(5)
# AutoresizingStyle:
# 0 Disable table column autoresizing.
# 1 Autoresize all columns by distributing space equally, simultaneously.
# 2 Autoresize each table column sequentially, from the last auto-resizable column to the first auto-resizable column; proceed to the next column when the current column has reached its minimum or maximum size.
# 3 Autoresize each table column sequentially, from the first auto-resizable column to the last auto-resizable column; proceed to the next column when the current column has reached its minimum or maximum size.
# 4 Autoresize only the last table column. When that table column can no longer be resized, stop autoresizing. Normally you should use one of the sequential autoresizing modes instead.
# 5 Autoresize only the first table column. When that table column can no longer be resized, stop autoresizing. Normally you should use one of the sequential autoresizing modes instead.

		self.w.line = vanilla.HorizontalLine((0, -(YOffset - 18), -0, 1))
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()

		# initialisation:
		# set the first instance in preview if there is an instance
		# set the slider and text
		# set preview area if closed
		# redraw
		uiList = self.w.list
		
		if len(font.instances) > 0:
			if not font.tabs:
				font.newTab("HALOGEN halogen 0123")
			if font.currentTab.previewHeight <= 1.0:
				font.currentTab.previewHeight = 150
			self.setupSliders(font.instances[0], uiList[0])
	
	def setupSliders(self, instance, uiList):
		font.currentTab.previewInstances = instance
		if slider1Min != slider1Max:
			self.w.edit1.set(int(uiList["Weight"]))
			self.w.slider1.set(uiList["Weight"])
		if slider2Min != slider2Max:
			self.w.edit2.set(int(uiList["Width"]))
			self.w.slider2.set(uiList["Width"])
		if slider3Min != slider3Max:
			self.w.edit3.set(int(uiList["Custom"]))
			self.w.slider3.set(uiList["Custom"])
		
		if slider1Min != slider1Max:
			if instance.customParameters["InterpolationWeightY"] != None:
				self.w.checkY.set(True)
				self.w.sliderY.show(True)
				self.w.editY.show(True)
				self.w.sliderY.set(uiList["WeightY"])
				self.w.editY.set(int(uiList["WeightY"]))
			else:
				self.w.checkY.set(False)
				self.w.sliderY.show(False)
				self.w.editY.show(False)
		Glyphs.redraw()
		
	def listClick(self, sender):
		try:
			# set the selected instance in preview
			# set the slider and edit text to current interpolation value
			# redraw
			uiList = self.w.list
			if sender.getSelection():
				index = sender.getSelection()[0]
				self.setupSliders(font.instances[index], uiList[index])
		except Exception, e:
			Glyphs.showMacroWindow()
			print "Instance Slider Error (listClick): %s" % e

	def addDelButtons(self, sender):
		try:
			# If it's an add button, ask for its name, and add an instance
			# if it's a delete button, give a warning, and delete the instance
			uiList = self.w.list
			if sender == self.w.add:
				newInstance = GSInstance()
				newInsName = AskString("Please name the new instance.", title="Creating New Instance")
				newInstance.active = True
				newInstance.name = newInsName
				newInstance.weightValue = weMin
				newInstance.widthValue = wiMin
				newInstance.customValue = csMin
				newInstance.isItalic = False
				newInstance.isBold = False
				font.addInstance_(newInstance)
				insList.append({"Instance": "%s %s" % (font.familyName, newInsName), "Weight": weMin, "Width": wiMin, "Custom": csMin, "WeightY": None})
				uiList.append({"Instance": "%s %s" % (font.familyName, newInsName), "Weight": weMin, "Width": wiMin, "Custom": csMin, "WeightY": None})
			elif sender == self.w.delete:
				if askYesNo("Deleting Instance", 'Are you sure you want to delete the selected instance?', alertStyle=1, parentWindow=None, resultCallback=None):
					index = uiList.getSelection()[0]
					font.removeInstanceAtIndex_(index)
					del insList[index]
					del uiList[index]
				else:
					pass
		except Exception, e:
			Glyphs.showMacroWindow()
			print "Instance Slider Error (addDelButtons): %s" % e

	def slide(self, sender):
		try:
			# pick the value and use it for instance value, edit text and vanilla List
			# redraw
			uiList = self.w.list
			index = uiList.getSelection()[0]
			if hasattr(self.w, 'slider1'):
				font.instances[index].setInterpolationWeight_(int(self.w.slider1.get()))
				self.w.edit1.set(int(self.w.slider1.get()))
				uiList[index]["Weight"] = int(self.w.slider1.get())
			
			if hasattr(self.w, 'slider2'):
				font.instances[index].setInterpolationWidth_(int(self.w.slider2.get()))
				self.w.edit2.set(int(self.w.slider2.get()))
				uiList[index]["Width"] = int(self.w.slider2.get())

			if hasattr(self.w, 'slider3'):
				font.instances[index].setInterpolationCustom_(int(self.w.slider3.get()))
				self.w.edit3.set(int(self.w.slider3.get()))
				uiList[index]["Custom"] = int(self.w.slider3.get())

			if hasattr(self.w, 'sliderY'):
				if font.instances[index].customParameters["InterpolationWeightY"] != None:
					font.instances[index].customParameters["InterpolationWeightY"] = int(self.w.sliderY.get())
					self.w.editY.set(int(self.w.sliderY.get()))
					uiList[index]["WeightY"] = int(self.w.sliderY.get())

			Glyphs.redraw()

		except Exception, e:
			Glyphs.showMacroWindow()
			print "Instance Slider Error (slide): %s" % e

	def typeValue(self, sender):
		try:
			# pick the value and use it for instance value, slider and vanilla List
			# warn the moment you type non-number
			# redraw as you type the number
			uiList = self.w.list
			index = uiList.getSelection()[0]
			try:
				# check if the input is a number
				if hasattr(self.w, 'edit1'):
					int(self.w.edit1.get())
					font.instances[index].setInterpolationWeight_(uiList[index]["Weight"])
					self.w.slider1.set(int(self.w.edit1.get()))
					uiList[index]["Weight"] = int(self.w.edit1.get())
				if hasattr(self.w, 'edit2'):
					int(self.w.edit2.get())
					font.instances[index].setInterpolationWidth_(uiList[index]["Width"])
					self.w.slider2.set(int(self.w.edit2.get()))
					uiList[index]["Width"] = int(self.w.edit2.get())
				if hasattr(self.w, 'edit3'):
					int(self.w.edit3.get())
					font.instances[index].setInterpolationCustom_(uiList[index]["Custom"])
					self.w.slider3.set(int(self.w.edit3.get()))
					uiList[index]["Custom"] = int(self.w.edit3.get())

				if hasattr(self.w, 'sliderY'):
					int(self.w.editY.get())
					if font.instances[index].customParameters["InterpolationWeightY"]:
						font.instances[index].customParameters["InterpolationWeightY"]
						self.w.sliderY.set(int(self.w.editY.get()))
						uiList[index]["WeightY"] = int(self.w.editY.get())

				Glyphs.redraw()
			except:
				Glyphs.displayDialog_("You can only type numerals here!")

		except Exception, e:
			Glyphs.showMacroWindow()
			print "Instance Slider Error (typeValue): %s" % e

	def checkboxY(self, sender):
		try:
			uiList = self.w.list
			index = uiList.getSelection()[0]
			if sender.get(): # When checked
				# add the "InterpolationWeightY" custom parameter
				# apply the same value as Weight
				uiList[index]["WeightY"] = uiList[index]["Weight"]
				self.w.sliderY.set(uiList[index]["Weight"])
				self.w.editY.set(uiList[index]["Weight"])
				self.w.sliderY.show(True)
				self.w.editY.show(True)
				font.instances[index].addCustomParameter_(GSCustomParameter("InterpolationWeightY", uiList[index]["Weight"]))
				Glyphs.redraw()
			else: # When unchecked
				# Glyphs does not redraw after custom parameter deletion,
				# so you need to fake the result as weightY=weight and then delete it
				font.instances[index].customParameters["InterpolationWeightY"] = uiList[index]["Weight"]
				Glyphs.redraw()
				del font.instances[index].customParameters["InterpolationWeightY"]
				uiList[index]["WeightY"] = None
				self.w.sliderY.show(False)
				self.w.editY.show(False)

		except Exception, e:
			Glyphs.showMacroWindow()
			print "Instance Slider Error (checkboxY): %s" % e

	def revert( self, sender ):
		try:
			# set the interpolation value to the original value using insList
			# set slider and edit text to current
			uiList = self.w.list
			index = self.w.list.getSelection()[0]

			if slider1Min != slider1Max: # same as hasattr() but checked in a different way
				font.instances[index].setInterpolationWeight_(insList[index]["Weight"])
				uiList[index]["Weight"] = insList[index]["Weight"]
				self.w.edit1.set(insList[index]["Weight"])
				self.w.slider1.set(int(insList[index]["Weight"]))
			if slider2Min != slider2Max:
				font.instances[index].setInterpolationWidth_(insList[index]["Width"])
				uiList[index]["Width"] = insList[index]["Width"]
				self.w.edit2.set(insList[index]["Width"])
				self.w.slider2.set(int(insList[index]["Width"]))
			if slider3Min != slider3Max:
				font.instances[index].setInterpolationCustom_(insList[index]["Custom"])
				uiList[index]["Custom"] = insList[index]["Custom"]
				self.w.edit3.set(insList[index]["Custom"])
				self.w.slider3.set(int(insList[index]["Custom"]))

			if slider1Min != slider1Max:
				if insList[index]["WeightY"] != None: # if it had WeightY
					if font.instances[index].customParameters["InterpolationWeightY"] != None: # if it still has WeightY
						font.instances[index].customParameters["InterpolationWeightY"] = insList[index]["WeightY"]
					else: # if it doesn't have it now
						font.instances[index].addCustomParameter_(GSCustomParameter("InterpolationWeightY", insList[index]["WeightY"]))
					uiList[index]["WeightY"] = insList[index]["WeightY"]
					self.w.checkY.set(True)
					self.w.editY.set(insList[index]["WeightY"])
					self.w.sliderY.set(int(insList[index]["WeightY"]))
				else: # if it had no WeightY
					if font.instances[index].customParameters["InterpolationWeightY"] != None: # if it does now
						# Glyphs does not redraw after custom parameter deletion,
						# so you need to fake the result and then delete it
						font.instances[index].customParameters["InterpolationWeightY"] = uiList[index]["Weight"]
					Glyphs.redraw()
					del font.instances[index].customParameters["InterpolationWeightY"]
					uiList[index]["WeightY"] = None
					self.w.sliderY.show(False)
					self.w.editY.show(False)
			Glyphs.redraw()
			
		except Exception, e:
			Glyphs.showMacroWindow()
			print "Instance Slider Error (revert): %s" % e

InstanceSlider()