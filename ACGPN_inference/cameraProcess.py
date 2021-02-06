import cv2

def getSourceImageFromCamera(imageWidth,imageHeight,imageSavePath):
    """
    :param imageWidth:the width of imagey
    :param imageHeight:the height of image
    :param imageSavePath: the path should be saved
    :return: imagepath
    """
    camera = cv2.VideoCapture(0)
    while(1):
        _,frame = camera.read()
        cv2.rectangle(frame,(110,40),(110+imageWidth,40+imageHeight),(0,0,255),1)
        ### 请将头部放置红色方框内，按y确定
        cv2.imshow("put your head  in the red box and press y to confirm",frame)
        if cv2.waitKey(1) & 0xFF == ord('y'):
            cv2.cvtColor(frame,cv2.COLOR_BGRA2RGB)
            sourceImage = frame[40+1:40+imageHeight-1,110+1:110+imageWidth-1]
            cv2.imwrite(imageSavePath,sourceImage)
            break
    camera.release()
    cv2.destroyAllWindows()
    return imageSavePath


#if __name__ == "__main__":
#    getSourceImageFromCamera(430,410,"sourceImage.jpg")