#MenuTitle: Random Wikipedia Article...
# -*- coding: utf-8 -*-
__doc__="""
(GUI) Gets a random Wikipedia article and typesets to your page.
"""

import GlyphsApp
import vanilla
import traceback
from AppKit import NSFloatingWindowLevel


try:
	import wikipedia
	wikiInstalled = True
except ModuleNotFoundError:
	try:
		wikiInstalled = False
		message = """This script requires "wikipedia" Python module to be installed. (It's very light)\n\n1. Open Terminal.app\n\n2. copy & paste the following command, and press return:\n\npip3 install wikipedia"""
		Message('', title=message, OKButton=None)
		# import subprocess
		# import sys
		# subprocess.check_call([sys.executable, "pip", "install", 'wikipedia'])
	except:
		LogToConsole(traceback.format_exc())

languagesDic = {
	'(LAT) Azeri':'az',
	'(LAT) Czech':'cs',
	'(LAT) Danish':'da',
	'(LAT) English':'en',
	'(LAT) French':'fr',
	'(LAT) German':'de',
	'(LAT) Icelandic':'is',
	'(LAT) Italian':'it',
	'(LAT) Latvian':'lv',
	'(LAT) Lithuanian':'lt',
	'(LAT) Maltese':'mt',
	'(LAT) Polish':'pl',
	'(LAT) Portuguese':'pt',
	'(LAT) Slovak':'sk',
	'(LAT) Spanish':'es',
	'(LAT) Swedish':'sv',
	'(LAT) Turkish':'tk',
	'(LAT) Vietnamese':'vi',
	'(GRE) Greek':'el',
	'(CYR) Bulgarian':'bg',
	'(CYR) Kazakh':'kk',
	'(CYR) Macedonian':'mk',
	'(CYR) Mongolian':'mn',
	'(CYR) Ukrainian':'uk',
	'(CYR) Russian':'ru',
	'(ARA) Arabic':'ar',
	'(ARA) Pashto':'ps',
	'(ARA) Persian':'fa',
	'(ARA) Urdu':'ur',
	'(THA) Thai':'th',
	'(TIB) Tibetan':'bo',
	'(TIB) Dzongkha':'dz',
	}
languages = languagesDic.keys()
cases = ('No Change', 'UPPERCASE')

class RandomWikiArticle( object ):
	def __init__( self ):
		# Window 'self.w':
		editX = 180
		editY = 22
		textY  = 17
		spaceX = 10
		spaceY = 10
		buttonSizeX = 60
		windowWidth  = 20
		windowHeight = 20
		self.w = vanilla.Window(
			( windowWidth, windowHeight ), # default window size
			"Random Wikipedia Article", # window title
			autosaveName = "com.Tosche.RandomWikiArticle.mainwindow" # stores last window position and size
		)
		self.w._window.setLevel_(NSFloatingWindowLevel)
		windowNS = self.w.getNSWindow()
		windowNS.setHidesOnDeactivate_(True)
		
		self.w.languages = vanilla.PopUpButton('auto', languages)
		self.w.languages.set(3) # English
		# self.w.warning = vanilla.TextBox('auto',"❗️ Your font doesn’t support it.")
		# self.w.warning.show(False)
		self.w.summary = vanilla.RadioGroup('auto',('Summary','Whole Article'), isVertical=False)
		self.w.summary.set(0)
		self.w.line1 = vanilla.HorizontalLine('auto')
		self.w.casing = vanilla.RadioGroup('auto',cases, isVertical=False)
		self.w.casing.set(0)
		self.w.currentTab = vanilla.Button('auto','Current Tab', callback=self.setText)
		self.w.newTab = vanilla.Button('auto','Open New Tab', callback=self.setText)
		rules = [
			'H:|-[languages]-|',
			# 'H:|-[warning]-|',
			'H:|-[summary]-|',
			'H:|-[line1]-|',
			'H:|-[casing]-|',
			'H:|-[currentTab]-[newTab]-|',
			# 'V:|-[languages]-[warning]-[summary]-[line1]-[casing]-[currentTab]-|',
			# 'V:|-[languages]-[warning]-[summary]-[line1]-[casing]-[newTab]-|',
			'V:|-[languages]-[summary]-[line1]-[casing]-[currentTab]-|',
			'V:|-[languages]-[summary]-[line1]-[casing]-[newTab]-|',
			]
		self.w.addAutoPosSizeRules(rules)
		self.w.open()

	def setText(self, sender):
		try:
			langTag = languagesDic[self.w.languages.getItem()]
			wikipedia.set_lang(langTag)
			wikipage = wikipedia.random(1)
			wikiload = wikipedia.page(wikipage)
			if self.w.summary.get() == 0:
				# text = wikiload.title+'\n'+wikiload.summary
				text = wikiload.summary
			else: # whole content
				# text = wikiload.title+'\n'+wikiload.content
				text = wikiload.content

			case = self.w.casing.get() # 0 = no change, 1 = UPPER, 2 = lower
			if case == 1:
				text = text.upper()

			if sender == self.w.newTab:
				Glyphs.font.newTab(text)
			else:
				Glyphs.font.currentTab.text = text

		except:
			print(traceback.format_exc())

if wikiInstalled:
	RandomWikiArticle()