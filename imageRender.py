"""
image rendering program
takes a sequence of parametric curve and prism data and renders a bitmap image
"""
import parametric
import bitmap
import jpg
import math

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
"""
aux = [
    [1,[25,78],[[54,92]],[97,74]],
    [1,[23,18],[[47,7]],[91,16]],
    [1,[97,74],[[78,57]],[91,16]],
    [1,[25,78],[[39,50]],[23,18]]
    ]
for i in range(11):
    aux.append([1,[i*10,0],[],[i*10,100]])
    aux.append([1,[0,i*10],[],[100,i*10]])

auxCurves = []
for i in range(len(aux)):
    if aux[i][0] == 1:
        auxCurves.append(parametric.bez(aux[i][1],aux[i][2],aux[i][3]))
    elif aux[i][0] == 2:
        auxCurves.append(parametric.spiral(aux[i][1],aux[i][2],aux[i][3],aux[i][4],aux[i][5],aux[i][6]))
    elif aux[i][0] == 3:
        sub = []
        for j in range(len(aux[i][1])):
            sub.append(auxCurves[aux[i][1][j]])
        sub2 = []
        for j in range(len(aux[i][2])):
            sub2.append(parametric.transformationNode(aux[i][2][j]))
        sub3 = parametric.transformCurve(sub,sub2)
        for j in range(len(sub3)):
            auxCurves.append(sub3[j])
    elif aux[i][0] == 4:
        auxCurves.append(parametric.para(auxCurves[aux[i][1]].x,auxCurves[aux[i][2]].y))
    elif aux[i][0] == 5:
        if aux[i][3]:
            auxCurves.append(parametric.wrap(auxCurves[aux[i][1]],auxCurves[aux[i][2]].y,parametric.quickTransform(aux[i][4][0],aux[i][4][1])))
        else:
            auxCurves.append(parametric.wrap(auxCurves[aux[i][1]],auxCurves[aux[i][2]].x,parametric.quickTransform(aux[i][4][0],aux[i][4][1])))
    elif aux[i][0] == 6:
        auxCurves.append(parametric.tangent(auxCurves[aux[i][1]],aux[i][2],auxCurves[aux[i][3]],aux[i][4]))
    elif aux[i][0] == 7:
        sub = []
        for j in range(len(aux[i][2])):
            sub.append(auxCurves[aux[i][2][j]])
        sub2 = parametric.singleWarp(auxCurves[aux[i][1]],sub,parametric.scopeDimensions(aux[i][3][0],aux[i][3][1]),parametric.orderedPair(aux[i][4][0],aux[i][4][1]))
        for j in range(len(sub2)):
            auxCurves.append(sub2[j])
    elif aux[i][0] == 8:
        sub = []
        for j in range(len(aux[i][3])):
            sub.append(auxCurves[aux[i][3][j]])
        sub2 = parametric.doubleWarp(auxCurves[aux[i][1]],auxCurves[aux[i][2]],sub,parametric.scopeDimensions(aux[i][4][0],aux[i][4][1]),parametric.orderedPair(aux[i][5][0],aux[i][5][1]))
        for j in range(len(sub2)):
            auxCurves.append(sub2[j])
    elif aux[i][0] == 9:
        sub = []
        for j in range(len(aux[i][5])):
            sub.append(auxCurves[aux[i][5][j]])
        sub2 = parametric.quadWarp(auxCurves[aux[i][1]],auxCurves[aux[i][2]],auxCurves[aux[i][3]],auxCurves[aux[i][4]],sub,parametric.scopeDimensions(aux[i][6][0],aux[i][6][1]),parametric.orderedPair(aux[i][7][0],aux[i][7][1]))
        for j in range(len(sub2)):
            auxCurves.append(sub2[j])

"""
where the curve data is stored
"""
sub = []
for i in range(4,len(aux)):
    sub.append(i)
lines = [
    [9,0,1,2,3,sub,[100,100],[0,0],1,[191,191,191]],
    [1,[25,78],[[54,92]],[97,74],1,[0,0,0]],
    [1,[23,18],[[47,7]],[91,16],1,[0,0,0]],
    [1,[97,74],[[78,57]],[91,16],1,[0,0,0]],
    [1,[25,78],[[39,50]],[23,18],1,[0,0,0]]
    ]

# where the prism data is stored
shapes = [
    #[[0,3,2,1],[128,128,128]]
    ]

# basic image info
dimensions = [300,300]
bgCol = [255,255,255]

# definition of raw curve data
curves = []
for i in range(len(lines)):
    if lines[i][0] == 1:
        curves.append(parametric.bez(lines[i][1],lines[i][2],lines[i][3]))
        curves[-1].th = lines[i][-2]
        curves[-1].col = lines[i][-1]
    elif lines[i][0] == 2:
        curves.append(parametric.spiral(lines[i][1],lines[i][2],lines[i][3],lines[i][4],lines[i][5],lines[i][6]))
        curves[-1].th = lines[i][-2]
        curves[-1].col = lines[i][-1]
    elif lines[i][0] == 3:
        sub = []
        for j in range(len(lines[i][1])):
            sub.append(auxCurves[lines[i][1][j]])
        sub2 = []
        for j in range(len(lines[i][2])):
            sub2.append(parametric.transformationNode(lines[i][2][j]))
        sub3 = parametric.transformCurve(sub,sub2)
        for j in range(len(sub3)):
            curves.append(sub3[j])
            curves[-1].th = lines[i][-2]
            curves[-1].col = lines[i][-1]
    elif lines[i][0] == 4:
        curves.append(parametric.para(auxCurves[lines[i][1]].x,auxCurves[lines[i][2]].y))
        curves[-1].th = lines[i][-2]
        curves[-1].col = lines[i][-1]
    elif lines[i][0] == 5:
        if lines[i][3]:
            curves.append(parametric.wrap(auxCurves[lines[i][1]],auxCurves[lines[i][2]].y,parametric.quickTransform(lines[i][4][0],lines[i][4][1])))
        else:
            curves.append(parametric.wrap(auxCurves[lines[i][1]],auxCurves[lines[i][2]].x,parametric.quickTransform(lines[i][4][0],lines[i][4][1])))
        curves[-1].th = lines[i][-2]
        curves[-1].col = lines[i][-1]
    elif lines[i][0] == 6:
        curves.append(parametric.tangent(auxCurves[lines[i][1]],lines[i][2],auxCurves[lines[i][3]],lines[i][4]))
        curves[-1].th = lines[i][-2]
        curves[-1].col = lines[i][-1]
    elif lines[i][0] == 7:
        sub = []
        for j in range(len(lines[i][2])):
            sub.append(auxCurves[lines[i][2][j]])
        sub2 = parametric.singleWarp(auxCurves[lines[i][1]],sub,parametric.scopeDimensions(lines[i][3][0],lines[i][3][1]),parametric.orderedPair(lines[i][4][0],lines[i][4][1]))
        for j in range(len(sub2)):
            curves.append(sub2[j])
            curves[-1].th = lines[i][-2]
            curves[-1].col = lines[i][-1]
    elif lines[i][0] == 8:
        sub = []
        for j in range(len(lines[i][3])):
            sub.append(auxCurves[lines[i][3][j]])
        sub2 = parametric.doubleWarp(auxCurves[lines[i][1]],auxCurves[lines[i][2]],sub,parametric.scopeDimensions(lines[i][4][0],lines[i][4][1]),parametric.orderedPair(lines[i][5][0],lines[i][5][1]))
        for j in range(len(sub2)):
            curves.append(sub2[j])
            curves[-1].th = lines[i][-2]
            curves[-1].col = lines[i][-1]
    elif lines[i][0] == 9:
        sub = []
        for j in range(len(lines[i][5])):
            sub.append(auxCurves[lines[i][5][j]])
        sub2 = parametric.quadWarp(auxCurves[lines[i][1]],auxCurves[lines[i][2]],auxCurves[lines[i][3]],auxCurves[lines[i][4]],sub,parametric.scopeDimensions(lines[i][6][0],lines[i][6][1]),parametric.orderedPair(lines[i][7][0],lines[i][7][1]))
        for j in range(len(sub2)):
            curves.append(sub2[j])
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
    curvePixels = curves[i].generatePixels(curves[i].th)
    for j in range(len(curvePixels)):
        if curvePixels[j].pos.x >= 0 and curvePixels[j].pos.x < dimensions[0] and curvePixels[j].pos.y >= 0 and curvePixels[j].pos.y < dimensions[1]:
            newPixelColor = pixels[dimensions[1]-curvePixels[j].pos.y-1][curvePixels[j].pos.x]
            for k in range(3):
                newPixelColor[k] = int(newPixelColor[k]*curvePixels[j].magnitude+curves[i].col[k]*(1-curvePixels[j].magnitude))
            pixels[dimensions[1]-curvePixels[j].pos.y-1][curvePixels[j].pos.x] = newPixelColor

# writing the final image file in selected format
resFile = "result"
form = ".bmp"
if form == ".bmp":
    bitmap.image(pixels, resFile+form)
elif form == ".jpg":
    jpg.image(pixels, resFile+form, 255)

