from mimetypes import init
import cv2,numpy as np

def display_flow(img,flow,stride=40):
    for index in np.ndindex(flow[::stride,::stride].shape[:2]):
        pt1=tuple(i*stride for i in index)
        delta=flow[pt1].astype(np.int32)
        pt2=tuple(pt1+10*delta)
        if 2<=cv2.norm(delta)<=10:
            cv2.arrowedLine(img,pt1[::-1],pt2[::-1],(0,0,255),5,cv2.LINE_AA,0,.4)
            norm_opt_flow=np.linalg.norm(flow,axis=2)
            norm_opt_flow=cv2.normalize(norm_opt_flow,None,0,1,cv2.NORM_MINMAX)
            cv2.imshow('optical flow',img)
            cv2.imshow('optical flow magnitude',norm_opt_flow)
            key=cv2.waitKey(1)
            if key==27:
                return 1
            else:
                return 0

cam=cv2.VideoCapture(0)
_,prev_frame=cam.read()

prev_frame=cv2.cvtColor(prev_frame,cv2.COLOR_BGR2GRAY)
prev_frame=cv2.resize(prev_frame,(0,0),None,.5,.5)
init_flow=True

while True:
    _,frame=cam.read()
    frame=cv2.resize(frame,(0,0),None,.5,.5)
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    if init_flow:
        opt_flow=cv2.calcOpticalFlowFarneback(prev_frame,gray,None,.5,5,13,10,5,1.1,cv2.OPTFLOW_FARNEBACK_GAUSSIAN)
        init_flow=False
    else:
        opt_flow=cv2.calcOpticalFlowFarneback(prev_frame,gray,None,.5,5,13,10,5,1.1,cv2.OPTFLOW_USE_INITIAL_FLOW)
        prev_frame=np.copy(gray)
        if display_flow(frame,opt_flow):
            break
cv2.destroyAllWindows()

cam.set(cv2.CAP_PROP_POS_FRAMES,0)
_,prev_frame=cam.read()
prev_frame=cv2.cvtColor(prev_frame,cv2.COLOR_BGR2GRAY)
prev_frame=cv2.resize(prev_frame,(0,0),None,.5,.5)
flow_DualTVL1=cv2.createOptFlow_DualTVl1()