import requests
from lxml import etree
import random
import os
import re
import Qiniu
import json


class RedBubble(object):
    def __init__(self, pages, sort_order="top%20selling", category=1):
        self._session = requests.session()
        self._category = category

        if category == 1:
            # 手机壳
            self._url = "https://www.redbubble.com/shop/*?iaCode=u-case-iphone&page=" + str(pages) + "&phoneModel=iPhoneModel-iphone_11&sortOrder=" + sort_order
            self._main = "/icr,iphone_11_soft,back,a,x600-pad,600x600,f8f8f8"
            self._title_cut = " iPhone Soft Case"
            self._size = "750x1000"
        elif category == 2:
            # 挂毯
            self._url = "https://www.redbubble.com/shop/*?iaCode=u-print-tapestry&page=" + str(pages) + "&sortOrder=" + sort_order
            self._main = "/tapestry,720x-pad,600x600,f8f8f8"
            self._title_cut = " Tapestry"
            self._size = "1000x800"
        elif category == 3:
            # 口罩
            self._url = "https://www.redbubble.com/shop/*?iaCode=u-mask&page=" + str(
                pages) + "&sortOrder=" + sort_order
            self._main = "/ur,mask_flatlay_front,product,600x600"
            self._title_cut = " Masks"
            self._size = "1000x500"

        elif category == 4:
            # 浴帘
            self._url = "https://www.redbubble.com/shop/*?iaCode=u-shower-curtain&page=" + str(
                pages) + "&sortOrder=" + sort_order
            self._main = "/ur,shower_curtain_closed,square,600x600"
            self._title_cut = " Curtain"
            self._size = "960x800"

        elif category == 5:
            # 胸针
            self._url = "https://www.redbubble.com/shop/*?iaCode=u-pin-button&page=" + str(
                pages) + "&sortOrder=" + sort_order
            self._main = "/ur,pin_large_front,square,600x600"
            self._title_cut = " Pin"
            self._size = "1000x1000"

        elif category == 6:
            # 抱枕
            self._url = "https://www.redbubble.com/shop/*?iaCode=u-pillows&page=" + str(
                pages) + "&sortOrder=" + sort_order + "&style=u-pillow-throw"
            self._main = "/throwpillow,small,600x-bg,f8f8f8-c,0,120,600,600"
            self._title_cut = " Throw Pillow"
            self._size = "1000x1000"

        elif category == 7:
            # 地枕
            self._url = "https://www.redbubble.com/shop/*?iaCode=u-pillows&page=" + str(
                pages) + "&sortOrder=" + sort_order + "&style=u-pillow-floor"
            self._main = "/throwpillow,36x36,600x-bg,f8f8f8-c,0,120,600,600"
            self._title_cut = " Floor Pillow"
            self._size = "1000x1000"

        # 标题和图片
        self._titles = None
        self._images = None

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        self._category = category

    @property
    def images(self):
        return self._images

    @images.setter
    def images(self, images):
        self._images = images

    @property
    def titles(self):
        return self._titles

    @titles.setter
    def titles(self, titles):
        self._titles = titles

    def get_products(self):
        try:
            res = self._session.get(self._url)
            if res.status_code == 200:
                tree = etree.HTML(res.text)
                # 获取标题、图片地址、去水印原图
                try:
                    self._titles = tree.xpath('//*[@id="SearchResultsGrid"]/a/div/div[3]/div/div[1]/span/text()')
                    result = tree.xpath('/html/body/script[5]/text()')[0]
                    pattern = re.compile("\"artwork\",\"url\":\"https:{{%2F}}{{%2F}}ih1.redbubble.net{{%2F}}image.(.*?){{%2F}}")
                    self._images = re.findall(pattern, result)
                except KeyError:
                    print("获取RedBubble数据失败，请检查是否网页布局发生变化")
                    return None

                return 1
            else:
                print("链接RedBubble失败，请检查网络，VPN等")
                return None

        except ConnectionError:
            print("链接RedBubble失败，请检查网络，VPN等")
            return None

    def up_down_images(self, sock, flag=0):
        for i in range(len(self._titles)):
            sock.send(json.dumps({"msg": "正在上传第{}个图片".format(str(i + 1)), "percent": i / len(self._titles) / 2 * 100}))
            self._images[i] = "https://ih1.redbubble.net/image." + self._images[i] + self._main + ".jpg"

            # 保存成品图
            img = None
            try:
                img = self._session.get(self._images[i]).content
            except ConnectionError:
                print("链接RedBubble失败，请检查网络，VPN等")
                return None

            title = self._titles[i].replace(self._title_cut, " ")[:40] + " " + ''.join(
                random.sample('zyxwvutsrqponmlkjihgfedcba', 3))
            title = re.sub('[.<>:|/\\*?!;#\"\']', '', title)
            title = ' '.join(title.split())
            self._titles[i] = title
            print(self._titles[i])

            path = os.path.dirname(__file__) + "\\img\\" + title + ".jpg"

            qn = Qiniu.Qiniu()
            try:
                with open(path, 'wb') as f:
                    f.write(img)
                if qn.upload(path, title + ".jpg") == 1:
                    if flag == 0:
                        os.remove(path)
            except EOFError:
                print("文件写入出错，请检查权限设置")
                return None

            # 保存原图
            try:
                img = self._session.get(self._images[i].replace(self._main, "/pad," + self._size + ",f8f8f8.jpg")).content
            except ConnectionError:
                print("链接RedBubble失败，请检查网络，VPN等")
                return None

            title = title + " original"
            path = os.path.dirname(__file__) + "\\img\\" + title + ".jpg"
            try:
                with open(path, 'wb') as f:
                    f.write(img)
                if qn.upload(path, title + ".jpg") == 1:
                    os.remove(path)
            except EOFError:
                print("文件写入出错，请检查权限设置")
                return None

        sock.send(json.dumps({"msg": "全部图片上传完毕", "percent": 50}))


