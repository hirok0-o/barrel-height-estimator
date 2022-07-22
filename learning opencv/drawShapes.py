import cv2,random,numpy as np

img=cv2.imread("./data/tree.jfif")
img_copy=np.copy(img)
w,h=img.shape[0],img.shape[1]

def rand_pos(mult=1.):
    return (random.randrange(0,int(w*mult)),random.randrange(0,int(h*mult)))

while True:
    key=cv2.waitKey(0)
    if key==ord("p"):
        for pt in [rand_pos() for _ in range (10)]:
            cv2.circle(img,pt,4,(255,0,0),-1)
    elif key==ord("l"):
        cv2.line(img,rand_pos(),rand_pos(),(0,255,0),3)
    elif key==ord("r"):
        cv2.rectangle(img,rand_pos(),rand_pos(),(0,0,255),-1)
    elif key==ord("c"):
        img=np.copy(img_copy)
    elif key==27:
        break
    cv2.imshow("img",img)

cv2.destroyAllWindows()