# 把粉色底色的战机bmp图片换成了深蓝色背景色，第一次用简单方法处理矩阵
import cv2
image = cv2.imread('D:\\alien_invasion\\images\\meteorite.bmp')


for i in range(0, 73):
    for j in range(0, 70):
        if image[i, j, 0] == 0 and image[i, j, 1] == 0:
            if image[i, j, 2] == 0:
                image[i, j] = (175, 39, 5)
cv2.imwrite('D:\\alien_invasion\\images\\meteorite.bmp', image)

