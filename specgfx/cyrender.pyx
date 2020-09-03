def cyrender(unsigned char [:] memory, int [:,:] specarray, int [:] ipalette, int flashframe, int showcursor, int cursorx, int cursory):
    cdef int cx, cy, attr, _ink, _paper, bright, flash, lowy, midy, highy, mp, m, xpos, ypos, b, mask, v
    for cx in range(32):
        for cy in range(24):
            attr = memory[0x5800+cx+32*cy]
            
            _ink = attr % 8
            
            _paper = int(attr/8)%8
            bright = int(attr/64)%2
            flash = int(attr/128)
            if showcursor and cx == cursorx and cy == cursory:
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
