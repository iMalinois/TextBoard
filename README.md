# TextBoard

 - [1. About](#1-about)
 - [2. Documentation](#2-documentation)
    - [2.1. Lines](#21-lines)
       - [2.1.1. Your First Line](#211-your-first-line)
          - [2.1.2.1. Accessing the line using its ID](#2121-accessing-the-line-using-its-id)
       - [2.1.2. Adding some fields](#212-adding-some-fields)
       - [2.1.3. Creating A Custom Dynamic Line Class](#213-creating-a-custom-dynamic-line-class)
          - [2.1.3.1. BoardLine ```create``` method](#2131-boardline-create-method)
          - [2.1.3.2. BoardLine ```duplicate``` method](#2132-boardline-duplicate-method)
          - [2.1.3.3. The PlainTextLine](#2133-the-plaintextline)
       - [2.1.4. Field Styles](#214-field-styles)
       - [2.1.5. Field Delegate](#215-field-delegate)
    - [2.2. Sector](#22-sector)
       - [2.2.1. Creating a sector](#221-creating-a-sector)
          - [2.2.1.1. Accessing lines inside of sectors](#2211-accessing-lines-inside-of-sectors)
       - [2.2.2. Sector size and empty lines](#222-sector-size-and-empty-lines)
          - [2.2.2.1. max_lines_count](#2221-max_lines_count)
          - [2.2.2.2. draw_empty](#2222-draw_empty)
       - [2.2.3. Sector Title](#223-sector-title)
       - [2.2.4. Creating A Custom Dynamic Sector Class](#224-creating-a-custom-dynamic-sector-class)
    - [2.3. The TextBoard](#23-the-textboard)
       - [2.3.1. Creating a TextBoard](#231-creating-a-textboard)
       - [2.3.2. Adding BoardObjects](#232-adding-boardobjects)
       - [2.3.3. The draw method](#233-the-draw-method)
          - [2.3.3.1. The redraws decorator](#2331-the-redraws-decorator)
    - [2.4. Special BoardObjects](#24-special-boardobjects)
       - [2.4.1. ProcessSector](#241-processsector)
 - [3. Change log](#3-change-log)
 - [4. License](#4-license)
 - [5. Contact](#5-contact)

## 1. About

TextBoard is a Python module for creating and displaying text and data, using your custom lines and sectors.

This module is useful for displaying logs or multi-processes tracking but it can be used for much more, as you can define your own sectors and lines structures, the possibilities are endless.

## 2. Documentation

### 2.1. **Lines**

Line is the most basic TextBoard object. lines are added to a board or a sector and they contain the actual text. their text is stored in one or move field.

#### **2.1.1. Your First Line**

Lets start with a simple example: Drawing a line to the board once.

```Python
from textboard.board import BoardLine, TextBoard

board = TextBoard() # Creates an empty text board

line = BoardLine().add("text") # Creates a line with a single field named 'text'
line.text = "Hello World!" # Sets the text of the 'text' field of our line.

board.add(line) # Add our line to the text board
board.draw() # Prints the text board
```

The output of this code would be:

```
Hello World!
```

> Please note that the board clears the screen when drawn, so your board would be printed from the beginning of your console.

##### **2.1.2.1. Accessing the line using its ID**

On this example, we created a board and added a line to it. now lets say that we want to create a board with multiple lines, and that we want to change the values of existing lines in the board, how do we do that?

For this purpose, any BoardObject (The base class of our TextBoard object, including the board itself) has a property called id.

When creating a line, we can give it a unique id that will be used to access this line later in its containing sector/board.

To show that, we will use the previous example and add an id for our line:

```Python
from textboard.board import BoardLine, TextBoard

board = TextBoard() # Creates an empty text board

line = BoardLine("first").add("text") # Creates a line with a single field named 'text'
line.text = "Hello World!" # Sets the text of the 'text' field of our line.

board.add(line) # Add our line to the text board
board.first.text = "Now I have a different text!"
board.draw() # Prints the text board
```

The output of this code would be:

```
Now I have a different text!
```

You may also use the ```get()``` method of boards and sectors to access a line. Using this method is necessary only if you want to access a line without a given ID. if that the case, the way to do it is as follows:

```Python
board.get(id(line)).text = "Now I have a different text!"
```


#### **2.1.2. Adding some fields**

Now lets create a more interesting text board, that prints some logs:

```Python
from textboard.board import BoardLine, TextBoard

board = TextBoard() # Creates an empty text board

# Creates a line for a log with 3 fields named: 'id', 'level' and 'info'. each field has a specific size.
line = BoardLine().add("log_id", size=3)\
                  .add("level", size=10)\
                  .add("info", size=20)
line.log_id = "0" # Sets the text of the 'log_id' field of our line.
line.level = "CRITICAL" # Sets the text of the 'level' field of our line.
line.info = "Such a critical log" # Sets the text of the 'info' field of our line.

board.add(line) # Add our line to the text board
board.draw() # Prints the text board
```

As stated, we added 3 fields to our line.
When adding fields, there is a mandatory parameter and multiple optional parameters:

The mandatory parameter is the **field's ID**. The field ID is used to access the field inside the line.

The optional parameters are:

* **size** - The size of the field in the line, if the text of the field is shorter than the field size, it would be padded. if longer, trimmed. default is not limited.
* **text** - The initial text of the field.
* **style** - The style of the field (See 2.4 for additional information)
* **delegate** - The delegate of the field (See 2.5 for additional information)

This time, the output would be:

```
0  CRITICAL  Such a critical log
```

As you can see, there is a padding for each field that fill it to the requested size.

#### **2.1.3. Creating A Custom Dynamic Line Class**

Creating a custom line is simple, as seen above, but what should you do if you want to create multiple lines like the log line we have created before? should you create a new line and add its fields each time?

Luckily, the answer is no! TextBoard lines allow you to create dynamic classes easily.

We will use the same line from the previous example:

```Python
from textboard.board import BoardLine, TextBoard

board = TextBoard() # Creates an empty text board

# Creates a dynamic line class for logs with 3 fields named: 'id', 'level' and 'info'. each field has a specific size.
LogLine = BoardLine().add("log_id", size=3)\
                  .add("level", size=10)\
                  .add("info", size=20) >> "LogLine"

line1 = LogLine()
line1.log_id = "0"
line1.level = "CRITICAL"
line1.info = "Such a critical log"

line2 = LogLine()
line2.log_id = "1"
line2.level = "LOW"
line2.info = "A not so interesting log"

# Add our lines to the text board
board.add(line1)
board.add(line2)
board.draw() # Prints the text board
```

The output, as expected:
```
0  CRITICAL  Such a critical log 
1  LOW       A not so interesting log
```

> Please note that the constructor of a dynamic line class is the same as ```BoardLine``` constructor, meaning that it only receives one argument: the id of the line.

##### **2.1.3.1. BoardLine ```create``` method**

We have learned how to create a dynamic line class but filling each line field separately can be a bit annoying.

Because of that, BoardLine, and any custom dynamic lines, have a class method named ```create```.

The method's signature is: ```create(cls, line_id=None, **fields)``` and it allows the creation of board lines in one line of code.

Knowing that, instead of creating the LogLine we defined previously this way:

```Python
line1 = LogLine()
line1.log_id = "0"
line1.level = "CRITICAL"
line1.info = "Such a critical log"
```

We can create it this way:

```Python
line1 = LogLine.create(log_id="0", level="CRITICAL", info="Such a critical log")
```

> Note that you can also assign an ID to your line using the ```create``` method. The ID is the first argument of this method but it has a default value of ```None```.

##### **2.1.3.2. BoardLine ```duplicate``` method**

another BoardLine method that is worth mentioning is the ```duplicate``` method. The ```duplicate``` method let you create a copy of your existing line which has only one difference from the original line - its ID.

The reason for the existance of this method is that you can't add a line to a sector if its ID already exist in that sector. Attempting to do so will result in a ```ValueError```.
Therefore, if you wish to fill your board with lines that have the same values, the ```duplicate``` method is your easiest way to do so.

The method's signature is: ```duplicate(self, line_id=None)```

If a line_id is given, it will be assigned as the ID of the duplicated line, otherwise a random ID will be assigned.

##### **2.1.3.3. The PlainTextLine**

Now that we have learend about the dynamic BoardLine classes, there is a dynamic BoardLine class supplied by the package, called PlainTextLine. This line class has only one field, named "text".


By learning that, we can rewrite our first example:

```Python
from textboard.board import BoardLine, TextBoard, PlainTextLine

board = TextBoard() # Creates an empty text board

line = PlainTextLine() # Creates a line with a single field named 'text'
line.text = "Hello World!" # Sets the text of the 'text' field of our line.

board.add(line) # Add our line to the text board
board.draw() # Prints the text board
```

And the output would be the same as the first example.

#### **2.1.4. Field Styles**

Printing text is nice, but what about adding some styles and colors? TextBoard supports that too!

When creating a field, you can pass a TextStyle instance that will change the style of the field when printed.

```Python
from textboard.ansi import TextStyle, TextColors
from textboard.board import BoardLine, TextBoard

board = TextBoard() # Creates an empty text board

style = TextStyle(fg=TextColors.green, bold=True)

LogLine = BoardLine().add("log_id", size=3)\
                  .add("level", size=10, style=style)\
                  .add("info", size=20) >> "LogLine"

line = LogLine()
line.log_id = "0"
line.level = "LOW"
line.info = "A not so interesting log"

board.add(line)
board.draw()
```

This time, when running, the LOW field would be printed in green and bold.

TextStyle supports many styles options:

* Foreground Color (fg)
* Background Color (bg)
* Bold (bold)
* Faint (faint)
* Italic (italic)
* Underline (underline)
* Slow Blinking (blink_slow)
* Fast Blinking (blink_fast)
* Crossed Out (crossed_out)

> Currently, only 8bit coloring is supported, 24bit coloring support will be available soon.

#### **2.1.5. Field Delegate**

until now, we learend that we can create dynamic text lines, and that we can change the style of the line's field.

But should we change the style or text of fields manually each time we create a line or changed its text to a value that we might want to change? Yet again, the answer is no, and the solution is delegates.

Lets take our LogLines again. There are many log levels and we want to print each one in a different color. We are going to do this with LineFieldDelegate.

```Python
from textboard.ansi import TextStyle, TextColors
from textboard.board import BoardLine, TextBoard, LineFieldDelegate

board = TextBoard() # Creates an empty text board

style = TextStyle(fg=TextColors.green, bold=True)

class LogLevelDelegate(LineFieldDelegate):
    def on_text_change(self, field):
        if field.text == "LOW":
            field.style = TextStyle(fg=TextColors.green, bold=True)
        elif field.text == "CRITICAL":
            field.style = TextStyle(fg=TextColors.red, bold=True)

LogLine = BoardLine().add("log_id", size=3)\
                  .add("level", size=10, delegate=LogLevelDelegate())\
                  .add("info", size=20) >> "LogLine"

line1 = LogLine()
line1.log_id = "0"
line1.level = "CRITICAL"
line1.info = "Such a critical log"

line2 = LogLine()
line2.log_id = "1"
line2.level = "LOW"
line2.info = "A not so interesting log"

board.add(line1)
board.add(line2)
board.draw()
```

Now, when running this code, two log lines would be printed, on the first line, the word critical would be bolded and red, and on the second line, the word low would be bolded and gree.

The LogLevelDelegate only delegates the field's text change.

### **2.2. Sector**

Sector is another TextBoard object. Sectors may contain multiple lines and a board may contain multiple sectors or none at all.

#### **2.2.1. Creating a sector**

Sectors, as a BoardObject, also have an id, but as opposed to lines the id field of the sector is mandatory. the usage of this ID is to access the sector inside a board.

Except for ID, there are other sectors properties, but they are optional:

* **Max Lines Count (max_lines_count)** - The maximum lines count of the sector (Not including the title line), if no value is specified, the default value is used.
* **Title Line (title_line)** - A title line to display when drawing the sector, if none is given, no title will be drawn,
otherwise a title will be drawn using the given BoardLine and both lines_count and max_lines_count will increase by one. (By default there is no title for the sector)
* **Should Empty Lines Be Drawn (draw_empty)** - A boolean that indicates whether or not the empty lines of the sector should be drawn (By default they will be drawn)

Now, lets see an example of how to create a sector:

```Python
from textboard.board import BoardLine, BoardSector, TextBoard

board = TextBoard() # Creates an empty text board

sector = BoardSector("sec") # Create a sector with an id equaks to 'sec'
board.add(sector) # Adding the sector to the board

line = BoardLine("first").add("text") # Creates a line with a single field named 'text'
line.text = "Hello World!" # Sets the text of the 'text' field of our line.

board.sec.add(line) # Add our line to the sector
board.draw() # Prints the text board
```

As you can see, we have created a sector and added it to the board. later we have created a line and added it to our sector. We used the sector's ID to access the sector from the board but we could have added the line to the sector directly.

The output of this example is:

```
Hello World!
```

> Note that the empty lines of the sector will also be printed, but more on that later.

##### **2.2.1.1. Accessing lines inside of sectors**

We previously learned that you can access a line from a board by its id and we just saw that we can access sectors by their id.

The existing BoardObjects makes it easy for you to access the objects that they contain by using those objects id.

from that you can understand, that the way to access a line inside a sector is the same way to access a line inside of a board:

```Python
sector.first.text = "A different text!" # Accessing a line, inside of a sector
board.sec.first.text = "A different text!" # Accessing a line, inside of a sector, inside of a board
```

You may also use the ```get()``` method of boards and sectors to access a line. Using this method is necessary only if you want to access a line without a given ID. if that the case, the way to do it is as follows:

```Python
board.sec.get(id(line)).text = "Now I have a different text!"
```

#### **2.2.2. Sector size and empty lines**

We mentioned earlier that when creating a sector, there are multiple optional parameters. two of them is "max_lines_count" and "draw_empty".

##### **2.2.2.1. max_lines_count**

The "max_lines_count" is a limit for the maximum number of lines the sector can hold. attempting to add a line to a full sector will result in an OverflowError

> Boards, like sectors, also have a maximum lines count, more on that later.

> It is worth mentioning that the current count of lines in your sector can be accessed with the ```lines_count``` property

> Note that if you give a title line to your sector, the maximum number of lines and the current number of lines will be increased by one.

##### **2.2.2.2. draw_empty**

Because sectors have a maximum lines count, and because you might want to add multiple sectors to your board with a vertical padding, sectors by default draw their empty lines to the screen. if you don't want those empty lines to be printed, then just pass false to the ```draw_empty``` argument of the sector's constructor, and the empty lines won't be printed.

#### **2.2.3. Sector Title**

When we listed the sector properties, we talked about a title line. the title line is a special optional line inside a sector, accessed through the ```title``` property.

if a title exists, it will be drawn first at the sector's drawing and it will increase both ```max_lines_count``` and ```lines_count```

if no title exists, the ```title``` property of the sector will be equal to ```None```.

Lets see a short example of how to use a title.

```Python
from textboard.board import BoardLine, BoardSector, TextBoard

TitleLine = BoardLine().add("index", 3)\
                       .add("name") >> "TitleLine"

LogLine = BoardLine().add("log_id", size=3)\
                  .add("level", size=10)\
                  .add("info", size=20) >> "LogLine"

board = TextBoard() # Creates an empty text board

log_title = TitleLine.create(index="0", name="LOGS") # Creating our title line for the sector.

sector = BoardSector("sec", title_line=log_title) # Create a sector with an id equaks to 'sec' and a title line.

line = LogLine.create(log_id="0", level="CRITICAL", info="Such a critical log")

sector.add(line)
board.add(sector)
board.draw()
```

And as expected, the output will be:

```
0  LOGS
0  CRITICAL  Such a critical log 
```

#### **2.2.4. Creating A Custom Dynamic Sector Class**

Sectors, like lines, also support dynamic class creation.
This is useful when you wish to have a sector with a title of a specific line class that you have created or to predefine the lines in a sector that you are creating.

For our example, we will create a sector class with a title line of type ```TitleLine``` that we have defined in the previous example.

```Python
from textboard.board import BoardLine, BoardSector, TextBoard

TitleLine = BoardLine().add("index", 3)\
                       .add("name") >> "TitleLine"

LogLine = BoardLine().add("log_id", size=3)\
                  .add("level", size=10)\
                  .add("info", size=20) >> "LogLine"

SectorWithTitle = BoardSector("SectorWithTitle", title_line=TitleLine()) >> "SectorWithTitle"

board = TextBoard() # Creates an empty text board

log_title = TitleLine.create(index="0", name="LOGS") # Creating our title line for the sector.

log_sector = SectorWithTitle("log_sec") # Create a sector of our custom class with an id equaks to 'log_sec' and a title line.

log_sector.title.index = "0"
log_sector.title.name = "LOGS"

general_sector = SectorWithTitle("general_sec") # Create a sector of our custom class with an id equaks to 'general_sec' and a title line.

general_sector.title.index = "1"
general_sector.title.name = "GENERAL"

line = LogLine.create(log_id="0", level="CRITICAL", info="Such a critical log")

board.add(log_sector)
board.add(general_sector)
board.log_sec.add(line)
board.draw()
```

So as we can see, we have created a custom sector class named ```SectorWithTitle``` and then created two sectors of that type.
We then add those two sectors to our board and later add a line to one of them. The output of this code is:

```
0  LOGS
0  CRITICAL  Such a critical log 



1  GENERAL
```

### **2.3. The TextBoard**

The ```TextBoard``` class is the main class of the package and it is used to display your sectors and lines. We have used it in our examples but on this sector we will dig into this class.

#### **2.3.1. Creating a TextBoard**

The ```TextBoard``` constructor have two optional argument:

* **ID (id)** - TextBoard is also a subclass of Boardobject and as one he may have an ID. currently there is no use for its ID in the package but it can be useful if there are multiple boards in your program and you need to identify them.
* **Max Lines Count (max_lines_count)** - The maximum lines count of the sector (Not including the title line), if no value is specified, the default value is used.

> Note that the max lines count of a board may also be modified after the creation of the board by changing the value of the ```max_lines_count``` property.

> The current lines count of the board is the sum of both the lines and the max lines count of the sectors (Including the title), when a BoardObject is appended to a board, the current lines count of the board is increased by the value of the ```max_lines_count``` property. the current lines count of a board is accessable through the ```lines_count``` property.

#### **2.3.2. Adding BoardObjects

Adding objects to the board is quite simple, we have seen examples thorugh the documentation - The way to do so is using the ```add``` method of the board. the ```add``` method is usable for any BoardObject.

lets take a look at one of the previous examples where we created a sector and a line and added them to a board:

```Python
from textboard.board import BoardLine, BoardSector, TextBoard

TitleLine = BoardLine().add("index", 3)\
                       .add("name") >> "TitleLine"

LogLine = BoardLine().add("log_id", size=3)\
                  .add("level", size=10)\
                  .add("info", size=20) >> "LogLine"

board = TextBoard() # Creates an empty text board

log_title = TitleLine.create(index="0", name="LOGS") # Creating our title line for the sector.

sector = BoardSector("sec", title_line=log_title) # Create a sector with an id equaks to 'sec' and a title line.

line = LogLine.create(log_id="0", level="CRITICAL", info="Such a critical log")

sector.add(line) # The line is appended to the sector but it could have been added to the board instead, just like we add the sector to the board in the next line.
board.add(sector)
board.draw()
```

And the output, as previously seen:

```
0  LOGS
0  CRITICAL  Such a critical log 
```

#### **2.3.3. The draw method**

The ```draw``` method of a board is probably the only draw method that you will be using because it does all of the hard work for you.
it clears the previously drawn board (or the entire screen) and then draws the current board (Printing all of its lines and sectors by calling to their own ```draw``` method).

The ```draw``` method begins from the first line of the screen and prints all of the ```max_lines_count``` of the board.

Lets take a look at the draw method signature:

```Python
draw(self, clear_screen=False)
```

We can see that this signature is pretty simple, with only one optional argument in existstance.

The ```clear_screen``` argument indicates whether or not the screen should be cleared before drawing the board or if the board should clear only the first ```max_lines_count``` from the screen.
On your first draw, you will probably want to pass ```True``` to this argument, to clear previously drawn text from the begining of the screen but later on you may run it with the default ```False``` value to prevent spam in the scrollback buffer.

##### **2.3.3.1. The redraws decorator**

The ```textboard.board``` module supplies a decorator named ```redraws``` which let you decrate your functions or method so they will draw a given board at the end of their logic.

The signature of the decorator is basically the same as the ```draw``` method of the board:

```Python
redraws(board, clear_screen=True)
```

As seen, instead of ```self```, you have to pass the board to redraw.

Here is a simple example that add 10 lines and redraws the board after each line:

```Python
from textboard.board import PlainTextLine, TextBoard, redraws

board = TextBoard()

@redraws(board)
def add_line(self, index):
    board.add(PlainTextLine.create(text="Line No. {}".format(index)))

for i in range(10):
    add_line(i)
```

The result after all of the iterations will be:
```
Line No. 0
Line No. 1
Line No. 2
Line No. 3
Line No. 4
Line No. 5
Line No. 6
Line No. 7
Line No. 8
Line No. 9
```

With each line being printed after each call to the ```add_line``` function.

### **2.4. Special BoardObjects**

This section of the documentation covers special BoardObjects custom classes that are supplied by the ```textboard``` package.

#### **2.4.1. ProcessSector**

The ```ProcessSector``` is a special ```BoardSector``` class, designed to be used with ```subprocess.Popen``` and thus track the progress of an executed process.

The signature of the ```ProcessSector``` is:

```Python
ProcessSector(self, sector_id, max_lines_count=LOG_BOARD_SECTOR_DEFAULT_LINES_COUNT, title_line=None,
              draw_empty=True, line_cls=PlainTextLine, line_handler=None, **line_fields)
```

* **Sector ID (sector_id)** - A mandatory field, it serves the same purpose as any ```BoardSector```'s ID.
* **Max Lines Count (max_lines_count)** - The maximum lines count of the sector (Not including the title line), if no value is specified, the default value is used.
* **Title Line (title_line)** - A title line to display when drawing the sector, if none is given, no title will be drawn,
otherwise a title will be drawn using the given BoardLine and both lines_count and max_lines_count will increase by one. (By default there is no title for the sector)
* **Should Empty Lines Be Drawn (draw_empty)** - A boolean that indicates whether or not the empty lines of the sector should be drawn (By default they will be drawn)
* **The Sector Lines' Class (line_cls)** - The ```ProcessSector``` create its own lines with data from the process that it tracks. By default it uses the ```PlainTextLine``` but you can give it a more complicated line class of your choice. The only limitation on that class is that it must contain a field named ```text```. In this field, the data from the tracked process will be presented.
* **The Line Handler (line_handler)** - The line handler is pretty much a delegate for the whole line. the line handler should be a callable that receives one argument - the line to manipulate. It then may edit any field or property of the given line. Note that in most of the cases, fields delegates can replace this handler and they are the ones that should be used. The handler should be used if you wish to manipulate a line in such way that requires an access to its properites and methods.
* **The Line Fields (\*\*line_fields)** - if you use a custom line class with custom fields, those keyword arguments let you to manipulate their values. for each argument, the keyword should be the field name in the line and the value should be either the actual value to set or a callable that returns the value to set.

The ```ProcessSector``` has one special method, named ```update_from_file```. The way to use this method is presented in the following example:

```Python
from textboard.board import TextBoard, ProcessSector
from subprocess import Popen, PIPE, STDOUT

board = TextBoard() # Creates an empty text board

proc_sec = ProcessSector("proc_sec") # Creates a default ProcessSector
board.add(proc_sec) # Adds the sector to the board

# Opens a process to track, the PIPE value for stdout is necessary, the STDOUT value for stderr let us also present the error output of our process.
proc = Popen('process-to-track', stdout=PIPE, stderr=STDOUT, shell=True)

# For each call of the update_from_file, a new line from the output of the process is added to the sector. false will
# be returned when there are no more lines to read from the output of the process.
while proc_sec.update_from_file(proc.stdout):
    board.draw(False)
    # Any other logic that you wish to execute between each line.
```

## 3. Change log

- ### **1.0.0**
  First version of the textboard, works only on Linux and OSX machines.

## 4. License

Copyright 2018 Or Yahalom

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## 5. Contact

If you wish to contact me, you can find me on:

Mail: itsMalinois@gmail.com

Twitter: [@iMalinois](https://twitter.com/iMalinois)