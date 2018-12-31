#!/usr/bin/env python

from __future__ import print_function

import sys

from enum import Enum

class ScrnClear(Enum):
    """ScrnClear - The screen clearing options"""
    CUR_TO_END, CUR_TO_BEG, ENTIRE, ENTIRE_W_BUFFER = range(4)

class LineClear(Enum):
    """LineClear - The line clearing options"""
    CUR_TO_END, CUR_TO_BEG, ENTIRE = range(3)

class _ANSI(object):
    """_ANSI
    A class for ANSI escape sequence operations
    """
    _ESC = ""

    def __init__(self):
        """_ANSI(self)
        A class for ANSI escape sequence operations
        """
        pass

    @classmethod
    def _get_esc(cls, action):
        """_get_esc(cls, action) -> str
        Get rhe escape sequence for the given action

        action - the action to get the escape sequence for
        """
        return cls._ESC + action

    @classmethod
    def _exec_esc(cls, action):
        """_exec_esc(cls, action)
        Execute the given action using ANSI escape sequence

        action - The action to execute
        """
        print(cls._get_esc(action), end="")

    @classmethod
    def scrn_reset(cls, scrollback_erase=False):
        """scrn_reset(cls, scrollback_erase=False)
        Clear the screen (Guaranteed to set cursor to the beginning of the screen)

        scrollback_erase - Should the scrollback history be erased? (default: False)
        """
        action = ScrnClear.ENTIRE if not scrollback_erase else ScrnClear.ENTIRE_W_BUFFER
        cls.scrn_erase(action)
        cls.cur_set()

    @classmethod
    def scrn_clear(cls):
        """scrn_clear(cls)
        Clear the screen
        """
        cls.scrn_erase(ScrnClear.ENTIRE)

    @classmethod
    def scrn_erase(cls, section):
        """scrn_erase(cls, section)
        Erase part of the screen

        section - Either from cursor to the end of screen, from cursor to the beginning of the screen,
        the whole screen or the whole screen with the scrollback buffer (Use ansi.ScrnClear)
        """
        cls._exec_esc("{s}J".format(s=section.value))

    @classmethod
    def ln_clear(cls):
        """ln_clear(cls)
        Clear the whole line.
        """
        cls.ln_erase(LineClear.ENTIRE)

    @classmethod
    def ln_erase(cls, section):
        """ln_erase(cls, section)
        Erase part of the line

        section - Either from cursor to the end of line, from cursor to the beginning of the line,
        or the whole line
        """
        cls._exec_esc("{s}K".format(s=section.value))

    @classmethod
    def cur_set(cls, row=1, col=1):
        """cur_set(cls, row=1, col=1)
        set the cursor position (1,1 is the screen beginning)

        row - Cursor row to set (Default: 1)
        col - Cursor column to set (Default: 1)
        """
        cls._exec_esc("{r};{c}H".format(r=row, c=col))

    @classmethod
    def cur_save(cls):
        """cur_save(cls)
        Save cursor position
        """
        cls._exec_esc("s")

    @classmethod
    def cur_restore(cls):
        """cur_restore(cls)
        Restore cursor position
        """
        cls._exec_esc("u")

    @classmethod
    def cur_forward(cls, by=1):
        """cur_forward(cls, by=1)
        Forward the cursor horizontally by the given number

        by - The value to forward the cursor by (default: 1)
        """
        cls._exec_esc("{n}C".format(n=by))

    @classmethod
    def cur_backward(cls, by=1):
        """cur_backward(cls, by=1)
        Move the cursor backwards horizontally by the given number

        by - The value to move the cursor backwards by (default: 1)
        """
        cls._exec_esc("{n}D".format(n=by))

    @classmethod
    def cur_horizontal_abs(cls, to=1):
        """cur_horizontal_abs(cls, to=1)
        Set the cursor horizontal absolute position to the given number

        to - The horizontal position to set the cursor to
        """
        cls._exec_esc("{n}G".format(n=by))

    @classmethod
    def cur_up(cls, by=1):
        """cur_up(cls, by=1)
        Move the cursor N lines backwards

        by - The number of lines to go backwards (default: 1)
        """
        cls._exec_esc("{n}A".format(n=by))

    @classmethod
    def cur_down(cls, by=1):
        """cur_down(cls, by=1)
        Move the cursor N lines forward

        by - The number of lines to go forward (default: 1)
        """
        cls._exec_esc("{n}B".format(n=by))

    @classmethod
    def cur_prev_ln(cls, by=1):
        """cur_prev_ln(cls, by=1)
        Same as ANSI.cur_up(by)
        """
        cls._exec_esc("{n}F".format(n=by))

    @classmethod
    def cur_next_ln(cls, by=1):
        """cur_next_ln(cls, by=1)
        Same as ANSI.cur_down(by)
        """
        cls._exec_esc("{n}E".format(n=by))

    @classmethod
    def cur_get_pos(cls):
        """cur_get_pos(cls)
        Return the vertical and horizontal position of the cursor.
        """
        # ANSI escape code: 6n
        raise NotImplementedError("Not supported yet.")


class LinuxANSI(_ANSI):
    """LinuxANSI
    A class for ANSI escape sequence operations (Linux implementation)
    """
    _ESC = "\033["

    def __init__(self):
        super(self, LinuxANSI).__init__()

class OSXANSI(_ANSI):
    """OSXANSI
    A class for ANSI escape sequence operations (MacOS implementation)
    """
    _ESC = "\033["

    def __init__(self):
        super(self, OSXANSI).__init__()

    @classmethod
    def cur_save(cls):
        print("\x1b7", end="")

    @classmethod
    def cur_restore(cls):
        print("\x1b8", end="")

class WinANSI(_ANSI):
    """OSXANSI
    A class for ANSI escape sequence operations (Windows implementation)
    """

    def __init__(self):
        super(self, WinANSI).__init__()
        raise NotImplementedError("Windows is currently not supported.")

class TextColors(Enum):
    """TextColors - The text colors options"""
    none = 0
    black=30
    red=31
    green=32
    yellow=33
    blue=34
    purple=35
    cyan=36
    white=37

    light_black=90
    light_red=91
    light_green=92
    light_yellow=93
    light_blue=94
    light_purple=95
    light_cyan=96
    light_white=97

    def to_bg(color):
        """to_bg(color) -> int
        Get the color value for ansi background color

        color - The color to get the ansi background color value for
        """
        return color.value + 10

    def from_bg(color):
        """from_bg(color) -> TextColors
        Get the color enum from the ansi background color value

        color - The ansi color value to get the color enum for
        """
        return TextColors(color - 10)

class _TextGraphicRender(Enum):
    """_TextGraphicRender - The graphic renderation options for the text"""
    clear = 0
    bold = 1
    faint = 2
    italic = 3
    underline = 4
    blink_slow = 5
    blink_fast = 6
    crossed_out = 9

class _TextStyle(object):
    _ESC = ""
    _CLEAR = _ESC+"0m"

    _FG = "fg"
    _BG = "bg"

    def __init__(self, fg=TextColors.none, bg=TextColors.none, 
                bold=False, faint=False, italic=False, underline=False,
                blink_slow=False, blink_fast=False, crossed_out=False):
        """_TextStyle(self, fg=TextColors.none, bg=TextColors.none, 
                bold=False, faint=False, italic=False, underline=False,
                blink_slow=False, blink_fast=False, crossed_out=False)
        Create a TextStyle instance

        fg  - Set the foreground color of the string (default: TextColors.none)
        bg  - Set the background color of the string (default: TextColors.none)
        bold  - Should the text be bolded (default: False)
        faint  - Should the text be faint (default: False)
        italic  - Should the text be italic (default: False)
        underline  - Should the text have an underline (default: False)
        blink_slow  - Make the string blink slow (default: False)
        blink_fast  - Make the string blink fast (default: False)
        crossed_out  - Make the string crossed out (default: False)
        """
        self._fmt = {}

        self.fg = fg
        self.bg = bg
        self.bold = bold
        self.faint = faint
        self.italic = italic
        self.underline = underline
        self.blink_slow = blink_slow
        self.blink_fast = blink_fast
        self.crossed_out = crossed_out

    @property
    def fg(self):
        """the fg color property of the TextStyle
        """
        return TextColors(self._fmt[self._FG]) if self._FG in self._fmt else TextColors.none

    @property
    def bg(self):
        """the bg color property of the TextStyle
        """
        return TextColors.from_bg(self._fmt[self._BG]) if self._BG in self._fmt else TextColors.none

    @property
    def bold(self):
        """the bold property of the TextStyle
        """
        return _TextGraphicRender.bold.name in self._fmt

    @property
    def faint(self):
        """the faint property of the TextStyle
        """
        return _TextGraphicRender.faint.name in self._fmt

    @property
    def italic(self):
        """the italic property of the TextStyle
        """
        return _TextGraphicRender.italic.name in self._fmt

    @property
    def underline(self):
        """the underline property of the TextStyle
        """
        return _TextGraphicRender.underline.name in self._fmt

    @property
    def blink_slow(self):
        """the blink_slow property of the TextStyle
        """
        return _TextGraphicRender.blink_slow.name in self._fmt

    @property
    def blink_fast(self):
        """the blink_fast property of the TextStyle
        """
        return _TextGraphicRender.blink_fast.name in self._fmt

    @property
    def crossed_out(self):
        """the crossed_out property of the TextStyle
        """
        return _TextGraphicRender.crossed_out.name in self._fmt

    def _color_setter(self, text_part, color, color_convert=lambda color: color.value):
        """_color_setter(self, text_part, val, color_convert=lambda color: color.value)
        Set a color for the given text part (Background or foreground)

        text_part - The text part to change the color of (Background or foreground)
        color - The color to set
        color_convert - A callable that receives a TextColor and returns its integer value
        """
        if color != TextColors.none:
            self._fmt[text_part] = color_convert(color)
        else:
            if text_part in self._fmt: self._fmt.pop(text_part)

    def _style_setter(self, style, val):
        """_style_setter(self, style, val)
        Toggle a given style on or off

        style - The style to toggle
        val - The value to set (Enabled/Disabled - True/False)
        """
        if val:
            self._fmt[style.name] = style.value
        else:
            if style.name in self._fmt: self._fmt.pop(style.name)

    @fg.setter
    def fg(self, val):
        """the fg color setter property of the TextStyle

        val - The fg color to set
        """
        self._color_setter(self._FG, val)

    @bg.setter
    def bg(self, val):
        """the bg color setter property of the TextStyle

        val - The bg color to set
        """
        self._color_setter(self._BG, val, TextColors.to_bg)

    @bold.setter
    def bold(self, val):
        """the bold property setter of the TextStyle

        val - The bold value to set
        """
        self._style_setter(_TextGraphicRender.bold, val)

    @faint.setter
    def faint(self, val):
        """the faint property setter of the TextStyle

        val - The faint value to set
        """
        self._style_setter(_TextGraphicRender.faint, val)

    @italic.setter
    def italic(self, val):
        """the italic property setter of the TextStyle

        val - The italic value to set
        """
        self._style_setter(_TextGraphicRender.italic, val)

    @underline.setter
    def underline(self, val):
        """the underline property setter of the TextStyle

        val - The underline value to set
        """
        self._style_setter(_TextGraphicRender.underline, val)

    @blink_slow.setter
    def blink_slow(self, val):
        """the blink_slow property setter of the TextStyle

        val - The blink_slow value to set
        """
        self._style_setter(_TextGraphicRender.blink_slow, val)

    @blink_fast.setter
    def blink_fast(self, val):
        """the blink_fast property setter of the TextStyle

        val - The blink_fast value to set
        """
        self._style_setter(_TextGraphicRender.blink_fast, val)

    @crossed_out.setter
    def crossed_out(self, val):
        """the crossed_out property setter of the TextStyle

        val - The crossed_out value to set
        """
        self._style_setter(_TextGraphicRender.crossed_out, val)

    def format(self, string):
        """format(self, string) -> str
        Return a formatted string of the given string with, a string with the configured styles

        string - The string to format with the configured styles
        """
        fmt = [str(style) for style in self._fmt.values()]
        if len(fmt) == 0: fmt.append(TextColors.none)

        return "{esc}{fmt}m{string}{esc}{clear}".format(esc=self._ESC, fmt=";".join(fmt), string=string, clear=_TextStyle._CLEAR)

class LinuxTextStyle(_TextStyle):
    _ESC = "\033["

class OSXTextStyle(_TextStyle):
    _ESC = "\033["

class WinTextStyle(_TextStyle):
    pass

ANSI = None
TextStyle = None

if sys.platform == "linux" or sys.platform == "linux2": # linux
    ANSI = LinuxANSI
    TextStyle = LinuxTextStyle

elif sys.platform == "darwin": # OS X
    ANSI = OSXANSI
    TextStyle = OSXTextStyle

elif sys.platform == "win32": # Windows
    ANSI = WinANSI
    TextStyle = WinTextStyle
    raise NotImplementedError("Windows is currently not supported.")