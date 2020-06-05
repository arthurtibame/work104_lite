import pandas as pd 

# readcsv
path = r'C:\python\work104_lite\data\數據分析\mapreduce.csv'

df = pd.read_csv(f'{path}', sep='delimiter', header=None, encoding='utf-8-sig')
# all values to list
#test = df.iloc[:,0].tolist()


import itertools
df_list = df.iloc[:,0].tolist()
list_of_list_description = [x.split(',') for x in df_list]
#b = list(itertools.chain.from_iterable(a))
#c1 = list(dict.fromkeys(b))
#c1 = [i.replace('\u200b','') for i in c1]
all_description_list = list(map(lambda x: x.replace('\u200b',''),list(dict.fromkeys(list(itertools.chain.from_iterable([x.split(',') for x in df.iloc[:,0].tolist()]))))))
#c1 = [i.replace('\u200b','') for i in c1]
#c2 = list(set(b))
#print(test) => 不用用到
print("========================================")
print(list_of_list_description) # ->
print("========================================")
#print(b)
print("========================================")
print(all_description_list)
print("========================================")
result_list = list()
for not_import_index ,each_description_list in enumerate(list_of_list_description):
    tmp_list = list()
    for i in range(len(all_description_list)):
        if all_description_list[i] not in each_description_list:
            tmp_list.append(0)
        else :
            tmp_list.append(1)
    result_list.append(tmp_list)

df_result = pd.DataFrame(result_list,columns=all_description_list)
df_result.drop(columns=['無條件'])
df1 = pd.read_csv(r'C:\python\work104_lite\數據分析-20200605.csv',encoding='utf-8-sig')
df_final = pd.concat([df1, df_result], axis=1)
df_final.to_csv(r'C:\python\work104_lite\數據分析-20200605.csv',index=None,encoding='utf-8-sig')

#df_result.to_csv('test.csv', header=all_description_list,index=None,encoding='utf-8-sig')





