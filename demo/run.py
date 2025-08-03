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
        value = 1 if self.counter is None else self.counter + 1
        self.counter = value


def app():
    view_model = TestViewModel("Some text")

    with wxc.App() as app:
        with wxc.Frame(title="Test", style=wx.DEFAULT_FRAME_STYLE | wx.CLIP_CHILDREN) as frame:
            with wxc.BoxSizer(orient=wx.VERTICAL):

                with wxc.StaticText() as _:
                    _.Label = bind(lambda: f"{view_model.label} {view_model.counter if view_model.counter else ''}")
                    bind_call(lambda c: c.control.Show(True))
                    layout(flag=wx.EXPAND | wx.ALL, border=5)

                with wxc.TextCtrl() as _:
                    _.Value = bind(lambda: str(view_model.counter) if view_model.counter else "").on(
                        wx.EVT_TEXT, lambda v: int(v) if v else None
                    )
                    layout(flag=wx.EXPAND | wx.ALL, border=5)

                with wxc.Button(label="Increment") as _:
                    _.Bind(wx.EVT_BUTTON, lambda _: view_model.increment())
                    layout(flag=wx.EXPAND | wx.ALL, border=5)
            frame.Show()

        app.MainLoop()


app()
