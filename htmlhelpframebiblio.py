import wx
import wx.html
import webbrowser


class HtmlHelpFrameCampus(wx.Frame):

	def __init__(self, parent, id, title, fname):

		if fname == 'Campus':
			# open a public URL, in this case, the webbrowser docs
			webbrowser.open("http://www.campus-astrologia.es/",new=2)

		if fname == 'Libros':
			# open a public URL, in this case, the webbrowser docs
			webbrowser.open("http://www.campus-astrologia.es/libros/",new=2)

		if fname == 'Aprende':
			# open a public URL, in this case, the webbrowser docs
			webbrowser.open("http://www.campus-astrologia.es/category/articulos/",new=2)



