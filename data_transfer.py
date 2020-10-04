#!/usr/bin/env python 
from os import path
import re
import PIL.Image as Image
from Qiniu import Qiniu
import random
import datetime
import pandas


class DataTransfer(object):
    @staticmethod
    def data_to_csv(data, template, free):
        category = "380230"
        material = ["ABS", "铝", "帆布", "棉布", "牛仔/丹宁", "EVA", "微纤维", "合成橡胶", "尼龙", "PE", "塑料", "涤纶", "PP", "PU", "PVC", "硅胶"]
        material_case = ["iphone 6", "iphone 6 plus", "iphone 6s", "iphone 6s plus", "iphone 7", "iphone 7 plus", "iphone 8", "iphone 8 plus", "iphone XR", "iphone XS MAX", "iphone X", "iphone XS", "iphone 11", "iphone 11 pro", "iphone 11 pro max", "iphone SE 2020"]
        color = ["米色", "黑色", "蓝色", "天蓝", "褐色", "透明", "金色", "灰色", "深灰色", "绿色", "军绿色"]
        csv_data = []

        length = min(len(data), 50)
        for i in range(length):
            title = data[i]["title"]
            image = data[i]["photoList"]
            if len(image) < 5:
                for i in range(len(image), 5):
                    image.append("")
            description = '<p><img alt="1_Luxury Case For iPhone X XS 8 7 6 s Plus Capinhas Ultra Thin Slim Soft_A0_1" src="http://ae01.alicdn.com/kf/H9e54ba7bb22f4240849f9607548313c9J.jpg?width=950&amp;height=950&amp;hash=1900" /><img alt="1_Luxury Case For iPhone X XS 8 7 6 s Plus Capinhas Ultra Thin Slim Soft_A1_2" src="http://ae01.alicdn.com/kf/H8997f170104c43b1a8e78ba2a2ec6f6ag.jpg?width=950&amp;height=950&amp;hash=1900" /><img alt="1_Luxury Case For iPhone X XS 8 7 6 s Plus Capinhas Ultra Thin Slim Soft_A2_3" src="http://ae01.alicdn.com/kf/Hf989820f8fbc4f8bb059ed5a5b05e077I.jpg?width=950&amp;height=950&amp;hash=1900" /><img alt="1_Luxury Case For iPhone X XS 8 7 6 s Plus Capinhas Ultra Thin Slim Soft_A3_4" src="http://ae01.alicdn.com/kf/H69b181ebe7e246bf9df16e77d74c3b38J.jpg?width=950&amp;height=950&amp;hash=1900" /><img alt="1_Luxury Case For iPhone X XS 8 7 6 s Plus Capinhas Ultra Thin Slim Soft_A4_5" src="http://ae01.alicdn.com/kf/H6cf754583b5f4d069195faba48d61e28C.jpg?width=950&amp;height=950&amp;hash=1900" /><img alt="1_Luxury Case For iPhone X XS 8 7 6 s Plus Capinhas Ultra Thin Slim Soft_A5_6" src="http://ae01.alicdn.com/kf/Hbce2da741c8e4aaeadbc1a514b1febb6P.jpg?width=950&amp;height=950&amp;hash=1900" /><img alt="1_Luxury Case For iPhone X XS 8 7 6 s Plus Capinhas Ultra Thin Slim Soft_A6_7" src="http://ae01.alicdn.com/kf/Hcad3cd5d4c30455e994eb338e2931368A.jpg?width=950&amp;height=950&amp;hash=1900" /><img alt="1_Luxury Case For iPhone X XS 8 7 6 s Plus Capinhas Ultra Thin Slim Soft_A7_8" src="http://ae01.alicdn.com/kf/He396ff86b0f747daa7e28ca9c14036639.jpg?width=950&amp;height=950&amp;hash=1900" /></p>'
            original = "https://haiyingshuju.com/wish/index.html#/index/goods_details?pid=" + data[i]["id"]
            color_case = list(set(data[i]["skus"]["colors"]))
            color_case = color_case[:11]

            print(color_case)

            for j in range(len(material)):
                for k in range(len(color_case)):
                    one_list = []
                    if color_case[k] == "null":
                        one_list = [category, i, material[j], material_case[j], "", "", "", "CN", "",
                                    "", 3.19, 999, "", "件/个",
                                    "单件出售", "", "", "", title, image[0], image[1], image[2], image[3], image[4],
                                    image[5], "支付减库存", "5", "30", description, "0.02", "1", "1", "1", template, free,
                                    "Service Template for New Sellers", "", original]
                    else:
                        one_list = [category, i, material[j], material_case[j], color[k], color_case[k], "", "CN", "", "", 3.19, 999, "", "件/个",
                            "单件出售", "", "", "", title, image[0], image[1], image[2], image[3], image[4], image[5], "支付减库存", "5", "30", description, "0.02", "1", "1", "1", template, free, "Service Template for New Sellers", "", original]

                    csv_data.append(one_list)
        try:
            today = datetime.datetime.now().strftime('%y-%m-%d %H-%M-%S')
            csv_pa = pandas.DataFrame(csv_data)
            csv_pa.to_csv(path.dirname(__file__) + "/excel/" + template + today + "_1.csv")
            print(template + today + "_1.csv")
            return template + today + "_1.csv"
        except:
            return None

    @staticmethod
    def red_to_csv(data, template, free):
        category = "380230"
        material = ["ABS", "铝", "帆布", "棉布", "牛仔/丹宁", "EVA", "微纤维", "合成橡胶", "尼龙", "PE", "塑料", "涤纶", "PP", "PU", "PVC",
                    "硅胶"]
        material_case = ["iphone 6", "iphone 6 plus", "iphone 6s", "iphone 6s plus", "iphone 7", "iphone 7 plus",
                         "iphone 8", "iphone 8 plus", "iphone XR", "iphone XS MAX", "iphone X", "iphone XS",
                         "iphone 11", "iphone 11 pro", "iphone 11 pro max", "iphone SE 2020"]

        csv_data = []

        for i in range(len(data)):
            title = data[
                        i] + " Transparent Case For iPhone X XSMAX XR 11 Pro Max case for iPhone 6 6s 5 5s 7plus 8plus iphone 7 8 case"
            image = (Qiniu.QiniuUrl + data[i] + ".jpg").replace(" ", "%20")
            original = Qiniu.QiniuUrl + data[i] + " original.jpg"
            description = '<p><img alt="1_Luxury Case For iPhone X XS 8 7 6 s Plus Capinhas Ultra Thin Slim Soft_A0_1" src="http://ae01.alicdn.com/kf/H9e54ba7bb22f4240849f9607548313c9J.jpg?width=950&amp;height=950&amp;hash=1900" /><img alt="1_Luxury Case For iPhone X XS 8 7 6 s Plus Capinhas Ultra Thin Slim Soft_A1_2" src="http://ae01.alicdn.com/kf/H8997f170104c43b1a8e78ba2a2ec6f6ag.jpg?width=950&amp;height=950&amp;hash=1900" /><img alt="1_Luxury Case For iPhone X XS 8 7 6 s Plus Capinhas Ultra Thin Slim Soft_A2_3" src="http://ae01.alicdn.com/kf/Hf989820f8fbc4f8bb059ed5a5b05e077I.jpg?width=950&amp;height=950&amp;hash=1900" /><img alt="1_Luxury Case For iPhone X XS 8 7 6 s Plus Capinhas Ultra Thin Slim Soft_A3_4" src="http://ae01.alicdn.com/kf/H69b181ebe7e246bf9df16e77d74c3b38J.jpg?width=950&amp;height=950&amp;hash=1900" /><img alt="1_Luxury Case For iPhone X XS 8 7 6 s Plus Capinhas Ultra Thin Slim Soft_A4_5" src="http://ae01.alicdn.com/kf/H6cf754583b5f4d069195faba48d61e28C.jpg?width=950&amp;height=950&amp;hash=1900" /><img alt="1_Luxury Case For iPhone X XS 8 7 6 s Plus Capinhas Ultra Thin Slim Soft_A5_6" src="http://ae01.alicdn.com/kf/Hbce2da741c8e4aaeadbc1a514b1febb6P.jpg?width=950&amp;height=950&amp;hash=1900" /><img alt="1_Luxury Case For iPhone X XS 8 7 6 s Plus Capinhas Ultra Thin Slim Soft_A6_7" src="http://ae01.alicdn.com/kf/Hcad3cd5d4c30455e994eb338e2931368A.jpg?width=950&amp;height=950&amp;hash=1900" /><img alt="1_Luxury Case For iPhone X XS 8 7 6 s Plus Capinhas Ultra Thin Slim Soft_A7_8" src="http://ae01.alicdn.com/kf/He396ff86b0f747daa7e28ca9c14036639.jpg?width=950&amp;height=950&amp;hash=1900" /></p>'
            for j in range(len(material)):
                one_list = [category, i, material[j], material_case[j], "", "", "", "CN", "", "", 3.19, 999, "", "件/个",
                            "单件出售", "", "", "", title, image, "", "", "", "", "", "支付减库存", "5", "30", description,
                            "0.02", "1", "1", "1", template, free, "Service Template for New Sellers", "", original]
                csv_data.append(one_list)

        try:
            today = datetime.datetime.now().strftime('%y-%m-%d %H-%M-%S')
            csv_pa = pandas.DataFrame(csv_data)
            csv_pa.to_csv(path.dirname(__file__) + "\\excel\\" + template + today + "_1.csv")
            return template + today + "_1.csv"
        except:
            return None

    @staticmethod
    def file_to_data(filename):
        filename = path.dirname(__file__) + "/" + filename
        links = None
        try:
            with open(filename, 'r') as f:
                links = f.readlines()

            if len(links) > 0:
                for i in range(len(links)):
                    pattern = re.compile("https://ih1.redbubble.net/image.(.*?)/icr,iphone_11")
                    links[i] = re.findall(pattern, links[i])[0]
            else:
                print("文件中没有链接数据")
                return None
        except FileNotFoundError:
            print("文件不存在")
            return None

        return links

    @staticmethod
    def image_to_big(titles):
        print("创建拼接主图")
        image_names = [path.dirname(__file__) + "\\img\\" + title + ".jpg" for title in titles][:8]

        if len(image_names) < 8:
            print("图片太少了")
            return None



        IMAGE_weight_SIZE = 575  # 每张小图片的大小的宽度
        IMAGE_hight_SIZE = 1000  # 每张小图片的大小的长度
        IMAGE_ROW = 2  # 图片间隔，也就是合并成一张图后，一共有几行
        IMAGE_COLUMN = 4  # 图片间隔，也就是合并成一张图后，一共有几列

        to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_weight_SIZE, IMAGE_ROW * IMAGE_hight_SIZE))  # 创建一个新图
        # 循环遍历，把每张图片按顺序粘贴到对应位置上
        for y in range(1, IMAGE_ROW + 1):
            for x in range(1, IMAGE_COLUMN + 1):
                from_image = Image.open(image_names[IMAGE_COLUMN * (y - 1) + x - 1]).resize(
                    (IMAGE_weight_SIZE, IMAGE_hight_SIZE), Image.ANTIALIAS)
                to_image.paste(from_image, ((x - 1) * IMAGE_weight_SIZE, (y - 1) * IMAGE_hight_SIZE))


        filename = (datetime.datetime.now()).strftime('%Y-%m-%d') + " " + ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 3)) + " final.jpg"
        save_path = path.dirname(__file__) + "\\img\\" + filename
        to_image.save(save_path)
        print("创建成功")

        return filename

    @staticmethod
    def image_to_html(url, titles):
        print("创建来源页面")
        save_path = path.dirname(__file__) + "\\img\\final.html"
        f = open(save_path, "w+")
        for title in titles:
            data = "<img src='" + url + title + " original.jpg' width='100px' height='170px'/>"
            f.write(data)
        f.close()

        filename = (datetime.datetime.now()).strftime('%Y-%m-%d') + " " + ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 3)) + " final.html"
        print("创建成功")
        q = Qiniu()
        q.upload(save_path, filename)

        return filename

    @staticmethod
    def data_to_excel(titles, finalImage, finalHtml):
        pass

    @staticmethod
    def data_to_txt(titles, finalImage, finalHtml):
        print("写出文件")
        save_path = path.dirname(__file__) + "\\img\\final.txt"
        f = open(save_path, "w+")
        for title in titles:
            data = Qiniu.QiniuUrl + title + ".jpg"
            f.write(data)
            f.write('\n')
        f.write(Qiniu.QiniuUrl + finalHtml)
        f.write('\n')
        f.write(Qiniu.QiniuUrl + finalImage)
        f.close()
        print("写出成功")

        return save_path

    @staticmethod
    def crop_pic(titles):
        """裁切图片"""
        for title in titles:
            try:
                # print("img is",img)
                # 打开图片
                old_img_path = path.dirname(__file__) + "\\img\\" + title + ".jpg"
                img1 = Image.open(old_img_path)
                # print("img1is",img1)
                # 获取图片的尺寸长
                # x = img.size[0]
                # 获取图片的尺寸宽
                # y = img.size[1]

                # 截图
                cropped = img1.crop((126, 0, 471, 600))
                # 保存到新的目录中
                new_img_path = path.dirname(__file__) + "\\img\\" + title + ".jpg"
                cropped.save(new_img_path)
            except EOFError:
                print("处理图片出错")
                return None

    def add_writing(filename):
        """ 添加文字"""
        #  学习链接：  https://blog.csdn.net/weixin_43945855/article/details/103485114
        img_path = path.dirname(__file__) + "\\img\\" + filename
        img_1 = Image.open(img_path)
        img_2 = Image.open(path.dirname(__file__) + "\\styles.jpg")

        new_image = Image.new('RGB', (2300, 2300), (255, 255, 255))
        new_image.paste(img_1, (0, 0))
        new_image.paste(img_2, (0, 2000))

        new_image.save(img_path)  # 合成后的图片路径以及文件名

        q = Qiniu()
        q.upload(img_path, filename)