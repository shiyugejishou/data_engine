import numpy as np
from pandas import DataFrame

items = np.arange(2, 101, 2)
item_sum = 0
for item in items:
    item_sum += item
print(item_sum)
print(sum(items))


print('>>>>>>>>>>>>>>>>>>>T2<<<<<<<<<<<<<<<<<<<<')
data = {'语文': [68, 95, 98, 90, 80],
        '数学': [65, 76, 86, 88, 90],
        '英语': [30, 98, 88, 77, 90]
        }
df = DataFrame(data,
               index=['张飞', '关羽', '刘备', '典韦', '许褚'],
            )
df.index.name = '姓名'
print(df)
print('>>>>>>>>>><<<<<<<<')
print(df.describe().loc[['mean', 'max', 'min', 'std']])
print('>>>>>>>>>><<<<<<<<')
df['总分'] = df.sum(axis=1)
print(df.sort_values(by='总分', ascending=False))
