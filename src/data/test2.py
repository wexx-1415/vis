import os
from math import nan

import aqi
import pandas as pd
import pymysql
import requests

CITY_PATH = "D:\\学习\\可视化\\实验\\final\\src\\data\\city.csv"
PROVINCE_PATH = "D:\\学习\\可视化\\实验\\final\\src\\data\\province.csv"
DIR="D:\\学习\\可视化\\实验\\final\\public"
def get_city():
  df=pd.read_csv("D:\\学习\\可视化\\实验\\final\\src\\data\\CN-Reanalysis-daily-2018120100.csv")
  df.columns = df.columns.str.replace(" ", "").str.replace("\(.+\)$", "")
  df.apply(lambda x: x.replace(" ", ""))
  db = pymysql.connect(host='localhost', user='root', password='0k9ruGa;*9gA', database='geo', charset="utf8mb4")
  cursor = db.cursor()
  sql="SELECT id,deep,name FROM geo WHERE ST_Intersects(polygon, ST_GeomFromText('POINT(%s %s)',0))=1"
  for i in range(len(df)):
    cursor.execute(sql,[float(df.loc[i]["lon"]),float(df.loc[i]["lat"])])
    data=cursor.fetchall()
    c=""
    if(len(data)==2):
      c=data[1][2]
    elif len(data)==1:
      c=data[0][2]
    else:
      c="未知"
    df.loc[i,"city"]=c
    print(c)
  df.to_csv("D:\\学习\\可视化\\实验\\final\\src\\data\\2018120100.csv",index=False)
  
def save_ity():
  df=pd.read_csv("D:\\学习\\可视化\\实验\\final\\src\\data\\2018120100.csv")
  df["city"].to_csv(CITY_PATH,index=False)
# saveCity()
def handle_city(path,save_path):
  df=pd.read_csv(path)
  df.columns = df.columns.str.replace(" ", "").str.replace("\(.+\)$", "")
  df.apply(lambda x: x.replace(" ", ""))
  city=pd.read_csv(PROVINCE_PATH)
  # print(city.columns)
  if not df.columns.values.tolist().__contains__("city"):
    df["city"]=city["city"]
  df["province"]=city["province"]
  # print(df["province"])
  df = df[df['city'] !="未知"]
  df=df[df['province'] !="未知"]
  df=df.groupby(["province", "city"]).mean().round(3)
  df.to_csv(save_path)
  # print(df)
city_no=set()
def handle_dir(dir,path):
  files=os.listdir(dir)
  for file in files:
    print(file,file.split("-")[-1])
    try:
      os.makedirs(DIR+"\\"+path)
      print(f"Directory '{path}' created")
    except FileExistsError:
      print(f"Directory '{path}' already exists")
    handle_city(dir+"\\"+file,DIR+"\\"+path+"\\"+file.split("-")[-1])
def city2province(city):
  area_data = {
        '北京': ['北京市','朝阳区', '海淀区', '通州区', '房山区', '丰台区', '昌平区', '大兴区', '顺义区', '西城区', '延庆县', '石景山区', '宣武区', '怀柔区', '崇文区', '密云县',
               '东城区', '门头沟区', '平谷区'],
        '广东':['广东省', '东莞市', '广州市', '中山市', '深圳市', '惠州市', '江门市', '珠海市', '汕头市', '佛山市', '湛江市', '河源市', '肇庆市','潮州市', '清远市', '韶关市', '揭阳市', '阳江市', '云浮市', '茂名市', '梅州市', '汕尾市'],
        '山东':['山东省', '济南市', '青岛市', '临沂市', '济宁市', '菏泽市', '烟台市','泰安市', '淄博市', '潍坊市', '日照市', '威海市', '滨州市', '东营市', '聊城市', '德州市', '莱芜市', '枣庄市'],
        '江苏':['江苏省', '苏州市', '徐州市', '盐城市', '无锡市','南京市', '南通市', '连云港市', '常州市', '扬州市', '镇江市', '淮安市', '泰州市', '宿迁市'],
        '河南':['河南省', '郑州市', '南阳市', '新乡市', '安阳市', '洛阳市', '信阳市','平顶山市', '周口市', '商丘市', '开封市', '焦作市', '驻马店市', '濮阳市', '三门峡市', '漯河市', '许昌市', '鹤壁市', '济源市'],
        '上海':['上海市', '松江区', '宝山区', '金山区','嘉定区', '南汇区', '青浦区', '浦东新区', '奉贤区', '闵行区', '徐汇区', '静安区', '黄浦区', '普陀区', '杨浦区', '虹口区', '闸北区', '长宁区', '崇明县', '卢湾区'],
        '河北':[ '河北省', '石家庄市', '唐山市', '保定市', '邯郸市', '邢台市', '河北区', '沧州市', '秦皇岛市', '张家口市', '衡水市', '廊坊市', '承德市'],
        '浙江':['浙江省', '温州市', '宁波市','杭州市', '台州市', '嘉兴市', '金华市', '湖州市', '绍兴市', '舟山市', '丽水市', '衢州市'],
        '陕西':['陕西省', '西安市', '咸阳市', '宝鸡市', '汉中市', '渭南市','安康市', '榆林市', '商洛市', '延安市', '铜川市'],
        '湖南':[ '湘西土家族苗族自治州','湖南省', '长沙市', '邵阳市', '常德市', '衡阳市', '株洲市', '湘潭市', '永州市', '岳阳市', '怀化市', '郴州市','娄底市', '益阳市', '张家界市', '湘西州'],
        '重庆':['重庆城区', '重庆郊县', '重庆市', '江北区', '渝北区', '沙坪坝区', '九龙坡区', '万州区', '永川市', '南岸区', '酉阳县', '北碚区', '涪陵区', '秀山县', '巴南区', '渝中区', '石柱县', '忠县', '合川市', '大渡口区', '开县', '长寿区', '荣昌县', '云阳县', '梁平县', '潼南县', '江津市', '彭水县', '璧山县', '綦江县',
     '大足县', '黔江区', '巫溪县', '巫山县', '垫江县', '丰都县', '武隆县', '万盛区', '铜梁县', '南川市', '奉节县', '双桥区', '城口县'],
        '福建':['福建省', '漳州市', '泉州市','厦门市', '福州市', '莆田市', '宁德市', '三明市', '南平市', '龙岩市'],
        '天津':['天津市', '和平区', '北辰区', '河北区', '河西区', '西青区', '津南区', '东丽区', '武清区','宝坻区', '红桥区', '大港区', '汉沽区', '静海县', '宁河县', '塘沽区', '蓟县', '南开区', '河东区'],
        '云南':['楚雄彝族自治州','迪庆藏族自治州','大理白族自治州','西双版纳傣族自治州', '临沧市','红河哈尼族彝族自治州','丽江市','普洱市','迪庆藏族 自治州','文山壮族苗族自治州','德宏傣族景颇族自治州', '怒江傈僳族自治州','云南省', '昆明市', '红河州', '大理州', '文山州', '德宏州', '曲靖市', '昭通市', '楚雄州', '保山市', '玉溪市', '丽江地区', '临沧地区', '思茅地区', '西双版纳州', '怒江州', '迪庆州'],
        '四川':['阿坝藏族羌族自治州','甘孜藏族自治州','凉山彝族自治州','四川省', '成都市', '绵阳市', '广元市','达州市', '南充市', '德阳市', '广安市', '阿坝州', '巴中市', '遂宁市', '内江市', '凉山州', '攀枝花市', '乐山市', '自贡市', '泸州市', '雅安市', '宜宾市', '资阳市','眉山市', '甘孜州'],
        '广西':['广西壮族自治区', '贵港市', '玉林市', '北海市', '南宁市', '柳州市', '桂林市', '梧州市', '钦州市', '来宾市', '河池市', '百色市', '贺州市', '崇左市',  '防城港市'],
        '安徽':['安徽省', '芜湖市', '合肥市', '六安市', '宿州市', '阜阳市','安庆市', '马鞍山市', '蚌埠市', '淮北市', '淮南市', '宣城市', '黄山市', '铜陵市', '亳州市','池州市', '巢湖市', '滁州市'],
        '海南':['昌江黎族自治县','白沙黎族自治县','琼中黎族苗族自治县','陵水黎族自治县','乐东黎族自治县','海南省', '三亚市', '海口市', '琼海市', '文昌市', '东方市', '昌江县', '陵水县', '乐东县', '五指山市', '保亭县', '澄迈县', '万宁市','儋州市', '临高县', '白沙县', '定安县', '琼中县', '屯昌县'],
        '江西':['江西省', '南昌市', '赣州市', '上饶市', '吉安市', '九江市', '新余市', '抚州市', '宜春市', '景德镇市', '萍乡市', '鹰潭市'],
        '湖北':['襄阳市','恩施土家族苗族自治州','湖北省', '武汉市', '宜昌市', '襄樊市', '荆州市', '恩施州', '孝感市', '黄冈市', '十堰市', '咸宁市', '黄石市', '仙桃市', '随州市', '天门市', '荆门市', '潜江市', '鄂州市', '神农架林区'],
        '山西':['山西省', '太原市', '大同市', '运城市', '长治市', '晋城市', '忻州市', '临汾市', '吕梁市', '晋中市', '阳泉市', '朔州市'],
        '辽宁':['辽宁省', '大连市', '沈阳市', '丹东市', '辽阳市', '葫芦岛市', '锦州市', '朝阳市', '营口市', '鞍山市', '抚顺市', '阜新市', '本溪市', '盘锦市', '铁岭市'],
        '台湾':['台湾省','台北市', '高雄市', '台中市', '新竹市', '基隆市', '台南市', '嘉义市'],
        '黑龙江':['黑龙江', '齐齐哈尔市', '哈尔滨市', '大庆市', '佳木斯市', '双鸭山市', '牡丹江市', '鸡西市','黑河市', '绥化市', '鹤岗市', '伊春市', '大兴安岭地区', '七台河市'],
        '内蒙古':['巴彦淖尔市','乌兰察布市','内蒙古自治区', '赤峰市', '包头市', '通辽市', '呼和浩特市', '乌海市', '鄂尔多斯市', '呼伦贝尔市','兴安盟', '巴彦淖尔盟', '乌兰察布盟', '锡林郭勒盟', '阿拉善盟'],
        '香港':["香港","香港特别行政区"],
        '澳门':['澳门','澳门特别行政区'],
        '贵州':['毕节市','黔东南苗族侗族自治州','黔西南布依族苗族自治州','铜仁市','黔南布依族苗族自治州','贵州省', '贵阳市', '黔东南州', '黔南州', '遵义市', '黔西南州', '毕节地区', '铜仁地区','安顺市', '六盘水市'],
        '甘肃':['甘南藏族自治州','陇南市','定西市','甘肃省', '兰州市', '天水市', '庆阳市', '武威市', '酒泉市', '张掖市', '陇南地区', '白银市', '定西地区', '平凉市', '嘉峪关市', '临夏回族自治州','金昌市', '甘南州'],
        '青海':['海北藏族自治州','保亭黎族苗族自治县','果洛藏族自治州','海西蒙古族藏族自治州','海南藏族自治州','海东市','吐鲁番市','青海省', '西宁市', '海西州', '海东地区', '海北州', '果洛州', '玉树州', '黄南藏族自治州'],
        '新疆':['巴音郭楞蒙古自治州','北屯市','伊犁哈萨克自治州','双河市','阿勒泰地区','博尔塔拉蒙古自治州','铁门关市', '昆玉市','克孜勒苏柯尔克孜自治州','胡杨河市','昌吉回族自治州','哈密市','可克达拉市','新星市','新疆','新疆维吾尔自治区', '乌鲁木齐市', '伊犁州', '昌吉州','石河子市', '哈密地区', '阿克苏地区', '巴音郭楞州', '喀什地区', '塔城地区', '克拉玛依市', '和田地区', '阿勒泰州', '吐鲁番地区', '阿拉尔市', '博尔塔拉州', '五家渠市',
     '克孜勒苏州', '图木舒克市'],
        '西藏':['日喀则市','那曲市','山南市','林芝市','昌都市','玉树藏族自治州','西藏区', '拉萨市', '山南地区', '林芝地区', '日喀则地区', '阿里地区', '昌都地区', '那曲地区'],
        '吉林':['延边朝鲜族自治州','吉林省', '吉林市', '长春市', '白山市', '白城市','延边州', '松原市', '辽源市', '通化市', '四平市'],
        '宁夏':['宁夏回族自治区', '银川市', '吴忠市', '中卫市', '石嘴山市', '固原市']
    }
  for i in area_data.items():
    if city in i[1]:
      return i[0]
  city_no.add(city)
  return "未知"
def get_province():
  df=pd.read_csv(CITY_PATH)
  open("D:\\学习\\可视化\\实验\\final\\src\\data\\city.txt","w").write(df['city'].unique().tolist().__str__())
  df["province"]=df["city"].apply(lambda x:city2province(x))
  print(city_no)
  df.to_csv(PROVINCE_PATH,index=False)
  # print(df["province"].count())
# get_province()
# handle_city(DIR+"CN-Reanalysis-daily-2018120100.csv",DIR+"2018120100.csv")
# handle_dir("D:\\学习\\可视化\\大气数据\\201812")
def get_month_city(month):
  _dir=f"D:\\学习\\可视化\\实验\\final\\public\\2018{month}"
  files=os.listdir(_dir)
  df=pd.DataFrame()
  for file in files:
    if(df.empty):
      df=pd.read_csv(_dir+"\\"+file)
      continue
    ndf=pd.read_csv(_dir+"\\"+file)
    # if not df.columns.tolist().__contains__("city") or not ndf.columns.tolist().__contains__("city"):
    #   print(file)
    #   os._exit(0)
    df=pd.merge(df,ndf,how="outer")
    df=df.groupby(["province","city"]).mean().round(3).reset_index()
  path="D:\\学习\\可视化\\实验\\final\\public\\2018"
  try:
    os.makedirs(path)
    print(f"Directory '{path}' created")
  except FileExistsError:
    print(f"Directory '{path}' already exists")
  df.to_csv(f"D:\\学习\\可视化\\实验\\final\\public\\2018\\2018{month}.csv",index=False)
# get_month_city(11)
def download():
  _dir="D:\学习\可视化\大气数据"
  for i in range(1,6):
   content= requests.get(f"http://naq.cicidata.top:10443/chinavis/opendata/download/daily/CN-Reanalysis20180{i}.zip")
   open(_dir+f"\\CN-Reanalysis20180{i}.zip","wb").write(content.content)
# download()
def handle_year():
  year=2018
  for i in range(1,12):
    handle_dir(f"D:\\学习\\可视化\\大气数据\\{year}{str(i).zfill(2)}",f"{year}{str(i).zfill(2)}")
# handle_year()
def handle_year_city():
  year=2018
  for i in range(1,12):
    get_month_city(f"{str(i).zfill(2)}")
# handle_year_city()
def full_year():
  df=pd.DataFrame()
  _dir="D:\\学习\\可视化\\实验\\final\\public\\"
  for i in range(1,12):
    if(df.empty):
      df=pd.read_csv(f"{_dir}2018\\2018{str(i).zfill(2)}.csv")
      continue
    df=pd.merge(df,pd.read_csv(f"{_dir}2018\\2018{str(i).zfill(2)}.csv"),how="inner")
    df=df.groupby(["city","province"]).mean().round(3).reset_index()
  df.to_csv(f"{_dir}year\\2018.csv",index=False)
# full_year()
# df1=pd.read_csv("D:\\学习\\可视化\\实验\\final\\public\\201811\\2018110200.csv")
# df2=pd.read_csv("D:\\学习\\可视化\\实验\\final\\public\\201811\\2018110300.csv")
# df=pd.merge(df1,df2,how="outer")
# print(df.columns)
# df=df.groupby(["province","city"]).mean().reset_index()
# print(df.columns)
# df3=pd.read_csv("D:\\学习\\可视化\\实验\\final\\public\\201811\\2018110400.csv")
# df=pd.merge(df,df3,how="outer")
# df=df.groupby(["province","city"]).mean()
# print(df.columns)
def get_year_city():
  df=pd.DataFrame()
  _dir="D:\\学习\\可视化\\实验\\final\\public\\"
  for i in range(1,12):
    year=2018
    files=os.listdir(f"{_dir}{year}{str(i).zfill(2)}")
    for file in files:
      if(df.empty):
        df=pd.read_csv(f"{_dir}{year}{str(i).zfill(2)}\\{file}")
        df=df[df["city"]=="上海市"]
        df=df.groupby(["province","city"]).mean().round(3).reset_index()
        df["date"]=file.split(".")[0][:8]
        continue
      ndf=pd.read_csv(f"{_dir}{year}{str(i).zfill(2)}\\{file}")
      ndf=ndf[ndf["city"]=="上海市"]
      ndf=ndf.groupby(["province","city"]).mean().round(3).reset_index()
      ndf["date"]=file.split(".")[0][:8]
      df=pd.merge(df,ndf,how="outer")
  print(df.columns)
  print(df.shape)
  df.to_csv(f"{_dir}year\\2018-上海.csv",index=False)
# get_year_city()
def province2area(province):
  areas={
    "南方区域":['江苏', '安徽', '浙江', '上海', '湖北', '湖南', '江西', '福建', '云南', '贵州', '四川', '重庆', '陕西', '广西', '广东', '香港', '澳门', '海南', '台湾'],
    "北方区域":['北京', '天津', '河北', '山西',  '河南',  '山东',  '黑龙江', '吉林', '辽宁'],
    "西北地区":['陕西', '宁夏', '甘肃',  '新疆',"内蒙古"],
    "青藏地区":['西藏', '青海'],
  }
  for i in areas.items():
    if i[1].__contains__(province):
      return i[0]
def get_area():
  
  #sum the number of cities in each area

  df=pd.read_csv("D:\\学习\\可视化\\实验\\final\\public\\year\\2018.csv")
  df["area"]=df.apply(lambda x: province2area(x["province"]),axis=1)
  df.to_csv("D:\\学习\\可视化\\实验\\final\\public\\year\\2018-area.csv",index=False)
# get_area()
def area2json():
  df=pd.read_csv("D:\\学习\\可视化\\实验\\final\\public\\year\\2018-area.csv")
  # print(grouped.groups)
  df["value"]=df.apply(lambda row: int(aqi.to_iaqi(
    aqi.POLLUTANT_PM25, row["PM2.5"]
))*10//(df["province"]==row["province"]).sum(), axis=1)
  df=df.rename(columns={"city":"name"})
  df = df[['province', 'name', 'area', 'value']]
  grouped=df.groupby(["area","province"])
  result = []
  print(df["area"].dropna().unique())
  for item in df["area"].dropna().unique():
    if item!=nan:
      result.append({"name":item,"children":[]})
  # df=df[["area","date","pm25","pm10","so2","no2","co","o3"]]
  for group in grouped:
    group_dict = {}
    group_dict['name'] = group[1]["province"].iloc[0]
    group_dict['children'] = group[1].to_dict(orient='records')
    for list in result:
      if list["name"]==group[0][0]:
        list["children"].append(group_dict)
        break
  # print(result)
  open("test.json","w").write(str(result).replace("'",'"'))
# area2json()
def get_month_aqi():
  df=pd.read_csv("D:\\学习\\可视化\\实验\\final\\public\\year\\2018.csv")
  df["area"]=df.apply(lambda x: province2area(x["province"]),axis=1)
  df=df[["area","province","PM2.5","city"]]
  for i in range(1,13):
    month=pd.read_csv(f"D:\\学习\\可视化\\实验\\final\\public\\2018\\2018{str(i).zfill(2)}.csv")
    df[str(i).zfill(2)]=month["PM2.5"].apply(lambda x: int(aqi.to_iaqi(aqi.POLLUTANT_PM25,x)))
  df.drop(["PM2.5"],axis=1,inplace=True)
  df.to_csv("D:\\学习\\可视化\\实验\\final\\public\\year\\2018-month.csv",index=False)
  df.to_json("D:\\学习\\可视化\\实验\\final\\public\\year\\2018-month.json",orient="records")
# get_month_aqi()
def get_city_pollution_month():
  df=pd.DataFrame()
  for i in range(1,13):
    month=pd.read_csv(f"D:\\学习\\可视化\\实验\\final\\public\\2018\\2018{str(i).zfill(2)}.csv")
    month=month[["province","PM2.5","PM10","SO2","NO2","CO","O3"]]
    month=month.groupby("province").sum().reset_index()
    month["month"]=i
    month["area"]=month.apply(lambda x: province2area(x["province"]),axis=1)
    if df.empty:
      df=month
      continue
    df=pd.merge(df,month,how="outer")
  print(df.columns)
  df.to_json("D:\\学习\\可视化\\实验\\final\\public\\year\\2018-city-month.json",orient="records")
get_city_pollution_month()