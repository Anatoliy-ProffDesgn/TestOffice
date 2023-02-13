import wx

filenames = ["image.bmp", "image.gif", "image.jpg", "image.png"]


class TestFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Loading Images")
        p = wx.Panel(self)

        fgs = wx.FlexGridSizer(cols=2, hgap=10, vgap=10)
        for name in filenames:
            # загружаем изображения из файла0
            img1 = wx.Image(name, wx.BITMAP_TYPE_ANY)

            w = img1.GetWidth()
            h = img1.GetHeight()
            # масштабируем изображения
            img2 = img1.Scale(w / 2, h / 2)

            # делаем из изображений bitmap
            sb1 = wx.StaticBitmap(p, -1, wx.BitmapFromImage(img1))
            sb2 = wx.StaticBitmap(p, -1, wx.BitmapFromImage(img2))

            fgs.Add(sb1)
            fgs.Add(sb2)

        p.SetSizerAndFit(fgs)
        self.Fit()


app = wx.PySimpleApp()

frm = TestFrame()
frm.Show()
app.MainLoop()