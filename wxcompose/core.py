from typing import List, Optional, cast

import wx

from wxcompose.component import Component, parent


class App(Component[wx.App]):

    def __init__(
        self,
        redirect: bool = False,
        filename: Optional[str] = None,
        useBestVisual: bool = False,
        clearSigInt: bool = True,
    ):
        super().__init__(
            wx.App(redirect=redirect, filename=filename, useBestVisual=useBestVisual, clearSigInt=clearSigInt)
        )


class BoxSizer(Component[wx.BoxSizer]):

    def __init__(self, orient: int = wx.HORIZONTAL):
        super().__init__(wx.BoxSizer(orient=orient))


class StaticBoxSizer(Component[wx.StaticBoxSizer]):
    def __init__(self, orient: int, label: str = ""):
        super().__init__(wx.StaticBoxSizer(orient, parent(), label=label))


class Panel(Component[wx.Panel]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.TAB_TRAVERSAL,
        name: str = wx.PanelNameStr,
    ):
        super().__init__(wx.Panel(parent(), id=id, pos=pos, size=size, style=style, name=name))


class MenuBar(Component[wx.MenuBar]):
    def __init__(self, style: int = 0) -> None:
        super().__init__(wx.MenuBar(style=style))


class Menu(Component[wx.Menu]):
    def __init__(self, title: Optional[str] = None, style: int = 0) -> None:
        if title is None:
            super().__init__(wx.Menu(style))
        else:
            super().__init__(wx.Menu(title=title, style=style))


class MenuItem(Component[wx.MenuItem]):
    def __init__(
        self,
        parentMenu: Optional[wx.Menu] = None,
        id: int = wx.ID_SEPARATOR,
        text: str = "",
        helpString: str = "",
        kind: wx.ItemKind = wx.ITEM_NORMAL,
        subMenu: Optional[wx.Menu] = None,
    ):
        super().__init__(
            wx.MenuItem(parentMenu=parentMenu, id=id, text=text, helpString=helpString, kind=kind, subMenu=subMenu)
        )


class ScrolledWindow(Component[wx.ScrolledWindow]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        name: str = wx.PanelNameStr,
    ):
        super().__init__(wx.ScrolledWindow(parent(), id=id, pos=pos, size=size, style=style, name=name))


class VScrolledWindow(Component[wx.VScrolledWindow]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        name: str = wx.PanelNameStr,
    ):
        super().__init__(wx.VScrolledWindow(parent(), id=id, pos=pos, size=size, style=style, name=name))


class HScrolledWindow(Component[wx.HScrolledWindow]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        name: str = wx.PanelNameStr,
    ):
        super().__init__(wx.HScrolledWindow(parent(), id=id, pos=pos, size=size, style=style, name=name))


class HVScrolledWindow(Component[wx.HVScrolledWindow]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        name: str = wx.PanelNameStr,
    ):
        super().__init__(wx.HVScrolledWindow(parent(), id=id, pos=pos, size=size, style=style, name=name))


class Control(Component[wx.Control]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.ControlNameStr,
    ):
        super().__init__(wx.Control(parent(), id=id, pos=pos, size=size, style=style, validator=validator, name=name))


class StaticText(Component[wx.StaticText]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        label: str = "",
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        name: str = wx.StaticTextNameStr,
    ):
        super().__init__(wx.StaticText(parent(), id=id, label=label, pos=pos, size=size, style=style, name=name))


class StaticBox(Component[wx.StaticBox]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        label: str = "",
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        name: str = wx.StaticBoxNameStr,
    ):
        super().__init__(wx.StaticBox(parent(), id=id, label=label, pos=pos, size=size, style=style, name=name))


class StatusBar(Component[wx.StatusBar]):
    def __init__(self, id: int = wx.ID_ANY, style: int = wx.STB_DEFAULT_STYLE, name: str = wx.StatusBarNameStr):
        super().__init__(wx.StatusBar(parent(), id=id, style=style, name=name))


class Choice(Component[wx.Choice]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        choices: List[str] = [],
        style: int = 0,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.ChoiceNameStr,
    ):
        super().__init__(
            wx.Choice(parent(), id=id, pos=pos, size=size, choices=choices, style=style, validator=validator, name=name)
        )


class Button(Component[wx.Button]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        label: str = "",
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.ButtonNameStr,
    ):
        super().__init__(
            wx.Button(parent(), id=id, label=label, pos=pos, size=size, style=style, validator=validator, name=name)
        )


class BitmapButton(Component[wx.BitmapButton]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        bitmap: wx.BitmapBundle = cast(wx.BitmapBundle, wx.NullBitmap),
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.ButtonNameStr,
    ):
        super().__init__(
            wx.BitmapButton(
                parent(), id=id, bitmap=bitmap, pos=pos, size=size, style=style, validator=validator, name=name
            )
        )


class Notebook(Component[wx.Notebook]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        name: str = wx.NotebookNameStr,
    ):
        super().__init__(wx.Notebook(parent(), id=id, pos=pos, size=size, style=style, name=name))


class SplitterWindow(Component[wx.SplitterWindow]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.SP_3D,
        name: str = "splitterWindow",
    ):
        super().__init__(wx.SplitterWindow(parent(), id=id, pos=pos, size=size, style=style, name=name))


class CollapsiblePane(Component[wx.CollapsiblePane]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        label: str = "",
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.CP_DEFAULT_STYLE,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.CollapsiblePaneNameStr,
    ):
        super().__init__(
            wx.CollapsiblePane(
                parent(), id=id, label=label, pos=pos, size=size, style=style, validator=validator, name=name
            )
        )


class StaticLine(Component[wx.StaticLine]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.LI_HORIZONTAL,
        name: str = wx.StaticLineNameStr,
    ):
        super().__init__(wx.StaticLine(parent(), id=id, pos=pos, size=size, style=style, name=name))


class TextCtrl(Component[wx.TextCtrl]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        value: str = "",
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.TextCtrlNameStr,
    ):
        super().__init__(
            wx.TextCtrl(parent(), id=id, value=value, pos=pos, size=size, style=style, validator=validator, name=name)
        )


class ComboBox(Component[wx.ComboBox]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        value: str = "",
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        choices: List[str] = [],
        style: int = 0,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.ComboBoxNameStr,
    ):
        super().__init__(
            wx.ComboBox(
                parent(),
                id=id,
                value=value,
                pos=pos,
                size=size,
                choices=choices,
                style=style,
                validator=validator,
                name=name,
            )
        )


class CheckBox(Component[wx.CheckBox]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        label: str = "",
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.CheckBoxNameStr,
    ):
        super().__init__(
            wx.CheckBox(parent(), id=id, label=label, pos=pos, size=size, style=style, validator=validator, name=name)
        )


class ListBox(Component[wx.ListBox]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        choices: List[str] = [],
        style: int = 0,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.ListBoxNameStr,
    ):
        super().__init__(
            wx.ListBox(
                parent(), id=id, pos=pos, size=size, choices=choices, style=style, validator=validator, name=name
            )
        )


class CheckListBox(Component[wx.CheckListBox]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        choices: List[str] = [],
        style: int = 0,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = "listBox",
    ):
        super().__init__(
            wx.CheckListBox(
                parent(), id=id, pos=pos, size=size, choices=choices, style=style, validator=validator, name=name
            )
        )


class Gauge(Component[wx.Gauge]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        range: int = 100,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.GA_HORIZONTAL,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.GaugeNameStr,
    ):
        super().__init__(
            wx.Gauge(parent(), id=id, range=range, pos=pos, size=size, style=style, validator=validator, name=name)
        )


class HeaderCtrl(Component[wx.HeaderCtrl]):
    def __init__(
        self,
        winid: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.HD_DEFAULT_STYLE,
        name: str = wx.HeaderCtrlNameStr,
    ):
        super().__init__(wx.HeaderCtrl(parent(), winid=winid, pos=pos, size=size, style=style, name=name))


class HeaderCtrlSimple(Component[wx.HeaderCtrlSimple]):
    def __init__(
        self,
        winid: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.HD_DEFAULT_STYLE,
        name: str = wx.HeaderCtrlNameStr,
    ):
        super().__init__(wx.HeaderCtrlSimple(parent(), winid=winid, pos=pos, size=size, style=style, name=name))


class SearchCtrl(Component[wx.SearchCtrl]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        value: str = "",
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.SearchCtrlNameStr,
    ):
        super().__init__(
            wx.SearchCtrl(parent(), id=id, value=value, pos=pos, size=size, style=style, validator=validator, name=name)
        )


class RadioBox(Component[wx.RadioBox]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        label: str = "",
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        choices: List[str] = [],
        majorDimension: int = 0,
        style: int = wx.RA_SPECIFY_COLS,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.RadioBoxNameStr,
    ):
        super().__init__(
            wx.RadioBox(
                parent(),
                id=id,
                label=label,
                pos=pos,
                size=size,
                choices=choices,
                majorDimension=majorDimension,
                style=style,
                validator=validator,
                name=name,
            )
        )


class RadioButton(Component[wx.RadioButton]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        label: str = "",
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.RadioButtonNameStr,
    ):
        super().__init__(
            wx.RadioButton(
                parent(), id=id, label=label, pos=pos, size=size, style=style, validator=validator, name=name
            )
        )


class Slider(Component[wx.Slider]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        value: int = 0,
        minValue: int = 0,
        maxValue: int = 100,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.SL_HORIZONTAL,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.SliderNameStr,
    ):
        super().__init__(
            wx.Slider(
                parent(),
                id=id,
                value=value,
                minValue=minValue,
                maxValue=maxValue,
                pos=pos,
                size=size,
                style=style,
                validator=validator,
                name=name,
            )
        )


class SpinButton(Component[wx.SpinButton]):
    def __init__(
        self,
        id: int = -1,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.SP_VERTICAL,
        name: str = "spinButton",
    ):
        super().__init__(wx.SpinButton(parent(), id=id, pos=pos, size=size, style=style, name=name))


class SpinCtrl(Component[wx.SpinCtrl]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        value: str = "",
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.SP_ARROW_KEYS,
        min: int = 0,
        max: int = 100,
        initial: int = 0,
        name: str = "wxSpinCtrl",
    ):
        super().__init__(
            wx.SpinCtrl(
                parent(),
                id=id,
                value=value,
                pos=pos,
                size=size,
                style=style,
                min=min,
                max=max,
                initial=initial,
                name=name,
            )
        )


class SpinCtrlDouble(Component[wx.SpinCtrlDouble]):
    def __init__(
        self,
        id: int = -1,
        value: str = "",
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.SP_ARROW_KEYS,
        min: float = 0,
        max: float = 100,
        initial: float = 0,
        inc: float = 1,
        name: str = "wxSpinCtrlDouble",
    ):
        super().__init__(
            wx.SpinCtrlDouble(
                parent(),
                id=id,
                value=value,
                pos=pos,
                size=size,
                style=style,
                min=min,
                max=max,
                initial=initial,
                inc=inc,
                name=name,
            )
        )


class ToggleButton(Component[wx.ToggleButton]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        label: str = "",
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        val: wx.Validator = wx.DefaultValidator,
        name: str = wx.CheckBoxNameStr,
    ):
        super().__init__(
            wx.ToggleButton(parent(), id=id, label=label, pos=pos, size=size, style=style, val=val, name=name)
        )


class BitmapToggleButton(Component[wx.BitmapToggleButton]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        label: wx.BitmapBundle = cast(wx.BitmapBundle, wx.NullBitmap),
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        val: wx.Validator = wx.DefaultValidator,
        name: str = wx.CheckBoxNameStr,
    ):
        super().__init__(
            wx.BitmapToggleButton(parent(), id=id, label=label, pos=pos, size=size, style=style, val=val, name=name)
        )


class ScrollBar(Component[wx.ScrollBar]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.SB_HORIZONTAL,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.ScrollBarNameStr,
    ):
        super().__init__(wx.ScrollBar(parent(), id=id, pos=pos, size=size, style=style, validator=validator, name=name))


class ToolBar(Component[wx.ToolBar]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.TB_HORIZONTAL,
        name: str = wx.ToolBarNameStr,
    ):
        super().__init__(wx.ToolBar(parent(), id=id, pos=pos, size=size, style=style, name=name))


class InfoBar(Component[wx.InfoBar]):
    def __init__(self, winid: int = wx.ID_ANY):
        super().__init__(wx.InfoBar(parent(), winid=winid))


class ListCtrl(Component[wx.ListCtrl]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.LC_ICON,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.ListCtrlNameStr,
    ):
        super().__init__(wx.ListCtrl(parent(), id=id, pos=pos, size=size, style=style, validator=validator, name=name))


class TreeCtrl(Component[wx.TreeCtrl]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.TR_DEFAULT_STYLE,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.TreeCtrlNameStr,
    ):
        super().__init__(wx.TreeCtrl(parent(), id=id, pos=pos, size=size, style=style, validator=validator, name=name))


class ColourPickerCtrl(Component[wx.ColourPickerCtrl]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        colour: wx.Colour = wx.BLACK,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.CLRP_DEFAULT_STYLE,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.ColourPickerCtrlNameStr,
    ):
        super().__init__(
            wx.ColourPickerCtrl(
                parent(), id=id, colour=colour, pos=pos, size=size, style=style, validator=validator, name=name
            )
        )


class FilePickerCtrl(Component[wx.FilePickerCtrl]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        path: str = "",
        message: str = wx.FileSelectorPromptStr,
        wildcard: str = wx.FileSelectorDefaultWildcardStr,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.FLP_DEFAULT_STYLE,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.FilePickerCtrlNameStr,
    ):
        super().__init__(
            wx.FilePickerCtrl(
                parent(),
                id=id,
                path=path,
                message=message,
                wildcard=wildcard,
                pos=pos,
                size=size,
                style=style,
                validator=validator,
                name=name,
            )
        )


class DirPickerCtrl(Component[wx.DirPickerCtrl]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        path: str = "",
        message: str = wx.DirSelectorPromptStr,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.DIRP_DEFAULT_STYLE,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.DirPickerCtrlNameStr,
    ):
        super().__init__(
            wx.DirPickerCtrl(
                parent(),
                id=id,
                path=path,
                message=message,
                pos=pos,
                size=size,
                style=style,
                validator=validator,
                name=name,
            )
        )


class FontPickerCtrl(Component[wx.FontPickerCtrl]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        font: wx.Font = wx.NullFont,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.FNTP_DEFAULT_STYLE,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.FontPickerCtrlNameStr,
    ):
        super().__init__(
            wx.FontPickerCtrl(
                parent(), id=id, font=font, pos=pos, size=size, style=style, validator=validator, name=name
            )
        )


class FileCtrl(Component[wx.FileCtrl]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        defaultDirectory: str = "",
        defaultFilename: str = "",
        wildCard: str = wx.FileSelectorDefaultWildcardStr,
        style: int = wx.FC_DEFAULT_STYLE,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        name: str = wx.FileCtrlNameStr,
    ):
        super().__init__(
            wx.FileCtrl(
                parent(),
                id=id,
                defaultDirectory=defaultDirectory,
                defaultFilename=defaultFilename,
                wildCard=wildCard,
                style=style,
                pos=pos,
                size=size,
                name=name,
            )
        )


class ComboCtrl(Component[wx.ComboCtrl]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        value: str = "",
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.ComboBoxNameStr,
    ):
        super().__init__(
            wx.ComboCtrl(parent(), id=id, value=value, pos=pos, size=size, style=style, validator=validator, name=name)
        )


class Choicebook(Component[wx.Choicebook]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        name: str = "",
    ):
        super().__init__(wx.Choicebook(parent(), id=id, pos=pos, size=size, style=style, name=name))


class Listbook(Component[wx.Listbook]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        name: str = "",
    ):
        super().__init__(wx.Listbook(parent(), id=id, pos=pos, size=size, style=style, name=name))


class Toolbook(Component[wx.Toolbook]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        name: str = "",
    ):
        super().__init__(wx.Toolbook(parent(), id=id, pos=pos, size=size, style=style, name=name))


class Treebook(Component[wx.Treebook]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.BK_DEFAULT,
        name: str = "",
    ):
        super().__init__(wx.Treebook(parent(), id=id, pos=pos, size=size, style=style, name=name))


class Simplebook(Component[wx.Simplebook]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        name: str = "",
    ):
        super().__init__(wx.Simplebook(parent(), id=id, pos=pos, size=size, style=style, name=name))


class VListBox(Component[wx.VListBox]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        name: str = wx.VListBoxNameStr,
    ):
        super().__init__(wx.VListBox(parent(), id=id, pos=pos, size=size, style=style, name=name))


class ActivityIndicator(Component[wx.ActivityIndicator]):
    def __init__(
        self,
        winid: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        name: str = "activityindicator",
    ):
        super().__init__(wx.ActivityIndicator(parent(), winid=winid, pos=pos, size=size, style=style, name=name))


class CollapsibleHeaderCtrl(Component[wx.CollapsibleHeaderCtrl]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        label: str = "",
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.BORDER_NONE,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.CollapsibleHeaderCtrlNameStr,
    ):
        super().__init__(
            wx.CollapsibleHeaderCtrl(
                parent(), id=id, label=label, pos=pos, size=size, style=style, validator=validator, name=name
            )
        )


class Dialog(Component[wx.Dialog]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        title: str = "",
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.DEFAULT_DIALOG_STYLE,
        name: str = wx.DialogNameStr,
    ):
        super().__init__(wx.Dialog(parent(), id=id, title=title, pos=pos, size=size, style=style, name=name))


class DirDialog(Component[wx.DirDialog]):
    def __init__(
        self,
        message: str = wx.DirSelectorPromptStr,
        defaultPath: str = "",
        style: int = wx.DD_DEFAULT_STYLE,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        name: str = wx.DirDialogNameStr,
    ):
        super().__init__(
            wx.DirDialog(parent(), message=message, defaultPath=defaultPath, style=style, pos=pos, size=size, name=name)
        )


class GenericDirCtrl(Component[wx.GenericDirCtrl]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        dir: str = wx.DirDialogDefaultFolderStr,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.DIRCTRL_DEFAULT_STYLE,
        filter: str = "",
        defaultFilter: int = 0,
        name: str = wx.TreeCtrlNameStr,
    ):
        super().__init__(
            wx.GenericDirCtrl(
                parent(),
                id=id,
                dir=dir,
                pos=pos,
                size=size,
                style=style,
                filter=filter,
                defaultFilter=defaultFilter,
                name=name,
            )
        )


class DirFilterListCtrl(Component[wx.DirFilterListCtrl]):
    def __init__(
        self, id: int = wx.ID_ANY, pos: wx.Point = wx.DefaultPosition, size: wx.Size = wx.DefaultSize, style: int = 0
    ):
        super().__init__(wx.DirFilterListCtrl(parent(), id=id, pos=pos, size=size, style=style))


class FileDialog(Component[wx.FileDialog]):
    def __init__(
        self,
        message: str = wx.FileSelectorPromptStr,
        defaultDir: str = "",
        defaultFile: str = "",
        wildcard: str = wx.FileSelectorDefaultWildcardStr,
        style: int = wx.FD_DEFAULT_STYLE,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        name: str = wx.FileDialogNameStr,
    ):
        super().__init__(
            wx.FileDialog(
                parent(),
                message=message,
                defaultDir=defaultDir,
                defaultFile=defaultFile,
                wildcard=wildcard,
                style=style,
                pos=pos,
                size=size,
                name=name,
            )
        )


class Frame(Component[wx.Frame]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        title: str = "",
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.DEFAULT_FRAME_STYLE,
        name: str = wx.FrameNameStr,
    ):
        super().__init__(wx.Frame(parent(), id=id, title=title, pos=pos, size=size, style=style, name=name))


class MessageDialog(Component[wx.MessageDialog]):
    def __init__(
        self,
        message: str,
        caption: str = wx.MessageBoxCaptionStr,
        style: int = wx.OK | wx.CENTRE,
        pos: wx.Point = wx.DefaultPosition,
    ):
        super().__init__(wx.MessageDialog(parent(), message, caption=caption, style=style, pos=pos))


class GenericMessageDialog(Component[wx.GenericMessageDialog]):
    def __init__(
        self,
        message: str,
        caption: str = wx.MessageBoxCaptionStr,
        style: int = wx.OK | wx.CENTRE,
        pos: wx.Point = wx.DefaultPosition,
    ):
        super().__init__(wx.GenericMessageDialog(parent(), message, caption=caption, style=style, pos=pos))


class RichMessageDialog(Component[wx.RichMessageDialog]):
    def __init__(self, message: str, caption: str = wx.MessageBoxCaptionStr, style: int = wx.OK | wx.CENTRE):
        super().__init__(wx.RichMessageDialog(parent(), message, caption=caption, style=style))


class GenericProgressDialog(Component[wx.GenericProgressDialog]):
    def __init__(self, title: str, message: str, maximum: int = 100, style: int = wx.PD_AUTO_HIDE | wx.PD_APP_MODAL):
        super().__init__(wx.GenericProgressDialog(title, message, maximum=maximum, parent=parent(), style=style))


class ProgressDialog(Component[wx.ProgressDialog]):
    def __init__(self, title: str, message: str, maximum: int = 100, style: int = wx.PD_APP_MODAL | wx.PD_AUTO_HIDE):
        super().__init__(wx.ProgressDialog(title, message, maximum=maximum, parent=parent(), style=style))


class PopupWindow(Component[wx.PopupWindow]):
    def __init__(self, flags: int = wx.BORDER_NONE):
        super().__init__(wx.PopupWindow(parent(), flags=flags))


class PopupTransientWindow(Component[wx.PopupTransientWindow]):
    def __init__(self, flags: int = wx.BORDER_NONE):
        super().__init__(wx.PopupTransientWindow(parent(), flags=flags))


class TipWindow(Component[wx.TipWindow]):
    def __init__(self, text: str, maxLength: int = 100):
        super().__init__(wx.TipWindow(parent(), text, maxLength=maxLength))


class ColourDialog(Component[wx.ColourDialog]):
    def __init__(self, data: Optional[wx.ColourData] = None):
        super().__init__(wx.ColourDialog(parent(), data=data))


class MultiChoiceDialog(Component[wx.MultiChoiceDialog]):
    def __init__(
        self,
        message: str,
        caption: str,
        choices: List[str],
        style: int = wx.CHOICEDLG_STYLE,
        pos: wx.Point = wx.DefaultPosition,
    ):
        super().__init__(wx.MultiChoiceDialog(parent(), message, caption, choices, style=style, pos=pos))


class SingleChoiceDialog(Component[wx.SingleChoiceDialog]):
    def __init__(
        self,
        message: str,
        caption: str,
        choices: List[str],
        style: int = wx.CHOICEDLG_STYLE,
        pos: wx.Point = wx.DefaultPosition,
    ):
        super().__init__(wx.SingleChoiceDialog(parent(), message, caption, choices, style=style, pos=pos))


class FindReplaceDialog(Component[wx.FindReplaceDialog]):
    def __init__(self, data: wx.FindReplaceData, title: str = "", style: int = 0):
        super().__init__(wx.FindReplaceDialog(parent(), data, title=title, style=style))


class MDIParentFrame(Component[wx.MDIParentFrame]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        title: str = "",
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.DEFAULT_FRAME_STYLE | wx.VSCROLL | wx.HSCROLL,
        name: str = wx.FrameNameStr,
    ):
        super().__init__(wx.MDIParentFrame(parent(), id=id, title=title, pos=pos, size=size, style=style, name=name))


class MDIChildFrame(Component[wx.MDIChildFrame]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        title: str = "",
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.DEFAULT_FRAME_STYLE,
        name: str = wx.FrameNameStr,
    ):
        super().__init__(wx.MDIChildFrame(parent(), id=id, title=title, pos=pos, size=size, style=style, name=name))


class FontDialog(Component[wx.FontDialog]):
    def __init__(self):
        super().__init__(wx.FontDialog(parent()))


class RearrangeList(Component[wx.RearrangeList]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        order: List[int] = [],
        items: List[str] = [],
        style: int = 0,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.RearrangeListNameStr,
    ):
        super().__init__(
            wx.RearrangeList(
                parent(),
                id=id,
                pos=pos,
                size=size,
                order=order,
                items=items,
                style=style,
                validator=validator,
                name=name,
            )
        )


class RearrangeCtrl(Component[wx.RearrangeCtrl]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        order: List[int] = [],
        items: List[str] = [],
        style: int = 0,
        validator: wx.Validator = wx.DefaultValidator,
        name: str = wx.RearrangeListNameStr,
    ):
        super().__init__(
            wx.RearrangeCtrl(
                parent(),
                id=id,
                pos=pos,
                size=size,
                order=order,
                items=items,
                style=style,
                validator=validator,
                name=name,
            )
        )


class RearrangeDialog(Component[wx.RearrangeDialog]):
    def __init__(
        self,
        message: str,
        title: str = "",
        order: List[int] = [],
        items: List[str] = [],
        pos: wx.Point = wx.DefaultPosition,
        name: str = wx.RearrangeDialogNameStr,
    ):
        super().__init__(
            wx.RearrangeDialog(parent(), message, title=title, order=order, items=items, pos=pos, name=name)
        )


class MiniFrame(Component[wx.MiniFrame]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        title: str = "",
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.CAPTION | wx.RESIZE_BORDER,
        name: str = wx.FrameNameStr,
    ):
        super().__init__(wx.MiniFrame(parent(), id=id, title=title, pos=pos, size=size, style=style, name=name))


class TextEntryDialog(Component[wx.TextEntryDialog]):
    def __init__(
        self,
        message: str,
        caption: str = wx.GetTextFromUserPromptStr,
        value: str = "",
        style: int = wx.TextEntryDialogStyle,
        pos: wx.Point = wx.DefaultPosition,
    ):
        super().__init__(wx.TextEntryDialog(parent(), message, caption=caption, value=value, style=style, pos=pos))


class PasswordEntryDialog(Component[wx.PasswordEntryDialog]):
    def __init__(
        self,
        message: str,
        caption: str = wx.GetPasswordFromUserPromptStr,
        defaultValue: str = "",
        style: int = wx.TextEntryDialogStyle,
        pos: wx.Point = wx.DefaultPosition,
    ):
        super().__init__(
            wx.PasswordEntryDialog(parent(), message, caption=caption, defaultValue=defaultValue, style=style, pos=pos)
        )


class NumberEntryDialog(Component[wx.NumberEntryDialog]):
    def __init__(
        self,
        message: str,
        prompt: str,
        caption: str,
        value: int,
        min: int,
        max: int,
        pos: wx.Point = wx.DefaultPosition,
    ):
        super().__init__(wx.NumberEntryDialog(parent(), message, prompt, caption, value, min, max, pos=pos))


class Process(Component[wx.Process]):
    def __init__(self, id: int = -1):
        super().__init__(wx.Process(parent(), id=id))


class ContextHelpButton(Component[wx.ContextHelpButton]):
    def __init__(
        self,
        id: int = wx.ID_CONTEXT_HELP,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
    ):
        super().__init__(wx.ContextHelpButton(parent(), id=id, pos=pos, size=size, style=style))


class PreviewControlBar(Component[wx.PreviewControlBar]):
    def __init__(
        self,
        preview: wx.PrintPreview,
        buttons: int,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        name: str = "panel",
    ):
        super().__init__(wx.PreviewControlBar(preview, buttons, parent(), pos=pos, size=size, style=style, name=name))


class PreviewCanvas(Component[wx.PreviewCanvas]):
    def __init__(
        self,
        preview: wx.PrintPreview,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        name: str = "canvas",
    ):
        super().__init__(wx.PreviewCanvas(preview, parent(), pos=pos, size=size, style=style, name=name))


class PreviewFrame(Component[wx.PreviewFrame]):
    def __init__(
        self,
        preview: wx.PrintPreview,
        title: str = "PrintPreview",
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.DEFAULT_FRAME_STYLE,
        name: str = wx.FrameNameStr,
    ):
        super().__init__(wx.PreviewFrame(preview, parent(), title=title, pos=pos, size=size, style=style, name=name))


class PrintAbortDialog(Component[wx.PrintAbortDialog]):
    def __init__(
        self,
        documentTitle: str,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = wx.DEFAULT_DIALOG_STYLE,
        name: str = "dialog",
    ):
        super().__init__(wx.PrintAbortDialog(parent(), documentTitle, pos=pos, size=size, style=style, name=name))


class PrintDialog(Component[wx.PrintDialog]):
    def __init__(self, data: wx.PrintData):
        super().__init__(wx.PrintDialog(parent(), data))


class PageSetupDialog(Component[wx.PageSetupDialog]):
    def __init__(self, data: Optional[wx.PageSetupDialogData] = None):
        super().__init__(wx.PageSetupDialog(parent(), data=data))


class BusyInfo(Component[wx.BusyInfo]):
    def __init__(self, msg: str):
        super().__init__(wx.BusyInfo(msg, parent()))


class Timer(Component[wx.Timer]):
    def __init__(self, id: int = -1):
        super().__init__(wx.Timer(parent(), id=id))


class StaticBitmap(Component[wx.StaticBitmap]):
    def __init__(
        self,
        id: int = wx.ID_ANY,
        bitmap: wx.Bitmap = wx.NullBitmap,
        pos: wx.Point = wx.DefaultPosition,
        size: wx.Size = wx.DefaultSize,
        style: int = 0,
        name: str = wx.StaticBitmapNameStr,
    ):
        super().__init__(wx.StaticBitmap(parent(), id=id, bitmap=bitmap, pos=pos, size=size, style=style, name=name))  # type: ignore
