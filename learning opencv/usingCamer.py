import cv2

cam=cv2.VideoCapture(0)

while True:
    _,frame=cam.read()
    if not _:
        break
    cv2.imshow("window",frame)
    key=cv2.waitKey(1)
    if key==27:
        break

cam.release()
cv2.destroyAllWindows()

