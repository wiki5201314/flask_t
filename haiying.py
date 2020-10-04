#!/usr/bin/env python
import requests
import json
import datetime


class Haiying(object):
    def __init__(self):
        data = {
            "username": "sjbb5VdTx2p5Rlh3gCHPLA==",
            "password":  "JqU23vNpkIKChJn36wknJg=="
        }
        login_url = "https://haiyingshuju.com/auth/login"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; OPPO R9s Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.7.9.1059 Mobile Safari/537.36",
        }

        self._session = requests.session()

        # 登陆
        res = self._session.post(login_url, data=data, headers=headers)

        self._token = res.headers["token"]
        check_url = "https://haiyingshuju.com/user/userInfo/info"
        headers["token"] = self._token
        data = {}
        res = self._session.post(check_url, data=data, headers=headers)
        if res.text.find("查询成功") != -1:
            print("海鹰数据登陆成功")

    def get_shopee_ids(self):
        ids = []
        end = datetime.date.today()
        start = (end - datetime.timedelta(days=180)).strftime('%Y-%m-%d')
        end = end.strftime('%Y-%m-%d')
        for index in range(10):
            print("采集第{}页".format(str(index + 1)))
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json;charset=UTF-8",
                "token": self._token
            }
            data = {
                "cids": [],
                "country": "1",
                "genTimeEnd": end,
                "genTimeStart": start,
                "historicalSoldEnd": "",
                "historicalSoldStart": "100",
                "index": index + 1,
                "isShopeeVerified": "",
                "likedCountEnd": "",
                "likedCountStart": "",
                "merchant": "",
                "merchantStatus": 1,
                "orderColumn": "historical_sold",
                "pageSize": 50,
                "paymentEnd": "",
                "paymentStart": "",
                "paymentThreeDay1End": "",
                "paymentThreeDay1Start": "",
                "pid": "",
                "pidOrTitle": "",
                "pidStatus": 1,
                "priceEnd": "",
                "priceStart": "",
                "ratingCountEnd": "",
                "token": self._token,
                "ratingCountStart": "",
                "ratingEnd": "",
                "ratingStart": "",
                "salesThreeDay1End": "",
                "salesThreeDay1Start": "",
                "salesThreeDayGrowthEnd": "",
                "salesThreeDayGrowthStart": "",
                "shopLocation": "",
                "shopLocationStatus": "",
                "soldEnd": "",
                "soldStart": "",
                "sort": "DESC",
                "title": "",
                "titleStatus": 1
            }
            jdata = json.dumps(data)
            try:
                url = "https://haiyingshuju.com/shopee/product/productList"
                res = requests.post(url, headers=headers, data=jdata)
                details = json.loads(res.text)
                for de in details["data"]:
                    shopee_link = "https://shopee.com.my/" + de["title"].replace(" ", "-") + "-i." + de["shopId"] + "." + de["pid"]
                    haiying_link = "https://haiyingshuju.com/newsShopee/index.html#/content/productDetail/" + de["pid"] + "/1"
                    ids.append([shopee_link, haiying_link])

            except KeyError:
                print("查询失败")
                continue

        return ids


    def get_ids(self, keywords):
        ids = []
        end = datetime.date.today()
        start = (end - datetime.timedelta(days=180)).strftime('%Y-%m-%d')
        end = end.strftime('%Y-%m-%d')
        for index in range(10):
            print("采集第{}页".format(str(index + 1)))
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json;charset=UTF-8",
                "token": self._token
            }
            data = {
                "cids": "",
                "dailySalesAccuracyEnd": "",
                "dailySalesAccuracyStart": "",
                "genTimeEnd": end,
                "genTimeStart": start,
                "hwc": "",
                "index": index + 1,
                "intervalRatingEnd": "",
                "intervalRatingStart": "",
                "maxNumBoughtEnd": "1000,5000,10000,20000,",
                "maxNumBoughtStart": "1000,5000,10000,20000,",
                "merchant": "",
                "merchantStatus": 1,
                "numRatingEnd": "",
                "numRatingStart": "",
                "orderColumn": "max_num_bought",
                "pageSize": 200,
                "pb": "",
                "pid": "",
                "pidStatus": 1,
                "pname": keywords,
                "pnameStatus": 1,
                "ratingEnd": "",
                "ratingStart": "",
                "sort": "DESC",
                "token": self._token,
                "totalSalesArrivalDateEnd": "",
                "totalSalesArrivalDateStart": "",
                "totalpriceEnd": "",
                "totalpriceStart": "",
                "verified": "",
                "viewRate1End": "",
                "viewRate1Start": ""
            }
            jdata = json.dumps(data)
            try:
                url = "https://haiyingshuju.com/wish_2.0/product/list"
                res = requests.post(url, headers=headers, data=jdata)
                details = json.loads(res.text)
                for de in details["data"]:
                    ids.append(de["pid"])

            except KeyError:
                print("查询失败")
                continue

        return ids

    def get_detail(self, id):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8",
            "user-agent": "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; OPPO R9s Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.7.9.1059 Mobile Safari/537.36",
            "token": self._token
        }
        data = {
            "pid": id
        }
        jdata = json.dumps(data)
        try:
            url = "https://haiyingshuju.com/wish_2.0/product/detail/base"
            res = requests.post(url, headers=headers, data=jdata)
            details = json.loads(res.text)

            # 销量太低的淘汰
            feed = int(details["productInfo"]["feedTileText"])
            if feed < 100:
                print("{} 销量太低".format(id))
                return None

            title = details["productInfo"]["pname"]
            tags = details["productInfo"]["tags"]
            if tags is None:
                tags = "ladies, fashion, jewelry, women, man"
            else:
                tags = ",".join(tags.split(",")[:9])
            description = details["productInfo"]["description"]
            photoList = details["productInfo"]["photosList"][:19]
            if len(photoList) == 0:
                print("没有图片")
                return None

            if photoList[0].find("theshelf") != -1:
                del (photoList[0])

            for i in range(len(photoList)):
                photoList[i] = photoList[i].replace("small", "large")
            skus = []

            data = {
                "pid": id,
                "index": 1,
                "orderColumn": "",
                "pageSize": 50,
                "sort": ""
            }
            jdata = json.dumps(data)
            sku_url = "https://haiyingshuju.com/wish_2.0/product/detail/sku"
            res = requests.post(sku_url, headers=headers, data=jdata)
            details = json.loads(res.text)
            colors = []
            sizes = []
            for detail in details["data"]:
                if detail["color"] is None:
                    colors.append("null")
                else:
                    colors.append(detail["color"])

                if detail["size"] is None:
                    sizes.append("one size")
                else:
                    sizes.append(detail["size"])

            skus = {
                "colors": colors,
                "sizes": sizes
            }

            pro = {
                "title": title,
                "tags": tags,
                "photoList": photoList,
                "skus": skus,
                "description": description,
                "id": id
            }

            return pro
        except:
            print("{} ID不存在".format(id))
            return None
