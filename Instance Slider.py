#MenuTitle: Instance Slider...
# -*- coding: utf-8 -*-
from __future__ import print_function, division, unicode_literals
__doc__="""
(GUI) Lets you define interpolation values of instances more graphically, using sliders and preview. It supports up to 10 axes.
"""

import vanilla
import GlyphsApp
from vanilla.dialogs import askYesNo
from robofab.interface.all.dialogs import AskString
from AppKit import NSNoBorder

f = Glyphs.font
if Glyphs.versionNumber >= 2.52:
	av = [[], [], [], [], [], []] # Axis Values, up to six supported in Glyphs 2.5
	# the list contains axis name, minimum, and maximum.
	for i in range(len(f.axes)):
		values = [ m.axes[i] for m in f.masters ]
		av[i] += ( f.axes[i].name, min(values), max(values) )
	av = [a for a in av if len(a)>0]

while len(av) < 6:
	av.append(["",0,10])

insList = []
for ins in f.instances:
	fn = ins.customParameters["familyName"] if ins.customParameters["familyName"] else f.familyName
	insParameters = {
		"Instance" : " ".join((fn, ins.name)),
		"WeightY" : ins.customParameters["InterpolationWeightY"]
		}
	if Glyphs.versionNumber >= 2.52:
		for i in range(len(f.axes)):
			insParameters[f.axes[i].name] = int(ins.axes[i])
	else:
		insParameters[ av[0][0] ] = int(ins.interpolationWeight())
		insParameters[ av[1][0] ] = int(ins.interpolationWidth())
		insParameters[ av[2][0] ] = int(ins.interpolationCustom())
		insParameters[ av[3][0] ] = int(ins.interpolationCustom1())
		insParameters[ av[4][0] ] = int(ins.interpolationCustom2())
		insParameters[ av[5][0] ] = int(ins.interpolationCustom3())
	insList.append(insParameters)

# replacing av minimum and maximum to slider minimum and maximum
for i in range(len(av)):
	mini, maxi = av[i][1], av[i][2]
	av[i][1] = mini-(maxi-mini)/2
	av[i][2] = maxi+(maxi-mini)/2

class InstanceSlider( object ):
	def __init__( self ):
		edX = 40
		txX  = 70
		sliderY = 18
		spX = 10
		axisX = 60
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

		YOffset = 27
		self.w.add = vanilla.Button((6, -YOffset, 24, 20), "+", callback=self.addDelButtons)
		self.w.delete = vanilla.Button((34, -YOffset, 24, 20), "–", callback=self.addDelButtons)
		self.w.revert = vanilla.Button((62, -YOffset, 60, 20), "Revert", callback=self.revert )

		global av
		LineHeight = 26
		YOffset += LineHeight
		axisCount = len([v for v in av if v[0] != ""])

		self.w.textY = vanilla.TextBox( (spX, -YOffset, txX, 14), "WeightY", sizeStyle='small' )
		self.w.checkY = vanilla.CheckBox((txX-spX, -YOffset-3, -10, 18), "", sizeStyle='small', callback=self.checkboxY, value=False)
		self.w.sliderY = vanilla.Slider((spX+txX, -YOffset, -spX*2-edX, sliderY), minValue=av[0][1], maxValue=av[0][2], tickMarkCount=5, sizeStyle="small", callback=self.valueChanged, continuous=True)
		self.w.editY = vanilla.EditText( (-spX-edX, -YOffset, edX, sliderY), "0", sizeStyle = 'small', callback=self.valueChanged)
		YOffset += LineHeight

		move = -LineHeight*2

		move -= LineHeight if axisCount == 6 else 0
		self.w.text5 = vanilla.TextBox( (spX, move, txX, 14), av[5][0], sizeStyle='small' )
		self.w.slider5 = vanilla.Slider((spX+txX, move, -spX*2-edX, sliderY), minValue=av[5][1], maxValue=av[5][2], tickMarkCount=5, sizeStyle="small", callback=self.valueChanged, continuous=True)
		self.w.edit5 = vanilla.EditText( (-spX-edX, move, edX, sliderY), "0", sizeStyle = 'small', callback=self.valueChanged)

		move -= LineHeight if axisCount >= 5 else 0
		self.w.text4 = vanilla.TextBox( (spX, move, txX, 14), av[4][0], sizeStyle='small' )
		self.w.slider4 = vanilla.Slider((spX+txX, move, -spX*2-edX, sliderY), minValue=av[4][1], maxValue=av[4][2], tickMarkCount=5, sizeStyle="small", callback=self.valueChanged, continuous=True)
		self.w.edit4 = vanilla.EditText( (-spX-edX, move, edX, sliderY), "0", sizeStyle = 'small', callback=self.valueChanged)

		move -= LineHeight if axisCount >= 4 else 0
		self.w.text3 = vanilla.TextBox( (spX, move, txX, 14), av[3][0], sizeStyle='small' )
		self.w.slider3 = vanilla.Slider((spX+txX, move, -spX*2-edX, sliderY), minValue=av[3][1], maxValue=av[3][2], tickMarkCount=5, sizeStyle="small", callback=self.valueChanged, continuous=True)
		self.w.edit3 = vanilla.EditText( (-spX-edX, move, edX, sliderY), "0", sizeStyle = 'small', callback=self.valueChanged)

		move -= LineHeight if axisCount >= 3 else 0
		self.w.text2 = vanilla.TextBox( (spX, move, txX, 14), av[2][0], sizeStyle='small' )
		self.w.slider2 = vanilla.Slider((spX+txX, move, -spX*2-edX, sliderY), minValue=av[2][1], maxValue=av[2][2], tickMarkCount=5, sizeStyle="small", callback=self.valueChanged, continuous=True)
		self.w.edit2 = vanilla.EditText( (-spX-edX, move, edX, sliderY), "0", sizeStyle = 'small', callback=self.valueChanged)

		move -= LineHeight if axisCount >= 2 else 0
		self.w.text1 = vanilla.TextBox( (spX, move, txX, 14), av[1][0], sizeStyle='small' )
		self.w.slider1 = vanilla.Slider((spX+txX, move, -spX*2-edX, sliderY), minValue=av[1][1], maxValue=av[1][2], tickMarkCount=5, sizeStyle="small", callback=self.valueChanged, continuous=True)
		self.w.edit1 = vanilla.EditText( (-spX-edX, move, edX, sliderY), "0", sizeStyle = 'small', callback=self.valueChanged)

		move -= LineHeight if axisCount >= 1 else 0
		self.w.text0 = vanilla.TextBox( (spX, move, txX, 14), av[0][0], sizeStyle='small' )
		self.w.slider0 = vanilla.Slider((spX+txX, move, -spX*2-edX, sliderY), minValue=av[0][1], maxValue=av[0][2],  tickMarkCount=5, sizeStyle="small", callback=self.valueChanged, continuous=True)
		self.w.edit0 = vanilla.EditText( (-spX-edX, move, edX, sliderY), "0", sizeStyle = 'small', callback=self.valueChanged)

		YOffset += LineHeight*axisCount

		av = [v for v in av if v[0] != ""]
		axisElements = [
			[self.w.text0, self.w.slider0, self.w.edit0],
			[self.w.text1, self.w.slider1, self.w.edit1],
			[self.w.text2, self.w.slider2, self.w.edit2],
			[self.w.text3, self.w.slider3, self.w.edit3],
			[self.w.text4, self.w.slider4, self.w.edit4],
			[self.w.text5, self.w.slider5, self.w.edit5],
		]

		for els in axisElements[len(av):]:
			els[0].show(False)
			els[1].show(False)
			els[2].show(False)

		self.usedAxisElements = axisElements[:len(av)]

		# TODO: disable WeightY if Weight doesn't exist
		if "Weight" not in [a[0] for a in av]:
			self.w.checkY.enable(False)

		columnTitles = [{"title":"Instance", "width":self.w.getPosSize()[2]-axisX*(len(av)+1) }]
		for i in range(len(av)):
			columnTitles += [{"title":av[i][0], "width":axisX}]

		self.w.list = vanilla.List( (0, 0, -0, -(YOffset-18)), insList, selectionCallback=self.listClick, allowsMultipleSelection=False, allowsEmptySelection=False, columnDescriptions=columnTitles)
		self.w.list._nsObject.setBorderType_(NSNoBorder)
		tableView = self.w.list._tableView
		tableView.setAllowsColumnReordering_(False)
		tableView.unbind_("sortDescriptors") # Disables sorting by clicking the title bar
		for i in range(len(av)):
			if i == 0:
				tableView.tableColumns()[i].setResizingMask_(1)
			else:
				tableView.tableColumns()[i].setResizingMask_(0)
			# setResizingMask_() 0=Fixed, 1=Auto-Resizable (Not user-resizable). There may be more options?

		tableView.setColumnAutoresizingStyle_(5)
# AutoresizingStyle:
# 0 Disable table column autoresizing.
# 1 Autoresize all columns by distributing space equally, simultaneously.
# 2 Autoresize each table column sequentially, from the last auto-resizable column to the first auto-resizable column; proceed to the next column when the current column has reached its minimum or maximum size.
# 3 Autoresize each table column sequentially, from the first auto-resizable column to the last auto-resizable column; proceed to the next column when the current column has reached its minimum or maximum size.
# 4 Autoresize only the last table column. When that table column can no longer be resized, stop autoresizing. Normally you should use one of the sequential autoresizing modes instead.
# 5 Autoresize only the first table column. When that table column can no longer be resized, stop autoresizing. Normally you should use one of the sequential autoresizing modes instead.

		self.w.line = vanilla.HorizontalLine((0, -(YOffset-18), -0, 1))
		self.w.open()
		self.w.makeKey()

		# initialisation:
		# set the first instance in preview if there is an instance
		# set the slider and text
		# set preview area if closed
		# redraw
		uiList = self.w.list
		
		if len(f.instances) > 0:
			if f.currentTab == None:
				f.newTab("HALOGEN halogen 0123")
			if f.currentTab.previewHeight <= 20.0:
				f.currentTab.previewHeight = 150
			self.setupSliders(0, uiList[0])
	
	def setupSliders(self, insIndex, uiList):
		try:
			instance = f.instances[insIndex]
			f.currentTab.previewInstances = instance
			axisCount = len(av)

			for i, els in enumerate(self.usedAxisElements):
				if Glyphs.versionNumber > 2.5:
					els[1].set(float(instance.axes[i]))
					els[2].set(int(instance.axes[i]))
				else:
					els[1].set(int(insList[insIndex][av[i+1][0]]))
					els[2].set(int(insList[insIndex][av[i+1][0]]))

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
		except Exception as e:
			print("setupSliders error:", e)
		
	def listClick(self, sender):
		try:
			# set the selected instance in preview
			# set the slider and edit text to current interpolation value
			# redraw
			uiList = self.w.list
			if sender.getSelection():
				index = sender.getSelection()[0]
				self.setupSliders(index, uiList[index])
		except Exception as e:
			Glyphs.showMacroWindow()
			print("Instance Slider Error (listClick): %s" % e)

	def addDelButtons(self, sender):
		try:
			# If it's an add button, ask for its name, and add an instance
			# if it's a delete button, give a warning, and delete the instance
			uiList = self.w.list
			values = [int((v[1]+v[2])/2) for v in av]

			if sender == self.w.add:
				newInstance = GSInstance()
				newInsName = AskString("Please name the new instance.", title="Creating New Instance")
				newInstance.active = True
				newInstance.name = newInsName
				newInstance.isItalic = False
				newInstance.isBold = False
				f.addInstance_(newInstance)
				newInstance.axes = values
				newInsParameters = { "Instance": "%s %s" % (f.familyName, newInsName), "WeightY": None }
				for i in range(len(self.usedAxisElements)):
					newInsParameters[self.usedAxisElements[i][0].get()] = int((av[i][1] + av[i][2])/2)
				insList.append(newInsParameters)
				uiList.append(newInsParameters)
			elif sender == self.w.delete:
				if askYesNo("Deleting Instance", 'Are you sure you want to delete the selected instance?', alertStyle=1, parentWindow=None, resultCallback=None):
					index = uiList.getSelection()[0]
					f.removeInstance_
					f.removeInstanceAtIndex_(index)
					del insList[index]
					del uiList[index]
				else:
					pass
		except Exception as e:
			Glyphs.showMacroWindow()
			print("Instance Slider Error (addDelButtons): %s" % e)

	def valueChanged(self, sender):
		try:
		# 0. if slider or text value has changed,
		# 1. pick the value and use it for instance value, editText and vanillaList
		# 2. redraw
			uiList = self.w.list # just a short name
			index = self.w.list.getSelection()[0]
			instance = f.instances[index] # selected instance
			values = []

			try:
				int(sender.get()) # check if text input is a number, else go to error handling
				for els in self.usedAxisElements:
					if sender in els:
						value = int(sender.get())
						els[1].set(value)
						els[2].set(value)
					else:
						value = els[1].get()
					self.w.list[index][ els[0].get() ] = value
					values += [ value ]

				if instance.customParameters["InterpolationWeightY"] != None:
					instance.customParameters["InterpolationWeightY"] = int(self.w.sliderY.get())
					self.w.editY.set(int(self.w.sliderY.get()))
					self.w.list[index]["WeightY"] = int(self.w.sliderY.get())

				instance.axes = values
				instance.updateInterpolationValues()
				Glyphs.redraw()
			except: # if the input came from text field and the value wasn't a number
				correctValue = ''.join([i for i in sender.get() if i.isdigit()])
				if sender.get()[0] == '-':
					correctValue = '-' + correctValue
				Glyphs.displayDialog_("You can only type numerals here!")
				sender.set(correctValue)
		except Exception as e:
			Glyphs.showMacroWindow()
			print("Instance Slider Error (valueChanged): %s" % e)

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
				f.instances[index].addCustomParameter_(GSCustomParameter("InterpolationWeightY", uiList[index]["Weight"]))
				Glyphs.redraw()
			else: # When unchecked
				# Glyphs does not redraw after custom parameter deletion,
				# so you need to fake the result as weightY=weight and then delete it
				f.instances[index].customParameters["InterpolationWeightY"] = uiList[index]["Weight"]
				Glyphs.redraw()
				del f.instances[index].customParameters["InterpolationWeightY"]
				# uiList[index]["WeightY"] = None
				self.w.sliderY.show(False)
				self.w.editY.show(False)

		except Exception as e:
			Glyphs.showMacroWindow()
			print("Instance Slider Error (checkboxY): %s" % e)

	def revert( self, sender ):
		try:
			# set the interpolation value to the original value using insList
			# set slider and edit text to current
			uiList = self.w.list
			index = self.w.list.getSelection()[0]
			values = []

			for els in self.usedAxisElements:
				originalValue = insList[index][els[0].get()]
				values += [originalValue]
				els[1].set( originalValue )
				els[2].set( originalValue )
				uiList[index][els[0].get()] = originalValue

			f.instances[index].axes = values

			if insList[index]["WeightY"] != None: # if it had WeightY
				if f.instances[index].customParameters["InterpolationWeightY"] != None: # if it still has WeightY
					f.instances[index].customParameters["InterpolationWeightY"] = insList[index]["WeightY"]
				else: # if it doesn't have it now
					f.instances[index].addCustomParameter_(GSCustomParameter("InterpolationWeightY", insList[index]["WeightY"]))
				uiList[index]["WeightY"] = insList[index]["WeightY"]
				self.w.checkY.set(True)
				self.w.editY.set(insList[index]["WeightY"])
				self.w.sliderY.set(int(insList[index]["WeightY"]))
			else: # if it had no WeightY
				if f.instances[index].customParameters["InterpolationWeightY"] != None: # if it does now
					# Glyphs does not redraw after custom parameter deletion,
					# so you need to fake the result and then delete it
					f.instances[index].customParameters["InterpolationWeightY"] = uiList[index]["Weight"]
				Glyphs.redraw()
				del f.instances[index].customParameters["InterpolationWeightY"]
				uiList[index]["WeightY"] = None
				self.w.sliderY.show(False)
				self.w.editY.show(False)
			Glyphs.redraw()
			
		except Exception as e:
			Glyphs.showMacroWindow()
			print("Instance Slider Error (revert): %s" % e)

InstanceSlider()