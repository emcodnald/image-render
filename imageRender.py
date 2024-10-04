"""
image rendering program
takes a sequence of parametric curve and prism data and renders a bitmap image
"""
import sys
sys.path.append("C:\\Users\\hates\\Desktop\\modules")
import parametric
import bitmap
import jpg
import math
import png

"""
where the auxiliary data is stored

1 = bezier curve
2 = spiral
3 = translation
4 = composite curve
5 = wrap
6 = tangent
7 = single warp
8 = double warp
9 = quad warp
10 = bSpline curve
"""

resFile = "result"
form = ".png"
"""
where the curve data is stored
"""
lines = [
    [1,[71,100],[[112,81]],[166,92],True,1,[0,0,0,1]],
    [1,[166,92],[[166,135]],[129,172],True,1,[0,0,0,1]],
    [1,[129,172],[[119,131]],[71,100],True,1,[0,0,0,1]],
    [1,[285,123],[[161,109]],[93,167],True,1,[0,0,0,1]],
    [1,[285,123],[[78,65]],[93,167],True,1,[0,0,0,1]]
    ]
# where the prism data is stored
shapes = [
    [[0,1,2],[255,0,0,0.5]],
    [[3,4],[0,255,255,0.5]],
    ]

# basic image info
dimensions = [300,300]
bgCol = [255,255,255]

# definition of raw curve data
curves = []
for i in range(len(lines)):
    if lines[i][0] == 1:
        sub = []
        for j in range(len(lines[i][2])):
            sub.append(parametric.orderedPair(lines[i][2][j][0],lines[i][2][j][1]))
        curves.append(parametric.bez(parametric.orderedPair(lines[i][1][0],lines[i][1][1]),sub,parametric.orderedPair(lines[i][3][0],lines[i][3][1])))
        curves[-1].vis = lines[i][-3]
        curves[-1].th = lines[i][-2]
        curves[-1].col = lines[i][-1]
    elif lines[i][0] == 2:
        curves.append(parametric.spiral(lines[i][1],lines[i][2],lines[i][3],lines[i][4],lines[i][5],lines[i][6]))
        curves[-1].vis = lines[i][-3]
        curves[-1].th = lines[i][-2]
        curves[-1].col = lines[i][-1]
    elif lines[i][0] == 3:
        sub = []
        for j in range(len(lines[i][1])):
            sub.append(curves[lines[i][1][j]])
        sub2 = []
        for j in range(len(lines[i][2])):
            sub2.append(parametric.transformationNode(lines[i][2][j]))
        sub3 = parametric.transformCurve(sub,sub2)
        for j in range(len(sub3)):
            curves.append(sub3[j])
            curves[-1].vis = lines[i][-3]
            curves[-1].th = lines[i][-2]
            curves[-1].col = lines[i][-1]
    elif lines[i][0] == 4:
        curves.append(parametric.para(curves[lines[i][1]].x,curves[lines[i][2]].y))
        curves[-1].vis = lines[i][-3]
        curves[-1].th = lines[i][-2]
        curves[-1].col = lines[i][-1]
    elif lines[i][0] == 5:
        if lines[i][3]:
            curves.append(parametric.wrap(curves[lines[i][1]],curves[lines[i][2]].y,parametric.quickTransform(lines[i][4][0],lines[i][4][1])))
        else:
            curves.append(parametric.wrap(curves[lines[i][1]],curves[lines[i][2]].x,parametric.quickTransform(lines[i][4][0],lines[i][4][1])))
        curves[-1].vis = lines[i][-3]
        curves[-1].th = lines[i][-2]
        curves[-1].col = lines[i][-1]
    elif lines[i][0] == 6:
        curves.append(parametric.tangent(curves[lines[i][1]],lines[i][2],curves[lines[i][3]],lines[i][4]))
        curves[-1].vis = lines[i][-3]
        curves[-1].th = lines[i][-2]
        curves[-1].col = lines[i][-1]
    elif lines[i][0] == 7:
        sub = []
        for j in range(len(lines[i][2])):
            sub.append(curves[lines[i][2][j]])
        sub2 = parametric.singleWarp(curves[lines[i][1]],sub,parametric.scopeDimensions(lines[i][3][0],lines[i][3][1]),parametric.orderedPair(lines[i][4][0],lines[i][4][1]))
        for j in range(len(sub2)):
            curves.append(sub2[j])
            curves[-1].vis = lines[i][-3]
            curves[-1].th = lines[i][-2]
            curves[-1].col = lines[i][-1]
    elif lines[i][0] == 8:
        sub = []
        for j in range(len(lines[i][3])):
            sub.append(auxCurves[lines[i][3][j]])
        sub2 = parametric.doubleWarp(curves[lines[i][1]],curves[lines[i][2]],sub,parametric.scopeDimensions(lines[i][4][0],lines[i][4][1]),parametric.orderedPair(lines[i][5][0],lines[i][5][1]))
        for j in range(len(sub2)):
            curves.append(sub2[j])
            curves[-1].vis = lines[i][-3]
            curves[-1].th = lines[i][-2]
            curves[-1].col = lines[i][-1]
    elif lines[i][0] == 9:
        sub = []
        for j in range(len(lines[i][5])):
            sub.append(curves[lines[i][5][j]])
        sub2 = parametric.quadWarp(curves[lines[i][1]],curves[lines[i][2]],curves[lines[i][3]],curves[lines[i][4]],sub,parametric.scopeDimensions(lines[i][6][0],lines[i][6][1]),parametric.orderedPair(lines[i][7][0],lines[i][7][1]))
        for j in range(len(sub2)):
            curves.append(sub2[j])
            curves[-1].vis = lines[i][-3]
            curves[-1].th = lines[i][-2]
            curves[-1].col = lines[i][-1]
    elif lines[i][0] == 10:
        sub = []
        for j in range(len(lines[i][2])):
            sub.append(parametric.orderedPair(lines[i][2][j][0],lines[i][2][j][1]))
        sub2 = parametric.bSpline(parametric.orderedPair(lines[i][1][0],lines[i][1][1]),sub,parametric.orderedPair(lines[i][3][0],lines[i][3][1]),lines[i][4][0],lines[i][4][1])
        for j in range(len(sub2)):
            curves.append(sub2[j])
            curves[-1].vis = lines[i][-3]
            curves[-1].th = lines[i][-2]
            curves[-1].col = lines[i][-1]

# definition of raw prism data
prisms = []
for i in range(len(shapes)):
    cl = []
    for j in range(len(shapes[i][0])):
        cl.append(curves[shapes[i][0][j]])
    sub = parametric.prism(cl)
    if sub.isPrism:
        prisms.append(sub)
        prisms[-1].col = shapes[i][1]

# definition pixel matrix that represents each pixel in the image
pixels = []
for i in range(dimensions[1]):
    pixels.append([])
    for j in range(dimensions[0]):
        if form == ".png":
            pixels[i].append([0,0,0,0])
        else:
            pixels[i].append([bgCol[0],bgCol[1],bgCol[2]])

# draws a single curve
def drawCurve(curve):
    curvePixels = curve.generatePixels(curve.th)
    for j in range(len(curvePixels)):
        if curvePixels[j].pos.x >= 0 and curvePixels[j].pos.x < dimensions[0] and curvePixels[j].pos.y >= 0 and curvePixels[j].pos.y < dimensions[1]:
            newPixelColor = pixels[dimensions[1]-curvePixels[j].pos.y-1][curvePixels[j].pos.x]
            if form == ".png":
                sub = []
                for k in range(3):
                    sub.append(curve.col[k])
                sub.append(1-curvePixels[j].magnitude)
                newPixelColor = png.addColors(newPixelColor, sub)
            else:
                for k in range(3):
                    newPixelColor[k] = int(newPixelColor[k]*curvePixels[j].magnitude+curve.col[k]*(1-curvePixels[j].magnitude))
            pixels[dimensions[1]-curvePixels[j].pos.y-1][curvePixels[j].pos.x] = newPixelColor

# draws a single prism
def drawPrism(prism):
    prismSpace = prism.fill(pow(2,math.ceil(math.log2(max(dimensions[0],dimensions[1])))),1,True)
    checked = []
    for j in range(len(prismSpace)):
        for k in range(prismSpace[j].center.y,prismSpace[j].center.y+prismSpace[j].size+1):
            for m in range(prismSpace[j].center.x,prismSpace[j].center.x+prismSpace[j].size+1):
                if form == ".png":
                    if not [dimensions[1]-k-1,m] in checked:
                        pixels[dimensions[1]-k-1][m] = png.addColors(pixels[dimensions[1]-k-1][m],prism.col)
                        checked.append([dimensions[1]-k-1,m])
                else:
                    for n in range(3):
                        pixels[dimensions[1]-k-1][m][n] = prism.col[n]

# specifies a draw order for each curve/prism
drawOrder = [
    [0,1],

    [0,0],
    [1,0],
    [2,0],

    [1,1],

    [3,0],
    [4,0],
    ]

for i in range(len(drawOrder)):
    if drawOrder[i][1]:
        drawPrism(prisms[drawOrder[i][0]])
    else:
        drawCurve(curves[drawOrder[i][0]])

# writing the final image file in selected format
if form == ".bmp":
    bitmap.image(pixels, resFile+form)
elif form == ".jpg":
    jpg.image(pixels, resFile+form, 255)
elif form == ".png":
    png.image(pixels, resFile+form)

