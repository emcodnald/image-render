"""
image rendering program
takes a sequence of parametric curve and prism data and renders a bitmap image
"""
import parametric
import bitmap
import jpg
import math

# example bezier curve
"""
lines = [
    [1,[50,50],[[100,50]],[100,100],1,[255,255,0]]
    ]
"""

# example enclosure with a filled in area

"""
where the curve data is stored

1 = bezier curve
"""
lines = [
    [1,[71,100],[[112,81]],[166,92],1,[0,0,0]],
    [1,[166,92],[[166,135]],[129,172],1,[0,0,0]],
    [1,[129,172],[[119,131]],[71,100],1,[0,0,0]],
    [1,[166,92],[[224,248]],[54,253],1,[0,0,0]],
    ]

# where the prism data is stored
shapes = [
    [[0,3,2,1],[128,128,128]]
    ]

# basic image info
dimensions = [300,300]
bgCol = [255,255,255]

# definition of raw curve data
curves = []
for i in range(len(lines)):
    if lines[i][0] == 1:
        curves.append(parametric.bez(lines[i][1],lines[i][2],lines[i][3]))

# definition of raw prism data
prisms = []
for i in range(len(shapes)):
    cl = []
    for j in range(len(shapes[i][0])):
        cl.append(curves[shapes[i][0][j]])
    sub = parametric.prism(cl)
    if sub.isPrism:
        prisms.append(sub)

# definition pixel matrix that represents each pixel in the image
pixels = []
for i in range(dimensions[1]):
    pixels.append([])
    for j in range(dimensions[0]):
        pixels[i].append([bgCol[0],bgCol[1],bgCol[2]])

# draws all prisms
for i in range(len(prisms)):
    prismSpace = prisms[i].fill(pow(2,math.ceil(math.log2(max(dimensions[0],dimensions[1])))),1,True)
    for j in range(len(prismSpace)):
        for k in range(prismSpace[j].center.y,prismSpace[j].center.y+prismSpace[j].size+1):
            for m in range(prismSpace[j].center.x,prismSpace[j].center.x+prismSpace[j].size+1):
                for n in range(3):
                    pixels[dimensions[1]-k-1][m][n] = shapes[i][1][n]

# draws all curves, done second so that outlines are on top
for i in range(len(curves)):
    curvePixels = curves[i].generatePixels(lines[i][-2])
    for j in range(len(curvePixels)):
        newPixelColor = pixels[dimensions[1]-curvePixels[j].pos.y-1][curvePixels[j].pos.x]
        for k in range(3):
            newPixelColor[k] = int(newPixelColor[k]*curvePixels[j].magnitude+lines[i][-1][k]*(1-curvePixels[j].magnitude))
        pixels[dimensions[1]-curvePixels[j].pos.y-1][curvePixels[j].pos.x] = newPixelColor

# writing the final image file in selected format
resFile = "result"
form = ".jpg"
if form == ".bmp":
    bitmap.image(pixels, resFile+form)
elif form == ".jpg":
    jpg.image(pixels, resFile+form, 255)

