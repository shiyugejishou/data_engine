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

base_url = 'http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-{}.shtml'
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')


def get_page(page):
    """

    :param page: 页码
    :return: 结果的dataframe
    """
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    new_url = base_url.format(page)
    chrome_options.add_argument('user-agent=%s'% headers)
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(new_url)
    td_list = browser.find_elements_by_tag_name('td')
    # print(td_list)
    cols = browser.find_elements_by_tag_name('th')
    col_list = []
    for col_item in cols:
        col_list.append(col_item.text)
    td_results = []
    for td_item in td_list:
        if td_item.text:
            td_results.append(td_item.text)
        else:
            status = td_item.find('img').get('title')
            td_results.append(status)
    step = 8
    results_list = [td_results[i:i + step] for i in range(0, len(td_results), step)]# 把数据每8个划为一个list
    results_df = DataFrame(columns=col_list)
    for item in results_list:
        temp_df = DataFrame(np.array(item).reshape(1, 8), columns=col_list)
        results_df = results_df.append(temp_df, ignore_index=True)
    return results_df


if __name__ == '__main__':
    print('开始爬取...')
    start_time = time.time()
    for page_num in range(1, 2):
        print('正在爬取第%s页'%page_num)
        if page_num == 1:
            df_init = get_page(page_num)
            # print(df_init)
        else:
            df_new = get_page(page_num)
            df_init = df_init.append(df_new, ignore_index=True)
            # print(df_init)
        # sleep(random.randint(1, 2))
    df_init.to_csv('./spider_result.csv', sep=',', header=True, index=False, encoding='utf_8_sig')
    print('爬取完成')
    end_time = time.time()
    cost_time = end_time - start_time
    print("爬取任务完成，共耗时%s分钟！" % str(round(cost_time / 60, 2)))


