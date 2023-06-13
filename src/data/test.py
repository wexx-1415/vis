import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymysql

db = pymysql.connect(host='localhost', user='root', password='0k9ruGa;*9gA', database='geo', charset="utf8mb4")
df = pd.read_csv("D:\学习\可视化\ok_geo.csv\ok_geo.csv")
cursor = db.cursor()
# print(df.loc[0].to_sql())
deep = {}
error_num=0
for i in range(1,len(df)):
  df.loc[i,"geo"] = "ST_GeomFromText('POINT ("+str(df.loc[i]["geo"])+")',0)"
  df.loc[i,"polygon"]="ST_GeomFromText('POLYGON (("+str(df.loc[i]["polygon"])+","+str(df.loc[i]["polygon"]).split(",")[0]+"))',0)"
  sql = 'INSERT INTO `geo` VALUES(%s,"%s","%s","%s","%s",%s,%s)'
  try:
    cursor.execute(sql%tuple(df.loc[i].to_list()))
    db.commit()
  except Exception as e :
    print(e)
    error_num+=1
    print(df.loc[i]["name"])
    if(deep.get(df.loc[i]["deep"])==None):
      deep[df.loc[i]["deep"]]=1
    else:
      deep[df.loc[i]["deep"]]+=1
    db.rollback()
    # break
print(error_num)
print(deep)
# # df=df[::2]
# print(df.shape)
# df.apply(lambda x: x.replace(" ", ""))
# df.to_csv("data1.csv", index=False)
# plt.plot(df["lat"], df["lon"])
# plt.show()
