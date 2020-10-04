import redbubble
import dianxiaomi
import haiying
import json
from data_transfer import DataTransfer

class Collect(object):
    cookies = {"6": ["_ati=3827030866387; _dxm_ad_client_id=A5774E497E2EC06BC2A2DD95DE9985A8E; Hm_lvt_f8001a3f3d9bf5923f780580eb550c0b=1595551107,1595605459,1595635187,1595643593; dxm_i=MjcxNTM3IWFUMHlOekUxTXpjIWFkN2JkYTliYzJiMDJlYjRmNjMwYTg4Nzc0NzA2Nzhh; dxm_t=MTU5NTY0NjAyOCFkRDB4TlRrMU5qUTJNREk0ITJlMmExNDUwYjdjNzY2NjYyYjQ3YjRhMDFlODE2NWQ1; dxm_c=VEI5S2RubU0hWXoxVVFqbExaRzV0VFEhMTIyODQ5MDY3OGY5MjU2OGJjNTE3YjdmNmE3NTNiOGU; dxm_w=Y2FiYmQ3MWYwMDI4N2U0Y2I3YmEyZTE3NDRlYTEzZDUhZHoxallXSmlaRGN4WmpBd01qZzNaVFJqWWpkaVlUSmxNVGMwTkdWaE1UTmtOUSE5YjM4YTc1MWFjOWJmMDFlNDljZWNmZWJjMzJiYmQ2Mg; dxm_s=LuLN0q7_EGzBhsg-tjVuY4lF-8O5AjzGGQVNprtnjBs; Hm_lpvt_f8001a3f3d9bf5923f780580eb550c0b=1595646058; JSESSIONID=9D30905F96F792665BB3ED52DE737958", "386513", "CN"],
               "1": ["_ati=3827030866387; _dxm_ad_client_id=A5774E497E2EC06BC2A2DD95DE9985A8E; Hm_lvt_f8001a3f3d9bf5923f780580eb550c0b=1595521469,1595550308,1595551107,1595605459; dxm_i=MjcxNTMyIWFUMHlOekUxTXpJITYxZDRkMTdmNmQyMWFlMDMxZjk2MjE0MDNhZDg3Y2M3; dxm_t=MTU5NTYwNzQ1NyFkRDB4TlRrMU5qQTNORFUzITY1NmU1NDE5NTE1MmFhZWI0N2MxZDBhMGUyYjNlZjk0; dxm_c=Yk9hT1I0dm0hWXoxaVQyRlBValIyYlEhMDVmZmMyMmIwNmJkNzU0ZjRjNWQwYzBkZTFkNWM3MDY; dxm_w=YWUwOTA0MDQyOTBjMjY3ZWNmZGYyZjQ2M2MzYmEzMWQhZHoxaFpUQTVNRFF3TkRJNU1HTXlOamRsWTJaa1pqSm1ORFl6WXpOaVlUTXhaQSEzMjU5MjM1OWY5MmYyN2YxMjY5ZTExOWRmM2ZiYzI5NQ; dxm_s=SUUhFGqbM6D1JWLxu_27rEhdapbP2vY0Ylqx9Q7un18; Hm_lpvt_f8001a3f3d9bf5923f780580eb550c0b=1595607922; JSESSIONID=235FD01E350556C4C01CE92FA16904BB", "384721", "CN"],
               "5": ["_ati=3827030866387; _dxm_ad_client_id=1780DD676BB0A6874921EB5301B382A4E; Hm_lvt_f8001a3f3d9bf5923f780580eb550c0b=1599266910,1599319476,1599351753,1599440553; dxm_i=MjgzNzE4IWFUMHlPRE0zTVRnITM5NWYyMWUxMGRhNjA3OWEzMjNiY2UyYjgxNTU0NjFl; dxm_t=MTU5OTQ0MjM4MyFkRDB4TlRrNU5EUXlNemd6IWJhZThkMmE1MjZmNGIwODZmNmI5NGEzYjQyZjg2OTcw; dxm_c=QThkRHZkRnkhWXoxQk9HUkVkbVJHZVEhYjVmZjFlY2RkYjM2Yjg5MDM0OGVjMzA5ZWE5MzM0NmM; dxm_w=ZDRjZDZkZDVlODUwZjEyN2U1NGExNzc2NWU2ODlkOGEhZHoxa05HTmtObVJrTldVNE5UQm1NVEkzWlRVMFlURTNOelkxWlRZNE9XUTRZUSEwNDM5NDUyMDEyZTQ3MDgxOThiNjE5OGE0ZTMwYmM3Mw; dxm_s=GQ40G25GonK8BVpbty3M2czMCudq_ZrqOW8Qf3LiPRg; JSESSIONID=25ECAC637CB8C1EA2AC7D034484197DD; Hm_lpvt_f8001a3f3d9bf5923f780580eb550c0b=1599442405", "719351", "CN"],
               "tap": ["_ati=6860750660892; dxm_i=NDc0NTkzIWFUMDBOelExT1RNIThjMWQyYjYzMDUzMTZlNTFlYWNjNmRjNDNkNjBiMTY4; dxm_t=MTU5ODQ4NzU2MCFkRDB4TlRrNE5EZzNOVFl3IWJlYmI3NTE1NzcyODdmNTliMGFjNTdiNDk0YmNiOTA1; dxm_c=VVV5U1NIUm0hWXoxVlZYbFRVMGhTYlEhNTM2OGJhYTEzNDBlMjdmYjJmODFjNjY2NDNlNTM5N2Y; dxm_w=MmEzNmY1YzZkNzMyMGViMTBjMDc5YTYzNGY3OTk3NTQhZHoweVlUTTJaalZqTm1RM016SXdaV0l4TUdNd056bGhOak0wWmpjNU9UYzFOQSE3YTJlZjE4MDRiYzFiN2EyY2M5YmJjODBkOTE4YmI4OQ; dxm_s=sE492owi4k3PFNrI9Wq5G8arSlGj1AbGPT5ybpeJtgA; _dxm_ad_client_id=16CEAEE076E8ED070844AC74DCEE902A8; Hm_lvt_f8001a3f3d9bf5923f780580eb550c0b=1599269796,1599271275,1599320957,1599493048; Hm_lpvt_f8001a3f3d9bf5923f780580eb550c0b=1599493053; JSESSIONID=16553C53E87EBF430A98B8706B6C21BD", "1115130", "CN"],
               "phone": ["_ati=6860750660892; dxm_i=NDc0NTkzIWFUMDBOelExT1RNIThjMWQyYjYzMDUzMTZlNTFlYWNjNmRjNDNkNjBiMTY4; dxm_t=MTU5ODQ4NzU2MCFkRDB4TlRrNE5EZzNOVFl3IWJlYmI3NTE1NzcyODdmNTliMGFjNTdiNDk0YmNiOTA1; dxm_c=VVV5U1NIUm0hWXoxVlZYbFRVMGhTYlEhNTM2OGJhYTEzNDBlMjdmYjJmODFjNjY2NDNlNTM5N2Y; dxm_w=MmEzNmY1YzZkNzMyMGViMTBjMDc5YTYzNGY3OTk3NTQhZHoweVlUTTJaalZqTm1RM016SXdaV0l4TUdNd056bGhOak0wWmpjNU9UYzFOQSE3YTJlZjE4MDRiYzFiN2EyY2M5YmJjODBkOTE4YmI4OQ; dxm_s=sE492owi4k3PFNrI9Wq5G8arSlGj1AbGPT5ybpeJtgA; _dxm_ad_client_id=16CEAEE076E8ED070844AC74DCEE902A8; Hm_lvt_f8001a3f3d9bf5923f780580eb550c0b=1599269796,1599271275,1599320957,1599493048; Hm_lpvt_f8001a3f3d9bf5923f780580eb550c0b=1599493053; JSESSIONID=16553C53E87EBF430A98B8706B6C21BD", "1202284", "CN"],
               "mask": ["_ati=6860750660892; dxm_i=NDc0NTkzIWFUMDBOelExT1RNIThjMWQyYjYzMDUzMTZlNTFlYWNjNmRjNDNkNjBiMTY4; dxm_t=MTU5ODQ4NzU2MCFkRDB4TlRrNE5EZzNOVFl3IWJlYmI3NTE1NzcyODdmNTliMGFjNTdiNDk0YmNiOTA1; dxm_c=VVV5U1NIUm0hWXoxVlZYbFRVMGhTYlEhNTM2OGJhYTEzNDBlMjdmYjJmODFjNjY2NDNlNTM5N2Y; dxm_w=MmEzNmY1YzZkNzMyMGViMTBjMDc5YTYzNGY3OTk3NTQhZHoweVlUTTJaalZqTm1RM016SXdaV0l4TUdNd056bGhOak0wWmpjNU9UYzFOQSE3YTJlZjE4MDRiYzFiN2EyY2M5YmJjODBkOTE4YmI4OQ; dxm_s=sE492owi4k3PFNrI9Wq5G8arSlGj1AbGPT5ybpeJtgA; _dxm_ad_client_id=16CEAEE076E8ED070844AC74DCEE902A8; Hm_lvt_f8001a3f3d9bf5923f780580eb550c0b=1599269796,1599271275,1599320957,1599493048; Hm_lpvt_f8001a3f3d9bf5923f780580eb550c0b=1599493053; JSESSIONID=16553C53E87EBF430A98B8706B6C21BD", "1224414", "CN"],
                "4": ["_ati=3827030866387; _dxm_ad_client_id=1780DD676BB0A6874921EB5301B382A4E; Hm_lvt_f8001a3f3d9bf5923f780580eb550c0b=1599351753,1599440553,1599492174,1599492341; dxm_i=MjcxNTMzIWFUMHlOekUxTXpNIWIxMmZiZmRmNzgwOGExNjdjZDU1ZGZiNThlZmU5ODM2; dxm_t=MTU5OTQ5MzI3OCFkRDB4TlRrNU5Ea3pNamM0ITY4Mjg5MzY5OWYzZTVkNmZmZjIzYWFkYTg0NDg2NTA5; dxm_c=MHJVTkVrdWMhWXowd2NsVk9SV3QxWXchMjYxYjUzYzRmNTk1ZGU3NWYwZGFmNTZlYWI1YzhiZTU; dxm_w=YTY2ZmViMWNjNjA0NGNlN2U0YmQ0NGIyODdhNzBkODMhZHoxaE5qWm1aV0l4WTJNMk1EUTBZMlUzWlRSaVpEUTBZakk0TjJFM01HUTRNdyE4M2QxNDk0ZDg3ZTM4NmJiODJjM2M0YmFiMTI4N2VkOA; dxm_s=JKyuzrK7_sZEkTD818rzj9PLvRHQKTVYMGDOOPY1WKk; Hm_lpvt_f8001a3f3d9bf5923f780580eb550c0b=1599493366; JSESSIONID=D8DB97550B9D492FB751D427B9FA4919", "282935", "CN"],
               "9":["_ati=3827030866387; _dxm_ad_client_id=1780DD676BB0A6874921EB5301B382A4E; dxm_i=MjcxNTM0IWFUMHlOekUxTXpRIWUzYzdhNDdjZTYwNDQ0ODUwNzFlNjAxMDAyZDNlZDAy; dxm_t=MTU5OTUyNzc0NyFkRDB4TlRrNU5USTNOelEzITRkYjllZDA3ODAxNjdiN2RjOWEyOTA3NzM2ZDFjOWI5; dxm_c=UXF4Z25EcUchWXoxUmNYaG5ia1J4UnchNTcwNDZlYmI1NmRjOWJhMWRiNTkzMzI1ZWYzYzhkOGU; dxm_w=NzIyNjg0MjQxZjMzNTk4ZmIwM2VkMjVmZTc4YWZhNDchZHowM01qSTJPRFF5TkRGbU16TTFPVGhtWWpBelpXUXlOV1psTnpoaFptRTBOdyEyMGZhNTcyYTczMDAxNmM1YTFjMzc5ZGQzM2E5MGM4Mw; dxm_s=pLIrGx7fC_pnFI9sZyPvKd9k0t4gpCm4mOstNduuoBs; Hm_lvt_f8001a3f3d9bf5923f780580eb550c0b=1599522487,1599527199,1599530278,1599542700; Hm_lpvt_f8001a3f3d9bf5923f780580eb550c0b=1599542862; JSESSIONID=550A01719E3695C69A3BC197BEA17678", "448049", "CN"],
               "8":["_ati=3827030866387; _dxm_ad_client_id=1780DD676BB0A6874921EB5301B382A4E; Hm_lvt_f8001a3f3d9bf5923f780580eb550c0b=1599530278,1599542700,1599578861,1599615021; dxm_i=MjcxNTM1IWFUMHlOekUxTXpVIWM5YmNmYzRlNDI2ZjdmYjNkNjkyYjJmNDFkYjE0OGM1; dxm_t=MTU5OTYxNzE1NiFkRDB4TlRrNU5qRTNNVFUyITA5YTMxZjMwN2Y1YzJlMDlmZmI5MTgzYWEzYzcyNTA4; dxm_c=dW5tT0tnYkYhWXoxMWJtMVBTMmRpUmchNDI2ZGQxZTM2ZGI4NGY0NjYxZGUxNWQ3NjM3OTJjMjU; dxm_w=MGEwYWVjNDFkYWJjZDkxZGIwNjc3NTU2ZTIwNmFhNWYhZHowd1lUQmhaV00wTVdSaFltTmtPVEZrWWpBMk56YzFOVFpsTWpBMllXRTFaZyFkMWQ4YmE2NTFhZTQ2NWY0MWYwY2YzNGRjYjI5MDEzNg; dxm_s=VaaHymXWc3oTSs5ywjhvmVd5ZOYdIXO99QcOgK2Iv5w; Hm_lpvt_f8001a3f3d9bf5923f780580eb550c0b=1599617166; JSESSIONID=114145350A46721F3D0E525D2F611B37", "312722", "CN"]
               }

    def __init__(self, sock, ch, data, merchants, brands):
        self._sock = sock
        self._ch = ch
        self._data = data
        self._merchants = merchants.split(",")
        self._brands = brands

    def red_to_wish(self):
        rb = redbubble.RedBubble(self._data[0], category=int(self._ch))
        if rb.get_products() is not None:
            rb.up_down_images(self._sock)
            pcs = []
            for merchant in self._merchants:
                pcs.append(dianxiaomi.UploadNew(Collect.cookies[merchant][0], Collect.cookies[merchant][1], rb, Collect.cookies[merchant][2]))

            for pc in pcs:
                pc.create_products(self._sock, self._brands)

    def id_to_wish(self):
        uws = []
        for merchant in self._merchants:
            uws.append(dianxiaomi.UploadWish(Collect.cookies[merchant][0], Collect.cookies[merchant][1], Collect.cookies[merchant][2]))
        self._sock.send(json.dumps({"msg": "店小秘登录成功", "percent": 0}))
        try:
            hy = haiying.Haiying()
            self._sock.send(json.dumps({"msg": "海鹰数据登录成功", "percent": 0}))

            for index, id in enumerate(self._data):
                print(id)
                detail = hy.get_detail(id.split()[0])
                if detail is not None:
                    self._sock.send(json.dumps({"msg": "正在处理 " + id, "percent": index / len(self._data) * 100}))
                    if len(id.split()) == 1:
                        detail["price"] = "1"
                    else:
                        detail["price"] = id.split()[1]

                    for uw in uws:
                        uw.upload(detail)
                else:
                    self._sock.send(json.dumps({"msg": "id失效" + id, "percent": index / len(self._data) * 100}))

        except EOFError:
            print("文件不存在")

    def id_to_ali(self):
        try:
            hy = haiying.Haiying()
            self._sock.send(json.dumps({"msg": "海鹰数据登录成功", "percent": 0}))

            details = []

            for index, id in enumerate(self._data):
                detail = hy.get_detail(id.split()[0])
                if detail is not None:
                    self._sock.send(json.dumps({"msg": "正在处理 " + id, "percent": (index + 1) / len(self._data) * 90}))
                    details.append(detail)
                else:
                    self._sock.send(json.dumps({"msg": "id失效" + id, "percent": (index + 1) / len(self._data) * 90}))

            self._sock.send(json.dumps({"msg": "开始创建文件", "percent": 95}))
            file = DataTransfer.data_to_csv(details, self._merchants[0], self._merchants[1])

            if file is not None:
                self._sock.send(json.dumps({"msg": "文件生成成功", "percent": 100}))
                self._sock.send(json.dumps({"msg": file, "percent": 100}))
            else:
                self._sock.send(json.dumps({"msg": "文件生成失败", "percent": 100}))

        except EOFError:
            print("文件不存在")

    def red_to_ali(self):
        self._sock.send(json.dumps({"msg": "开始采集", "percent": 0}))
        rb = redbubble.RedBubble(int(self._data[0]), "trending")
        if rb.get_products() is not None:
            rb.up_down_images(self._sock)
            self._sock.send(json.dumps({"msg": "开始创建文件", "percent": 95}))
            file = DataTransfer.red_to_csv(rb.titles, self._merchants[0], self._merchants[1])

            if file is not None:
                self._sock.send(json.dumps({"msg": "文件生成成功", "percent": 100}))
                self._sock.send(json.dumps({"msg": file, "percent": 100}))
            else:
                self._sock.send(json.dumps({"msg": "文件生成失败", "percent": 100}))

    def execute(self):
        if self._ch == "0":
            self.id_to_wish()
        elif 1 <= int(self._ch) <= 7:
            self.red_to_wish()
        elif self._ch == "100":
            self.id_to_ali()
        elif self._ch == "101":
            self.red_to_ali()


