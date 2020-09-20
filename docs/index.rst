.. specgfx documentation master file, created by
   sphinx-quickstart on Tue Sep  1 18:26:59 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

specgfx
=======

ZX-Spectrum style text and graphics for Python. 

Requires Python 3, pygame and numpy. The easiest way to install is from pip:

``python -m pip install specgfx``

(you may want to try `python3` instead of `python` if that's how your system is set up). 

The best way to use this module is:

``from specgfx import *``

To start, run `INIT()`. If the screen is a little small, try `INIT(SIZEX=2)` or `INIT(SIZEX=3)` to
double or triple the size. For fullscreen, try `INIT(FULL=True)`.

Example program:

::

    from specgfx import *
    INIT()
    PRINT("Hello world!")
    PRINT(AT(2,2),"at 2,2 ",INK(1),"blue ",PAPER(5),"on yellow")
    PRINT(AT(5,2),"at 5,2 ",INVERSE(1),"inverse")
    name = INPUT(AT(6,0),"What is your name? ")
    PRINT("Hello, ", name, end="\\n")
    PRINT("Press any key to exit")
    while INKEYS() == "": UPDATE()
    BYE()
    
Some notes:

Colours - 0=Black 1=Blue 2=Red 3=Magenta 4=Green 5=Cyan 6=Yellow 7=White

Most of the characters are normal 7-bit ASCII. The pound sign is assigned to code point
96 - i.e. what is normally a backtick (`````). ASCII 127 (``"\\x7f"``) is a copyright sign.
ASCII 128-143 (i.e. ``"\\x80"`` to ``"\\x8f"`` - or ``chr(128)`` to ``chr(143)``) are block 
drawing characters. The characters from 144 to 255 are blank, but can be redefined using the
`UDG` command, as can all of the other characters.

Pressing the PAUSE BREAK key or the ESC key will exit from specgfx.

.. toctree::
   :maxdepth: 3
   :caption: Contents:
   
   tutorial
   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
