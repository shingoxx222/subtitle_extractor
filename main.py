# base64是一种将不可见字符转换为可见字符的编码方式
import base64
# opencv是跨平台计算机视觉库，实现了图像处理和计算机视觉方面的很多通用算法

import requests
from aip import AipOcr

import corp_frames
import get_frames
import get_subtitle

def requestApi(img):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    params = {"image": img,'language_type':'CHN_ENG'}
    access_token = '24.5f09f482c96e5def035059968b7b7246.2592000.1622070494.282335-24072800'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    results=response.json()
    return results

if __name__ =="__main__":
    path2frames = 'D:/ocr/video/frames/talkshow/%s.jpg'  # 视频转为图片存放的路径（帧）
    path2corpedframes = 'D:/ocr/video/frames/talkshow_tailored/%s.jpg'  # 图片截取字幕后存放的路径

    print('-------------subtitle extractor---------------')
    input("Press Enter to continue...")

    begin=0
    end=84560
    step_size=20

    get_frames.main()
    corp_frames.main(path2frames,path2corpedframes,begin,end,step_size)
    get_subtitle.main(path2corpedframes,begin,end,step_size)