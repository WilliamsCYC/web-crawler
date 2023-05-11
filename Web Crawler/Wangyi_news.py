from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from time import sleep
from lxml import etree
import re
import pickle
import random
import requests


date = str(input('请输入今天的日期（YYYY-MM-DD）：'))
filename = date + '.pkl'
path = 'C:/Users/Williams/Desktop/网易新闻处理/网易财经新闻备份/'


# 用selenium获取页面源代码
# webdriver的基本配置
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = Chrome(options=options)

# 获取动态页面源代码
driver.get('https://money.163.com/')
page_source = driver.page_source
driver.quit()




# 获取网易财经页面上方的14条内容
# requests的基本配置
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}

# 创建空文件
whole_data = {}
with open(path + filename, 'wb') as f:
    pickle.dump(whole_data, f, pickle.HIGHEST_PROTOCOL)

# 找到新闻标题和url
# 然后储存
tree = etree.HTML(page_source)
li_list = tree.xpath('//*[@id="index2016_wrap"]/div/div[3]/div[3]/div[3]/div/div[2]/div[1]/ul/li')
for li in li_list:
    try:
        title = li.xpath('./h2/a/text() | ./h3/a/text()')[0]
        news_url = li.xpath('./h2/a/@href | ./h3/a/@href')[0]

        # 获取页面内容以及生成etree实例


        # selenium 版本
        # driver = Chrome(options=options)
        # driver.get(news_url)
        # news_page = driver.page_source
        # news_tree = etree.HTML(news_page)


        # requests版本
        page_text = requests.get(news_url, headers=headers).text
        tree = etree.HTML(page_text)

        # 获取日期
        news_date = tree.xpath('//div[@class="post_info"]/text()')[0]
        news_date = re.findall(r"(\d{4}-\d{1,2}-\d{1,2})", news_date)[0]

        # 判断是不是当天的新闻
        if news_date != date:
            continue

        # 获取新闻内容
        news_content = tree.xpath('//div[@class="post_body"]/p//text()')
        news_content = ''.join(news_content)
    except Exception as e:
        print(news_url, '\n', repr(e), '\n', ' ')
        continue

    # 将数据打包在字典里以及储存
    news_data = {
        'title': title,
        'date': news_date,
        'url': news_url,
        'content': news_content
    }
    with open(path + filename, 'rb') as f:
        whole_data = pickle.load(f)
    whole_data[title] = news_data
    with open(path + filename, 'wb') as f:
        pickle.dump(whole_data, f, pickle.HIGHEST_PROTOCOL)

    sleep_time = random.uniform(0.1, 0.15)
    sleep(sleep_time)


    # driver.quit()







# 获取网易财经页面下方各个板块的内容
# 用正则表达式获取页面下方全部板块的全部新闻的标题和url
# 对正则表达式打包
main_obj = re.compile(r'<!-- // 首页 -->.*?</div>', re.S)
section_obj = re.compile(r' -->.*?<!-- // ', re.S)
news_obj = re.compile(r'<a href="(?P<url>.*?)">(?P<title>.*?)</a>', re.S)

# 解析出标题和网址
# 找到全部板块打包的数据
main = main_obj.findall(page_source)[0]
# 找到每一个板块的数据
sections = section_obj.finditer(main)
# 获取每一条新闻的标题的网址
for i in sections:
    i = i.group()
    news = news_obj.finditer(i)
    for j in news:
        news_url = j.group('url')
        title = j.group('title')

        try:
            # 获取页面内容以及生成etree实例

            # selenium版本
            # driver = Chrome(options=options)
            # driver.get(news_url)
            # news_page = driver.page_source
            # news_tree = etree.HTML(news_page)


            # requests版本
            page_text = requests.get(news_url, headers=headers).text
            tree = etree.HTML(page_text)

            # 获取日期
            news_date = tree.xpath('//div[@class="post_info"]/text()')[0]
            news_date = re.findall(r"(\d{4}-\d{1,2}-\d{1,2})", news_date)[0]

            # 判断是不是当天的新闻
            if news_date != date:
                continue

            # 获取新闻内容
            news_content = tree.xpath('//div[@class="post_body"]/p//text()')
            news_content = ''.join(news_content)
        except Exception as e:
            print(news_url, '\n', repr(e), '\n', ' ')
            continue

        # 将数据打包在字典里以及储存
        news_data = {
            'title': title,
            'date': news_date,
            'url': news_url,
            'content': news_content
        }
        with open(path + filename, 'rb') as f:
            whole_data = pickle.load(f)
        whole_data[title] = news_data
        with open(path + filename, 'wb') as f:
            pickle.dump(whole_data, f, pickle.HIGHEST_PROTOCOL)

        sleep_time = random.uniform(0.1, 0.15)
        sleep(sleep_time)


        # driver.quit()