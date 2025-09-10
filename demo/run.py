import wx

from wxcompose import core as wxc
from wxcompose.binding import bind, sync, to
from wxcompose.component import sizer_add
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
                    bind(_).Label = to(lambda: f"{view_model.label} {view_model.counter if view_model.counter else ''}")
                    sizer_add(flag=wx.EXPAND | wx.ALL, border=5)

                with wxc.TextCtrl() as _:
                    sync(_, wx.EVT_TEXT, lambda v: int(v) if v else None).Value = to(view_model).counter.map_(
                        lambda v: str(v) if v else ""
                    )
                    sizer_add(flag=wx.EXPAND | wx.ALL, border=5)

                with wxc.Button(label="Increment") as _:
                    _.Bind(wx.EVT_BUTTON, lambda _: view_model.increment())
                    sizer_add(flag=wx.EXPAND | wx.ALL, border=5)
            frame.Show()

        app.MainLoop()


app()
