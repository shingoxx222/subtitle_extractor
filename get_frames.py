import os
import cv2

def main():
    # 要提取视频的文件名，隐藏后缀
    sourceFileName = 'talkshow'
    # 在这里把后缀接上
    video_path = os.path.join("D:/ocr/video", sourceFileName + '.mp4')
    times = 0
    # 提取视频的频率，每10帧提取一个
    frameFrequency = 20
    # 输出图片到当前目录video文件夹下
    outPutDirName = 'D:/ocr/video/frames/' + sourceFileName + '/'
    if not os.path.exists(outPutDirName):
        # 如果文件目录不存在则创建目录
        os.makedirs(outPutDirName)
    camera = cv2.VideoCapture(video_path)
    while True:
        times += 1
        res, image = camera.read()
        if not res:
            print('not res , not image')
            break
        if times % frameFrequency == 0:
            cv2.imwrite(outPutDirName + str(times) + '.jpg', image)  #文件目录下将输出的图片名字命名为10.jpg这种形式
            print(outPutDirName + str(times) + '.jpg')
    print('图片提取结束')