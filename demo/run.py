import wx

from wxcompose import core as wxc
from wxcompose.binding import bind, bind_call
from wxcompose.component import layout
from wxcompose.viewmodel import ViewModel


class TestViewModel(ViewModel):
    def __init__(self, label: str):
        super().__init__()
        self.label = label
        self.counter = 0

    def increment(self):
        self.counter += 1


def app():
    view_model = TestViewModel("Some text")

    with wxc.App() as app:
        with wxc.Frame(title="Test", style=wx.DEFAULT_FRAME_STYLE | wx.CLIP_CHILDREN) as frame:
            with wxc.BoxSizer(orient=wx.VERTICAL):
                with wxc.StaticText() as _:
                    _.Label = bind(lambda: f"{view_model.label} {view_model.counter}")
                    bind_call(lambda c: c.control.Show(True))
                    layout(flag=wx.EXPAND | wx.ALL)
                with wxc.Button(label="Increment") as _:
                    _.Bind(wx.EVT_BUTTON, lambda _: view_model.increment())
                    layout(flag=wx.EXPAND | wx.ALL)
            frame.Show()

        app.MainLoop()

app()
