# wxcompose

[![CI](https://github.com/eumis/wxcompose/actions/workflows/ci.yml/badge.svg?branch=dev)](https://github.com/eumis/wxcompose/actions/workflows/ci.yml)

Declarative UI style and view model binding for wxPython

## Installation

```bash
pip install wxcompose
```

## Usage

### Using components

Here is comparison between wxpython and wxcompose

```python
import wx

app = wx.App()
frame = wx.Frame(None, title="Test", style=wx.DEFAULT_FRAME_STYLE | wx.CLIP_CHILDREN)
sizer = wx.BoxSizer(wx.VERTICAL)
txt = wx.StaticText(frame)
txt.SetLabel("Some text")
sizer.Add(txt, flag=wx.EXPAND | wx.ALL)

frame.Show()
app.MainLoop()
```

```python
import wx

from wxcompose import core as wxc
from wxcompose.component import layout

with wxc.App() as app:
    with wxc.Frame(title="Test", style=wx.DEFAULT_FRAME_STYLE | wx.CLIP_CHILDREN) as frame:
        with wxc.BoxSizer(orient=wx.VERTICAL):
            with wxc.StaticText() as _:
                _.Label = "Some text"
                layout(flag=wx.EXPAND | wx.ALL)
        frame.Show()
    app.MainLoop()
```

---

`wxcompose.core` contains components for core wxpython controls, such as `wx.Frame`, `wx.BoxSizer`, `wx.StaticText`, etc.
Examples of using generic component for controls

```python
import wx
from wx.lib.agw import pygauge

from wxcompose import core as wxc
from wxcompose.component import Component, cmp, parent

with wxc.Frame(title="Test", style=wx.DEFAULT_FRAME_STYLE | wx.CLIP_CHILDREN) as frame:
    with Component(pygauge.PyGauge(frame)) as gauge:
        pass

    with Component(pygauge.PyGauge(parent())):
        pass

    with cmp(pygauge.PyGauge(parent())):
        pass

    with cmp(pygauge.PyGauge):
        pass
```

### Binding

`bind()` can be used to bind control property to view model

```python
from wxcompose import core as wxc
from wxcompose.binding import bind
from wxcompose.viewmodel import ViewModel


class TestViewModel(ViewModel):
    def __init__(self):
        super().__init__()
        self.name = "label"
        self.label = "label"


view_model = TestViewModel()

with wxc.StaticText() as _:
    _.Label = bind(lambda: f"{view_model.name}: {view_model.label}")
```

---

if control property should be updated only when some specific view model field is changed, when() can be used

```python
from wxcompose import core as wxc
from wxcompose.binding import bind
from wxcompose.viewmodel import ViewModel


class TestViewModel(ViewModel):
    def __init__(self):
        super().__init__()
        self.name = "label"
        self.label = "label"


view_model = TestViewModel()

with wxc.StaticText() as _:
    _.Label = bind(lambda: f"{view_model.name}: {view_model.label}").when(lambda: view_model.name)
```

---

two way binding - on() method can be used to set ui event when view model should be updated and mapper

```python
import wx

from wxcompose import core as wxc
from wxcompose.binding import bind
from wxcompose.viewmodel import ViewModel


class TestViewModel(ViewModel):
    def __init__(self):
        super().__init__()
        self.value = 0


view_model = TestViewModel()

with wxc.TextCtrl() as _:
    _.Value = bind(lambda: str(view_model)).on(wx.EVT_TEXT, lambda v: int(v))
```

## License

[MIT](LICENSE)
