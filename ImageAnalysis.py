import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def processWithColor(imgPath, scale_factor, invert):
    #remove ` (backtick not apostrophe) from before the .
    #scale = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{{C}}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"
    #scale = " .-':_,^=;+!rc*z?sLTv)J7(|FiCfI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%@"
    #scale = " .-':_,^=;+!rc*z?sLTv)J7FiCfI31tluneoZ5Yxjya2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%@"
    scale = " .':,^=;!rc*z?sLTv)J7FiCfI31tluneoZ5Yxjya2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%@"

    output = ""

    img = cv.imread(imgPath)
    height, width, depth = img.shape

    img = cv.resize(img, (int(width/scale_factor), int(height/scale_factor)), interpolation = cv.INTER_AREA)
    width = int(width/scale_factor)
    height = int(height/scale_factor)
    #cv.imshow('image',img)
    if invert == 'True':
        img = cv.bitwise_not(img)
    #img = cv.addWeighted( img, contrast, img, 0, brightness)

    sharpen_filter2 =np.array([[-1,-1,-1],
                    [-1,6,-1],
                    [-1,-1,-1]])
    
    img_edge = cv.filter2D(img,-1,sharpen_filter2)

    edgeBright = 0
    edgeContrast = 10
    img_edge = cv.addWeighted( img_edge, edgeContrast, img_edge, 0, edgeBright)
    img=cv.addWeighted(img, .8, img_edge, .2, 0)

    output+="<pre>"
    for i in range(height):
        for j in range(width):
            greyVal = (int(img[i,j][0]) + int(img[i,j][1]) + int(img[i,j][2])) /3
            color = "rgb(" + str(img[i,j][2]) + ", " + str(img[i,j][1]) + ", " + str(img[i,j][0]) + ")"
            #color =  str("0x{:02x}".format(img[i,j][1]))[2:] + str("0x{:02x}".format(img[i,j][2]))[2:] + str("0x{:02x}".format(img[i,j][0]))[2:]
            output += "<span style = 'color:" + color + "'>" + scale[int(float(greyVal)/256 * len(scale))] + "</span>"
        output += "</pre><pre>"
    output += "</pre>"   

    text_file = open("static/spanOut.txt", "w")

    text_file.write(output)

    text_file.close()

    return (150/width)

def process(imgPath, scale_factor=15, color=False, edgeDetect = 3, contrast = 1, brightness=-100, invert=False):
    if color == 'True':
        return processWithColor(imgPath, scale_factor, invert)
    #remove ` (backtick not apostrophe) from before the .
    #scale = " `.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{{C}}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"
    scale = " .':,^=;!rc*z?sLTv)J7FiCfI31tluneoZ5Yxjya2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%@"
    output = ""

    img = cv.imread(imgPath)
    #img = cv.imread('./Duck.png')
    height, width, depth = img.shape

    img = cv.resize(img, (int(width/scale_factor), int(height/scale_factor)), interpolation = cv.INTER_AREA)
    width = int(width/scale_factor)
    height = int(height/scale_factor)
    #cv.imshow('image',img)
    if invert == 'True':
        img = cv.bitwise_not(img)
    img = cv.addWeighted( img, contrast, img, 0, brightness)
    print(brightness)
    print(contrast)


    sharpen_filter2 =np.array([[-1,-1,-1],
                    [-1,9-float(int(edgeDetect)*.5),-1],
                    [-1,-1,-1]])
    
    sharpen_filter1 =np.array([[-1,-1,-1],
                    [-1,8.5,-1],
                    [-1,-1,-1]])
    
    #img = cv.filter2D(img,-1,sharpen_filter1)
    # applying kernels to the input image to get the sharpened image
    #img = cv.filter2D(img,-1,sharpen_filter1)

    edgeBright = 0
    edgeContrast = 10
    #img_edge = cv.addWeighted( img_edge, edgeContrast, img_edge, 0, edgeBright)
    if edgeDetect != 0:
        img=cv.addWeighted(cv.filter2D(img,-1,sharpen_filter2), .8, cv.filter2D(img,-1,sharpen_filter1), .2, 0)
    #cv.imshow("image", img)
    #cv.waitKey(0)
    
    """alpha = 1.3
    beta = .5
    img = alpha*img + beta"""

    #cv.imshow('image',img)

    #cv.waitKey(0)




    for i in range(height):
        for j in range(width):
            greyVal = (int(img[i,j][0]) + int(img[i,j][1]) + int(img[i,j][2])) /3
            output += scale[int(float(greyVal)/256 * len(scale))]
        output += "\n"

    text_file = open("static/Output.txt", "w")
    text_file.write(output)

    text_file.close()

    return (150/width)

#process("static/images/tester.jpg", scale_factor = 3)
