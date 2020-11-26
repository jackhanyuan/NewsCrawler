#!/usr/bin/python3
# coding=utf-8

from flask import Flask, request, render_template, redirect, url_for
from search import mongo_search, snapshot_search, content_search, info_search, str2img, del_file
import jieba
import re
import math
import time

id_list = []
app = Flask(__name__, static_url_path="")


@app.route("/", methods=['POST', 'GET'])
def main():
    if request.method == 'POST' and request.values.get('query'):
        query = request.values.get('query')
        query = re.sub(r'[^\w ]', ' ', query)
        # print(query)
        global id_list
        id_list = []
        return redirect(url_for('search', query=query))
    return render_template('index.html')


@app.route("/s/<query>", methods=['POST', 'GET'])
def search(query):
    id_search_start = time.time()
    global id_list
    if not len(id_list):
        id_list = mongo_search(query)
    id_search_end = time.time()
    print("id查询时间：", id_search_end - id_search_start)

    query_list = jieba.cut_for_search(query)
    query_list = list(filter(lambda s: s and (type(s) != str or len(s.strip()) > 0), set(query_list)))
    # print(query_list)
    # print("-" * 100)

    if request.method == 'POST' and request.values.get('snapshot'):
        snapshot = request.values.get('snapshot')
        return redirect(url_for('show_snapshot', snapshot=snapshot))

    page = 1
    one_page_number = 10
    total_page = math.ceil(len(id_list)/one_page_number)

    if request.method == 'GET' and request.values.get('page'):

        try:
            page = int(eval(request.values.get('page')))
        except:
            page = 1
        # print(page)

    if 1 <= page <= total_page:
        results = get_highlight_content(one_page_number*(page-1), one_page_number*page, id_list, query_list)
    elif page < 1:
        results = get_highlight_content(0, one_page_number, id_list, query_list)
        page = 1
    else:
        # print(one_page_number*(total_page-1),one_page_number*total_page)
        results = get_highlight_content(one_page_number*(total_page-1), one_page_number*total_page, id_list, query_list)
        page = total_page

    return render_template('search.html', docs=results, query=query, length=len(id_list), pages=total_page,
                           page=page)


def get_highlight_content(start_id, end_id, id_list, query_list):
    content_search_start = time.time()
    page_id_list = id_list[start_id:end_id]
    query_results = content_search(page_id_list)
    # print(query_results)
    results = highlight(query_results, query_list)
    content_search_end = time.time()
    print("content查询时间：", content_search_end - content_search_start)
    return results


def highlight(docs, terms):  # 高亮doc中term部分
    result = []
    for doc in docs:
        url = doc["url"] if "url" in doc.keys() else "None"
        title = doc["article"]['title'] if "title" in doc["article"].keys() else "None"
        content = doc["article"]['content'][0:250] if "content" in doc["article"].keys() else "None"
        publish_time = doc["article"]["publish_time"] if "publish_time" in doc["article"].keys() else ""
        # print(title,url)

        for term1 in terms:
            for term in list(re.findall(term1, title, flags=re.IGNORECASE)):
                title = title.replace(term, '<font color="red">{}</font>'.format(term))
                # title = re.sub(term, '<em><font color="red">{}</font></em>'.format(term), title, flags=re.IGNORECASE)
            for term in list(re.findall(term1, content, flags=re.IGNORECASE)):
                content = content.replace(term, '<font color="red">{}</font>'.format(term))
        result.append((url, title, content, publish_time))

    return result


@app.route("/snapshot", methods=['POST', 'GET'])
def show_snapshot():
    if request.method == 'GET' and request.values.get('snapshot'):
        url = request.values.get('snapshot')
        snapshot_result = snapshot_search(url)
        info_result = info_search(url)
        del_file("./static/snapshots")
        images = str2img(url)
        # print(images)
        return render_template('snapshot.html', doc=snapshot_result, info=info_result, images=images)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
