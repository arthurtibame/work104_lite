import pandas as pd

#reducer_path = r'./mapreduce/reducer.csv'
#df = pd.read_csv(reducer_path, encoding='utf-8-sig')
#
#a = df.sum(axis = 0, skipna = True).sort_values(ascending=False)
#a.to_csv('test.csv', header=False, encoding='utf-8-sig')
path = r'test.csv'
df = pd.read_csv(path, header=None)
print(df.loc[:,0].tolist())

