import numpy as np


def bbToVtx(boundingBox, vertices):
    xMin,yMin,xMax,yMax = boundingBox
    width = xMax-xMin 
    height = yMax-yMin
    xCenter = (xMax+xMin)//2
    yCenter = (yMax+yMin)//2

    if width < 8 or height < 8:
        x,y,z = vertices[xCenter,yCenter]
        return np.array([x,y,z])

    focusWidth = width//8
    focusHeight = height//8  
     


    xFocusMin = xCenter - focusWidth
    xFocusMax = xCenter + focusWidth
    yFocusMin = yCenter - focusHeight
    yFocusMax = yCenter + focusHeight
    
    sum = np.array([0,0,0]).astype("float")
    for line in vertices[xFocusMin:xFocusMax,yFocusMin:yFocusMax]:
        for v in line:    
            x,y,z = v
            sum += np.array([x,y,z])

    return sum/(4*focusWidth*focusHeight)


if __name__ == "__main__":
    shape = (10,10)
    size = shape[0]*shape[1]

    vtcs = np.array([(1,1,1) for i in range(size)],'i,i,i').reshape(shape)
    bb = [0,0,4,4]


    print(bbToVtx(bb,vtcs))
