import requests
from lxml import etree
import Qiniu
import time
import datetime
import json
import random


# 点小米实现上传功能
class Dianxiaomi(object):
	def __init__(self, cookies_str, merchant_id):
		url = "https://www.dianxiaomi.com/home.htm"
		self._cookies = dict(map(lambda x: x.split('='), cookies_str.split(";")))
		self._session = requests.session()
		self._merchant_id = merchant_id
		try:
			res = self._session.get(url, cookies = self._cookies)
			tree = etree.HTML(res.content)
			name = tree.xpath('/html/body/div[2]/div[3]/div/div[1]/div[2]/text()')
			if len(name[0]) > 0:
				print("店小密登陆成功， 姓名{}".format(name[0]))
				self._name = name[0]
			else:
				print("店小密登录失败，请检查")
				self._cookies = None
		except ConnectionError:
			print("店小密登录失败，请检查")
			self._cookies = None

	@property
	def merchant_id(self):
		return self._merchant_id

	@merchant_id.setter
	def merchant_id(self, merchant_id):
		self._merchant_id = merchant_id

	def __str__(self):
		return self._name

	def close_pb(self, times):
		if self._cookies is None:
			return 0

		# 重试次数
		if times > 10:
			return 0

		detail = {'shopId': self._merchant_id}
		try:
			url = "https://www.dianxiaomi.com/wishProductBoost/syncListCampaigns.json"
			header = {
				"Accept": "application/json, text/javascript, */*; q=0.01",
				"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
				"X-Requested-With": "XMLHttpRequest"
			}

			res = self._session.post(url, data=detail, headers=header, cookies=self._cookies)
			if res.status_code == 200:
				print("正在同步....")
				time.sleep(3)
				uuid = json.loads(res.content)
				url = "https://www.dianxiaomi.com/checkProcess.json"
				res = self._session.post(url, data=uuid, headers=header, cookies=self._cookies)
				syn = 1
				print(res.text)
				find = res.text.find("同步完成")
				while ((find < 0) and (syn < 4)) :
					print("同步未完成，等待同步...")
					time.sleep(3)
					res = self._session.post(url, data=uuid, headers=header, cookies=self._cookies)
					find = res.text.find("同步完成")
					syn += 1
				print("同步完成")
			else:
				print("链接店小秘出错，重试...")
				return self.close_pb(times + 1)
		except ConnectionError:
			print("链接店小秘出错，重试...")
			return self.close_pb(times + 1)

		url = "https://www.dianxiaomi.com/wishProductBoost/pageList.htm"
		detail["pageNo"] = "1"
		detail["pageSize"] = "100"
		detail["hasLowBudget"] = "0"
		detail["searchType"] = "0"
		detail["sortName"] = "9"
		detail["sortValue"] = "0"
		detail["state"] = "STARTED"
		# detail["state"] = "NEW"
		try:
			res = self._session.post(url, data=detail, cookies=self._cookies)
			if res.status_code == 200:
				tree = etree.HTML(res.content)
				pb_ids = tree.xpath("/html/body/table/tbody/tr[1]/td[13]/div/ul/li[4]/a/@onclick")
				if len(pb_ids) < 1:
					print("没有需要关闭的PB，请等待")
					time.sleep(3)
					return self.close_pb(times + 1)
				else:
					pb_id = pb_ids[0].lstrip("stopCampaign('").rstrip("');")
					print(pb_id)
					data = {"idStr": pb_id}
					header = {
						"Accept": "application/json, text/javascript, */*; q=0.01",
						"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
						"X-Requested-With": "XMLHttpRequest"
					}
					url = "https://www.dianxiaomi.com/wishProductBoost/stopCampaign.json"
					res = self._session.post(url, data=data, headers=header, cookies=self._cookies)
					if res.status_code == 200:
						print(res.text)
						if res.text.find('"code":0') != -1:
							print("取消成功")
						else:
							print("取消失败")
					else:
						print("取消失败")
			else:
				print("链接店小秘出错，重试...")
				return self.close_pb(times + 1)
		except ConnectionError:
			print("链接店小秘出错，重试...")
			return self.close_pb(times + 1)

	# 获取需要取消的A+
	def get_a_plus_order(self, wish_id):
		if self._cookies is None:
			return 0

		url = "https://www.dianxiaomi.com/package/list.htm?pageNo=1&pageSize=300&shopId=" + self._merchant_id +"&state=approved&platform=&isSearch=0&searchType=orderId&authId=-1&startTime=&endTime=&country=CN&orderField=order_pay_time&isVoided=0&isRemoved=0&ruleId=-1&sysRule=&applyType=&applyStatus=&printJh=-1&printMd=-1&commitPlatform=&productStatus=&jhComment=-1&storageId=0&isOversea=-1&isFree=0&isBatch=0&history=&custom=-1&timeOut=0&refundStatus=0&buyerAccount=&forbiddenStatus=-1&forbiddenReason=0&behindTrack=-1&orderId="
		try:
			res = self._session.get(url, cookies=self._cookies)
			print(res)
			tree = etree.HTML(res.text)
			order_ids = tree.xpath('//*[@id="orderListTable"]/tbody/tr/td[4]/a/text()')
			order_id_str = ",".join(order_ids)

			#  运单号申请
			package_ids = tree.xpath('//*[@id="orderListTable"]/tbody/tr/td[1]/input[1]/@value')
			for package_id in package_ids:
				url = "https://www.dianxiaomi.com/package/moveProcessed.json"
				headers = {
					"Accept": "application/json, text/javascript, */*; q=0.01",
					"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
					"Origin": "https://www.dianxiaomi.com",
					"Host": "www.dianxiaomi.com",
					"Referer": "https://www.dianxiaomi.com/order/index.htm",
					"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
					"X-Requested-With": "XMLHttpRequest"
				}

				data = {
					"packageId": package_id
				}
				res = self._session.post(url, data=data, headers=headers, cookies=self._cookies)

			return order_id_str
		except ConnectionError:
			print("链接店小秘出错，重试...")
			return None

	# 获得失败的列表
	def get_failed_tracking(self, wp):
		if self._cookies is None:
			return 0

		url = "https://www.dianxiaomi.com/package/list.htm?pageNo=1&pageSize=100&shopId=-1&state=processed&platform=&isSearch=0&searchType=orderId&authId=-1&startTime=&endTime=&country=&orderField=order_pay_time&isVoided=0&isRemoved=0&ruleId=-1&sysRule=&applyType=&applyStatus=fail&printJh=-1&printMd=-1&commitPlatform=&productStatus=&jhComment=-1&storageId=0&isOversea=-1&isFree=0&isBatch=0&history=&custom=-1&timeOut=0&refundStatus=0&buyerAccount=&forbiddenStatus=-1&forbiddenReason=0&behindTrack=-1&orderId="
		try:
			res = self._session.get(url, cookies=self._cookies)
			tree = etree.HTML(res.text)
			states = tree.xpath('//*[@id="orderListTable"]/tbody/tr/td[6]/p[1]/span[2]/span[1]/text()')
			order_id = tree.xpath('//*[@id="orderListTable"]/tbody/tr/td[4]/a/text()')
			if len(states) > 0:
				for i in range(len(states)):
					# 需要后台取消
					print(states[i])
					if states[i].find("其他真实有效") != -1:
						print("需要取消的订单是{}".format(order_id[i]))
						if(wp.close(order_id[i]) < 0):
							print("订单{}取消失败".format(order_id[i]))
						else:
							print("订单{}取消成功".format(order_id[i]))
				print("全部订单取消完成")
		except ConnectionError:
			print("链接店小秘出错，重试...")
			return 0

	def get_all_tracking(self):
		if self._cookies is None:
			return 0

		url = "https://www.dianxiaomi.com/order/batchReApply.json"
		headers = {
			"Accept": "application/json, text/javascript, */*; q=0.01",
			"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
		}
		data = {
			"type": "0",
		}
		try:
			res = self._session.post(url, data=data, headers=headers, cookies=self._cookies)
			if res.status_code == 200:
				print(res.text)
				return 1

		except ConnectionError:
			return 0


# wish上传wish
class UploadWish(Dianxiaomi):
	def __init__(self, cookies_str, merchant_id, localized = "US"):
		super().__init__(cookies_str, merchant_id)
		self._localized = localized
		self._sku = None
		self._title = None
		self._merchant_id = merchant_id

	def upload(self, detail):
		colors = detail["skus"]["colors"]
		sizes = detail["skus"]["sizes"]
		parentSku = "cw" + datetime.datetime.now().strftime('%d-%H%M%S') + "".join(random.sample('zyxwvutsrqponmlkjihgfedcba', 5))

		if len(sizes) == 0:
			sizes = ["one size"]

		if len(colors) == 0:
			colors = ["null"]


		# 1+1库存按照SKU分配
		goodsNum_1 = "100"

		# 添加1+1抢流量SKU
		tmp1 = []
		tmp2 = []
		for size in sizes:
			tmp1.append(size + ".")
			tmp2.append("." + size + ".")

		tmp2.extend(tmp1)
		tmp2.extend(sizes)
		sizes = tmp2

		tmp = colors
		colors.extend(tmp)
		colors.extend(tmp)

		# 拼接sku
		size_ran = "".join(random.sample('zyxwvutsrqponmlkjihgfedcba', 2))
		if colors[0] == "null":
			sku_str = [parentSku + "-" + i[:20] + size_ran for i in sizes]
		else:
			sku_str = [parentSku + "-" + sizes[i][:20] + size_ran + "-" + colors[i] for i in range(len(sizes))]

		product_detail = {
			"shopIds": self._merchant_id,
			"parentSku": parentSku,
			"name": detail["title"],
			"description": detail["description"],
			"tags": detail["tags"],
			"brand": "",
			"upc": "",
			"maxQuantity": "",
			"landingPageUrl": "",
			"cleanImage": "",
			"sizeCategory": "Custom",
			"inventory": "9999",
			"shippingTime": "7-14",
			"op": "1",
			"msrp": "4",
			"shipping": "0.0",
			"localizedShipping": "0.0",
			"price": "4",
			"localizedPrice": "4",
			"mainImage": detail["photoList"][0],
			"extraImages": "|".join(detail["photoList"][1:]),
			"skuStr": "&-&".join(sku_str),
			"sizeStr": "&-&".join([i for i in sizes]),
			"imageStr": "&-&".join(["null" for i in sizes]),
			"colorStr": "&-&".join([i for i in colors]),
			"priceStr": "&-&".join(detail["price"] for i in range(int(len(sizes) / 3))) + "&-&" + "&-&".join(str(int(detail["price"]) + 1) + ".0" for i in range(int(len(sizes) / 3))) + "&-&" + "&-&".join(str(int(detail["price"]) + 2) + ".0" for i in range(int(len(sizes) / 3))),
			"localizedPriceStr": "&-&".join(detail["price"] for i in range(int(len(sizes) / 3))) + "&-&" + "&-&".join(str(int(detail["price"]) + 1) + ".0" for i in range(int(len(sizes) / 3))) + "&-&" + "&-&".join(str(int(detail["price"]) + 2) + ".0" for i in range(int(len(sizes) / 3))),
			"msrpStr": "&-&".join("4.0" for i in range(len(sizes))),
			"goodsNumStr": "&-&".join("6" for i in range(int(len(sizes) / 3))) + "&-&" + "&-&".join(goodsNum_1 for i in range(int(len(sizes) / 3))) + "&-&" + "&-&".join("9999" for i in range(int(len(sizes) / 3))),
			"sTimeStr": "&-&".join("7" for i in range(len(sizes))),
			"bTimeStr": "&-&".join("14" for i in range(len(sizes))),
			"dxmScheduleTimeStr": "",
			"sourceUrl": "https://haiyingshuju.com/wish/index.html#/index/goods_details?pid=" + detail["id"],
			"productShipping": "",
		}
		if self._localized == "CN":
			product_detail["localizedShipping"] = product_detail["localizedShipping"].replace("1.0", "7")
			product_detail["localizedPrice"] = "28"
			product_detail["localizedPriceStr"] = "&-&".join(str((int(detail["price"])) * 7) for i in range(int(len(sizes) / 3))) + "&-&" + "&-&".join(str((int(detail["price"]) + 1) * 7) + ".0" for i in range(int(len(sizes) / 3))) + "&-&" + "&-&".join(str((int(detail["price"]) + 2) * 7) + ".0" for i in range(int(len(sizes) / 3)))

		print(product_detail["localizedPriceStr"])
		print(product_detail["goodsNumStr"])
		print(product_detail["skuStr"])

		url = "https://www.dianxiaomi.com/product/add.json"
		header = {
			"Accept": "application/json, text/javascript, */*; q=0.01",
			"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
			"X-Requested-With": "XMLHttpRequest",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Site": "same-origin",
			"Referer": "https://www.dianxiaomi.com/product/add.htm",
			"Pragma": "no-cache",
			"Origin": "https://www.dianxiaomi.com",
			"Host": "www.dianxiaomi.com"
		}
		try:
			res = self._session.post(url, data=product_detail, headers=header, cookies=self._cookies)
			print(res.text)
			code = res.status_code
			if code == 200:
				print("{} 创建完毕".format(detail["id"]))
				return 1
			else:
				print("{} 创建失败".format(detail["id"]))
				return 0
		except ConnectionError:
			print("店小密登录失败，请检查")
			return 0

# wish上传挂毯和手机壳
class UploadNew(Dianxiaomi):
	def __init__(self, cookies_str, merchant_id, content, localized = "US"):
		super().__init__(cookies_str, merchant_id)
		self._localized = localized
		self._content = content
		self._sku = None
		self._title = None

		# 公共部分
		self._product_detail = {
			"shopIds": merchant_id,
			"brand": "",
			"upc": "",
			"maxQuantity": "",
			"landingPageUrl": "",
			"cleanImage": "",
			"sizeCategory": "Custom",
			"inventory": "9999",
			"shippingTime": "7-14",
			"op": "1",
			"dxmScheduleTimeStr": "",
			"productShipping": ""
		}

		# 手机壳
		if content.category == 1:
			self.init_phone()
		elif content.category == 2:
			self.init_tap()
		elif content.category == 3:
			self.init_mask()
		elif content.category == 4:
			self.init_curtain()
		elif content.category == 5:
			self.init_pin()
		elif content.category == 6:
			self.init_throw_pillow()
		elif content.category == 7:
			self.init_floor_pillow()

	def init_throw_pillow(self):
		self._product_detail["msrp"] = "4.0"
		self._product_detail["shipping"] = "1.0"
		self._product_detail["localizedShipping"] = "1.0"
		self._product_detail["price"] = "3"
		self._product_detail["localizedPrice"] = "3"

		sizeStr = "one size.&-&one size"
		sizes = sizeStr.split("&-&")

		self._product_detail[
			"description"] = "Soft Decorative Throw Pillow Cover for Home 45cmX45cm(18inchX18inch) Pillows NOT Included"
		self._product_detail[
			"tags"] = "case, Home & Kitchen, Home Decor, Classical, sofacushioncover, Home & Living, Sofas, squarepillow, Cover"
		self._product_detail["imageStr"] = "&-&".join(["null"] * len(sizes))
		self._product_detail["sizeStr"] = sizeStr
		self._product_detail["colorStr"] = "&-&".join(["null"] * len(sizes))
		self._product_detail["priceStr"] = "2.0&-&3.0"
		self._product_detail["localizedPriceStr"] = "2.0&-&3.0"
		self._product_detail["msrpStr"] = "&-&".join(["4.0"] * len(sizes))
		self._product_detail["goodsNumStr"] = "30&-&9999"
		self._product_detail["sTimeStr"] = "&-&".join(["7"] * len(sizes))
		self._product_detail["bTimeStr"] = "&-&".join(["14"] * len(sizes))

		if self._localized == "CN":
			self._product_detail["localizedShipping"] = "7"
			self._product_detail["localizedPrice"] = "21"
			self._product_detail["localizedPriceStr"] = "14&-&21"

		self._sku = " Pin"
		self._title = " Soft Decorative Throw Pillow Cover for Home 45cmX45cm(18inchX18inch) Pillows NOT Included"

	def init_floor_pillow(self):
		self._product_detail["msrp"] = "14.0"
		self._product_detail["shipping"] = "3.0"
		self._product_detail["localizedShipping"] = "3.0"
		self._product_detail["price"] = "3"
		self._product_detail["localizedPrice"] = "3"

		sizeStr = "one size.&-&one size"
		sizes = sizeStr.split("&-&")

		self._product_detail[
			"description"] = "100cmX100cm(36inchX36inch) Large Fashion Floor Pillow Case Cover Sleepover and Parties, Pillows NOT Included"
		self._product_detail[
			"tags"] = "case, Home & Kitchen, Home Decor, Classical, sofacushioncover, Home & Living, Sofas, squarepillow, Cover"
		self._product_detail["imageStr"] = "&-&".join(["null"] * len(sizes))
		self._product_detail["sizeStr"] = sizeStr
		self._product_detail["colorStr"] = "&-&".join(["null"] * len(sizes))
		self._product_detail["priceStr"] = "9&-&10.0"
		self._product_detail["localizedPriceStr"] = "9.0&-&10.0"
		self._product_detail["msrpStr"] = "&-&".join(["4.0"] * len(sizes))
		self._product_detail["goodsNumStr"] = "30&-&9999"
		self._product_detail["sTimeStr"] = "&-&".join(["7"] * len(sizes))
		self._product_detail["bTimeStr"] = "&-&".join(["14"] * len(sizes))

		if self._localized == "CN":
			self._product_detail["localizedShipping"] = "21"
			self._product_detail["localizedPrice"] = "98"
			self._product_detail["localizedPriceStr"] = "63&-&70"

		self._sku = " Pin"
		self._title = " 100cmX100cm(36inchX36inch) Large Fashion Floor Pillow Case Cover Sleepover and Parties, Pillows NOT Included"

	def init_pin(self):
		self._product_detail["msrp"] = "4.0"
		self._product_detail["shipping"] = "1.0"
		self._product_detail["localizedShipping"] = "1.0"
		self._product_detail["price"] = "3"
		self._product_detail["localizedPrice"] = "3"

		sizeStr = "25mmx25mm&-&38mmx38mm"
		sizes = sizeStr.split("&-&")

		self._product_detail[
			"description"] = "Round pinback buttons for instant awesome, just about anywhere"
		self._product_detail[
			"tags"] = "hatpin, Fashion, Jewelry, Pins, harrypotterjewelry, Denim, harrypotterpin, enamelpin"
		self._product_detail["imageStr"] = "&-&".join(["null"] * len(sizes))
		self._product_detail["sizeStr"] = sizeStr
		self._product_detail["colorStr"] = "&-&".join(["null"] * len(sizes))
		self._product_detail["priceStr"] = "2.0&-&3.0"
		self._product_detail["localizedPriceStr"] = "2.0&-&3.0"
		self._product_detail["msrpStr"] = "&-&".join(["4.0"] * len(sizes))
		self._product_detail["goodsNumStr"] = "30&-&9999"
		self._product_detail["sTimeStr"] = "&-&".join(["7"] * len(sizes))
		self._product_detail["bTimeStr"] = "&-&".join(["14"] * len(sizes))

		if self._localized == "CN":
			self._product_detail["localizedShipping"] = "7"
			self._product_detail["localizedPrice"] = "21"
			self._product_detail["localizedPriceStr"] = "14&-&21"

		self._sku = " Pin"
		self._title = " Brooches Cartoon Creative Brooch Pins"

	def init_mask(self):
		self._product_detail["msrp"] = "4.0"
		self._product_detail["shipping"] = "1.0"
		self._product_detail["localizedShipping"] = "1.0"
		self._product_detail["price"] = "3"
		self._product_detail["localizedPrice"] = "3"

		sizeStr = "one size.&-&one size"
		sizes = sizeStr.split("&-&")

		self._product_detail[
			"description"] = "Cute Cartoon Face Cover Unisex Outdoor Sport Protective"
		self._product_detail[
			"tags"] = "cute, Fashion, bandana, hazeproof, Warm, icesilk, dustproof, expression, Cartoons, Cotton"
		self._product_detail["imageStr"] = "&-&".join(["null"] * len(sizes))
		self._product_detail["sizeStr"] = sizeStr
		self._product_detail["colorStr"] = "&-&".join(["null"] * len(sizes))
		self._product_detail["priceStr"] = "2.0&-&3.0"
		self._product_detail["localizedPriceStr"] = "2.0&-&3.0"
		self._product_detail["msrpStr"] = "&-&".join(["4.0"] * len(sizes))
		self._product_detail["goodsNumStr"] = "30&-&9999"
		self._product_detail["sTimeStr"] = "&-&".join(["7"] * len(sizes))
		self._product_detail["bTimeStr"] = "&-&".join(["14"] * len(sizes))

		if self._localized == "CN":
			self._product_detail["localizedShipping"] = "7"
			self._product_detail["localizedPrice"] = "21"
			self._product_detail["localizedPriceStr"] = "14&-&21"

		self._sku = " Cover"
		self._title = " Cute Cartoon Face Cover Unisex Outdoor Sport Protective"

	def init_curtain(self):
		self._product_detail["msrp"] = "16.0"
		self._product_detail["shipping"] = "3.0"
		self._product_detail["localizedShipping"] = "3.0"
		self._product_detail["price"] = "6.9"
		self._product_detail["localizedPrice"] = "6.9"

		sizeStr = "80x180cm&-&180x120cm&-&200x150cm"
		sizes = sizeStr.split("&-&")

		self._product_detail["description"] = "Bathroom Print Mildew-proof Waterproof Shower Curtain"
		self._product_detail[
			"tags"] = "doormat, Polyester, Floor Mats, bathroomcurtain, Shower Curtains, pedestalrug, Cover, Rugs, toiletseatcover, Shower"
		self._product_detail["imageStr"] = "&-&".join(["null"] * len(sizes))
		self._product_detail["sizeStr"] = sizeStr
		self._product_detail["colorStr"] = "&-&".join(["null"] * len(sizes))
		self._product_detail["priceStr"] = "6.9&-&12.0&-&16.0"
		self._product_detail["localizedPriceStr"] = "6.9&-&12.0&-&16.0"
		self._product_detail["msrpStr"] = "&-&".join(["16.0"] * len(sizes))
		self._product_detail["goodsNumStr"] = "&-&".join(["9999"] * len(sizes))
		self._product_detail["sTimeStr"] = "&-&".join(["7"] * len(sizes))
		self._product_detail["bTimeStr"] = "&-&".join(["14"] * len(sizes))

		if self._localized == "CN":
			self._product_detail["localizedShipping"] = "21.21"
			self._product_detail["localizedPrice"] = "48.78"
			self._product_detail["localizedPriceStr"] = "48.78&-&84.84&-&113.12"

		self._sku = " Curtain"
		self._title = " Bathroom Print Mildew-proof Waterproof Shower Curtain"

	def init_tap(self):
		self._product_detail["msrp"] = "16.0"
		self._product_detail["shipping"] = "2.0"
		self._product_detail["localizedShipping"] = "2.0"
		self._product_detail["price"] = "6"
		self._product_detail["localizedPrice"] = "6"

		sizeStr = "93x75cm&-&150x130cm&-&200x150cm"
		sizes = sizeStr.split("&-&")

		self._product_detail["description"] = "Fashion Room Decor Pattern Tapestry Multicolored Mandala Printed Tapestry Indian Boho Wall Bedroom Carpet Bed Sheets"
		self._product_detail[
			"tags"] = "decoration, Fashion, Wall Art, takeablanket, comfortersduvet, wallhanging, Home & Kitchen, Home & Living"
		self._product_detail["imageStr"] = "&-&".join(["null"] * len(sizes))
		self._product_detail["sizeStr"] = sizeStr
		self._product_detail["colorStr"] = "&-&".join(["null"] * len(sizes))
		self._product_detail["priceStr"] = "5.0&-&10.0&-&14.0"
		self._product_detail["localizedPriceStr"] = "5.0&-&10.0&-&14.0"
		self._product_detail["msrpStr"] = "&-&".join(["16.0"] * len(sizes))
		self._product_detail["goodsNumStr"] = "&-&".join(["9999"] * len(sizes))
		self._product_detail["sTimeStr"] = "&-&".join(["7"] * len(sizes))
		self._product_detail["bTimeStr"] = "&-&".join(["14"] * len(sizes))

		if self._localized == "CN":
			self._product_detail["localizedShipping"] = "14"
			self._product_detail["localizedPrice"] = "42"
			self._product_detail["localizedPriceStr"] = "35&-&70&-&98"

		self._sku = " Tapestry"
		self._title = " Fashion Room Decor Pattern Tapestry Multicolored Mandala Printed Tapestry Indian Boho Wall Bedroom Carpet Bed Sheets"

	def init_phone(self):
		self._product_detail["msrp"] = "3.0"
		self._product_detail["shipping"] = "1.0"
		self._product_detail["localizedShipping"] = "1.0"
		self._product_detail["price"] = "2.0"
		self._product_detail["localizedPrice"] = "2.0"

		sizeStr = "iphone 5&-&iphone 6/6s&-&iphone 6/6s plus&-&iphone 7&-&iphone 7 plus&-&iphone 8&-&iphone 8 plus&-&iphone X&-&iphone XS&-&iphone XR&-&iphone XS MAX&-&iphone 11&-&iphone 11 pro&-&iphone 11 pro max&-&Samsung S10&-&Samsung S9 Plus&-&Samsung S8&-&Samsung S6&-&Samsung S8 Plus&-&Samsung S9&-&Samsung S10 Plus&-&Samsung S11&-&Samsung S11 Plus&-&Samsung NOTE9&-&Samsung NOTE10&-&HUAWEI MATE 7&-&HUAWEI MATE 7s&-&HUAWEI MATE 8&-&HUAWEI MATE9&-&HUAWEI MATE PRO&-&HUAWEI MATE10&-&HUAWEI MATE10 PRO&-&HUAWEI mate 20&-&HUAWEI Mate 20 Pro&-&HUAWEI Mate 20x&-&HUAWEI Mate 30&-&HUAWEI Mate 30 pro&-&Nova&-&Nova 2&-&Nova 2i&-&Nova 2S&-&Nova 2 Plus&-&Nova 3&-&Nova 3i&-&Nova 3E&-&Nova 4&-&Nova 5&-&Nova 5i&-&Nova 5i Pro&-&P8&-&P9&-&P10&-&P9 Plus&-&P20&-&P20 Pro&-&P30 Pro&-&P30&-&P40&-&P40 Pro"
		sizes = sizeStr.split("&-&")

		self._product_detail["description"] = "PC Perfect realization full protect PC Material phone case"
		self._product_detail[
			"tags"] = "iphone8pluscase, Samsung, iphone 6, iphone7, Iphone 4, Shockproof, Mobile, Luxury, iphone8case, iphone"
		self._product_detail["imageStr"] = "&-&".join(["null"] * len(sizes))
		self._product_detail["sizeStr"] = sizeStr
		self._product_detail["colorStr"] = "&-&".join(["null"] * len(sizes))
		self._product_detail["priceStr"] = "2.0&-&" + "&-&".join(["3.0"] * (len(sizes) - 1))
		self._product_detail["localizedPriceStr"] = "2.0&-&" + "&-&".join(["3.0"] * (len(sizes) - 1))
		self._product_detail["msrpStr"] = "&-&".join(["3.0"] * len(sizes))
		self._product_detail["goodsNumStr"] = "&-&".join(["9999"] * len(sizes))
		self._product_detail["sTimeStr"] = "&-&".join(["7"] * len(sizes))
		self._product_detail["bTimeStr"] = "&-&".join(["14"] * len(sizes))

		if self._localized == "CN":
			self._product_detail["localizedShipping"] = "7.07"
			self._product_detail["localizedPrice"] = "14.06"
			self._product_detail["localizedPriceStr"] = "14.14&-&" + "&-&".join(["21.21"] * (len(sizes) - 1))

		self._sku = " Case"
		self._title = " phone case for iPhone 6/6s/Plus/6s Plus/iPhone 7/7 Plus and Samsung Galaxy S7/S7 Edge Coque iPhone 6S Funda iPhone 6s Plus"

	def test(self):
		url = "https://www.dianxiaomi.com/product/getCountryTemplate.json"
		header = {
			"Accept": "application/json, text/javascript, */*; q=0.01",
			"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
			"X-Requested-With": "XMLHttpRequest",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Site": "same-origin",
			"Referer": "https://www.dianxiaomi.com/product/add.htm",
			"Pragma": "no-cache",
			"Origin": "https://www.dianxiaomi.com",
			"Host": "www.dianxiaomi.com"
		}

		data = {
			"shopId": self.merchant_id
		}
		print(data)
		res = requests.post(url, data=data, headers=header, cookies=self._cookies)
		print(res.text)

	def create_products(self, sock, brands):
		titles = self._content.titles
		for i, title in enumerate(titles):
			set = 1
			for brand in brands:
				if brand.brand_name.lower() in title.lower():
					sock.send(
						json.dumps({"msg": "第{}个产品检测到仿品{}".format(str(i + 1), brand), "percent": i / len(titles) / 2 * 100 + 50}))
					set = 0
					break
			sock.send(json.dumps({"msg": "正在上传第{}个产品".format(str(i + 1)), "percent": i / len(titles) / 2 * 100 + 50}))
			if set == 1:
				if self.create_product_per(title) == 0:
					return 0

		print("全部创建完毕")
		return 1

	def create_product_per(self, product):
		print("开始创建产品")
		if self._cookies is not None:
			detail = self._product_detail
			detail["parentSku"] = product + self._sku
			detail["name"] = product + self._title
			detail["mainImage"] = Qiniu.Qiniu.QiniuUrl + product + ".jpg"
			detail["sourceUrl"] = Qiniu.Qiniu.QiniuUrl + product + " original.jpg"
			if detail["sizeStr"] != "":
				detail["skuStr"] = product + "-" + detail["sizeStr"].replace("&-&", "&-&" + product + "-")
			else:
				detail["skuStr"] = ""

			url = "https://www.dianxiaomi.com/product/add.json"
			header = {
				"Accept": "application/json, text/javascript, */*; q=0.01",
				"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
				"X-Requested-With": "XMLHttpRequest",
				"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
				"Referer": "https://www.dianxiaomi.com/product/add.htm",
				"Pragma": "no-cache",
				"Origin": "https://www.dianxiaomi.com",
				"Host": "www.dianxiaomi.com"
			}
			try:
				code = 1
				while code != 200:
					if code == 1:
						print("开始创建{}".format(product))
					else:
						print("创建失败{}，稍等继续。".format(product))
						print(code)
						time.sleep(10)
						print("休息完毕，开始创建{}".format(product))

					res = self._session.post(url, data=detail, headers=header, cookies=self._cookies)
					print(res.text)
					code = res.status_code

				print("创建完毕")

			except ConnectionError:
				print("店小密登录失败，请检查")
				return 0

		else:
			print("店小密创建产品失败，请检查")
			return 0

		return 1
