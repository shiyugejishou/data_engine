import pandas as pd

# 数据读取
result = pd.read_csv('.\wk2\spider_result.csv', encoding='utf8')
# 数据预处理
# result = result.drop('problem', 1).join(result.problem.str.get_dummies(','))

# 品牌投诉总数
df_brand = result.groupby(['brand'])['id'].agg(['count']).sort_values('count', ascending=False)
print(df_brand)

# 车型投诉总数
df_model = result.groupby(['car_model'])['id'].agg(['count']).sort_values('count', ascending=False)
print(df_model)

# 品牌平均车型投诉数量
df_brand_model = result.groupby(['brand', 'car_model'])['id'].agg(['count']).groupby(['brand']).mean()\
    .sort_values('count', ascending=False)
print(df_brand_model)