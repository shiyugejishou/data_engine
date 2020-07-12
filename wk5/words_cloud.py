import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk


def get_data(path):
    """

    :param path: 数据文件路径
    :return: words_list 词表
    """
    # 读取文件
    raw_data = pd.read_csv(path, header=None)
    # 将数据转为DataFrame
    words_df = DataFrame(raw_data)
    # 将数据中的所有词生成list并返回
    words_list = []
    for i in range(0, words_df.shape[0]):
        for j in range(0, raw_data.shape[1]):
            word_item = words_df.values[i, j]
            if str(word_item) !='nan':
                words_list.append(str(word_item))
    return words_list


def create_word_cloud(words_list):
    """

    :param words_list:
    :return: word_cloud 词云
    """
    # 统计词频
    freq_dict = nltk.FreqDist(words_list)
    # 将字典按value降序排列
    new_dict = dict(sorted(freq_dict.items(), key=lambda e: e[1], reverse=True))
    # 输出字典前十个键值，即top10的商品
    print('Top 10 的商品为：')
    for i in range(0, 10):
        print(list(new_dict.items())[i])
    print('=====================================================')
    wc = WordCloud(
        max_words=100,
        width=2000,
        height=1200,
    )
    # 将商品名称组成text，以空格分隔
    cut_text = " | ".join(words_list)
    # 生成词云并保存
    word_cloud = wc.generate(cut_text)
    word_cloud.to_file("./wk5/wordcloud.jpg")
    return word_cloud


if __name__ == '__main__':
    filepath = 'C:/Users/34401/PycharmProjects/data_engine/wk5/Market_Basket_Optimisation.csv'
    words_list = get_data(filepath)
    # print(words_list)
    my_word_cloud = create_word_cloud(words_list)
    # 显示词云文件
    plt.imshow(my_word_cloud)
    plt.axis("off")
    plt.show()

