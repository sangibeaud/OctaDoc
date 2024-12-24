import wx
import construct as cs
from construct_editor.wx_widgets import WxConstructHexEditor

constr = cs.Struct(
    "a" / cs.Int16sb,
    "b" / cs.Int16sb,
)
b = bytes([0x12, 0x34, 0x56, 0x78])

app = wx.App(False)
frame = wx.Frame(None, title="Construct Hex Editor", size=(1000, 200))
editor_panel = WxConstructHexEditor(frame, construct=constr, binary=b)
editor_panel.construct_editor.expand_all()
frame.Show(True)
app.MainLoop()

