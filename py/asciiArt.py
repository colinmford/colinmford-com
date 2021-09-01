import gzip
from math import ceil, floor

import numpy as np
import svgwrite
from PIL import Image, ImageEnhance
from scour import scour

# TODO: Analize glyphs in font for % area coverage
ASCII_CHARS = [" ", ".", ":", "−", "÷", "+", "×", "=", "*", "&", "%", "#", "@", "░", "▒", "▒"]  # Sorted in order of coverage


def resizeImg(image, width=100):
    height = width * image.height / image.width
    return image.resize((int(width), int(height/2)))


def crop_image(img, tolerance=0):
    img = np.array(img)
    mask = img > tolerance
    return img[np.ix_(mask.any(1), mask.any(0))]


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
    return int(minV + (maxV-minV) * pct)


def asciiToSVG(asciiImg):
    rows = len(asciiImg)
    cols = len(asciiImg[0])
    fontSize = 15
    pitch = (fontSize/1000)*601
    lineHeight = fontSize * 1.2

    svg = svgwrite.Drawing()
    svg.viewbox(minx=0, miny=0, width=ceil(cols*pitch), height=ceil(rows*lineHeight))
    for i, r in enumerate(asciiImg):
        for j, c in enumerate(r):
            if c[1] != " ":
                svg.add(svg.text(c[1],
                        insert=(round(j*pitch, 3),
                        round((i*lineHeight)+lineHeight), 3),
                    fill='#%02x%02x%02x' % (interpolatedColor(c[0], 9, 235) + 20,
                                            interpolatedColor(c[0], 24, 235) + 20,
                                            interpolatedColor(c[0], 45, 235) + 20)))
    options = scour.sanitizeOptions()
    options.digits = 3
    options.remove_descriptive_elements = True
    options.enable_viewboxing = True
    options.newlines = False
    cleanSVG = scour.scourString(svg.tostring(), options=options)
    with open("src/assets/images/test.svg", "w", encoding="utf-8") as f:
        f.write(cleanSVG)
    # with gzip.open("py/test.svgz", "wb") as f:
    #     f.write(cleanSVG.encode("utf-8"))


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
