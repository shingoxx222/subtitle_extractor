# base64是一种将不可见字符转换为可见字符的编码方式
import base64
# opencv是跨平台计算机视觉库，实现了图像处理和计算机视觉方面的很多通用算法
import os

import cv2
import requests
from aip import AipOcr

def tailor_video():
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

def text_create(name, msg):
    full_path = "D:/ocr/baidu/" + name + '.txt'  # 也可以创建一个.doc的word文档
    file = open(full_path, 'w')
    file.write(msg)
    file.close()

def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def tailor(path1,path2,begin,end,step_size):  #截取字幕
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

def requestApi(img):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    params = {"image": img,'language_type':'CHN_ENG'}
    access_token = '24.5f09f482c96e5def035059968b7b7246.2592000.1622070494.282335-24072800'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    results=response.json()
    return results

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        # 将读取出来的图片转换为b64encode编码格式
        return base64.b64encode(fp.read())

# 定义函数字幕，用来对字幕进行操作
# step_size 步长
def subtitle(fname,begin,end,step_size):
    array =[] #定义一个数组用来存放words
    for i in range(begin,end,step_size):  #begin开始，end结束，循环按照步长step_size遍历，共有419张图片，也就是（1,420,10）
        fname1=fname % str(i)
        print(fname1)
        image = get_file_content(fname1)
        try:
            results=requestApi(image)['words_result']  #调用requestApi函数，获取json字符串中的words_result
            for item in results:
                print(results)
                array.append(item['words'])
                # if is_Chinese(item['words']):
                #     array.append(item['words'].replace('猎奇笔记本', '')) # 将图片中不需要的字幕“猎奇笔记本”替换为空
        except Exception as e:
            print(e)

    text=''
    result = list(set(array))  # 将array数组准换为一个无序不重复元素集达到去重的效果，再转为列表
    result.sort(key=array.index) # 利用sort将数组中的元素即字幕重新排序，达到视频播放字幕的顺序
    for item in result:
        print(item)
        text+=item+'\n'
    text_create('talkshow',text)

if __name__ =="__main__":
    path1 = 'D:/ocr/video/frames/talkshow/%s.jpg'  # 视频转为图片存放的路径（帧）
    path2 = 'D:/ocr/video/frames/talkshow_tailored/%s.jpg'  # 图片截取字幕后存放的路径
    print("""
    1.图片裁剪
    2.提取字幕
    3.裁剪视频
    """)
    choose=input()
    begin=10100
    end=84560
    step_size=20
    if choose=='1':
        tailor(path1,path2,begin,end,step_size)
    if choose=='2':
        subtitle(path2,begin,end,step_size)
    if choose=='3':
        tailor_video()