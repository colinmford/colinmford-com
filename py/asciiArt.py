from PIL import Image, ImageEnhance
import numpy as np
# from flat import rgb, font, shape, strike, document, paragraph, text
# from flat.otf import otf as flatOTF
import svgwrite
from math import floor, ceil

from svgwrite.mixins import ViewBox

# TODO: Analize glyphs in font for % area coverage
ASCII_CHARS = [" ", ".", ":", "−", "÷", "+", "×", "=", "*", "&", "%", "#", "@", "░", "▒", "▒"] # Sorted in order of coverage

def resizeImg(image, width=100):
    height = width * image.height / image.width
    return image.resize((int(width), int(height/2)))

def crop_image(img, tolerance=0):
    img = np.array(img)
    mask = img > tolerance
    return img[np.ix_(mask.any(1),mask.any(0))]

def pixelToAscii(image):
    pixels = image.getdata()
    asciiPixels = []
    for pixel in pixels:
        p = floor((pixel/max(pixels))*(len(ASCII_CHARS)-1))
        asciiPixels.append((pixel, ASCII_CHARS[p]))
    
    asciiImg = []
    for i in range(0, len(asciiPixels), image.width):
        asciiImg.append(asciiPixels[i:i+image.width])
    
    # print("\n".join(["".join([c[1] for c in r]) for r in asciiImg]))
        
    return asciiImg

def interpolatedColor(gray, minV, maxV):
    pct = gray/255
    return minV + (maxV-minV) * pct

def asciiToSVG(asciiImg):
    rows = len(asciiImg)
    cols = len(asciiImg[0])
    fontSize = 15
    pitch = (fontSize/1000)*601
    lineHeight = fontSize * 1.2
    
    #rgb(9, 24, 45)
    svg = svgwrite.Drawing("py/test.svg", profile="tiny")
    svg.viewbox(minx=0, miny=0, width=ceil(cols*pitch), height=ceil(rows*lineHeight))
    for i, r in enumerate(asciiImg):
        for j, c in enumerate(r):
            if c[1] != " ":
                svg.add(svg.text(c[1], insert=(round(j*pitch, 3), round((i*lineHeight)+lineHeight), 3), fill=svgwrite.rgb(interpolatedColor(c[0], 9, 235) + 20,
                                                                                                      interpolatedColor(c[0], 24, 235) + 20, 
                                                                                                      interpolatedColor(c[0], 45, 235) + 20)))
    svg.save()
    
    # ttFont = TTFont('src/assets/styles/fonts/SpotMono-Light.woff')
    # ttFont.flavor = None
    # stream = BytesIO()
    # ttFont.save(stream)
    # stream.seek(0)
    # ttfData = stream.read()
    
    # spot = font(flatOTF(ttfData))
    # strikes = []
    # for i in range(0, 256):
    #     strikes.append(strike(spot).size(fontSize).color(rgb(i, i, i)))
    
    # doc = document(int(cols*pitch), int(rows*fontSize), "pt")
    # page = doc.addpage()
    # t = []
    # for r in asciiImg:
    #     p = []
    #     for c in r:
    #         p.append(strikes[c[0]].span(c[1]))
    #     t.append(paragraph(p))
    # page.place(text(t)).position(0,0)
    
    # page.svg('py/test.svg')
    
    

def main():
    image = Image.open("py/IMG_0499.jpg").convert('L')
    image = Image.fromarray(crop_image(image, tolerance=18))
    e = ImageEnhance.Brightness(image)
    image = e.enhance(1.025)
    for wd in range(80, 81):
        resizedImg = resizeImg(image, width=wd)
        asciiImg = pixelToAscii(resizedImg)
        asciiToSVG(asciiImg)
main()