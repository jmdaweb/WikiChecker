#WikiChecker for NVDA.
#This file is covered by the GNU General Public License.
#See the file COPYING.txt for more details.
#Copyright (C) 2021 Antonio Cascales <antonio.cascales@gmail.com>

# We import the modules necessary for the operation of the plugin.
import globalPluginHandler
import ui
import api
import gui
import languageHandler
import globalVars
import config
import core
import addonHandler

from scriptHandler import script

from .view import *

addonHandler.initTranslation()

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()

		if globalVars.appArgs.secure or config.isAppX:
			return

		self.mainWindow = MainWindow(gui.mainFrame, _("WikiChecker - Ventana Principal"))
		if hasattr(globalVars, 'wikiChecker'):
			self.postStartupHandler()
		core.postNvdaStartup.register(self.postStartupHandler)
		globalVars.wikiChecker = None

	@script(gesture=None, description=_("Busca los artículos relacionados con el término introducido en Wikipedia."), category=_("WikiChecker"))
	def script_checkWikiTerm(self, gesture):
		if len(self.mainWindow.languages)==0:
			self.mainWindow.loadLanguagesList()
		if not self.mainWindow.IsShown():
			gui.mainFrame.prePopup()
			self.mainWindow.Show()
			self.mainWindow.searchTermCtrl.SetFocus()
			self.mainWindow.resultsList.Enabled = False
			self.mainWindow.resultsList.SetItems([])
			self.mainWindow.CenterOnScreen()
			gui.mainFrame.postPopup()

	def postStartupHandler(self):
		self.mainWindow.loadLanguagesList()

	def terminate(self):
		core.postNvdaStartup.unregister(self.postStartupHandler)
