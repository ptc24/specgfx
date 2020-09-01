import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame.locals import *
import numpy as np
import time
import sys

inkeys = ""

def INIT(FULL=False):
    global size, width, height, screen, specsurf, defchar, memory, autoupdate, flashframe
    global palette, ipalette, specarray, defcharset
    global flashc, flashrate, clock, cursorx, cursory, showcursor, printstate
    global ink, paper, flash, bright, inverse, over, border, keysdown, inkeys, keyd
    global graphicsx, graphicsy

    graphicsx = 0
    graphicsy = 0

    pygame.init()

    size = width, height = 320,240

    if FULL:
        screen = pygame.display.set_mode(size, FULLSCREEN)
    else:
        screen = pygame.display.set_mode(size)

    specsurf = pygame.Surface((256, 192))

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

    ipalette = [256*256*i[0]+256*i[1]+i[2] for i in palette]

    memory = np.zeros((32*1024,),dtype=np.uint8)
    screen.fill(palette[2])
    specsurf.fill(palette[2])
    specarray = pygame.surfarray.array2d(specsurf)

    autoupdate = True
    flashframe = False
    flashc = 0
    flashrate = 5
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
    screen.blit(specsurf, ((320-256)/2,(240-192)/2))
           

def putchar(ascii,x,y):
    lowy = y % 8
    highy = int(y/8)
    addr = 0x4000+x+32*lowy+256*8*highy
    if over:
        for a in range(8):
            memory[a*256+addr] ^= defcharset[ascii-32][a]
    elif inverse:
        for a in range(8):
            memory[a*256+addr] = 255 - defcharset[ascii-32][a]        
    else:
        for a in range(8):
            memory[a*256+addr] = defcharset[ascii-32][a]

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
    global border
    border = int(n)
    if autoupdate: UPDATE()
       
def INK(n):
    return "".join((chr(16),chr(int(n))))

def PAPER(n):
    return "".join((chr(17),chr(int(n))))

def FLASH(n):
    return "".join((chr(18),chr(int(n))))

def BRIGHT(n):
    return "".join((chr(19),chr(int(n))))

def INVERSE(n):
    return "".join((chr(20),chr(int(n))))

def OVER(n):
    return "".join((chr(21),chr(int(n))))
    
def AT(y,x):
    return "".join((chr(22),chr(int(y)),chr(int(x))))

def TAB(n):
    return "".join((chr(23),chr(int(n))))
    
def printitem(ss):
    if type(ss) is not str: ss = str(ss)
    for c in ss:
        printchar(c)
    
def PRINT(*s, sep="", end="", set=False):
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
    PRINT(*s, set=True)

def CLS():
    global cursorx, cursory, inverse
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
    return inkeys

def INPUT(*s, **args):
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
                print(event)
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
        
def PLOT(x,y,**args):
    plot(x,y,**args)
    if autoupdate: UPDATE()

def DRAW(dx,dy,**args):
    x = graphicsx + 0.5
    y = graphicsy + 0.5
    steps = max(abs(dx),abs(dy))
    if steps < 1: return
    mdx = dx/steps
    mdy = dy/steps
    for i in range(steps):
        x += mdx
        y += mdy
        plot(x, y, **args)

def UPDATE():
    global running, flashframe, inkeys
    update()
    for event in pygame.event.get():
        if event.type == QUIT:
            BYE()
        elif event.type == KEYDOWN:
            u = event.unicode
            print(event)
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
    
def AUTOUPDATE():
    global autoupdate
    autoupdate = True
    
def MANUALUPDATE():
    global autoupdate
    autoupdate = False

def BYE():
    pygame.quit()
    sys.exit(0)
