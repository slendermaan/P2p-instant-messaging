from PIL import Image
# PIL,Python Imaging Library.图像处理功能
def plus(str):
    # Python zfill() 方法返回指定长度的字符串，原字符串右对齐，前面填充0。

    return str.zfill(8)


def get_key(strr):
    # 获取要隐藏的文件内容

    tmp = strr

    f = open(tmp, "rb")  # 要读取二进制文件，比如图片、视频等等，用'rb'模式打开文件

    s = f.read()
    str = ""

    for i in range(len(s)):
        # 逐个字节将要隐藏的文件内容转换为二进制，并拼接起来
        # 1.使用bin()函数将十进制的ascii码转换为二进制

        # 2.由于bin()函数转换二进制后，二进制字符串的前面会有"0b"来表示这个字符串是二进制形式，所以用replace()替换为空

        # 3.又由于这样替换之后是七位，而正常情况下每个字符由8位二进制组成，所以使用自定义函数plus将其填充为8位

        str = str + plus(bin(s[i]).replace('0b', ''))  # s[i]为该位置字符的十进制表示的ascll码

        # print str

    f.closed

    return str


def mod(x, y):
    return x % y


# str1为载体图片路径，str2为隐写文件，str3为加密图片保存的路径

def lsb_write(str1, str2, str3):
    msg = str2
    print(len(str2))
    with open('hide.txt', "w") as f:
        f.write(msg)
        f.close()
    im = Image.open(str1)
    # 获取图片的宽和高
    width = im.size[0]
    height = im.size[1]
    count = 0
    # 获取需要隐藏的信息

    key = get_key('hide.txt')

    keylen = len(key)

    for h in range(0, height):

        for w in range(0, width):

            pixel = im.getpixel((w, h))  # 返回该像素点三原色的二进制信息，形成一个数组

            a = pixel[0]  # R

            b = pixel[1]  # G

            c = pixel[2]  # B

            if count == keylen:
                break

            # 下面的操作是将信息隐藏进去

            # 分别将每个像素点的RGB值余2，这样可以去掉最低位的值

            # 再从需要隐藏的信息中取出一位，转换为整型

            # 两值相加，就把信息隐藏起来了

            a = a - mod(a, 2) + int(key[count])

            count += 1

            if count == keylen:
                im.putpixel((w, h), (a, b, c))

                break

            b = b - mod(b, 2) + int(key[count])

            count += 1

            if count == keylen:
                im.putpixel((w, h), (a, b, c))

                break

            c = c - mod(c, 2) + int(key[count])

            count += 1

            if count == keylen:
                im.putpixel((w, h), (a, b, c))

                break

            if count % 3 == 0:
                im.putpixel((w, h), (a, b, c))

    im.save(str3)
# -*- coding:UTF-8 -*-

from PIL import Image


def mod(x, y):
    return x % y;


# le为所要提取的信息的长度，str1为加密载体图片的路径，str2为提取文件的保存路径

def lsb_tq(le, str1, str2):
    b = ""
    im = Image.open(str1)

    lenth = le * 8

    width = im.size[0]

    height = im.size[1]

    count = 0

    for h in range(0, height):

        for w in range(0, width):

            # 获得(w,h)点像素的值

            pixel = im.getpixel((w, h))

            # 此处余3，依次从R、G、B三个颜色通道获得最低位的隐藏信息

            if count % 3 == 0:

                count += 1

                b = b + str((mod(pixel[0], 2)))

                if count == lenth:
                    break

            if count % 3 == 1:

                count += 1

                b = b + str((mod(pixel[1], 2)))

                if count == lenth:
                    break

            if count % 3 == 2:

                count += 1

                b = b + str((mod(pixel[2], 2)))

                if count == lenth:
                    break

        if count == lenth:
            break
    fina_msg=""
    for i in range(0, len(b), 8):
        # 以每8位为一组二进制，转换为十进制
        stra = int(b[i:i + 8], 2)
        # 将转换后的十进制数视为ascii码，再转换为字符串写入到文件中
        fina_msg=fina_msg+chr(stra)
        stra = ""
    print(fina_msg)
    return fina_msg


