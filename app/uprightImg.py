from itertools import groupby
import cv2,numpy as np,random


def get_type():
    if cask_h<.17:
        return "unknown"
    elif cask_h<.25:
        return "blood tub"

def get_h(obj_h,cask_m,real_obj_h=1,):
    global metre_per_pix
    metre_per_pix=real_obj_h/obj_h
    dist=cask_m*metre_per_pix
    return dist


def get_w(h_val=None):
    global cask_contour

    #if no height is given a radom height is used
    if (not h_val) or h_val>=h//2:
        h_val=random.randint(0,h//2)
    elif h_val:
        h_val=h_val/metre_per_pix
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



def main(im=cv2.imread("./data/cask.jfif")):
    global img,centre_x,centre_y,cask_contour,h,cask_h
    #img=cv2.resize(im,(0,0),fx=2,fy=2)
    img=im.copy()
    img_process=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


    img_process=cv2.GaussianBlur(img_process,(5,5),0)
    cv2.imshow("img",img_process)
    cv2.waitKey(0)
    #create mask to get the contour of the cask and known object
    mask=cv2.inRange(img_process,0,180)

    #chain approx none used, as even though it uses more memory it gives 
    #more reliable results for getting width later
    contours,_=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    #get largest contours which should be the cask and the object and get bounding box and circle
    #cask should be the largest contour
    contours=sorted(list(contours),key=cv2.contourArea,reverse=True)
    cask_contour=contours[0]
    obj_contour=contours[1]
    cask_box=cv2.boundingRect(cask_contour)
    obj_box=cv2.boundingRect(obj_contour)
    circ=cv2.minEnclosingCircle(cask_contour)
    #index of the casks contour
    cnt_ind=0

    x,y,w,h=cask_box
    centre_x,centre_y=((w)//2+x,(h)//2+y)


    #draw the shapes and informations
    cv2.drawContours(img,[cask_contour],-1,(0,0,255),2)
    cv2.rectangle(img,(cask_box[0],cask_box[1]),(cask_box[0]+cask_box[2],cask_box[1]+cask_box[3]),(0,255,0),2)
    cv2.rectangle(img,(obj_box[0],obj_box[1]),(obj_box[0]+obj_box[2],obj_box[1]+obj_box[3]),(0,255,0),2)
    cv2.circle(img,(int(circ[0][0]),int(circ[0][1])),int(circ[1]),(0,255,0),2)
    cv2.putText(img,"cask",(cask_box[0],cask_box[1]),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)

    real_h=f"{get_h(obj_box[3],cask_box[3],1):.2f}"
    cv2.putText(img,real_h,(cask_box[0]+cask_box[2],cask_box[1]),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)

    cask_h=get_h(obj_box[3],cask_box[3],1)
    print(obj_box)

    cv2.circle(img,(centre_x,centre_y),5,(255,255,0),2)
    get_w()
    cv2.imshow('img',img)
    cv2.imshow('mask',mask)
    cv2.waitKey(0)

if __name__=='__main__':
    main()