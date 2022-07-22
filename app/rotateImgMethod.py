from itertools import groupby
import cv2,numpy as np,random

#this function is from 
# https://stackoverflow.com/questions/43892506/opencv-python-rotate-image-without-cropping-sides
def rotate_image(mat, angle):
    """
    Rotates an image (angle in degrees) and expands image to avoid cropping
    """
    # image shape has 3 dimensions
    height, width = mat.shape[:2] 
    image_center = coords_cask 
    # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

    # rotation calculates the cos and sin, taking absolutes of those.
    abs_cos = abs(rotation_mat[0,0]) 
    abs_sin = abs(rotation_mat[0,1])

    # find the new width and height bounds
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    # subtract old image center (bringing image back to origo) and adding the new image center coordinates
    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]

    # rotate image with the new bounds and translated rotation matrix
    rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))
    return rotated_mat

def get_h(obj_h,cask_m,real_obj_h=1,):
    global metre_per_pix
    metre_per_pix=real_obj_h/obj_h
    dist=cask_m*metre_per_pix
    return dist


def get_w(h_val=None):
    global cask_contour

    if (not h_val) or h_val>=h//2:
        h_val=random.randint(0,h//2)
    
    y1,y2=centre_y-h_val,centre_y+h_val
    tot=[]
    
    #find points on contour with the given height and return average width and both widths
    cask_contour=sorted(cask_contour,key=lambda x:x[0][1])
    for key,group in groupby(cask_contour,lambda x:x[0][1]):
        group=list(group)
        if key==y1 or key==y2:
            first,last=group[0][0],group[-1][0]
            dist=(group[-1][0][0]-group[0][0][0])*metre_per_pix
            tot.append(dist)
            cv2.line(img,first,last,(0,0,255),2)
            cv2.putText(img,f"{dist:.2f}",(first[0],first[1]-5),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),2)
    return sum(tot)/2,tot

#find all the contours and shapes in the image
def get_shapes():
    global mask,contours,cask_contour,cask_box,obj_contour,obj_box,centre_x,centre_y,x,y,w,h,cnt_ind,coords_obj,dimens_obj,angle_obj
    mask=cv2.inRange(img_process,0,180)
    contours,_=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    contours=sorted(list(contours),key=cv2.contourArea,reverse=True)
    cask_contour=contours[0]
    cask_box=cv2.boundingRect(cask_contour)

    obj_contour=contours[1]
    obj_box=coords_obj,dimens_obj,angle_obj=cv2.minAreaRect(obj_contour)
    print(dimens_obj)
    obj_box=cv2.boxPoints(obj_box)
    obj_box=np.int0(obj_box)
    cnt_ind=0
    x,y,w,h=cask_box
    centre_x,centre_y=((w)//2+x,(h)//2+y)

img=cv2.imread("./data/cask7.png")
img=cv2.resize(img,(0,0),fx=2,fy=2)

img_process=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow("img",img_process)
cv2.imshow("img",img)
cv2.waitKey(0)

img_process=cv2.GaussianBlur(img_process,(5,5),0)
#create mask to get the contour of the cask and known object
mask=cv2.inRange(img_process,0,180)

#chain approx none used, as even though it uses more memory it 
# ives more reliable results for getting width later
contours,_=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

#get largest contours which should be the cask and the object and get bounding box and circle
#cask should be the largest contour
contours=sorted(list(contours),key=cv2.contourArea,reverse=True)
cask_contour=contours[0]
cask_box=coords_cask,dimens_cask,angle_cask=cv2.minAreaRect(cask_contour)
cask_box=cv2.boxPoints(cask_box)
cask_box=np.int0(cask_box)


#rotate the box to get the object in the right orientation
if angle_cask>0 and angle_cask!=90:
    print(angle_cask)
    img=rotate_image(img,angle_cask)

black_mask=cv2.inRange(img,0,0)
img=cv2.bitwise_not(img,img,mask=black_mask)
img_process=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img_process=cv2.GaussianBlur(img_process,(5,5),0)

get_shapes()

#if it is horizontal then rotate it to vertical
if cask_box[2]>cask_box[3]:
    img=cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)
    img_process=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_process=cv2.GaussianBlur(img_process,(5,5),0)
    get_shapes()


#draw the shapes and information
cv2.drawContours(img,[obj_box],-1,(0,0,255),2)
circ=cv2.minEnclosingCircle(cask_contour)
cv2.drawContours(img,[cask_contour],-1,(0,255,0),2)
cv2.rectangle(img,(cask_box[0],cask_box[1]),(cask_box[0]+cask_box[2],cask_box[1]+cask_box[3]),(0,255,0),2)
cv2.circle(img,(int(circ[0][0]),int(circ[0][1])),int(circ[1]),(0,255,0),2)
cv2.putText(img,"cask",(cask_box[0],cask_box[1]),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)
real_h=f"{get_h(max(dimens_obj),cask_box[3],1):.2f}"
cv2.putText(img,real_h,(cask_box[0]+cask_box[2],cask_box[1]),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)

cask_h=get_h(max(dimens_obj),cask_box[3],1)
cv2.circle(img,(centre_x,centre_y),5,(255,255,0),2)
get_w()

cv2.imshow('img',img)
cv2.waitKey(0)