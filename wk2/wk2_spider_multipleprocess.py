# -*- coding: utf-8 -*-
from pandas import DataFrame
import numpy as np
from time import sleep
import random
from selenium import webdriver
import time
from fake_useragent import UserAgent
import threading
from queue import Queue
import datetime

base_url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-{}.shtml'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
df_init = DataFrame(columns=['id', 'brand', 'car_model', 'type', 'desc', 'problem', 'datetime', 'status'])
date = datetime.datetime.now().strftime('%Y%m%d')


class MyThread(threading.Thread):
    def __init__(self, queue, thread_name):
        threading.Thread.__init__(self)
        self.queue = queue
        self.name = thread_name

    def run(self):
        print('线程%s已开始……'% self.name)
        # 判断队列是否为空
        while not self.queue.empty():
            url = self.queue.get()
            rest_task = self.queue.qsize()
            print('当前还有 %s 页等待爬取' % rest_task)
            re_df = get_page(url, self.name)
            # print(re_df)
            df_result = df_init.append(re_df, ignore_index=True)
            df_result.to_csv('./%s_spider_result.csv'% date, mode='a', header=False, index=False, encoding='utf_8_sig')

        print('线程%s结束'% self.name)


def get_page(new_url, thread_name):
    """

    :param page: 页码
    :return: 结果的dataframe
    """
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    chrome_options.add_argument('user-agent=%s'% headers)
    browser = webdriver.Chrome(options=chrome_options)
    sleep(random.randint(1, 2))
    print('线程%s 开始爬取'% thread_name)
    browser.get(new_url)
    td_list = browser.find_elements_by_tag_name('td')
    # print(td_list)
    td_results = []
    for td_item in td_list:
        # print(td_item.text)
        if td_item.text:
            td_results.append(td_item.text)
        else:
            status = td_item.find('img').get('title')
            td_results.append(status)
    step = 8
    results_list = [td_results[i:i + step] for i in range(0, len(td_results), step)]# 把数据每8个划为一个list
    results_df = DataFrame(
        columns=['id', 'brand', 'car_model', 'type', 'desc', 'problem', 'datetime', 'status']
    )
    for item in results_list:
        temp_df = DataFrame(np.array(item).reshape(1, 8),
        columns=['id', 'brand', 'car_model', 'type', 'desc', 'problem', 'datetime', 'status'])
        results_df = results_df.append(temp_df, ignore_index=True)
    browser.close()
    print('线程%s 爬取完成' % thread_name)
    return results_df


if __name__ == '__main__':
    print('开始爬取...')
    start_time = time.time()
    myqueue = Queue()
    for page_num in range(1, 10424):
        new_url = base_url.format(page_num)
        myqueue.put(new_url)

    allthread = []
    # 实例化多个线程
    for v in range(10):
        name = 'thread%s'%str(v+1)
        mythread = MyThread(myqueue, name)
        mythread.start()
        allthread.append(mythread)

    # 等待多个子线程结束
    for v in allthread:
        v.join()
    print('爬取完成')
    end_time = time.time()
    cost_time = end_time - start_time
    print("爬取任务完成，共耗时%s分钟！" % str(round(cost_time / 60, 2)))

