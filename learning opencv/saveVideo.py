import cv2

cam=cv2.VideoCapture(0)

w=int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
h=int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

vid=cv2.VideoWriter("./data/video_capture.avi",cv2.VideoWriter_fourcc(*'X264'),25,(w,h))

while True:
    _,frame=cam.read()
    vid.write(frame)
    cv2.imshow("frame",frame)
    key=cv2.waitKey(1)
    if key==27:
        break

cam.release()
vid.release()
cv2.destroyAllWindows()