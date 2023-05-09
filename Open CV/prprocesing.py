import cv2 as cv

img = cv.imread('img 1.jpg')

cv.imshow('gambar', img)

cv.waitKey(0)

cv.destroyAllWindows()