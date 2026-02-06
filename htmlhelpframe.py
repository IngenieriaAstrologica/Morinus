import wx
import wx.html


class HtmlHelpFrame(wx.Frame):

	def __init__(self, parent, id, title, fname):
		wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(680, 600))

		self.myhtml = wx.html.HtmlWindow(self, id)
		self.myhtml.LoadPage(fname)







