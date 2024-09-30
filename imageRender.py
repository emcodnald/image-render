"""
image rendering program
takes a sequence of parametric curve and prism data and renders a bitmap image
"""
import parametric
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
    ]

# where the prism data is stored
shapes = [
    [[0,1,2],[128,128,128]]
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
    prisms.append(parametric.prism(cl))

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
                    pixels[k][m][n] = shapes[i][1][n]

# draws all curves, done second so that outlines are on top
for i in range(len(curves)):
    curvePixels = curves[i].generatePixels(lines[i][-2])
    for j in range(len(curvePixels)):
        newPixelColor = pixels[curvePixels[j].pos.y][curvePixels[j].pos.x]
        for k in range(3):
            newPixelColor[k] = int(newPixelColor[k]*curvePixels[j].magnitude+lines[i][-1][k]*(1-curvePixels[j].magnitude))
        pixels[curvePixels[j].pos.y][curvePixels[j].pos.x] = newPixelColor

# writing the final image file in .bmp format
startBytes = [66, 77, 110, 87, 7, 0, 0, 0, 0, 0, 54, 0, 0, 0, 40, 0, 0, 0, dimensions[0]%256, int(dimensions[0]/256)%256, int(dimensions[0]/65536)%256, int(dimensions[0]/16777216)%256, dimensions[1]%256, int(dimensions[1]/256)%256, int(dimensions[1]/65536)%256, int(dimensions[1]/16777216)%256, 1, 0, 24, 0, 0, 0, 0, 0, 56, 87, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
with open("result.bmp", 'wb') as f:
    for i in range(len(startBytes)):
        f.write(startBytes[i].to_bytes(1,byteorder='big'))
    for i in range(len(pixels)):
        for j in range(len(pixels[i])):
            for k in range(len(pixels[i][j])):
                f.write(pixels[i][j][2-k].to_bytes(1,byteorder='big'))
