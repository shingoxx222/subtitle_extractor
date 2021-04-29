import os
import cv2

# 定义函数字幕，用来对字幕进行操作
# step_size 步长
def main(fname,begin,end,step_size):
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

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        # 将读取出来的图片转换为b64encode编码格式
        return base64.b64encode(fp.read())

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