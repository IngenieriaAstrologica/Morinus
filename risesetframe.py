import wx
import riseset
import risesetwnd


class RiseSetFrame(wx.Frame):
	XSIZE = 640
	YSIZE = 400
	def __init__(self, parent, title, chrt, options):
		wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(RiseSetFrame.XSIZE, RiseSetFrame.YSIZE))

		if chrt.riseset is None:
			chrt.riseset = riseset.RiseSet(chrt.time.jd, chrt.time.cal, chrt.place.lon, chrt.place.lat, chrt.place.altitude, chrt.planets)
		rw = risesetwnd.RiseSetWnd(self, chrt, options, parent)
		
		self.SetMinSize((200,200))


