#MenuTitle: Sync Edit views
# -*- coding: utf-8 -*-
__doc__="""
Refreshes the edit view contents of non-front files. Have multiple files open!
"""

import vanilla
import GlyphsApp

class SyncEditViews( object ):
	def __init__( self ):
		# Window 'self.w':
		space = 10
		windowWidth  = 200
		windowHeight = 44
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Sync Edit views", # window title
			autosaveName = "com.Tosche.SyncEditViews.mainwindow" # stores last window position and size
		)
		# Run Button:
		self.w.runButton = vanilla.Button((space, space, -space, -space), "Refresh Other Files", sizeStyle='regular', callback=self.SyncEditViewsMain )
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()

	def SyncEditViewsMain( self, sender ):
		try:
			font0 = Glyphs.orderedDocuments()[0].font # frontmost font
			thisTab = font0.tabs[-1]
			thisMaster = font0.selectedFontMaster
			mindex = thisTab.masterIndex()
			thisText = thisTab.text
			thisScale = thisTab.graphicView().scale()
			doKern = thisTab.graphicView().doKerning()
			doSpace = thisTab.graphicView().doSpacing()
			try:
				for i in range(len(Glyphs.orderedDocuments())):
					if i != 0:
						iFont = Glyphs.orderedDocuments()[i].font
						iTab = Glyphs.orderedDocuments()[i].font.tabs[-1]
						if mindex <= len(iFont.masters):
							iTab.setMasterIndex_(mindex)
						iTab.graphicView().setScale_(thisScale)
						iTab.text = thisText
						iTab.graphicView().setDoKerning_(doKern)
						iTab.graphicView().setDoSpacing_(doSpace)
			except Exception, e:
				Glyphs.showMacroWindow()
				print "Sync Edit views Error (Inside Loop): %s" % e

		except Exception, e:
			Glyphs.showMacroWindow()
			print "Sync Edit views Error: %s" % e

SyncEditViews()