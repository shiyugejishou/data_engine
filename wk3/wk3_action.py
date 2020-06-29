import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# 数据加载
car_data = pd.read_csv('.\car_data.csv', encoding='gbk')
train_x = car_data[['人均GDP', '城镇人口比重', '交通工具消费价格指数', '百户拥有汽车量']]

# LabelEncoder
le = LabelEncoder()
# train_x['地区'] = le.fit_transform(train_x['地区'])

# 规范化到[0,1]空间
min_max_scaler = preprocessing.MinMaxScaler()
train_x = min_max_scaler.fit_transform(train_x)
print(train_x)

# K-Means手肘法
sse =[]
for k in range(2, 11):
    # kmeans算法
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(train_x)
    # 计算inertia簇内误差平方和
    sse.append(kmeans.inertia_)
x = range(2, 11)
plt.xlabel("K")
plt.ylabel("SSE")
plt.plot(x, sse, 'o-')
# plt.savefig("K-Means.png")
plt.show()
plt.figure()
# 轮廓系数法
sc_scores = []
for k in range(2, 11):
    kmeans = KMeans(n_clusters=k)
    kmeans_model = kmeans.fit(train_x)
    sc_score = silhouette_score(train_x, kmeans_model.labels_, metric='euclidean')
    sc_scores.append(sc_score)
k = range(2, 11)
plt.xlabel('k')
plt.ylabel('SCS')
plt.plot(k, sc_scores, '*-')
plt.show()

# 使用K-Means聚类，由手肘法可知最佳k值为5
k_means = KMeans(n_clusters=5)
k_means.fit(train_x)
predict_y = k_means.predict(train_x)
# 合并聚类结果，插入到原数据中
result = pd.concat((car_data, pd.DataFrame(predict_y)), axis=1)
result.rename({0: u'聚类结果'}, axis=1, inplace=True)
print(result)
# 将结果导出到CSV文件中
result.to_csv("car_data_result.csv", index=False, encoding='gbk')

