from ast import parse
import cv2, argparse

parser=argparse.ArgumentParser()
parser.add_argument('--path',default='./data/tree.jfif',help='Image path.')
params=parser.parse_args()
img=cv2.imread(params.path)

assert img is not None
print(f"read {params.path}")
print(f"shape {img.shape}")
print(f"dtype {img.dtype} \n")

#convert to grey scale
img=cv2.imread(params.path,cv2.IMREAD_GRAYSCALE)
assert img is not None
print(f"read {params.path}")
print(f"shape {img.shape}")
print(f"dtype {img.dtype}")

img=cv2.imread("./data/tree.jfif")
img_size=img.shape[0:2]

cv2.imshow("img",img)
cv2.waitKey(2000)