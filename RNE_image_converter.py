# 游戏: 《Robotics;Notes Elite》
# 平台: PSVita
# 背景及CG图片转码（bin转png）
# 作者: wetor (www.wetor.top / wetor.top@gmail.com)
# 时间: 2020.5.8
# RNE_image_converter 0.1

# 目前仅支持RGBA格式，256色图像

import os
import struct

from PIL import Image


def getFileNameWithoutExtension(path):
    return path.split('\\').pop().split('/').pop().rsplit('.', 1)[0]


def bin2png(file, saveDir='.'):
    fl = open(file, 'rb')
    filename = getFileNameWithoutExtension(file)
    fileDir = os.path.dirname(file) if saveDir == '.' else saveDir
    width, = struct.unpack('<H', fl.read(2))
    height, = struct.unpack('<H', fl.read(2))
    pixelFormat, = struct.unpack('<H', fl.read(2))
    unKnow, = struct.unpack('<H', fl.read(2))

    pixelColor = {}
    for i in range(pixelFormat * 32):
        color = fl.read(4)
        pixelColor.update({i: (color[2], color[1], color[0], color[3])})

    img = Image.new('RGBA', (width, height))
    for y in range(height):
        for x in range(width):
            img.putpixel((x, y), pixelColor[fl.read(1)[0]])
    fl.close()
    img.save(fileDir + '/' + filename + '.png', 'png')
    print("bin2png: '" + file + "' convert png success! Save as '" + fileDir + '/' + filename + '.png' + "'")


def png2bin(file, saveDir='.'):
    img = Image.open(os.path.abspath(file))
    if len(img.getcolors(256)) is None or img.mode != 'RGBA':
        print('不是是256色，RGBA格式的图像！')
        return
    width = img.size[0]
    height = img.size[1]
    filename = getFileNameWithoutExtension(file)
    fileDir = os.path.dirname(file) if saveDir == '.' else saveDir
    saveAs = fileDir + '/' + filename + '.bin'
    fl = open(saveAs, 'wb')
    fl.write(struct.pack('<H', width))
    fl.write(struct.pack('<H', height))
    fl.write(struct.pack('<H', 8))
    fl.write(struct.pack('<H', 0))
    pixelColor = {}
    for i in range(256):
        color = img.getcolors()[i][1]
        pixelColor.update({color: struct.pack('<B', i)})
        fl.write(bytes([color[2], color[1], color[0], color[3]]))

    for y in range(height):
        for x in range(width):
            fl.write(pixelColor[img.getpixel((x, y))])

    img.close()
    fl.close()
    print("png2bin: '" + file + "' convert bin success! Save as '" + saveAs + "'")


if __name__ == '__main__':
    bin2png('./data/bin/1.bin', './data/png')
    bin2png('./data/bin/2.bin', './data/png')
    bin2png('./data/bin/3.bin', './data/png')
    bin2png('./data/bin/4.bin', './data/png')
    bin2png('./data/bin/5.bin', './data/png')
    bin2png('./data/bin/6.bin', './data/png')

    # png2bin('./data/png/1.png')
    # bin2png('./data/png/1.bin', './data/png')
