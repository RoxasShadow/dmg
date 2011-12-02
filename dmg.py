#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    dmg permits to emulate the Nintendo DS to download one or more Pokémon as .pkm file. <http://www.giovannicapuano.net>
    Copyright (C) 2011  Giovanni 'Roxas Shadow' Capuano

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib, wx
from wx.lib.buttons import GenButton

from pokehaxlib import *
from sys import *
from pkmlib import encode, decode
from platform import system
from boxtoparty import *
import os, struct, re

class Dmg(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, size=(250, 240), style=wx.CAPTION | wx.CLOSE_BOX) # Not resizable with this style
		panel = wx.Panel(self)
		
		# Text
		wx.StaticText(panel, -1, 'IP', (10, 20))
		wx.StaticText(panel, -1, 'Filename', (10, 60))
		wx.StaticText(panel, -1, 'Path', (10, 100))
		wx.StaticText(panel, -1, 'Count', (10, 140))
		wx.StaticText(panel, -1, 'DMG - DownloadMyGTS \n<http://www.giovannicapuano.net>', (10, 200))

		# Inputbox
		self.ip = wx.TextCtrl(panel, -1, '127.0.0.1',  (110, 15), (120, -1))
		self.filename = wx.TextCtrl(panel, -1, 'Example',  (110, 55), (120, -1))
		# Python ternary operator: (true) if (op) else (false)
		# C ternary operator: op ? true : false
		# C > Python, sry :(
		self.path = wx.TextCtrl(panel, -1, 'C:\yourname\Desktop\\' if system() == 'Windows' else '/home/yourname/Desktop/',  (110, 95), (120, -1))
		self.count = wx.TextCtrl(panel, -1, '2',  (110, 135), (120, -1))

		# Buttons
		self.submit = wx.Button(panel, 1, 'Start', (110, 170))
		self.submit.SetDefault() # Click with enter too
		
		# Events
		self.Bind(wx.EVT_BUTTON, self.download, id=1)
		
		self.Centre()
		self.Show()
		
	def download(self, event):
		i = 0
		self.submit.SetLabel('Start')
		while i < int(self.count.GetValue()):
			self.submit.SetLabel('Stop')
			i += 1
			try:
				# File download
				webFile = urllib.urlopen('http://'+self.ip.GetValue()+'/worldexchange/result.asp?')
				localFile = open(self.path.GetValue()+self.filename.GetValue()+str(i)+'.pkm', 'w')
				localFile.write(webFile.read())
				webFile.close()
				localFile.close()
			except:
				wx.MessageBox('Download failed.', 'Failed')
				self.submit.SetLabel('Start')
				continue # Jump to next iteration
			try: # Exception = File not exists
				f = open(self.path.GetValue()+self.filename.GetValue()+str(i)+'.pkm', 'r')
				pkm = f.read()
				f.close()
			except:
				wx.MessageBox('Download failed.\n'+self.filename.GetValue()+str(i)+'.pkm not exists.', 'Failed')
				self.submit.SetLabel('Start')
				continue # Jump to next iteration
			# Shifting
			f = open(self.path.GetValue()+self.filename.GetValue()+str(i)+'.pkm', 'r')
			pkm = f.read()
			f.close()
			pkm = decode(pkm)
			if len(pkm) != 136:
			    pkm = pkm[0:136] #-- only take the top 136 bytes
			    new_pkm_file_name = self.path.GetValue()+self.filename.GetValue()+str(i)+'.pkm'
			    new_pkm_fh = open (new_pkm_file_name, 'w' )
			    new_pkm_fh.write(pkm)
			    new_pkm_fh.close()
			if not((len(pkm) == 136) or (len(pkm) == 336)):
				wx.MessageBox('The Pokémon is not integer.', 'Failed')
				self.submit.SetLabel('Start')
		self.submit.SetLabel('Start')
		
app = wx.App()
Dmg(None, -1, 'DMG - DownloadMyGTS')
app.MainLoop()
