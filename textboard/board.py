#!/usr/bin/env python3

from __future__ import print_function

from copy import copy
from  collections import OrderedDict
from abc import ABCMeta, abstractmethod, abstractproperty

from textboard.ansi import ANSI

LOG_BOARD_DEFAULT_LINES_COUNT = 20
LOG_BOARD_SECTOR_DEFAULT_LINES_COUNT = 4

def _validate_id_property(cls, _id):
    if not isinstance(_id, bytes) and not isinstance(_id, str):
        raise TypeError("{cls} id should be either a string or bytes".format(cls=cls))

def _is_brd_obj(self, obj):
    if not isinstance(obj, BoardObject):
        raise TypeError("Given object is not a board object")

class BoardObject(object):
    """BoardObject - The abstract class of a board object"""
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractproperty
    def id(self):
        pass

    @abstractproperty
    def lines_count(self):
        pass

    @abstractproperty
    def max_lines_count(self):
        pass

    @abstractmethod
    def draw(self):
        pass

class BoardLine(BoardObject):
    class LineField(object):
        class Delegate(object):
            """The abstract class of a LineField delegate. The delegate
            is used to manipultae the field on different events of the field
            """
            __metaclass__ = ABCMeta
            
            @abstractmethod
            def on_text_change(self, field):
                """on_text_change(self, field)
                Manipulate the given field on its text change.

                field - The field being delegated.
                """
                pass

        def __init__(self, field_id, size=None, text="", style=None, delegate=None):
            """LineField(self, field_id, size=None, text="", style=None)
            Creates a BoardLine's field

            field_id - The ID to access the field inside the line
            size - The size of the field in the line (default: None - Unlimited)
            text - The text of the field (default: empty)
            style - The text style of the field (Default: None - the terminal's current style)
            delegate - The field delegate.
            """
            _validate_id_property(self.__class__, field_id)
            self._id = field_id
            self._size = size
            self._text = text
            self._style = style
            self._delegate = delegate if delegate is not None else EmptyFieldDelegate()

        @property
        def id(self):
            """The id property of the LineField"""
            return self._id

        @property
        def size(self):
            """The size property of the LineField"""
            return self._size if self._size != None else len(self.text)

        @property
        def size_limit(self):
            """The size lmit property of the LineField"""
            return self._size

        @property
        def text(self):
            """The text property of the LineField"""
            return self._text

        @property
        def style(self):
            """The style property of the LineField"""
            return self._style

        @property
        def delegate(self):
            """The delegate property of the LineField"""
            return self._delegate

        @text.setter
        def text(self, val):
            """The text property's setter of the LineField
            
            val - The new text to set
            """
            if isinstance(val, bytes):
                val = val.decode("utf-8")
            self._text = val
            self._delegate.on_text_change(self)

        @style.setter
        def style(self, val):
            """The style property's setter of the LineField

            val - The new style to set
            """
            self._style = val

        @delegate.setter
        def delegate(self, val):
            """The delegate property's setter of the LineField

            val - The new delegate to set
            """
            self._delegate = val

        def build(self):
            """build(self)
            Build the string of the LineField
            """
            text = "{text:{size}}".format(text=self.text[:self.size], size=(self.size if self.size != 0 else "")).replace("\n", '')
            if self.style is not None:
                text = self.style.format(text)
            return text

        @classmethod
        def create_from(cls, field):
            """create_from(cls, field) -> LineField
            Create a new line field instance from the given line field.

            field - The line field to duplicate
            """
            return cls(field.id, field.size, field.text, field.style, field.delegate)

    def __init__(self, line_id=None):
        """BoardLine(line_id=None)
        Creates a board line

        line_id - The ID for the line, used for accessing it from the contatining board object,
        if none given, line is inaccessable (default: None)
        """
        super(BoardLine, self).__init__()
        if line_id is not None:
            _validate_id_property(self.__class__, line_id)
        self._id = line_id
        if not hasattr(self, "_fields"):
            self._fields = OrderedDict()
        else:
            self._copy_fields(self._fields)

    def _copy_fields(self, fields_to_copy):
        """_copy_fields(self, fields_to_copy)
        Copy the given fields dictionary into this line's fields dictionary

        fields_to_copy - The fields to copy into this line's field dictionary
        """
        fields = [field for field in fields_to_copy.values()]
        self._fields = OrderedDict()
        for field in fields:
            self.add(field.id, field.size, field.text, field.style, field.delegate)

    @property
    def id(self):
        """The id property of the BoardLine"""
        return self._id if self._id is not None else id(self)

    @property
    def lines_count(self):
        """The lines count property of the BoardLine"""
        return 1

    @property
    def max_lines_count(self):
        """The max lines count property of the BoardLine"""
        return self.lines_count

    def add(self, field_id, size=None, text="", style=None, delegate=None):
        """add(self, field_id, size=None, text="") -> self
        Add a field to the board line

        field_id - The ID to access the field inside the line
        size - The size of the field in the line (default: None - Unlimited)
        text - The text of the field (default: empty)
        style - The text style of the field (Default: None - the terminal's current style)
        delegate - The delegate of the field
        """
        field = BoardLine.LineField(field_id, size=size, text=text, style=style, delegate=delegate)
        setattr(self, field_id, field)

        return self

    def get(self, field_id):
        """get(self, field_id) -> LineField
        Get the requested field from this line

        field_id - The ID of the field to get
        """
        return self._fields[field_id]

    def remove(self, field_id):
        """remove(self, field_id) -> LineField
        Remove a field from the line by its iD, the removed field is returned

        field_id - The ID of the field to remove
        """
        ret_val = self._fields.pop(field_id)
        delattr(self, field_id)
        return ret_val

    def _build(self):
        """_build(self) -> str
        Returns the string value of this line
        """
        line_txt = ""
        for field in self._fields.values():
            line_txt += field.build()

        return line_txt

    def draw(self):
        """draw(self)
        Draw the line to the screen
        """
        print(self._build())

    def __setattr__(self, name, value):
        if hasattr(self, name):
            attr_to_set = getattr(self, name)
            if isinstance(value, str) or isinstance(value, bytes):
                if isinstance(attr_to_set, BoardLine.LineField):
                    attr_to_set.text = value
                    return
            elif isinstance(value, BoardLine.LineField):
                if not isinstance(attr_to_set, BoardLine.LineField):
                    raise ValueError("Can not override BoardLine property with field '{field_name}'".format(field_name=name))

        try:
            if isinstance(value, BoardLine.LineField):
                self._fields[value.id] = value
                super(BoardLine, self).__setattr__(name, value)
        except AttributeError:
            pass

        super(BoardLine, self).__setattr__(name, value)

    def __rshift__(self, cls_name):
        """__rshift__(self, cls_name) -> custom BoardLine subclass
        Dynamically creating a new custom subclass of BoardLine. the new class will have the same
        fields as the one of this BoardLine instance and their current text will be set as the initial text
        value for the newly created class fields.

        cls_name - The name of the newly created subclass
        """
        return type(cls_name, (self.__class__, ), self.__dict__)

    @classmethod
    def create(cls, line_id=None, **fields):
        """create(cls, line_id=None, **fields)
        Create a new line instance with the given id. the fields of
        the created line will be filled from the passed fields.

        line_id - The id of the line to create
        **fields - The fields to set.
        """
        line = cls(line_id)
        for field_name, field_val in fields.items():
            if hasattr(line, field_name):
                setattr(line, field_name, field_val)
            else:
                raise ValueError("Field '{field}' does not exist in line.".format(field=field_name))
        return line

    def duplicate(self, line_id=None):
        """duplicate(self, line_id=None) -> BoardLine
        Duplicates the instance of the given line, with a new chosen/random id.

        line_id - The id of the line to create, if none is given, a random id will be selected.
        """
        return self.create(line_id, **self._fields)

    @classmethod
    def create_from(cls, line):
        """create_from(cls, line) -> BoardLine
        Create a new line instance from the given line.

        line - The line to duplicate
        """
        new_line = cls(line._id)
        new_line._copy_fields(line._fields)
        return new_line

class BoardSector(BoardObject):
    def __init__(self, sector_id, max_lines_count=LOG_BOARD_SECTOR_DEFAULT_LINES_COUNT, title_line=None, draw_empty=True):
        """BoardSector(self, sector_id, name, max_lines_count, title_line, draw_empty)
        Creates a board sector

        sector_id - The ID of the sector, used for accessing it from the containing board object
        max_lines_count - The maximum lines count to set for this sector (Not including the title line)
        title_line - A title line to display when drawing the sector, if none is given, no title will be drawn,
        otherwise a title will be drawn using the given BoardLine and both lines_count and max_lines_count will increase by one.
        (default: None)
        draw_empty - A boolean that indicates wether or not the empty lines of the sector should be drawn (default: True)
        """
        super(BoardSector, self).__init__()
        _validate_id_property(self.__class__, sector_id)
        self._id = sector_id
        if not hasattr(self, "_lines"):
            self._lines = OrderedDict()
        else:
            self._copy_lines(self._lines)

        self._max_lines_count = max_lines_count
        if not hasattr(self, "_title") or title_line is not None:
            self._title = title_line
        elif hasattr(self, "_title") and self._title != None:
            self._title = BoardLine.create_from(self._title)

        self._draw_empty = draw_empty

    def _copy_lines(self, lines_to_copy):
        """_copy_lines(self, lines_to_copy)
        Copy the given lines dictionary into this sector's lines dictionary

        lines_to_copy - The lines to copy into this sector's field dictionary
        """
        lines = [line.__class__.create_from(line) for line in lines_to_copy.values()]
        self._lines = OrderedDict()
        self.add(*lines)

    @property
    def id(self):
        """The id property of the BoardSector"""
        return self._id

    @property
    def lines(self):
        """The lines property of the BoardSector"""
        return self._lines

    @property
    def lines_count(self):
        """The lines count property of the BoardSector"""
        return len(self.lines) + int(self._has_title)

    @property
    def max_lines_count(self):
        """The max lines count property of the BoardSector"""
        return self._max_lines_count + int(self._has_title)

    @property
    def title(self):
        """The title property of the BoardSector"""
        return self._title

    @property
    def _has_title(self):
        """The _has_title property of the BoardSector
        indicates wether this sector has a title or not
        """
        return self._title != None

    @property
    def draw_empty(self):
        """The draw_empty property of the BoardSector
        indicates wether the empty lines should be drawn or not
        """
        return self._draw_empty

    def add(self, *lines):
        """add(self, *lines) -> self
        Add line(s) to this sector

        *lines - The line(s) to add to the sector
        """
        for line in lines:
            if self.lines_count >= self.max_lines_count:
                raise OverflowError("Board sector '{sector}' has reached the maximum lines count of {max_cnt}".format(sector=self.id, 
                                                                                                                   max_cnt=self.max_lines_count))
            if line.id in self._lines:
                raise ValueError("Board sector '{sector}' already contains a line with the ID '{line.id}'".format(sector=self.id, line=line))

            self._lines[line.id] = line
            if not isinstance(line.id, int):
                setattr(self, line.id, line)

        return self

    def get(self, line_id):
        """get(self, line_id) -> BoardLine
        Get a line from the sector by its ID

        line_id - The ID of the line to get
        """
        return self._lines[line_id]

    def remove(self, *lines_ids):
        """remove(self, *lines_ids)
        Remove line(s) from the sector by ID(s)

        *lines_ids - The ID(s) of the line(s) to remove
        """
        for line_id in lines_ids:
            self._lines.pop(line_id)

    def clear(self):
        """clear(self)
        Clear all of the lines in this sector
        """
        self.lines.clear()

    def draw(self):
        """draw(self)
        Draw the sector to the screen
        """
        if self._has_title:
            self.title.draw()
        for line in self.lines.values():
            line.draw()
        if self.draw_empty:
            print("\n"*(self.max_lines_count-self.lines_count), end="")

    def __setattr__(self, name, value):
        try:
            if name in self._lines:
                super(BoardSector, self).__setattr__(name, self._lines[name])
        except AttributeError:
            pass

        super(BoardSector, self).__setattr__(name, value)

    def __rshift__(self, cls_name):
        """__rshift__(self, cls_name) -> custom BoardSector subclass
        Dynamically creating a new custom subclass of BoardSector. the new class will have the same
        lines and title as the one of this BoardSector instance and their current data will be set as the initial data
        value for the newly created class lines and title.

        cls_name - The name of the newly created subclass
        """
        return type(cls_name, (self.__class__, ), self.__dict__)

class TextBoard(BoardObject):
    def __init__(self, id=None, max_lines_count=LOG_BOARD_DEFAULT_LINES_COUNT):
        super(TextBoard, self).__init__()
        self._id = id
        self._max_lines_count = max_lines_count
        self._board = OrderedDict()

    @property
    def id(self):
        """The id property of the TextBoard"""
        return self._id if self._id is not None else id(self)

    @property
    def lines_count(self):
        """The lines count property of the TextBoard"""
        count = 0
        for brd_obj in self._board.values():
            count += brd_obj.max_lines_count
        return count

    @property
    def max_lines_count(self):
        """The max lines count property of the TextBoard"""
        return self._max_lines_count

    @max_lines_count.setter
    def max_lines_count(self, val):
        """The max lines count property setter of the TextBoard
        
        val - The max lines count to set"""
        self._max_lines_count = val

    def add(self, *brd_objects):
        """add(self, *brd_objects) -> self
        Add board object(s) to this board

        *brd_objects - The board object(s) to add
        """
        for brd_object in brd_objects:
            if self.lines_count + brd_object.max_lines_count > self.max_lines_count:
                raise OverflowError("Failed to add board object: The board has reached the maximum lines count of {max_cnt}".format(max_cnt=self.max_lines_count))
            self._board[brd_object.id] = brd_object

        return self

    def get(self, obj_id):
        """get(self, obj_id) -> BoardObject
        Get a board object from this board

        obj_id - The ID of the board object to get
        """
        return self._board[obj_id]

    def remove(self, *obj_ids):
        """remove(self, *obj_ids) -> BoardObject
        Remove board object(s) from this board

        *obj_ids - The ID(s) of the board object(s) to remove
        """
        for r_id in r_ids:
            self._lines.pop(r_id)

    def clear(self):
        """clear(self)
        Clear all of the board objects in this board
        """
        self._board.clear()

    def draw(self, clear_screen=False):
        """draw(self, clear_screen=True)
        Draw the board to the screen

        clear_screen - indicates wether the screen should be cleared
        first or not. in any case the drawing of the board will start
        from the first line and the previously drawn board will be
        erased. (Default: False)
        """
        if clear_screen:
            ANSI.scrn_reset()
        else: 
            ANSI.cur_set()
            self._erase_printed_board()

        for obj in self._board.values():
            obj.draw()

    def _erase_printed_board(self):
        """_erase_printed_board(self)
        Erase the printed board from the screen.
        """
        ANSI.cur_save()
        for i in range(self.max_lines_count):
            ANSI.ln_clear()
            ANSI.cur_next_ln()
        ANSI.cur_restore()

    def __getattr__(self, name):
        if name in self._board:
            return self._board[name]

    def __del__(self):
        ANSI.cur_down(self.max_lines_count)

def redraws(board, clear_screen=True):
    """redraws(board)
    A decorator that redraws the given board at the end of the
    decorated function

    board - The board to redraw
    """
    def _exec_and_redraw(func):
        def wrapper(*args, **kwargs):
            ret_val = func(*args, **kwargs)
            board.draw(clear_screen)
            return ret_val
        return wrapper
    return _exec_and_redraw

LineFieldDelegate = BoardLine.LineField.Delegate
class EmptyFieldDelegate(LineFieldDelegate):
    """EmptyFieldDelegate - An empty LineField delegate"""
    def on_text_change(self, field):
        pass

"""PlainTextLine - The most simple BoardLine one could wish.
This line has only field named text.
"""
PlainTextLine = BoardLine().add("text") >> "PlainTextLine"

class ProcessSector(BoardSector):
    def __init__(self, sector_id, max_lines_count=LOG_BOARD_SECTOR_DEFAULT_LINES_COUNT, title_line=None,
                 draw_empty=True, line_cls=PlainTextLine, line_handler=None, **line_fields):
        """__init__(self, sector_id, max_lines_count, title_line, draw_empty, line_cls, line_handler, **line_fields)
        Creates a ProcessSector which is a subclass of BoardSector
        This is a special sector class dedicated to work with subprocess.Popen that was created with the flags:
        stdout=PIPE and optionally stderr=STDOUT (Both values from the subprocess module)

        sector_id - The ID of the sector, used for accessing it from the containing board object
        max_lines_count - The maximum lines count to set for this sector (Not including the title line)
        title_line - A title line to display when drawing the sector, if none is given, no title will be drawn,
        otherwise a title will be drawn using the given BoardLine and both lines_count and max_lines_count will increase by one.
        (default: None)
        draw_empty - A boolean that indicates wether or not the empty lines of the sector should be drawn (default: True)
        line_cls - The BoardLine class to use for drawing the tracked process (default: PlainTextLine)
        line_handler - A callable that receives a line and manipulates it as desired
        **line_fields - kwargs to format the created Boardlines. The values should be either a callable that returns a string or a string.
        """
        super(ProcessSector, self).__init__(sector_id, max_lines_count=max_lines_count, title_line=title_line, draw_empty=draw_empty)
        if not hasattr(line_cls, "text"):
            raise ValueError("ProcessSector BoardLine must have a text field.")
        self._line_cls = line_cls
        self._line_fields = line_fields
        self._line_handler = line_handler

    def update_from_file(self, file):
        """update_from_file(self, file) -> bool
        Update the sector with output from the given file object, returning true as long as there is data to read.

        file - The file object to read the lines from
        * NOTE: file must supply a readline method.
        """
        line = file.readline()
        if not line: return False
        brd_line = self._line_cls()
        brd_line.text = line
        for field, field_val_getter in self._line_fields.items():
            brd_line.get(field).text = field_val_getter if not callable(field_val_getter) else field_val_getter()
        if self._line_handler is not None: self._line_handler(brd_line)
        if self.lines_count >= self.max_lines_count:
            self.lines.popitem(False)

        self.add(brd_line)
        return True