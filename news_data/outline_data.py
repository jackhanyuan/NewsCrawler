#! /usr/bin/python3
# coding=utf-8

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import re
import urllib.request
import base64
from lxml import etree
from user_agent import random_agent


def open_chrome():
	chrome_opt = Options()  # 创建参数设置对象.
	chrome_opt.add_argument('--headless')  # 无界面化.
	chrome_opt.add_argument('--disable-gpu')  # 配合上面的无界面化，禁用GPU加速.
	chrome_opt.add_argument('--window-size=1366,768')  # 设置窗口大小, 窗口大小会有影响.
	chrome_opt.add_argument(f'--user-agent={random_agent()}')  # 设置请求头
	# chrome_opt.add_argument('--proxy-server=' + '47.240.88.149')  # 设置代理
	driver = webdriver.Chrome(executable_path=r'/usr/bin/chromedriver', options=chrome_opt)
	return driver


def get_contents(driver, temp_url):
	article_dict = dict()
	new_url = "https://outline.com/" + temp_url
	wait = WebDriverWait(driver, 12)
	try:
		driver.get(new_url)
		# agent = driver.execute_script("return navigator.userAgent")
		# print("\t" + agent)
		element = wait.until(ec.presence_of_element_located((By.XPATH, "/html/body/outline-app/outline-article"
		                                                               "/div[@class='article-wrapper']/div["
		                                                               "@class='yue']")))
		html = etree.HTML(driver.page_source)
		# print(html)
		article_raw = html.xpath(
			"/html/body/outline-app/outline-article/div[@class='article-wrapper']/div[@class='yue']/raw//*")
		# print(article_raw)

		article_info = html.xpath(
			"/html/body/outline-app/outline-article/div[@class='article-wrapper']/div[@class='yue']/div[@class='article-info']/*")
		article_title = article_info[0].text if article_info[0].text is not None else ""
		article_author = article_info[1].text if article_info[1].text is not None else ""
		article_time = article_info[2].text if article_info[2].text is not None else ""
		print("\t" + article_title, article_author, article_time)

		count = 0
		content_html = ""
		img_list = []
		filter_list = ["p", "img"]
		for i in article_raw:
			# print(i.tag, i.attrib, i.text)
			if i.tag in filter_list:
				if i.tag == "img":
					count += 1
					n = temp_url.rindex('/')
					file_name = re.sub(r'\W', '', temp_url[n+1:])
					img_name = "snapshots/" + file_name + "_" + str(count) + ".jpg"
					img_tag = "<br><p><img src=" + img_name + "></p><br>"
					content_html += img_tag
					# print(img_tag)

					m = i.attrib["src"]
					# if re.match(r'.+?(jpg|png|jpeg|gif|webp|ico|bmp|jfif)', m):
					img_list.append(m)
				# print(img_list)

				else:
					content = etree.tostring(i, encoding="utf-8", pretty_print=True, method="html").decode("utf-8")
					content_html += content
		# print(content_html)

		article_content = driver.find_element_by_xpath(
			"/html/body/outline-app/outline-article/div[@class='article-wrapper']/div[@class='yue']/raw").text
		if len(article_content) > 100:
			article_dict['title'] = article_title
			article_dict['author'] = article_author
			article_dict['publish_time'] = article_time
			article_dict['content'] = article_content
			article_dict['content_html'] = content_html
			article_dict['images'] = download_img(img_list)
			return article_dict
		else:
			print('\tContent is too short')
			return None

	except Exception as error:
		print('\tGet content error:', error)
		return 'Exception'


def get_article(url):
	driver = open_chrome()
	article = get_contents(driver, url)
	driver.quit()
	return article


def download_img(img_list):
	images = []
	headers = {'User-Agent': random_agent()}
	for img in img_list:
		try:
			request = urllib.request.Request(img, headers=headers)
			response = urllib.request.urlopen(request)
			if response.getcode() == 200:
				res = base64.b64encode(response.read())
				r = res.decode("ascii")
				images.append(r)
		except Exception as error:
			print('\tGet image error:', error)

	if len(images):
		print(f"\tDownload {len(images)}/{len(img_list)} picture successfully")

	return images

# if __name__ == '__main__':
	# url = 'https://news.ifeng.com/c/81WX4GGq1rC'
# url = 'http://news.163.com/special/freedom/'
# url = 'http://www.xinhuanet.com/world/2020-11/09/c_1126717938.htm'
# url = "http://news.163.com/special/freedom/"
# url = "http://news.ifeng.com/c/7qZXSs5mXj6"
# 	art = get_article(url)
# print(art)
# random_agent()
