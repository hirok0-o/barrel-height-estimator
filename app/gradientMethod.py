import cv2,numpy as np,random,uprightImg

def get_h(obj_h,cask_m,real_obj_h=1,):
    global metre_per_pix
    metre_per_pix=real_obj_h/obj_h
    dist=cask_m*metre_per_pix
    return dist

#incomplete
def get_w(h_val=None):
    global cask_contour

    if (not h_val) or h_val>=h//2:
        h_val=random.randint(0,h//2)

def get_coords(h_val=None):
    h_val=random.randint(28,h//2)
    #find values for quadratic equation
    a=1+m**2
    b=2*m*y_intercept
    c=(y_intercept**2)-(h_val**2)
    
    #use quadratic equation to find Δx values
    x_1=(-b+((b**2)-(4*a*c))**.5)/(2*a)
    x_2=(-b-((b**2)-(4*a*c))**.5)/(2*a)
    
    #find Δy values
    y_1=((h_val**2)-(x_1**2))**.5
    y_2=((h_val**2)-(x_2**2))**.5
    
    #find the points using the Δx and Δy values
    #im not sure why none of these values get the correct points
    x_coord_1_1=centre_x-x_1
    y_coord_1_1=m*x_coord_1_1+y_intercept

    x_coord_2_1=centre_x-x_2
    y_coord_2_1=m*x_coord_2_1+y_intercept

    x_coord_1_2=centre_x-x_1
    y_coord_1_2=centre_y+y_1

    x_coord_2_2=centre_x-x_2
    y_coord_2_2=centre_y+y_2

    #find the actual points using the perpendicular lines equations 
    x_final_1=((x_coord_1_2/m)+y_coord_1_2-y_intercept)/(m+(1/m))
    y_final_1=m*x_final_1+y_intercept

    x_final_2=((x_coord_2_2/m)+y_coord_2_2-y_intercept)/(m+(1/m))
    y_final_2=m*x_final_2+y_intercept

    y_intercept_2=y_final_2-(-1/m)*x_final_2

    points=[]
    for point in cask_contour:
        if point[0][0]*(-1/m)+y_intercept_2==point[0][1]:
            points.append(point)
            cv2.circle(img,(int(point[0][0]),int(point[0][1])),5,(255,0,255),-1)
    print(points)

    cv2.circle(img,(int(x_coord_1_2),int(y_coord_1_2)),5,(0,0,255),2)
    cv2.circle(img,(int(x_coord_2_2),int(y_coord_2_2)),5,(0,0,255),2)
    
    cv2.circle(img,(int(x_coord_1_1),int(y_coord_1_1)),5,(255,0,0),2)
    cv2.circle(img,(int(x_coord_2_1),int(y_coord_2_1)),5,(255,0,0),2)

    cv2.circle(img,(int(x_final_1),int(y_final_1)),5,(0,255,0),2)
    cv2.circle(img,(int(x_final_2),int(y_final_2)),5,(0,255,0),2)
img=cv2.imread("./data/cask7.png")
img=cv2.resize(img,(0,0),fx=2,fy=2)

img_process=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

img_process=cv2.GaussianBlur(img_process,(5,5),0)

#cv2.imshow("img",img_process)
#cv2.waitKey(0)
#create mask to get the contour of the cask and known object
mask=cv2.inRange(img_process,0,180)

#chain approx none used, as even though it uses more memory it gives more reliable results for getting width later
contours,_=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

#get largest contours which should be the cask and the object and get bounding box and circle
#cask should be the largest contour
contours=sorted(list(contours),key=cv2.contourArea,reverse=True)
cask_contour=contours[0]
obj_contour=contours[1]
cask_box=coords_cask,dimens_cask,angle_cask=cv2.minAreaRect(cask_contour)
cask_box=cv2.boxPoints(cask_box)
cask_box=np.int0(cask_box)
centre_x,centre_y=coords_cask[0],coords_cask[1]

obj_box=coords_obj,dimens_obj,angle_obj=cv2.minAreaRect(obj_contour)
obj_box=cv2.boxPoints(obj_box)
obj_box=np.int0(obj_box)

circ=cv2.minEnclosingCircle(cask_contour)
cnt_ind=0

cask_h=get_h(max(dimens_obj),max(dimens_cask))

for point in cask_box:
    cv2.circle(img,(int(point[0]),int(point[1])),5,(255,0,255),2)

#if it is upright use upright fuction
if angle_cask==0 or angle_cask==90:
    uprightImg.main(img)
    quit()

#find equation of line parrallel edge of point 1 and 4 (purple line) and passes through centre
m=(cask_box[3][1]-cask_box[0][1])/(cask_box[3][0]-cask_box[0][0])
y_intercept=centre_y-m*(centre_x)
h=((cask_box[3][1]-cask_box[0][1])**2+(cask_box[3][0]-cask_box[0][0])**2)**0.5

get_coords()

#draw everything on the image
cv2.circle(img,(int(centre_x),int(centre_y)),5,(0,255,255),-1)
cv2.putText(img,f"HEIGHT: {cask_h:.2f}",(200,20),cv2.FONT_HERSHEY_SIMPLEX,.5,(0,0,255),2)
cv2.drawContours(img,[contours[cnt_ind]],-1,(0,0,255),2)
cv2.drawContours(img,[cask_box],cnt_ind,(0,255,0),2)
cv2.drawContours(img,[obj_box],cnt_ind,(0,255,0),2)
#cv2.circle(img,(int(circ[0][0]),int(circ[0][1])),int(circ[1]),(0,255,0),2)
#cv2.circle(img,(int(centre_x),int(centre_y)),5,(0,0,255),2)

#draw the shapes and informations
cv2.line(img,(int(cask_box[0][0]),int(cask_box[0][1])),(int(cask_box[3][0]),int(cask_box[3][1])),(255,0,255),2)
cv2.imshow('img',img)
cv2.waitKey(0)