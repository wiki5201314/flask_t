import re
import pandas

try:
    content = ""
    with open("../excel/brands.txt", "r") as f:
        content = f.read()

    brands = re.findall("_(.*)_logo", content)
    print(brands)
    csv_data = []
    for brand in brands:
        csv_data.append(brand)
    csv_pa = pandas.DataFrame(csv_data)
    csv_pa.to_csv("../excel/brand_1.csv")
except:
    print("文件不存在")