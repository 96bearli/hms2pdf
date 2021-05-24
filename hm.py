# -*- codeing = utf-8 -*-
# @Time : 2021/4/1 16:04
# @Author : 96bearli
# @File : hm.py
# @Software : PyCharm
from time import sleep
import os
import requests
import re
import os
import sys
import glob
import platform

from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.platypus import SimpleDocTemplate, Image
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab import rl_settings
from PIL import Image
import importlib, sys

choice = input("是否开启默认转pdf y/n(default yes)")

headers = {
    "referer": "http://twhentai.com/",
    "user-agent": "Mozilla/5.0 (X11; CrOS x86_64 12239.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.102 Safari/537.36"
}


def intro():
    print("*须知1： 若在墙内本工具需翻墙使用\n")
    print("*须知2： 下载大小为0kb请挂代理翻墙\n")
    # sleep(2)
    print("本工具用于下载 http://twhentai.com/ 内H本\n@Author : 96bearli\n下载路径为本脚本目录下网站同名文件夹\n")
    # sleep(2)
    print("您有以下选项:")
    print("1.自行在网站获取url单本下载\n2.自行在网站获取urls多本下载\n3.通过本工具搜索关键词自动获取url或urls")


def get_img(url, path):
    # print(url)
    imgData = requests.get(url=url, headers=headers, timeout=5).content
    print("下载成功，正在保存%s" % path)
    with open(path, "wb") as f:
        f.write(imgData)


"""
convert image to pdf file
"""

# Author: mrbeann <https://github.com/mrbeann/jpg2pdf>



# importlib.reload(sys)
# sys.setdefaultencoding("utf-8")

def topdf(path_2, recursion=None, pictureType=None, sizeMode=None, width=None, height=None, fit=None, save=None):
    """
    Parameters
    ----------
    path : string
           path of the pictures

    recursion : boolean
                None or False for no recursion
                True for recursion to children folder
                wether to recursion or not

    pictureType : list
                  type of pictures,for example :jpg,png...
    sizeMode : int
           None or 0 for pdf's pagesize is the biggest of all the pictures
           1 for pdf's pagesize is the min of all the pictures
           2 for pdf's pagesize is the given value of width and height
           to choose how to determine the size of pdf

    width : int
            width of the pdf page

    height : int
            height of the pdf page

    fit : boolean
           None or False for fit the picture size to pagesize
           True for keep the size of the pictures
           wether to keep the picture size or not

    save : string
           path to save the pdf
    """
    if platform.system() == 'Windows':
        path_2 = path_2.replace('\\', '/')
    if path_2[-1] != '/':
        path_2 = (path_2 + '/')
    if recursion is True:
        for i in os.listdir(path_2):
            if os.path.isdir(os.path.abspath(os.path.join(path_2, i))):
                topdf(path_2 + i, recursion, pictureType, sizeMode, width, height, fit, save)
    filelist = []
    if pictureType is None:
        filelist = glob.glob(os.path.join(path_2, '*.jpg'))
    else:
        for i in pictureType:
            filelist.extend(glob.glob(os.path.join(path_2, '*.' + i)))

    maxw = 0
    maxh = 0
    if sizeMode is None or sizeMode == 0:
        for i in filelist:
            im = Image.open(i)
            if maxw < im.size[0]:
                maxw = im.size[0]
            if maxh < im.size[1]:
                maxh = im.size[1]
    elif sizeMode == 1:
        maxw = 999999
        maxh = 999999
        for i in filelist:
            im = Image.open(i)
            if maxw > im.size[0]:
                maxw = im.size[0]
            if maxh > im.size[1]:
                maxh = im.size[1]
    else:
        if width is None or height is None:
            raise Exception("no width or height provid")
        maxw = width
        maxh = height

    maxsize = (maxw, maxh)
    if save is None:
        filename_pdf = path_2 + path_2.split('/')[-2]
    else:
        filename_pdf = save + path_2.split('/')[-2]
    filename_pdf = filename_pdf + '.pdf'
    c = canvas.Canvas(filename_pdf, pagesize=maxsize)

    l = len(filelist)
    for i in range(l):
        (w, h) = maxsize
        width, height = letter
        if fit is True:
            c.drawImage(filelist[i], 0, 0)
        else:
            c.drawImage(filelist[i], 0, 0, maxw, maxh)
        c.showPage()
    c.save()


def retry(fail_List):
    for i in range(3):
        print("第%d次尝试" % (i + 1))
        fail_Lists = fail_List
        fail_List = []
        for lists in fail_Lists:
            sleep(3)
            try:
                get_img(lists[0], lists[1])
            except Exception as imgError:
                print(imgError)
                print("%s再次失败" % lists[0])
                fail_List.append(lists)
                continue
    try:
        lists = fail_List[0]
        print("失败列表依旧不为空，请检查是否是网站问题\n* 下方为最终失败列表:")
        for lists in fail_List:
            print(lists[0])
        sleep(5)
    except:
        print("恭喜，全部完成")


def down_url(url):
    find_url = re.compile(r"twhentai.com/(hentai_.+?/\d*)")
    find_title = re.compile(r"<title>(.+?)</title>")
    find_name = re.compile(r"(.*)\[")
    find_pages = re.compile(r"\[1/(\d+?)\]")
    # /imglink/doujin/53/0000053467/001.jpg
    find_imgUrl = re.compile(r"(/imglink/.+?)001.jpg")

    try:
        url = re.findall(find_url, url)[0]
    except Exception as urlError:
        print(urlError)
        print("该链接有问题，请检查重试: %s" % url)
        return

    url = "http://twhentai.com/" + url + "/1/"
    response = requests.get(url=url, headers=headers)
    # print(response)
    html = response.text
    title = re.findall(find_title, html)[0]
    name = re.findall(pattern=find_name, string=title)[0].replace(" ", "")
    # print(name)
    pages = re.findall(pattern=find_pages, string=title)[0]
    # print(pages)
    imgUrl = "http://twhentai.com" + re.findall(pattern=find_imgUrl, string=html)[0]
    # imgUrl = imgUrl.replace("1.jpg", "")
    print("信息解析完毕\n漫画名称：%s\n共计%s页" % (name, pages))
    sleep(3)
    name = re.sub("\[.+?\]", "", name)
    name = name.replace("/",' ')
    thisPath = "./twhentai.com/" + name
    fail_List = []
    if not os.path.exists(thisPath):
        os.mkdir(thisPath)
    for i in range(int(pages)):
        if i + 1 < 10:
            imgName = "00" + str(i + 1) + ".jpg"
            imgUrls = imgUrl + imgName
            imgPath = thisPath + '/' + imgName
        elif i + 1 < 100:
            imgName = "0" + str(i + 1) + ".jpg"
            imgUrls = imgUrl + imgName
            imgPath = thisPath + '/' + imgName
        else:
            imgName = str(i + 1) + ".jpg"
            imgUrls = imgUrl + imgName
            imgPath = thisPath + '/' + imgName
        try:
            print("正在下载...当前进度%d/%s" % (i + 1, pages))
            get_img(imgUrls, imgPath)
        except Exception as imgError:
            print(imgError)
            print("%s失败" % imgUrls)
            fail_List.append([imgUrls, imgPath])
            continue
    print("顺利下载阶段完成")
    try:
        lists = fail_List[0]
        print("正在重新尝试失败列表,访问间隔调整为3s")
        print("* 请注意：最多重试3轮")
        retry(fail_List)
    except:
        print("失败列表为空")
        print("恭喜，全部完成")
    if "n" not in choice:
        print("开始转pdf")
        try:
            topdf(thisPath, pictureType=['png', 'jpg'], save='./twhentai.com/')
            print(thisPath + ".pdf")
        except Exception as e:
            print(e)
            print("转pdf失败")


def down_urls(urls):
    for url in urls:
        print("正在进行的Url是：%s" % url)

        down_url(url)


def get_search(key_word, page):
    urls = []
    findList = re.compile('"headline":"(.+?)".+?"url": "(http.+?)"')
    url = "http://twhentai.com/search/" + key_word + '/' + str(page)
    response = requests.get(url=url, headers=headers)
    html = response.text
    # print(html)
    lists = re.findall(findList, html)
    for list in lists:
        print(lists.index(list), "\t", list[0], "\t", list[1].replace("\\", ""))
    chose = input("请选择你想下载的序号，空格间隔多选下载。\n例如：0 1 2 3[回车]为下载这四项\n另:输入next浏览下一页，依此类推\n")
    if 'next' in chose:
        page += 1
        urls = get_search(key_word, page)
        return urls
    else:
        choices = chose.split(" ")
        for i in choices:
            try:
                urls.append(lists[int(i)][1].replace("\\", ""))
                # for u in urls:
                #     print(u)
            except Exception as e:
                print(e)
                print("无法处理，跳过")
                continue
        return urls


def search():
    key_word = input("请输入要搜索的关键字：")
    # http://twhentai.com/search/%e5%88%80%e5%89%91%e7%a5%9e%e5%9f%9f/2/
    page = 1
    urls = get_search(key_word, page)
    print("QAQ,依次要处理的列表如下")
    for i in urls:
        print(i)

    down_urls(urls)


def main():
    intro()
    # sleep(1)
    chose = input("请输入选项并回车\n")
    if chose == "1":
        print("请自行打开网站http://twhentai.com/获取页面链接")
        print("\tlike this:'http://twhentai.com/hentai_manga/28101/1/','http://twhentai.com/hentai_doujin/2807/1/'")
        hm_url = input("请输入网站并回车")
        down_url(hm_url)
    elif chose == '2':
        print("请自行打开网站http://twhentai.com/获取页面链接")
        print("\t输入格式like this:'http://twhentai.com/hentai_manga/28101/1/ http://twhentai.com/hentai_doujin/2807/1/'")
        hm_urls = input("请依次输入链接，以空格' '分隔，最终回车")
        urls = hm_urls.split(' ')
        print("条目处理完成，请查看：")
        for i in urls:
            print("%i.\t%s" % (urls.index(i) + 1, i))
        sleep(2)
        down_urls(urls)
    elif chose == '3':
        print("关键词搜索模式开启")
        search()
    else:
        print("error,默认进入关键词搜索")
        search()


if __name__ == '__main__':
    path = "./twhentai.com"
    if not os.path.exists(path):
        os.mkdir(path)
    main()
