"""
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

Pressing the PAUSE BREAK key will exit from specgfx.

"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame.locals import *
import numpy as np
import time
import sys
import math

from .cyrender import cyrender

inkeys = ""

def INIT(FULL=False, SIZEX=1):
    """
    Initialise the specgfx system.
    
    Args:
    
    - FULL - boolean - whether to initialise fullscreen. 
    - SIZEX - integer - size multiplier for the output screen.
    """
    
    global size, width, height, screen, specsurf, defchar, memory, autoupdate, flashframe
    global charset
    global palette, ipalette, specarray, defcharset
    global flashc, flashrate, clock, cursorx, cursory, showcursor, printstate
    global ink, paper, flash, bright, inverse, over, border, keysdown, inkeys, keyd
    global graphicsx, graphicsy
    global sizex, scaledsurf

    graphicsx = 0
    graphicsy = 0

    pygame.mixer.pre_init(44100,8,1)
    pygame.init()

    sizex = int(SIZEX)
    if sizex < 1:
        sizex = 1

    size = width, height = 320*sizex,240*sizex

    if FULL:
        screen = pygame.display.set_mode(size, FULLSCREEN)
    else:
        screen = pygame.display.set_mode(size)

    specsurf = pygame.Surface((256, 192))
    if sizex > 1: scaledsurf = pygame.Surface((256*sizex,192*sizex))

    defcharset = [
    (0,0,0,0,0,0,0,0),
    (0,16,16,16,16,0,16,0),
    (0,36,36,0,0,0,0,0),
    (0,36,126,36,36,126,36,0),
    (0,8,62,40,62,10,62,8),
    (0,98,100,8,16,38,70,0),
    (0,16,40,16,42,68,58,0),
    (0,8,16,0,0,0,0,0),
    (0,4,8,8,8,8,4,0),
    (0,32,16,16,16,16,32,0),
    (0,0,20,8,62,8,20,0),
    (0,0,8,8,62,8,8,0),
    (0,0,0,0,0,8,8,16),
    (0,0,0,0,62,0,0,0),
    (0,0,0,0,0,24,24,0),
    (0,0,2,4,8,16,32,0),
    (0,60,70,74,82,98,60,0),
    (0,24,40,8,8,8,62,0),
    (0,60,66,2,60,64,126,0),
    (0,60,66,12,2,66,60,0),
    (0,8,24,40,72,126,8,0),
    (0,126,64,124,2,66,60,0),
    (0,60,64,124,66,66,60,0),
    (0,126,2,4,8,16,16,0),
    (0,60,66,60,66,66,60,0),
    (0,60,66,66,62,2,60,0),
    (0,0,0,16,0,0,16,0),
    (0,0,16,0,0,16,16,32),
    (0,0,4,8,16,8,4,0),
    (0,0,0,62,0,62,0,0),
    (0,0,16,8,4,8,16,0),
    (0,60,66,4,8,0,8,0),
    (0,60,74,86,94,64,60,0),
    (0,60,66,66,126,66,66,0),
    (0,124,66,124,66,66,124,0),
    (0,60,66,64,64,66,60,0),
    (0,120,68,66,66,68,120,0),
    (0,126,64,124,64,64,126,0),
    (0,126,64,124,64,64,64,0),
    (0,60,66,64,78,66,60,0),
    (0,66,66,126,66,66,66,0),
    (0,62,8,8,8,8,62,0),
    (0,2,2,2,66,66,60,0),
    (0,68,72,112,72,68,66,0),
    (0,64,64,64,64,64,126,0),
    (0,66,102,90,66,66,66,0),
    (0,66,98,82,74,70,66,0),
    (0,60,66,66,66,66,60,0),
    (0,124,66,66,124,64,64,0),
    (0,60,66,66,82,74,60,0),
    (0,124,66,66,124,68,66,0),
    (0,60,64,60,2,66,60,0),
    (0,254,16,16,16,16,16,0),
    (0,66,66,66,66,66,60,0),
    (0,66,66,66,66,36,24,0),
    (0,66,66,66,66,90,36,0),
    (0,66,36,24,24,36,66,0),
    (0,130,68,40,16,16,16,0),
    (0,126,4,8,16,32,126,0),
    (0,14,8,8,8,8,14,0),
    (0,0,64,32,16,8,4,0),
    (0,112,16,16,16,16,112,0),
    (0,16,56,84,16,16,16,0),
    (0,0,0,0,0,0,0,255),
    (0,28,34,120,32,32,126,0),
    (0,0,56,4,60,68,60,0),
    (0,32,32,60,34,34,60,0),
    (0,0,28,32,32,32,28,0),
    (0,4,4,60,68,68,60,0),
    (0,0,56,68,120,64,60,0),
    (0,12,16,24,16,16,16,0),
    (0,0,60,68,68,60,4,56),
    (0,64,64,120,68,68,68,0),
    (0,16,0,48,16,16,56,0),
    (0,4,0,4,4,4,36,24),
    (0,32,40,48,48,40,36,0),
    (0,16,16,16,16,16,12,0),
    (0,0,104,84,84,84,84,0),
    (0,0,120,68,68,68,68,0),
    (0,0,56,68,68,68,56,0),
    (0,0,120,68,68,120,64,64),
    (0,0,60,68,68,60,4,6),
    (0,0,28,32,32,32,32,0),
    (0,0,56,64,56,4,120,0),
    (0,16,56,16,16,16,12,0),
    (0,0,68,68,68,68,56,0),
    (0,0,68,68,40,40,16,0),
    (0,0,68,84,84,84,40,0),
    (0,0,68,40,16,40,68,0),
    (0,0,68,68,68,60,4,56),
    (0,0,124,8,16,32,124,0),
    (0,14,8,48,8,8,14,0),
    (0,8,8,8,8,8,8,0),
    (0,112,16,12,16,16,112,0),
    (0,20,40,0,0,0,0,0),
    (60,66,153,161,161,153,66,60),
    # block character
    (0,0,0,0,0,0,0,0),
    (15,15,15,15,0,0,0,0),
    (240,240,240,240,0,0,0,0),
    (255,255,255,255,0,0,0,0),
    (0,0,0,0,15,15,15,15),
    (15,15,15,15,15,15,15,15),
    (240,240,240,240,15,15,15,15),
    (255,255,255,255,15,15,15,15),
    (0,0,0,0,240,240,240,240),
    (15,15,15,15,240,240,240,240),
    (240,240,240,240,240,240,240,240),
    (255,255,255,255,240,240,240,240),
    (0,0,0,0,255,255,255,255),
    (15,15,15,15,255,255,255,255),
    (240,240,240,240,255,255,255,255),
    (255,255,255,255,255,255,255,255)
    ]
    
    charset = [defcharset[i-32] if i>32 and i-32<len(defcharset) else (0,0,0,0,0,0,0,0) for i in range(256)]

    palette = [
        (0,0,0),
        (0,0,215),
        (215,0,0),
        (215,0,215),
        (0,215,0),
        (0,215,215),
        (215,215,0),
        (215,215,215),
        (0,0,0),
        (0,0,255),
        (255,0,0),
        (255,0,255),
        (0,255,0),
        (0,255,255),
        (255,255,0),
        (255,255,255)
    ]

    running = True

    ipalette = np.array([256*256*i[0]+256*i[1]+i[2] for i in palette], dtype=np.int32)

    memory = np.zeros((32*1024,),dtype=np.uint8)
    screen.fill(palette[2])
    specsurf.fill(palette[2])
    specarray = np.zeros((256,192), dtype=np.int32)
    #specarray = pygame.surfarray.array2d(specsurf)

    autoupdate = True
    flashframe = False
    flashc = 0
    flashrate = 25
    clock = pygame.time.Clock()

    cursorx = 0
    cursory = 0
    showcursor = False

    ink = 0
    paper = 7
    flash = 0
    bright = 0
    inverse = 0
    over = 0

    border = 7

    keysdown = []
    inkeys = ""
    keyd = {}

    set_attr()
    printstate = ""

    for i in range(32):
        for j in range(24):
            #memory[0x5800+i+32*j] = (i+32*j)%256
            memory[0x5800+i+32*j] = attr
            

def set_attr():
    global attr
    attr = ink + 8*(paper) + 64*bright + 128*flash

def render():
    t = time.time()
    cyrender(memory, specarray, ipalette, flashframe, showcursor, cursorx, cursory)
    screen.fill(palette[border])
    pygame.surfarray.blit_array(specsurf, specarray)
    if sizex == 1:
        screen.blit(specsurf, ((width-256)/2,(height-192)/2))
    else:
        pygame.transform.scale(specsurf, (256*sizex,192*sizex), scaledsurf)
        screen.blit(scaledsurf, ((width-256*sizex)/2,(height-192*sizex)/2))
    #print(time.time()-t)

# Old non-Cython render code
def slowrender():
    t = time.time()
    for cx in range(32):
        for cy in range(24):
            attr = memory[0x5800+cx+32*cy]
            
            _ink = attr % 8
            
            _paper = int(attr/8)%8
            bright = int(attr/64)%2
            flash = int(attr/128)
            if showcursor and cx == cursorx and cy == cursory:
                _ink = ink
                _paper = paper
                flash = True
            
            _ink += bright*8
            _paper += bright*8
            
            if flash and flashframe: _ink,_paper = _paper,_ink
            
            _ink = ipalette[_ink]
            _paper = ipalette[_paper]
            
            lowy = cy % 8
            highy = int(cy/8)
            mp = 0x4000+cx+32*lowy+256*8*highy
            for midy in range(8):
                ypos = midy+8*cy
                m = int(memory[mp+256*midy])
                #print(type(m))
                xpos = 8*cx
                for b,mask in enumerate((128,64,32,16,8,4,2,1)):
                    v = m & mask
                    if v:
                        specarray[xpos+b,ypos] = _ink
                    else: 
                        specarray[xpos+b,ypos] = _paper
    screen.fill(palette[border])
    pygame.surfarray.blit_array(specsurf, specarray)
    if sizex == 1:
        screen.blit(specsurf, ((width-256)/2,(height-192)/2))
    else:
        pygame.transform.scale(specsurf, (256*sizex,192*sizex), scaledsurf)
        screen.blit(scaledsurf, ((width-256*sizex)/2,(height-192*sizex)/2))
        

def putchar(ascii,x,y):
    lowy = y % 8
    highy = int(y/8)
    addr = 0x4000+x+32*lowy+256*8*highy
    if over:
        for a in range(8):
            memory[a*256+addr] ^= charset[ascii][a]
    elif inverse:
        for a in range(8):
            memory[a*256+addr] = 255 - charset[ascii][a]        
    else:
        for a in range(8):
            memory[a*256+addr] = charset[ascii][a]

stated = {
    16: "INK",
    17: "PAPER",
    18: "FLASH",
    19: "BRIGHT",
    20: "INVERSE",
    21: "OVER",
    22: "AT1",
    23: "TAB",
}

def printchar(ch):
    global cursorx, cursory, printstate, ink, paper, attr, bright, flash, inverse, over
    if type(ch) == str: ch = ord(ch)
    if printstate:
        if printstate == "AT1":
            cursory = ch
            printstate = "AT2"
        elif printstate == "AT2":
            cursorx = ch
            printstate = ""
        elif printstate == "INK":
            ink = ch % 8
            set_attr()
            printstate = ""
        elif printstate == "PAPER":
            paper = ch % 8
            set_attr()
            printstate = ""
        elif printstate == "FLASH":
            flash = ch % 2
            set_attr()
            printstate = ""
        elif printstate == "BRIGHT":
            bright = ch % 2
            set_attr()
            printstate = ""
        elif printstate == "INVERSE":
            inverse = ch % 2
            set_attr()
            printstate = ""
        elif printstate == "OVER":
            over = ch % 2
            set_attr()
            printstate = ""
        elif printstate == "TAB":
            newx = ch % 32
            if newx < cursorx: cursory += 1
            cursorx = newx
            printstate = ""
    elif ch < 32:
        if ch == 10:
            cursorx = 0
            cursory += 1
        elif ch == 12:
            cursorx -= 1
            if cursorx < 0:
                cursorx = 31
                cursory -= 1
                if cursory < 0:
                    cursory = 23
            putchar(ord(" "), cursorx, cursory)
        elif ch in stated:
            printstate = stated[ch]
    else:    
        putchar(ch, cursorx, cursory)
        memory[0x5800+cursorx+32*cursory] = attr
        cursorx += 1
    while cursorx >= 32:
        cursorx -= 32
        cursory += 1
    while cursory >= 24:
        cursory -= 24
        
def BORDER(n):
    """
    Sets the border colour.
    
    Args:
        
    - n - integer - the border colour (0-7)
    """
    global border
    border = int(n) % 8
    if autoupdate: UPDATE()
       
def INK(n):
    """
    Returns control codes to set the ink colour (0-7).
    
    Use this in a PRINT or SET command. Example: 
    ``PRINT("normal",INK(1),"blue",INK(2),"red")``
    
    Args: 
    
    - n - integer - the ink colour (0-7)
    """
    return "".join((chr(16),chr(int(n))))

def PAPER(n):
    """
    Returns control codes to set the paper colour (0-7).
    
    Use this in a PRINT or SET command. Example: 
    ``PRINT("normal",PAPER(1),"blue",PAPER(2),"red")``
    
    Args: 
    
    - n - integer - the paper colour (0-7)
    """
    return "".join((chr(17),chr(int(n))))

def FLASH(n):
    """
    Returns control codes to set or unset flashing text.
    
    Use this in a PRINT or SET command. Example: 
    ``PRINT("normal",FLASH(1),"flashing",FLASH(0),"normal")``
    
    Args: 
    
    - n - integer - flashing or not (0-1)
    """
    return "".join((chr(18),chr(int(n))))

def BRIGHT(n):
    """
    Returns control codes to set or unset bright text.
    
    Use this in a PRINT or SET command. Example: 
    ``PRINT("normal",BRIGHT(1),"bright",BRIGHT(0),"normal")``
    
    Args:

    - n - integer - bright or not (0-1)
    """
    return "".join((chr(19),chr(int(n))))

def INVERSE(n):
    """
    Returns control codes to set or unset inverse video text.
    
    Use this in a PRINT or SET command. Example: 
    ``PRINT("normal",INVERSE(1),"inverse",INVERSE(0),"normal")``
    
    Args:

    - n - integer - inverse or not (0-1)
    """
    return "".join((chr(20),chr(int(n))))

def OVER(n):
    """
    Returns control codes to set or unset XOR mode text. This has interesting results when
    text or graphics is overwritten. Notably, writing text OVER the same text will erase the text.
    See the ZX Spectrum manual for more details.
    
    Use this in a PRINT or SET command. Example: 
    ``PRINT(AT(0,0),"over and",AT(0,0),OVER(1),"over again we go")``
    
    Args:

    - n - integer - XOR mode or not (0-1)
    """

    return "".join((chr(21),chr(int(n))))
    
def AT(y,x):
    """
    Returns control codes to set the coordinates of the text cursor.
    
    Use this in a PRINT or SET command. Example: 
    ``PRINT("normal",AT(5,15),"row 5 column 15",AT(14,4),"row 14 column 4")``
    
    Args:
    
    -    y - integer - the y coordinate to move to (0-23)
    -    x - integer - the x coordinate to move to (0-31)
    """

    return "".join((chr(22),chr(int(y)),chr(int(x))))

def TAB(n):
    """
    Returns control codes to set the x-coordinate of the text cursor.
    If this moves the cursor forwards, the cursor stays on the line that it is on.
    Otherwise, the cursor moves one line downwards.
    
    Use this in a PRINT or SET command. Example: 
    ``PRINT(TAB(0),"tab 0",TAB(16),"halfway along",TAB(8),"quarter way on the next line")``
    
    Args:

    - n - integer - the x coordinate to move to (0-31)
    """

    return "".join((chr(23),chr(int(n))))
    
def printitem(ss):
    if type(ss) is not str: ss = str(ss)
    for c in ss:
        printchar(c)
    
def PRINT(*s, sep="", end="", set=False):
    """
    Outputs characters to the screen. By default this does not include a newline (use \\\\n),
    or spaces between the outputs.
    
    Args:
    
    -    s - things to print.
    -    sep - same as Python's sep option for print.
    -    end - same as Python's end option for print.
    -    set - boolean - whether any changes made with INK, PAPER, BRIGHT, FLASH, INVERSE or OVER are permanent or not.
    """
    global ink,paper,flash,bright,inverse,over
    if not set: store = (ink,paper,flash,bright,inverse,over)
    first = True
    for ss in s:
        if first:
            first = False
        elif sep:
            printitem(sep)
        printitem(ss)
    if end: printitem(end)
    if not set: 
        ink,paper,flash,bright,inverse,over = store
        set_attr()
    if autoupdate: UPDATE()

def SET(*s, **args):
    """
    Use this to set ink, paper, inverse etc. for text. This works like PRINT, but all changes to ink
    etc. are permanent.
    
    Args:
    
    -    s - things to print.
    -    sep - same as Python's sep option for print.
    -    end - same as Python's end option for print.
    
    """
    PRINT(*s, set=True)

def CLS():
    """
    Clears the screen, and moves the text cursor to the top left.
    """
    global cursorx, cursory
    set_attr()
    memory[0x4000:0x5800] = 0
    memory[0x5800:0x5b00] = attr
    cursorx, cursory = 0,0
    set_attr()
    if autoupdate: UPDATE()

def update():
    global flashframe, flashc
    flashc += 1
    if flashc >= flashrate:
        flashc = 0
        flashframe = not flashframe
    render()
    pygame.display.flip()
    clock.tick(60)

def INKEYS():
    """
    If one or more keys that produce a character are held down, returns the ASCII character of
    the most recently held down key. Otherwise, returns "". Equivalent to INKEY$ in ZX Spectrum Basic.
    """
    return inkeys

def INPUT(*s, **args):
    """Interactive input - prints a prompt, returns a string. Not so much like the ZX Spectrum INPUT
    - more like the INPUT on the Amstrad CPC.
    
    Args:
    
    - s - things to print for the prompt
    - args - arguments to pass onto PRINT
    """
    global showcursor
    PRINT(*s, **args)
    #print(s)
    scx, scy = cursorx, cursory
    res = ""
    finished = False
    pygame.key.set_repeat(500,10)
    osc = showcursor
    showcursor = True
    while not finished:
        update()
        for event in pygame.event.get():
            if event.type == QUIT:
                BYE()
            elif event.type == KEYDOWN:
                u = event.unicode
                if u == "\r" or u == "\n": # return
                    finished = True
                    printchar("\n")
                    continue
                if u == "\x08" and len(res) > 0: # delete
                    res = res[:-1]
                    printchar(12)
                    continue
                #print(event)
                if event.scancode == 69:
                    BYE()
                if u == "£": u="`" # character set malarkey
                if u and (ord(u) < 32 or ord(u) > 127): u=""
                if u:
                    res = res + u
                    printchar(u)
    pygame.key.set_repeat(0)
    showcursor = osc
    return res

def MOVE(x,y):
    """
    Moves the graphics cursor to x,y.
    
    Args:
    
    - x - the x coordinate to move to
    - y - the y coordinate to move to
    """
    graphicsx, graphicsy = int(x),int(y)

def plot(x,y,INK=None,PAPER=None,FLASH=None,BRIGHT=None,
    OVER=None,INVERSE=None):
    global graphicsx, graphicsy
    x,y = int(x),int(y)
    graphicsx, graphicsy = x,y
    if x < 0: return
    if x >= 256: return
    if y < 0: return
    if y >= 192: return
    midy = y % 8
    cy = int(y/8)
    lowy = cy % 8
    highy = int(cy/8)
    cx = int(x/8)
    xp = x % 8
    xm = 1 << (7-xp)
    mp = 0x4000+cx+32*lowy+256*midy+256*8*highy
    if OVER:
        memory[mp] ^= xm
    elif INVERSE:
        memory[mp] &= (1-xm)
    else:
        memory[mp] |= xm
    if INK is not None or PAPER is not None or FLASH is not None or BRIGHT is not None:
        mask = 0
        val = 0
        if INK is not None:
            mask |= 7
            val |= int(INK) % 8
        if PAPER is not None:
            mask |= 56 # 8+16+32
            val |= (int(PAPER) % 8)*8 
        if BRIGHT is not None:
            mask |= 64
            val |= (int(BRIGHT) % 2)*64
        if FLASH is not None:
            mask |= 128
            val |= (int(FLASH) % 2)*128
        memory[0x5800+cx+32*cy] &= (255-mask)
        memory[0x5800+cx+32*cy] |= val

def POINT(x,y):
    """
    Tests the pixel at x,y, returns 1 if it is the ink colour and 0 if it is the paper colour.

    Args:
    
    - x - the x coordinate to test
    - y - the y coordinate to test
    """
    x,y = int(x),int(y)
    if x < 0: return
    if x >= 256: return
    if y < 0: return
    if y >= 192: return
    midy = y % 8
    cy = int(y/8)
    lowy = cy % 8
    highy = int(cy/8)
    cx = int(x/8)
    xp = x % 8
    xm = 1 << (7-xp)
    mp = 0x4000+cx+32*lowy+256*midy+256*8*highy
    val = 1 if memory[mp] & xm else 0
        
def PLOT(x,y,**args):
    """Moves the graphics cursor to the point (x,y) and plots a pixel. NOTE: graphics coordinates
    are relative to the top left, so (10,30) is 10 pixels to the right of and 30 below the top left.
    
    Args:
    
    - x - the x coordinate to move to
    - y - the y coordinate to move to
    - INK (0-7)
    - PAPER (0-7)
    - BRIGHT (0-1)
    - FLASH (0-1)
    - OVER (0-1) - draw in XOR or not
    - INVERSE (0-1) - erase or not
    """
    plot(x,y,**args)
    if autoupdate: UPDATE()

def DRAWTO(x, y, **args):
    """
    Draws a line from the last graphics point drawn (by PLOT or DRAW), to the
    point specified by x and y. Note that the coordinates are absolute.
    
    Args:
    
    - x - the x coordinate to draw to
    - y - the y coordinate to draw to
    - INK (0-7)
    - PAPER (0-7)
    - BRIGHT (0-1)
    - FLASH (0-1)
    - OVER (0-1) - draw in XOR or not
    - INVERSE (0-1) - erase or not
    """
    dx = x - graphicsx
    dy = y - graphicsy
    return DRAW(dx,dy,**arg)

def DRAW(dx,dy,a=None,**args):
    """
    Draws a line from the last graphics point drawn (by PLOT or DRAW). Note that the
    coordinates are relative from that point, not absolute - ie. they specify the number
    of pixels to go right or down.
    
    When called with the ``a`` argument, draws an arc from the graphics cursor position, ending dx pixels to the
    right of and dy pixels below that position. Turns through a radians - to the left if a is positive, to the
    right if a is negative.
    
    Args:
    
    - dx - the number of pixels to move right (can be negative)
    - dy - the number of pixels to move down (can be negative)
    - a - optional - draws an arc the angle to turn through, in radians (can be negative)
    - INK (0-7)
    - PAPER (0-7)
    - BRIGHT (0-1)
    - FLASH (0-1)
    - OVER (0-1) - draw in XOR or not
    - INVERSE (0-1) - erase or not
    """

    if a is not None: return arc(dx, dy, a)

    x = graphicsx + 0.5
    y = graphicsy + 0.5
    steps = max(abs(dx),abs(dy))
    if steps < 1: return
    mdx = dx/steps
    mdy = dy/steps
    for i in range(int(steps)):
        x += mdx
        y += mdy
        plot(x, y, **args)
    if autoupdate: UPDATE()

def arc(dx, dy, a, **args):
    global graphicsx, graphicsy
    A = 1/np.tan(a/2)
    sgx, sgy = graphicsx+dx, graphicsy+dy
    
    x = graphicsx + 0.5
    y = graphicsy + 0.5    
    cx = x+(A*dy/2)+dx/2
    cy = y-(A*dx/2)+dy/2
        
    r = np.sqrt((x-cx)**2+(y-cy)**2)
    graphicsx += dx
    graphicsy += dy
    
    t0=math.atan2(x-cx,y-cy)
    print(cx, cy)
    print(t0, np.cos(t0), np.sin(t0))
    
    if a > 0:
        p = np.arange(0,a,1/r)+t0
    else:
        p = -np.arange(0,-a,1/r)+t0

    xv = (r * np.sin(p)) + cx
    yv = (r * np.cos(p)) + cy
    for x, y in zip(xv, yv):
        plot(x, y, **args)

    graphicsx, graphicsy = sgx, sgy
        
    if autoupdate: UPDATE()

def CIRCLE(x, y, r, **args):
    """Draws a circle.
    
    - x - the x coordinate of the circle center
    - y - the y coordinate of the circle center
    - r - the radius of the circle, in pixels
    - INK (0-7)
    - PAPER (0-7)
    - BRIGHT (0-1)
    - FLASH (0-1)
    - OVER (0-1) - draw in XOR or not
    - INVERSE (0-1) - erase or not
    """
    global graphicsx, graphicsy
    sgx, sgy = graphicsx, graphicsy

    # These make the circles come out nicer
    cx=x
    cy=y

    p = np.arange(0,np.pi*2,1/r)

    xv = (r * np.sin(p)) + cx
    yv = (r * np.cos(p)) + cy
    for x, y in zip(xv, yv):
        plot(x, y, **args)

    graphicsx, graphicsy = sgx, sgy

    if autoupdate: UPDATE()
        
        

    
def ATTR(x,y):
    """Gets the attribute at a given text position. The attribute is an 8-bit value. The lowest three bits
    specify the ink colour, the next three bits specify the paper, the next bit specifies brightness,
    and the highest bit specified flash.
    
    Args:
    
    - x - integer (0-31) - the column of the attribute to get
    - y - integer (0-23) - the row of the attribute to get
    """
    x = int(x)
    y = int(y)
    if x<0 or x>31 or y<0 or y>23: return -1
    return memory[0x5800+x+(y*32)]
    
def SETATTR(x, y, ATTR=None, INK=None, PAPER=None, BRIGHT=None, FLASH=None):
    """Sets the attribute at a given text position. The attribute is an 8-bit value. The lowest three bits
    specify the ink colour, the next three bits specify the paper, the next bit specifies brightness,
    and the highest bit specified flash.
    
    Calling this with only x and y will have no effect. Calling this with x, y and ATTR will change the
    whole attribute. Calling this with x, y, and at least one of INK, PAPER, BRIGHT and FLASH will
    
    Args:
    
    - x - integer (0-31) - the column of the attribute to set
    - y - integer (0-23) - the row of the attribute to set
    - ATTR - integer (0-255) - optional - the new attribute
    - INK - integer (0-7) - optional - the new ink value
    - PAPER - integer (0-7) - optional - the new paper value
    - BRIGHT - integer (0-1) - optional - the new brightness value
    - FLASH - integer (0-1) - optional - the new flash value
    """
    x = int(x)
    y = int(y)
    if x<0 or x>31 or y<0 or y>23: return -1
    mask = 255
    attr = 0
    # todo check input
    if ATTR is not None:
        attr = attr
        mask = 0
    if INK is not None:
        attr += INK
        mask &= 0b11111000
    if PAPER is not None:
        attr += 8 * PAPER
        mask &= 0b11000111
    if BRIGHT is not None:
        attr += 64 * BRIGHT
        mask &= 0b10111111
    if FLASH is not None:
        attr += 128 * FLASH
    addr = 0x5800+x+(y*32)
    memory[addr] = (mask & memory[addr]) | attr
    
def SCREENSTR(x,y):
    """
    Examines a text position to see what character might be there. Roughly equivalent to SCREEN$ on the ZX Spectrum.
    Returns a string containing the possible characters, may be empty.
    
    This uses the current contents of the character set, from position 32 to 255, and compares them against the
    pixels on screen. Redefining the character set will affect the results of this function. This function will
    not be able to detect characters written with INVERSE, or characters with graphics drawn over the top, or with
    other characters drawn over the top with OVER.
    
    Args:
    
    - x - integer (0-31) - the column of the character to examine
    - y - integer (0-23) - the row of the character to examine.
    """
    lowy = y % 8
    highy = int(y/8)
    addr = 0x4000+x+32*lowy+256*8*highy
    vals = tuple([memory[a*256+addr] for a in range(8)])
    return [chr(i) for i in range(32,256) if charset[i] == vals]

def UPDATE():
    """
    Updates the display, INKEYS, and checks for the PAUSE BREAK key and closing the pygame window. 

    There are various reasons for calling this:
    
    - If MANUALUPDATE has been called, call this every time you want to show the current graphics state to the user.
    - In a loop repeatedly calling INKEYS, call this to get INKEYS up to date.
    - In a delay loop, call this to pause briefly, while updating the display, keeping flashing things flashing, respecting BREAK and the window close button.
    - When doing a lot of computation (i.e. that takes a significant amount of time), call this occasionally so the system doesn't appear to have hung.    
    """
    global running, flashframe, inkeys
    update()
    for event in pygame.event.get():
        if event.type == QUIT:
            BYE()
        elif event.type == KEYDOWN:
            u = event.unicode
            #print(event)
            if event.scancode == 69:
                BYE()
            if u == "£": u="`" # character set malarkey
            if u and (ord(u) < 32 or ord(u) > 127): u=""
            if u:
                keysdown.append(u)
                inkeys = u
                keyd[event.key] = u
        elif event.type == KEYUP:
            if event.key in keyd: 
                keysdown.remove(keyd[event.key])
                if keysdown:
                    inkeys = keysdown[-1]
                else:
                    inkeys = ""
        
def BEEP(duration, pitch):
    """Plays a beep. This is pretty crude, and the pitches become more and more approximate the higher they go.

    Args:
        - duration - float - approximate time in seconds
        - pitch - float (-60 to 69) - the approximate number of semitones above middle C
    """
    if pitch < -60 or pitch > 69: raise Exception
    freq = 261.625565 * 2 ** (pitch/12)
    cycles = 44100 / freq
    clen = int(cycles / 2)
    snd = pygame.sndarray.make_sound(np.concatenate([np.zeros(clen,dtype=np.uint8),np.ones(clen,dtype=np.uint8)*255]))
    print(cycles)
    snd.play(-1)
    pygame.time.wait(int(duration*1000))    
    snd.stop()
        
def PAUSE(frames):
    """Pauses for a specified number of frames, while updating the screen. If specgfx is running well, it runs at 60
    frames a second.
    
    Args:
    
    - frames - integer - the number of frames to wait for.
    """
    for frame in range(frames):
        UPDATE()
    
def AUTOUPDATE():
    """Enable automatic updating, allowing the effects of all text and graphics operations
    to be seen immediately. Note that this is the default, and so it is only useful
    to call this if you have previously called MANUALUPDATE."""
    global autoupdate
    autoupdate = True
    
def MANUALUPDATE():
    """Disable automatic updating - all text and graphics operations will only take effect when
    UPDATE is called. This is useful for speed or smooth animation. To re-enable automatic updating
    call AUTOUPDATE."""
    global autoupdate
    autoupdate = False

def BYE():
    """Shut down the display and exit python."""
    pygame.quit()
    sys.exit(0)

def UDG(charno, values):
    """
    Redefine a character in the character set, in a manner similar to User Defined Graphics (UDG)
    on the ZX Spectrum.
    
    This can be used to redefine already-existing characters, if (for example) you want to use a
    different font, or sacrifice some or all of the letters, numbers punctuation etc. for more
    graphics characters. Note also that any characters already drawn to the screen will not
    be altered by this - if you print an "a", then redefine "a", then print another "a", then
    the first "a" will be in the old style and the second will be in the new style.
    
    Example::
    
        UDG(0x90, (0b00000001,
                   0b00000011,
                   0b00000111,
                   0b00001111,
                   0b00011111,
                   0b00111111,
                   0b01111111,
                   0b11111111))
        PRINT("\x90")
    
    defines a triangle character and assigns it to character number 0x90 (144 in decimal) and prints it.
    
    Args:
    
    - charno - integer (32-255) - the character to define
    - values - tuple of 8 integers, 0-255, representing the character.
    """
    if len(values) != 8 or [i for i in values if type(i) != int or i < 0 or i > 255]: raise Exception
    charset[charno] = tuple(values)
    
def GETCHARDEF(charno):
    """
    Fetches the definition of a character, as a tuple of 8 integers. See UDG for more details.
    
    Args:
    
    - charno - integer (32-255) - the character to get the definition of.
    """
    return charset[charno]
    
def RESETCHARS():
    """
    Resets the character set to its original state. Undoes the effects of UDG.
    """
    for i in range(256):
        charset[i] = defcharset[i-32] if i>32 and i-32<len(defcharset) else (0,0,0,0,0,0,0,0)

def GETMEMORY():
    """
    Advanced: Gets the screen memory, as a numpy array. This is a 32k array of unsigned 8-bit
    integers (mimicing the address space of a 16k ZX Spectrum, with the first 16k representing ROM),
    and is mostly zeros. The screen memory is laid out as in a ZX Spectrum, with
    the pixels starting at 0x4000 and the attributes starting at 0x5800, ending at 0x5aff
    
    This gets the actual array that specgfx works with - changing values in this array (between
    0x4000 and 0x5aff) will change the screen once you call UPDATE.
    """
    return memory

def PEEK(address):
    """
    Reads a byte in the screen memory, at the given address.
    
    Args:
    
    - address - integer, from 0 to 0x7fff, but only values from 0x4000 to 0x5800 are of interest.
    """
    return memory[address]
    
def POKE(address, value):
    """
    Writes a byte to the screen memory, at the given address. Writing between 0x4000 and 0x5aff will
    change the screen once you call UPDATE.
    
    Args:
    
    - address - integer, from 0 to 0x7fff, but only values from 0x4000 to 0x5800 are of interest.
    - value - integer - the byte to write.
    """
    memory[address] = value