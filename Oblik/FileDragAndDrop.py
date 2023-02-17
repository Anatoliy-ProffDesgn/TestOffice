import os
import stat
import time
import wx
from ObjectListView import ObjectListView, ColumnDefn
#import ImageViewer as iv
class MyFileDropTarget(wx.FileDropTarget):
    """"""

    def __init__(self, window):
        """Constructor"""
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        """
        Когда файлы перетащены, обновляет дисплей
        """
        self.window.updateDisplay(filenames)
        return True


class FileInfo(object):
    """"""

    def __init__(self, path, date_created, date_modified, size):
        """Constructor"""
        self.name = os.path.basename(path)
        self.path = path
        self.dir = path.replace(os.path.basename(path),'')[:-1]
        self.date_created = date_created
        self.date_modified = date_modified
        self.size = size


class MainPanel(wx.Panel):
    """"""

    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.file_list = []
        file_drop_target = MyFileDropTarget(self)
        self.olv = ObjectListView(
            self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.olv.SetDropTarget(file_drop_target)
        self.setFiles()
        # Позволяет редактировать ячейки таблицы после двойного клика по ним
        self.olv.cellEditMode = ObjectListView.CELLEDIT_SINGLECLICK
        self.olv.SetEmptyListMsg("Перетягніть сюди файл або зображення")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.olv, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def updateDisplay(self, file_list):
        """"""
        for path in file_list:
            file_stats = os.stat(path)
            creation_time = time.strftime(
                "%m/%d/%Y %I:%M %p",
                time.localtime(file_stats[stat.ST_CTIME]))
            modified_time = time.strftime(
                "%m/%d/%Y %I:%M %p",
                time.localtime(file_stats[stat.ST_MTIME]))
            file_size = file_stats[stat.ST_SIZE]
            if file_size > 1024:
                file_size = file_size / 1024.0
                file_size = "%.2f KB" % file_size

            self.file_list.append(FileInfo(path,
                                           creation_time,
                                           modified_time,
                                           file_size))

        self.olv.SetObjects(self.file_list)
        #print(self.olv.GetObjects())
        global rez
        rez = self.olv.GetObjects()
        return self.olv.GetObjects()

    def setFiles(self):
        """"""
        self.olv.SetColumns([
            ColumnDefn("Dir", "left", 220, "dir"),
            ColumnDefn("Name", "left", 220, "name"),
            ColumnDefn("Date created", "left", 150, "date_created"),
            ColumnDefn("Date modified", "left", 150, "date_modified"),
            ColumnDefn("Size", "left", 100, "size")
        ])
        self.olv.SetObjects(self.file_list)

    def clickItm(self):
        print(self.olv.SelectedItemCount)




class MainFrame(wx.Frame):
    """"""

    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None,
                          title="Облік", size=(1000, 600))
        panel = MainPanel(self)
        self.Show()

def main():
    """"""
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
    return rez



if __name__ == "__main__":
    main()