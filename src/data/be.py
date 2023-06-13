import os

import pandas as pd
import pymysql
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)
DIR="D:\\学习\\可视化\\实验\\final\\src\\data"
df=pd.read_csv("D:\\学习\\可视化\\实验\\final\\src\\data\\CN-Reanalysis-daily-2018120100.csv")
df.columns = df.columns.str.replace(" ", "").str.replace("\(.+\)$", "")
df.apply(lambda x: x.replace(" ", ""))
db = pymysql.connect(host='localhost', user='root', password='0k9ruGa;*9gA', database='geo', charset="utf8mb4")
cursor = db.cursor()

@app.route("/test", methods=["post"])
def test():
    print(request.form["city"])
    sql="SELECT id,deep,name FROM geo WHERE ST_Intersects(polygon, ST_GeomFromText('POINT(%s %s)',0))=1"
    
    city=pd.DataFrame()
    # city.append(df.loc[0])
    for i in range(len(df)):
        cursor.execute(sql,[float(df.loc[0]["lon"]),float(df.loc[0]["lat"])])
        data=cursor.fetchall()
        if(data.__str__().index(request.form["city"])!=-1):
            city.append(df.loc[0])
    # city=df[df["city"]==request.form["city"]]
    print(type(data[0][2]))
    return city.to_json(orient="records")

@app.route("/file", methods=["post"])
def file():
    print(request.form["file"])
    if os.path.exists(DIR+"\\"+request.form["file"]):
        return send_from_directory("./", request.form["file"], as_attachment=True)
    else:
        return "文件不存在"
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
