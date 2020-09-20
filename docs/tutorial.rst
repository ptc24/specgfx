Tutorial
========

This tutorial is intended to introduce the basic concepts of specgfx - further details are available in the
API documentation.

Screen Layout
-------------

The specgfx screen consists of a border (which can be one of 8 colours) and a main display. The main display is
256x192 pixels, divided into 32x24 8x8 character cells. Colour is slightly complicated. Each character cell
has an ink colour (one of 8) and a paper colour (one of 8), and can be bright or not (the border is
never bright), and flashing or not.
Each pixel can be either the ink colour or the paper colour. Some commands work with text coordinates, in the
range 0-31,0-23, and some work with pixel coordinates, in the range 0-255,0-191. In both cases, 0,0 corresponds
to the top left of the main display.

The colours are 0=black, 1=blue, 2=red, 3=magenta, 4=green, 5=cyan, 6=yellow, 7=white. The idea seems to be that
colours that look brighter on screen (and which would be shown brighter on a black-and-white TV) have higher values.
Another way of thinking about it is that these numbers are not RGB values but BRG values - i.e. 1 * blue + 2 * red
+ 4 * green.

The Basics
----------

A "hello world" example::

    from specgfx import *
    INIT()
    PRINT("Hello world!")
	PRINT("Press any key to end")
	GETKEY()
	BYE()

specgfx is designed to be imported with ``from specgfx import *``. All of the commands are in upper-case, like in most
8-bit BASICs.

It is necessary to call ``INIT()`` to initialise the system before calling any further commands. You may wish to add some
options to the call - for example ``INIT(SIZEX=2)`` will show the screen double-sized.

The ``PRINT`` command is the heart of specgfx. Mostly, it works like the ``print`` command in regular Python - it has
``sep`` and ``end`` options. There is one difference, sep is the empty string by default, so ``PRINT("A","B")`` will print
``AB``, not ``A B``. The end option by default is ``"\n"``, so strings will be printed by default with a newline.
There are additional options which will be introduced later.

``GETKEY()`` will wait for the user to press a key, and return the key pressed. If, instead, you want to wait for a defined
span of time, then use ``PAUSE``. It takes one argument - the number of frames to pause for. Specgfx will try to run at 60
frames per second if possible, by may run slower if there is a lot of computation going on.

``BYE()`` shuts down specgfx and the python program that is running.

Many of the examples I present below are not full programs. You will typicially need ``from specgfx import *`` and ``INIT()``
before the commands, and ``GETKEY()`` and ``BYE()`` after them, in order for the program to work, and for the output to last
long enough to be seen.

Text
----

First, it is necessary to mention the character set. It is mostly 7-bit ASCII, with control characters below
character 32 (some standard,
some special to specgfx, reflecting the control characters on the ZX Spectrum). The pound sign is assigned to code point
96 - i.e. what is normally a backtick (`````). ASCII 127 (``"\\x7f"``) is a copyright sign.
ASCII 128-143 (i.e. ``"\\x80"`` to ``"\\x8f"`` - or ``chr(128)`` to ``chr(143)``) are block 
drawing characters. The characters from 144 to 255 are blank, but can be redefined using the
``UDG`` command (see later), as can all of the other characters.

The control characters are the key to working with the colour and positioning capabilities of specgfx,
but you do not need to use them directly. Instead, functions - ``AT``, ``TAB``, ``INK``, ``PAPER``,
``BRIGHT``, ``FLASH``, ``OVER`` and ``INVERSE`` are provided. 

``AT`` and ``TAB`` move the cursor. ``AT`` has two arguments - the first is the row number and the second is the column
number. Note that this may not be the way around that you expect - it does follow how ZX Spectrum BASIC works. ``TAB`` has
one argument - the column you wish to go to. An example::

	PRINT(AT(12,16),"Middle of the screen")
	PRINT(AT(0,0),"Top left")
	PRINT(AT(1,1),"Diagonal of stars",AT(2,2),"*",AT(3,3),"*",AT(4,4),"*",AT(5,5),"*")
	PRINT(AT(14,0),"Tab Test",TAB(16),"On the same line",TAB(0),"On the next line")
	
Note that the results of ``AT`` and ``TAB`` are strings, and can be manipulated like other strings. Example::
	
	a = AT(2,2) + "*" + AT(3,3) + "*" + AT(4,4) + "*" + AT(5,5) + "*"
	PRINT(a)

``INK`` and ``PAPER`` control colour. Each character sits in an 8x8 pixel "character cell", and each character cell has an
"attribute", that controls the ink colour of the cell, the paper colour of the cell, and whether the colours there are "bright"
and "flashing". There are eight colour values, as on the ZX Spectrum: 0=Black 1=Blue 2=Red 3=Magenta 4=Green 5=Cyan 6=Yellow 7=White

Example::

	PRINT("Black text ",INK(2),"then red text ",PAPER(1),"on blue.")
	
Note that any changes made using this are temporary - the next call to ``PRINT`` will not use those options. Example::

	PRINT("Black text ",INK(2),"then red text ",PAPER(1),"on blue.")
	PRINT("Back to black")
	
However, these changes can be made permanent, using the ``set`` keyword for ``PRINT``. Example::

	PRINT("Black text ",INK(2),"then red text ",PAPER(1),"on blue.", set=True)
	PRINT("Still red on blue")
	PRINT(INK(0),PAPER(7),"Back to black on white", set=True)
	
If you just want to set the paper and ink colour (or the other options below), then you can use ``SET`` instead of
``PRINT``. It works just like ``PRINT``, except it uses the arguments ``end=""`` and ``set=True``. Example::

	SET(INK(2),PAPER(1))
	PRINT("Red on blue.")

As well as ``INK`` and ``PAPER`` there are ``BRIGHT`` and ``FLASH``. These take values from 0-1 rather than 0-7,
but otherwise work in the same way. 0 is off, 1 is on.
	
There is also ``OVER`` and ``INVERSE`` - again, these take values 0-1. ``OVER(1)`` writes with XOR - for every pixel
it is going to draw, it checks to see if there is a pixel there already, and if so, deletes that pixel rather than
drawing one. ``INVERSE(1)`` writes in inverse video - within a character cell, it draws pixels only in the places where
it would not normally draw pixels, and erases pixels in the places in would normally draw them. Example::

    PRINT(AT(0,0),"over and",AT(0,0),OVER(1),"over again we go")
	PRINT(AT(1,0),INVERSE(1),"Inverse video")

There are a couple of additional commands which are not strictly text commands, but are useful when working with text.
``CLS()`` clears the screen, and sends the cursor to the top left. ``BORDER`` sets the border. It has one argument - the
border colour - from 0-7. For example ``BORDER(1)`` sets the border to blue. Note that there is no way to make the border
bright or flashing, just as on the ZX Spectrum.

Advanced text commands
----------------------

Three commands let you do further work with the text and colour capabilities. ``SCREENSTR`` looks at the screen to see
what character is drawn there. ``ATTR`` and ``SETATTR`` work with the "attributes" at a text position - these are 8-bit numbers
that encode the ink and paper colours along with whether the character position is bright or not and flashing or not. The
lowest three bits encode ink, then the next three encode paper, then one bit for bright, and the highest bit encodes flash.
http://www.breakintoprogram.co.uk/computers/zx-spectrum/screen-memory-layout has more detail on attributes. Anyway,
``ATTR`` looks up the attribute at a character position and ``SETATTR`` sets it.

``SETATTR`` can also just set the bits corresponding to ink, paper, bright or flash, using the optional arguments.

Example::

	PRINT(AT(0,0),"Inks")
	PRINT(AT(1,0),"01234567")
	for i in range(8): SETATTR(i,1,INK=i)
	PRINT(AT(2,0),"Papers")
	PRINT(AT(3,0),"01234567")
	for i in range(8): SETATTR(i,3,PAPER=i)
	PRINT(AT(4,0),"Bright")
	PRINT(AT(5,0),"01")
	for i in range(2): SETATTR(i,5,BRIGHT=i)
	PRINT(AT(6,0),"Flash")
	PRINT(AT(7,0),"01")
	for i in range(2): SETATTR(i,7,FLASH=i)
	PRINT(AT(8,0),"Attrs")
	PRINT(AT(9,0),"0123456789abcdef")
	for i in range(16): SETATTR(i,9,i) # SETATTR(i,9,ATTR=i) also works
	PRINT(AT(10,0),"Combo")
	PRINT(AT(11,0),"0")
	SETATTR(0,11,INK=4,PAPER=3,BRIGHT=1,FLASH=0)
	PRINT(AT(12,0),"Attr at 0,0: ",ATTR(0,0)) # Should be ink 0 paper 7 bright 0 flash 0 - i.e. 56


The Keyboard
------------

There are three ways to read the keyboard. ``GETKEY`` waits for a keypress and returns a string corresponding to the key
pressed. This is useful for "get any key" situations. ``INKEYS`` works like INKEY$ on a ZX Spectrum - it returns a string
corresponding to a key that is down, or the empty string if no key is down. ``INPUT`` displays a prompt and allows the user
to type in text.

Example::

	PRINT("Press a key to continue")
	key = GETKEY()
	PRINT("You pressed: ", key)
	name = INPUT("What is your name")
	PRINT("Hello, ", name, "!")
	while True:
		key = INKEYS()
		if key == "": key = " "
		PRINT(AT(12,16), key)

Pixel Graphics
--------------

Pixel graphics in specgfx work on a 256x192 grid, with 0,0 at the top left. Just as there is a text cursor which moves
as text is written to the screen, there is a graphics cursor that moves as graphics are drawn.

``PLOT`` draws a single pixel, at the coordinates specified. It also moves the graphics cursor to that point. To move
the graphics cursor without drawing to the screen, use ``MOVE``.

``DRAW`` and ``DRAWTO`` draw lines - straight or curved - from the graphics cursor. ``DRAW`` draws relative to the graphics
cursor, ``DRAWTO`` draws to the specified point. An example should illuminate::

	PLOT(10,10)
	for i in range(10):
		DRAW(0,10) # draw along 10 pixels
		DRAW(10,0) # draw down 10 pixels
	PLOT(100,10)
	for i in range(10):
		DRAWTO(100+10*(i+1),10+10*i))
		DRAWTO(100+10*(i+1),10+10*(i+1))
		
This should draw two staircases - in this case it is simpler to use ``DRAW`` but sometimes ``DRAWTO`` is simpler.

You can draw arcs with ``DRAW`` and ``DRAWTO``, with the third argument being the angle the arc goes through. This
is in radians, so pi draws a semicircle, pi/2 draws a quarter circle, etc. Be careful of values close to 2*pi as this
will try to draw a very large circle that will mostly go off screen. By default the arcs curve to the left - to curve to
the right, make the third argument negative. To draw a full circle, use ``CIRCLE``. It has three arguments - the x and y
of the centre, and the radius. An example::

	MOVE(10,10)
	for i in range(8):
		DRAW(25,15,i*3.14159/4) # Draw increasingly curvy arcs, from a straight line to seven-eighths of a circle
	CIRCLE(200,50,40) # A full circle elsewhere, for comparison.

The commands ``PLOT``, ``DRAW``, ``DRAWTO`` and ``CIRCLE`` can draw using various options - an ink colour, and 
"inverse" and "over" settings. These may be set permanently using the ``SET`` command, as for text, or
temporarily using the additional arguments INK, OVER and INVERSE. An example::

	PLOT(10,10) # starting point
	DRAW(50,0) # draw in default colour - black
	SET(INK(2)) # change to red
	DRAW(10,20) # draw in red
	DRAW(-10,20,INK=4) # draw temporarily in green
	DRAW(10,20) # now we're back to red

Note that the colours don't go neatly where you put them. This is due to the "character cell" effect - for every point
drawn, the entire character cell containing that point has its ink colour set. This is just like how a ZX Spectrum works!

The OVER and INVERSE options are useful for erasing pixels. Plotting and drawing with INVERSE on simply erases pixels.
Plotting and drawing with OVER on draws pixels where the screen originally had no pixel, but erases pixels where they
are already there - i.e. it XORs with what's already there. The following snippet should show the differences::

	MOVE(10,50) # starting point
	DRAW(40,0) # A line for reference
	MOVE(20,40)
	DRAW(0,20) # Draws over the existing line
	MOVE(30,40)
	DRAW(0,20,OVER=1) # Erases the crossing point, but draws the rest of the line
	MOVE(40,40)
	DRAW(0,20,INVERSE=1) # Just erases the crossing point

There is also the POINT command, which looks at the pixel at a given location, returning 1 if the pixel is set, and 0 if
it is unset. Example::

	CLS()
	PLOT(100,100)
	PRINT(POINT(100,100)) # should print 1
	PRINT(POINT(100,101)) # should print 0

Updating
--------

Getting graphics to the screen is more complicated with specgfx than with a ZX Spectrum. With a ZX Spectrum, all the system
has to do is write to the screen memory, and the graphics hardware will automatically find what has been written there
and display it to the screen. Specgfx needs to turn its screen memory into an image a modern computer can work with,
manipulate that image a bit, then send it to the operating system. This process is know as "updating", and is also
an opportunity for specgfx to read the keyboard, update flashing graphics, deal with the window the program is running in,
etc.

There are two schedules for updating - automatic and manual. Automatic is the default - it updates after every text and
graphics command. This is simple but slow. Manual updating mode can be accessed using ``MANUALUPDATE()``. There, an
update will only happen when ``UPDATE()`` is called. You can go back to automatic updating by calling ``AUTOUPDATE()``.
The following example should illuminate::

	CLS()
	
	# Auto-updating, the slowest
	MOVE(0,0)
	for i in range(32):
		DRAW(0,4)
		DRAW(4,0)
		DRAW(0,-4)
		DRAW(4,0)

	MANUALUPDATE()
	# This updates every fourth DRAW, and so is four times as fast
	MOVE(0,50)
	for i in range(32):
		DRAW(0,4)
		DRAW(4,0)
		DRAW(0,-4)
		DRAW(4,0)
		UPDATE()

	# This only updates when the whole thing is drawn, and so is the fastest
	MOVE(0,100)
	for i in range(32):
		DRAW(0,4)
		DRAW(4,0)
		DRAW(0,-4)
		DRAW(4,0)
	UPDATE()

	AUTOUPDATE()

There are other reasons to call ``UPDATE()``. If you're doing hard computation, which takes a lot of time, calling
``UPDATE()`` every now and again will keep things moving, and avoid the impression that the system has hung. If you're
waiting for ``INKEYS()`` to return something, updating will keep reading the keyboard, to make sure the value returned
will be up-to-date.


User-Defined Graphics
---------------------

The ZX Spectrum has options to redefine the character set, and specgfx takes this further. The ``UDG`` command
allows characters to be redefined. It takes two arguments - the first argument is the character number to redefine - values
from 32 to 255 are meaningful, values above 144 (i.e. 0x90) will avoid clashing with pre-existing characters. The second
argument is a tuple of 8-bit integers, with each bit representing a pixel.

``GETCHARDEF`` is the inverse of ``UDG`` - give it a character number and it'll return the character definition.
``RESETCHARS`` will return everything to normal.

Example::

	# Make and print a UDG
	UDG(0x90, (0b00000001,
			   0b00000011,
			   0b00000111,
			   0b00001111,
			   0b00011111,
			   0b00111111,
			   0b01111111,
			   0b11111111))
	PRINT("\x90")
	# Examine the letter 'a'
	d = GETCHARDEF(ord('a'))
	for i in d:
		PRINT(format(i, "08b"))
	# Redefine characters to be upside down - i.e. with the first row last etc.
	for i in range(32,128):
		UDG(i, tuple(reversed(GETCHARDEF(i))))
	PRINT("Upside down!")
	# ...and put everything back.
	RESETCHARS()
	PRINT("Right way up!")

Sound
-----

The one sound command is ``BEEP()``, and it is currently very crude. It takes two parameters - a duration in seconds,
and a pitch - in semitones above middle C (this may be negative for pitches below middle C). The duration and pitch are
very approximate, don't count on anything musical. The following example attempts to play a scale::

	BEEP(0.25,0)
	BEEP(0.25,2)
	BEEP(0.25,4)
	BEEP(0.25,5)
	BEEP(0.25,7)
	BEEP(0.25,9)
	BEEP(0.25,11)
	BEEP(0.25,12)


Internals
---------

For people intending to use specgfx for prototyping things for the real ZX Spectrum.

``GETMEMORY()`` gets the screen memory, as a numpy array. This is a 32k array of unsigned 8-bit
integers (mimicing the address space of a 16k ZX Spectrum, with the first 16k representing ROM),
and is mostly zeros. The screen memory is laid out as in a ZX Spectrum, with
the pixels starting at 0x4000 and the attributes starting at 0x5800, ending at 0x5aff.
    
This gets the actual array that specgfx works with - changing values in this array (between
0x4000 and 0x5aff) will change the screen once you call UPDATE.

``PEEK`` and ``POKE`` are similar, but allows the memory to be read and written at specific locations.

An example::

	mem = GETMEMORY()
	# Write random stuff to the whole of screen memory
	for i in range(0x4000,0x5aff):
		mem[i] = random.randint(0,255)
		UPDATE()

	# Just the attributes - update odd-numbered cells to have the same attribute as the cells next to them.
	for i in range(0x5800,0x5aff,2):
		POKE(i+1,PEEK(i))
		UPDATE()
