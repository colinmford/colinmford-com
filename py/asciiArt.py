import os
import shutil
from math import ceil, floor

import numpy as np
import svgwrite
from PIL import Image, ImageEnhance
from scour import scour
from fontTools.subset import main as subsetMain


# TODO: Analize glyphs in font for % area coverage
ASCII_CHARS = [" ", ".", ":", "−", "÷", "+", "×", "=", "*", "&", "%", "#", "@", "░", "▒", "▒"]  # Sorted in order of coverage


def createDir(base, name):
    full = os.path.join(base, name)

    if os.path.exists(full):
        shutil.rmtree(full)

    os.makedirs(full, exist_ok=True)

    return full


def subsetFont(url):
    fontPath = os.path.join(os.path.dirname(__file__), "temp.woff2")
    subsetMain([os.path.abspath(url),
          "--text=%s" % "".join(ASCII_CHARS),
          "--output-file=%s" % os.path.join(os.path.dirname(__file__), "temp.woff2"),
          "--flavor=woff2",
          "--layout-features=''",
          "--layout-scripts=''",
          "--no-hinting"
          ])
    return fontPath


def resizeImg(image, height=100):
    width = height * image.width / image.height
    return image.resize((round(width), round(height/2)))


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


def asciiToSVG(asciiImg, location, fontPath):
    rows = len(asciiImg)
    cols = len(asciiImg[0])
    fontSize = 15
    pitch = (fontSize/1000)*604
    lineHeight = fontSize * 1.2

    svg = svgwrite.Drawing()
    svg.viewbox(minx=0, miny=0, width=ceil(cols*pitch), height=ceil(rows*lineHeight))
    svg.embed_font("S", fontPath)
    svg.fit(horiz="left", vert="top", scale="slice")
#     svg.embed_stylesheet("""@font-face {
#   font-family: "Spot Mono";
#   src: url(/assets/fonts/SpotMono-Light.woff) format("woff");
#   font-weight: 300;
#   font-style: normal;
# }""")
    group = svg.g(style="font-size:%spx;font-family:'S',monospace;" % fontSize)
    for i, r in enumerate(asciiImg):
        for j, c in enumerate(r):
            if c[1] != " ":
                group.add(svg.text(c[1],
                                   insert=(round(j*pitch, 3), round((i*lineHeight)+lineHeight), 3),
                                   fill='#%02x%02x%02x' % (interpolatedColor(c[0], 9, 235) + 20,
                                                           interpolatedColor(c[0], 24, 235) + 20,
                                                           interpolatedColor(c[0], 45, 235) + 20)))
    svg.add(group)
    options = scour.sanitizeOptions()
    options.digits = 3
    options.remove_descriptive_elements = True
    options.enable_viewboxing = True
    options.newlines = False
    cleanSVG = scour.scourString(svg.tostring(), options=options)
    with open(os.path.join(location, "face-%s.svg" % (str(rows))), "w", encoding="utf-8") as f:
        f.write(cleanSVG)
    # with gzip.open(os.path.join(location, "face-%s.svgz" % (str(rows))), "wb") as f:
    #     f.write(cleanSVG.encode("utf-8"))


def main():
    d = createDir("src/assets", "faces")
    fontPath = subsetFont("src/assets/styles/fonts/SpotMono-Light.woff")
    image = Image.open("py/IMG_0499.jpg").convert('L')
    image = Image.fromarray(crop_image(image, tolerance=18))
    e = ImageEnhance.Brightness(image)
    image = e.enhance(1.025)
    for ht in range(60, 121):
        resizedImg = resizeImg(image, height=ht)
        asciiImg = pixelToAscii(resizedImg)
        asciiToSVG(asciiImg, d, fontPath)
    os.remove(fontPath)


main()
