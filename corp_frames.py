def main(path1,path2,begin,end,step_size):  #截取字幕
    for i in range(begin,end,step_size):
        fname1=path1 % str(i)
        print(fname1)
        img = cv2.imread(fname1)
        print(img.shape)
        cropped = img[600:660, 250:1030]  # 裁剪坐标为[y0:y1, x0:x1]
        imgray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        thresh = 200
        ret, binary = cv2.threshold(imgray, thresh, 255, cv2.THRESH_BINARY)  # 输入灰度图，输出二值图
        binary1 = cv2.bitwise_not(binary)  # 取反
        cv2.imwrite(path2 % str(i), binary1)