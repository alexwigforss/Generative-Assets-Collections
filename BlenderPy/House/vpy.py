import numpy as np

def genScrape(w,h):
    a = []

    for e in range(h):
        a.append(getFrame(w))

    return a

def getFrame(w):
    core = np.zeros((w-2,w-2))
    walls = np.pad(core, pad_width=1, mode="constant", constant_values=1)
    b = walls.astype(bool)
    return b.tolist()

width = 5
height = 5
fields = genScrape(width,height)

print(fields)