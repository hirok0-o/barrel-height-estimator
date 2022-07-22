
import cv2,numpy as np

img=cv2.imread("./data/car.jfif")
img=cv2.resize(img,(0,0),img,2,2)
show_img=np.copy(img)


mouse_press=False
x=y=w=h=0
label=cv2.GC_BGD
lbl_clrs={cv2.GC_BGD:(0,0,0),cv2.GC_FGD:(255,255,255)}

def mouse_callback(event,_x,_y,flags,param):
    global show_img,x,y,w,h,mouse_press
    if event==cv2.EVENT_LBUTTONDOWN:
        mouse_press=True
        x,y=_x,_y
        show_img=np.copy(img)
    
    elif event==cv2.EVENT_MOUSEMOVE:
        if mouse_press:
            show_img=np.copy(img)
            cv2.rectangle(show_img,(x,y),(_x,_y),(255,0,0),3)
    
    elif event==cv2.EVENT_LBUTTONUP:
        mouse_press=False
        w,h=_x-x,_y-y

cv2.namedWindow("img")
cv2.setMouseCallback("img",mouse_callback)

while True:
    cv2.imshow("img",show_img)
    key=cv2.waitKey(1)
    if key==ord("a") and not mouse_press:
        if w*h>0:
            break




labels=np.zeros(img.shape[:2],np.uint8)
lables,bgdModel,fgdModel=cv2.grabCut(img,labels,(x,y,w,h),None,None,5,cv2.GC_INIT_WITH_RECT)
show_img=np.copy(img)
show_img[(labels==cv2.GC_PR_BGD)|(labels==cv2.GC_BGD)]//=3

cv2.imshow("img",show_img)
cv2.waitKey()
cv2.destroyAllWindows()

def mouse_callback(event,_x,_y,flags,param):
    global show_img,x,y,w,h,mouse_press
    if event==cv2.EVENT_LBUTTONDOWN:
        mouse_press=True
        cv2.circle(labels,(_x,_y),5,label,cv2.FILLED)
        cv2.circle(show_img,(_x,_y),5,lbl_clrs[label],cv2.FILLED)
    
    elif event==cv2.EVENT_MOUSEMOVE:
        if mouse_press:
            cv2.circle(labels,(_x,_y),5,label,cv2.FILLED)
            cv2.circle(show_img,(_x,_y),5,lbl_clrs[label],-1)
    
    elif event==cv2.EVENT_LBUTTONUP:
        mouse_press=False

cv2.namedWindow("img")
cv2.setMouseCallback("img",mouse_callback)

while True:
    cv2.imshow("img",show_img)
    key=cv2.waitKey(1)
    if key==ord("a") and not mouse_press:
        break
    elif key==ord("l"):
        label=cv2.GC_FGD-label



labels,bgdModel,fgdModel=cv2.grabCut(img,labels,None,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_MASK)
show_img=np.copy(img)
show_img[(labels==cv2.GC_PR_BGD)|(labels==cv2.GC_BGD)]//=3

cv2.imshow("img",show_img)
cv2.waitKey()
cv2.destroyAllWindows()

print(fgdModel)