# 导入
import requests
from bs4 import BeautifulSoup
import csv

# 表格数据
lst = []

# 获取网页源码
def get_html(url):
    # 发请求
    html = requests.get(url)
    # 发现乱码，处理编码
    html.encoding = 'utf-8'
    # 得到网页源码
    html = html.text
    # 返回到函数调用处
    return html

# 解析网页数据
def parse_html(html):
    # 创建对象
    soup = BeautifulSoup(html,'html5lib')
    # 解析
    conMidtab = soup.find('div', class_='conMidtab')
    # print(conMidtab)
    tables = conMidtab.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index, tr in enumerate(trs):
            dic = {}
            # 拿到对应的标签
            if index == 0: # 判断是否是第一个城市
                # 第一个城市
                city_td = tr.find_all('td')[1]
            else:
                # 其他城市
                city_td = tr.find_all('td')[0]
            temp_td = tr.find_all('td')[-2]
            # print(city_td,temp_td)
            # 对应的标签里面拿文本内容
            dic['city'] = list(city_td.stripped_strings)[0]
            dic['temp'] = temp_td.string
            lst.append(dic)

# 保存数据
def save_data():
    # 规定表头
    head = ('city','temp')
    # csv 文件写入
    with open('weather.csv','w',encoding='utf-8-sig',newline='') as f:
        # 创建 csv 对象
        writer = csv.DictWriter(f, fieldnames=head)
        # 写入表头
        writer.writeheader()
        # 写入数据
        writer.writerows(lst)

# 获取不同地区 url
def area(link):
    # 获取网页源码
    link = get_html(link)
    # 创建对象
    soup = BeautifulSoup(link, 'html5lib')
    # 解析
    conMidtab = soup.find('ul', class_='lq_contentboxTab2')
    # 找到 a 链接
    tagas = conMidtab.find_all('a')
    # url 列表
    hrefs = []
    # 循环获取 url
    for i in tagas:
        hrefs.append('http://www.weather.com.cn' + i.get('href'))
    # 打印 url 列表
    # print(hrefs)
    # 返回函数值
    return hrefs

# 处理主逻辑
def main():
    # 确定 url
    link = 'http://www.weather.com.cn/textFC/hb.shtml'
    # 不同地区 url
    lst = area(link)
    # print(lst)
    for i in lst:
        url = i
        # 获取网页源码
        html = get_html(url)
        # 数据解析
        parse_html(html)
    # 保存内容
    save_data()

# 运行主程序
main()