import golly as g
import os, re, math
#This script is meant to be used as an alternative to the canonical synthesise-constellation-4G.py
MAXPERIOD = 60
def bijoscar(maxsteps):
    initpop = int(g.getpop())
    initrect = g.getrect()
    if (len(initrect) == 0):
        return 0
    inithash = g.hash(initrect)
    
    for i in range(maxsteps):
        g.run(1)
        if (int(g.getpop()) == initpop):
            prect = g.getrect()
            phash = g.hash(prect)
            if (phash == inithash):
                period = i + 1
                if (prect == initrect):
                    return period
                else:
                    return -period
    
    return -1
r270 = ( 0, -1,  1,  0)
r180 = (-1,  0,  0, -1)
r90 = ( 0,  1, -1,  0)
def canonise():
    p = bijoscar(MAXPERIOD)
    if p == -1:
        # In rules with photons the pattern may be periodic, but not in CGoL
        return ""
    
    representation = "#"
    for i in range(abs(p)):
        rect = g.getrect()
        representation = compare_representations(representation, canonise_orientation(rect[2], rect[3], rect[0], rect[1], 1, 0, 0, 1))
        representation = compare_representations(representation, canonise_orientation(rect[2], rect[3], rect[0]+rect[2]-1, rect[1], -1, 0, 0, 1))
        representation = compare_representations(representation, canonise_orientation(rect[2], rect[3], rect[0], rect[1]+rect[3]-1, 1, 0, 0, -1))
        representation = compare_representations(representation, canonise_orientation(rect[2], rect[3], rect[0]+rect[2]-1, rect[1]+rect[3]-1, -1, 0, 0, -1))
        representation = compare_representations(representation, canonise_orientation(rect[3], rect[2], rect[0], rect[1], 0, 1, 1, 0))
        representation = compare_representations(representation, canonise_orientation(rect[3], rect[2], rect[0]+rect[2]-1, rect[1], 0, -1, 1, 0))
        representation = compare_representations(representation, canonise_orientation(rect[3], rect[2], rect[0], rect[1]+rect[3]-1, 0, 1, -1, 0))
        representation = compare_representations(representation, canonise_orientation(rect[3], rect[2], rect[0]+rect[2]-1, rect[1]+rect[3]-1, 0, -1, -1, 0))
        g.run(1)
    
    if (p<0):
        prefix = "xq" + str(abs(p))
    elif (p==1):
        prefix = "xs" + str(g.getpop())
    else:
        prefix = "xp" + str(p)
    
    return prefix + "_" + representation

# A subroutine used by canonise:
def canonise_orientation(length, breadth, ox, oy, a, b, c, d):
    representation = ""
    chars = "0123456789abcdefghijklmnopqrstuvwxyz"
    runzeroes = len(chars) + 3
    
    for v in range(int((breadth-1)/5)+1):
        zeroes = 0
        if (v != 0):
            representation += "z"
        for u in range(length):
            baudot = 0
            for w in range(5):
                x = ox + a*u + b*(5*v + w)
                y = oy + c*u + d*(5*v + w)
                baudot = (baudot >> 1) + 16*g.getcell(x, y)
            if (baudot == 0):
                zeroes += 1
            else:
                if (zeroes > 0):
                    if (zeroes == 1):
                        representation += "0"
                    elif (zeroes == 2):
                        representation += "w"
                    elif (zeroes == 3):
                        representation += "x"
                    else:
                        while(zeroes > runzeroes):
                            representation += "yz"
                            zeroes -= runzeroes
                        representation += "y"
                        representation += chars[zeroes - 4]
                zeroes = 0
                representation += chars[baudot]
    
    return representation

# Compares strings first by length, then by lexicographical ordering.
# A hash character is worse than anything else.
def compare_representations(a, b):
    if (a == "#"):
        return b
    elif (b == "#"):
        return a
    elif (len(a) < len(b)):
        return a
    elif (len(b) < len(a)):
        return b
    elif (a < b):
        return a
    else:
        return b
def reconstruct(gstr, stepback=2):
    """Reconstruct a pattern representing a glider set from its (canonical)
    string. The transformation is assumed to be the identity. Returns a single
    Golly cell list with all gliders at <stepback> gen prior to canonical time.
    """
    fields, at, trans_str = gstr.partition("@")
    res = []
    glider = g.parse("bo$2bo$3o") # SE
    # Process transformation
    # XXX unimplemented (but not required here)
    t, o, shift_x, shift_y = 0, "identity", 0, 0
    # Step back to separate gliders (same as Shinjuku uses for realising syntheses)
    t += stepback
    # Process glider sets
    for i, field in enumerate(gstr.split("/")):
        salvo = []
        for (time, lane) in zip(*[iter(field.split())] * 2):
            time, lane = - int(time) - t - 4, int(lane)
            dist, time = time // 4, time % 4
            salvo += g.evolve(g.transform(glider, dist, dist - lane), time)
        if   i == 1: salvo = g.transform(salvo, 0, 0, r270[0], r270[1], r270[2], r270[3]) # "rot270"
        elif i == 2: salvo = g.transform(salvo, 0, 0, r180[0], r180[1], r180[2], r180[3]) # "rot180"
        elif i == 3: salvo = g.transform(salvo, 0, 0, r90[0], r90[1], r90[2], r90[3]) # "rot90"
        res += salvo
    return g.transform(res, shift_x, shift_y)
rles = open("4g_database.txt").read().split("\n")
g.show("Read file")
apgcode = canonise()
if not apgcode:
    g.warn("Failed to detect periodic behavior!")
patterns = []
for rle in rles:
    if apgcode == rle.split(" ")[0]:
        #g.warn(rle)
        gliderset = rle.split(" ")[1:]
        if len(gliderset) == 7:
            gliders = ""
            for item in gliderset:
                gliders = gliders + item + " "
            #g.warn(gliders)
            patterns.append(reconstruct(gliders))
ncols = len(patterns)
if ncols:
    g.new("Solutions")
    g.show("{} collisions found".format(ncols))
    g.setname(apgcode)
    if ncols <= 20:
        N = 5
    else:
        N = math.ceil(math.sqrt(ncols)) + 1
    offset = 100
    i = 0
    for col in patterns:
        #g.warn(str(patterns))
        g.putcells(col, int((i % N) * offset), int((i // N) * offset))
        i += 1
    g.fit()
else:
    g.note("No glider collisions found for constellation {}. Better luck next time".format(apgcode))
