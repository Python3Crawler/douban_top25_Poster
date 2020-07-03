import os
from PIL import Image
import requests
from pyquery import PyQuery as pq


url = 'https://movie.douban.com/top250?start={}&filter='
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}


def get_one_page(url):
    """获取单个网页"""
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except:
        print("爬取失败")


def parse_page(html):
    """解析单个网页内容"""
    doc = pq(html)
    links = doc('div.pic > a > img')
    for link in links.items():
        image_url = link.attr['src']
        yield image_url


def get_image(image_url):
    """获取图片二进制内容"""
    try:
        response = requests.get(image_url, headers=headers)
        if response.status_code == 200:
            return response.content
        return None
    except:
        print("爬取失败")


def save_image(image_url, content):
    """保存文件到目录"""
    try:
        folder = 'images'
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(folder + os.path.sep + image_url.split('/')[-1], 'wb') as f:
            f.write(content)
            print('Done')
    except:
        print(image_url, '写入失败')


def main(pages):
    """遍历循环"""
    for i in range(pages):
        new_url = url.format(i * 25)
        html = get_one_page(new_url)
        for image_url in parse_page(html):
            content = get_image(image_url)
            save_image(image_url, content)


main(10)


# 拼图

files = os.listdir("./images")   # 获得所有图片的文件名列表
row = 25  # 每行的图片数
column = 10
image_width = 170  # 每张图片的宽
image_height = 256  # 每张图片的高
image = Image.new("RGB", (image_width * row, image_height * column))  # 准备空画布
# 记录坐标
x = y = 0
# 循环画图
for i in range(0, 250):        # 这里我假定行列图片数一样，不一样的话可以简单修改
    img = Image.open("./images/" + files[i])
    img = img.resize((image_width, image_height))  # 调整尺寸
    image.paste(img, (x * image_width, y * image_height))  # 粘贴到指定位置
    x += 1
    if x == row:     # 满一行重置x，y+=1
        x = 0
        y += 1
image.show()
image.save("豆瓣top250海报合并.jpg")
