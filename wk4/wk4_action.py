import pandas as pd
from efficient_apriori import apriori
from mlxtend.frequent_patterns import apriori as ml_apriori, association_rules
import time


def read_data(path):
    # 读取数据，不将第一行置为header
    raw_data = pd.read_csv(path, header=None)
    return raw_data


def apriori_efficient(raw_data):
    # 将数据放入transaction, 实例化一个名为transaction的list
    transactions = []
    for i in range(0, raw_data.shape[0]):
        # 每一行有效值放入items
        items = []
        for j in range(0, raw_data.shape[1]):
            # 需要转成string
            if str(raw_data.values[i, j]) != 'nan':
                items.append(str(raw_data.values[i, j]))
        transactions.append(items)
    start_time = time.time()
    item_sets, rules = apriori(transactions, min_support=0.02, min_confidence=0.4)
    end_time =time.time()
    cost_time = end_time - start_time
    print("频繁项集1：", item_sets)
    print("关联规则1：", rules)
    print("efficient_apriori方式耗时%s" % cost_time)


def mlxtend_preparation(raw_data):
    # 生成全量产品清单
    products = []
    for i in range(0, raw_data.shape[0]):
        for j in range(0, raw_data.shape[1]):
            temp_data = raw_data.values[i, j]
            if str(temp_data) !='nan' and str(temp_data) not in products:
                products.append(temp_data)
    products_series = pd.Series(products)
    # print(products_series)
    # 构建一个列标题为全量产品清单的DataFrame
    df_products = pd.DataFrame(index=raw_data.index, columns=products_series)
    # one-hot化
    for i in df_products.index:
        for j in df_products.columns:
            if j in raw_data.loc[i].values:
                df_products.at[i, j] = 1
            else:
                df_products.at[i, j] = 0
    return df_products


def apriori_mlxtend(hot_encoded):
    start_time = time.time()
    # 挖掘频繁项集，最小支持度为0.02
    item_sets = ml_apriori(hot_encoded, use_colnames=True, min_support=0.02)
    # 根据频繁项集计算关联规则，设置最小提升度为1
    rules = association_rules(item_sets, metric='lift', min_threshold=1)
    end_time = time.time()
    cost_time = end_time-start_time
    print("频繁项集2：", item_sets)
    print("关联规则2：", rules)
    print("mlxtend方式耗时%s" % cost_time)


if __name__ == '__main__':
    filepath = './Market_Basket_Optimisation.csv'
    raw_data = read_data(filepath)
    apriori_efficient(raw_data)
    print('==============开始one-hot处理==============')
    hot_encoded = mlxtend_preparation(raw_data)
    print('==============one-hot处理完成==============')
    apriori_mlxtend(hot_encoded)

