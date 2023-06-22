
可视化5组 大气数据图表联动分析系统
## 项目总览 - 数据部分
- 首先, 我们借助pandas和MySQL对数据进行基本的处理, 对每条数据标注上省份城市, 并计算出对应的aqi
- 通过pandas或者js计算每个城市每个省份以及全国范围内每个污染物以及aqi在一个月, 一年的平均. 
- 根据时间保存一份, 比如说将2018年1月份的全国城市的数据保存一份
- 根据地区保存一份, 比如将上海市2018年12个月的数据保存一份
- 可以借助这些数据进行不同地区同一时间上的对比, 和相同地区不同时间上的对比
- 日历图之类的图表需要的是扁平的数据, 就用csv的格式进行存储, 读取的时候再用d3进行解析
- 旭日图这样需要嵌套类型数据的图表, 我们用json格式来存储
## 项目总览 - 图表部分
- 前端部分使用 `react` + `typescript` 编写, 采用 `next.js` 框架
- 可视化部分使用 `d3js` 和 `antv` 以及 `echart`编写
- 项目图表分为两组图, 每组图包含3个子图, 子图之间可以进行图表联动
- 每个图我们设置有对应的工具提示, 提供良好的交互体验
- 第一组图分别有3个小的子图, 第一个是全国范围内的中国污染物浓度分布图, 对于浓度高的省份我们用红色的颜色表示污染严重, 浓度低的颜色是绿色, 其余浓度使用插值
- 第二个图是污染物浓度最高的10个城市的排名图
- 第三个图是当前年份污染物分布日历图, 如果一天的污染物浓度比较高, 那么对应日期的矩形的颜色也是地图一样的处理方式
- 第一组图设有一个控制台, 可以更改当前所有子图的日期以及污染物类型, 当更改这两个变量时, 3个子图的数据都会同步更新, 实现图表间的联动
- 同时也可以点击日历图上对应的日期, 3个图表的日期也会同步更改
- 对于中国地图, 我们使用geojson进行绘制
- 第二组图同样包含3个子图, 分别是aqi分布旭日图, 描述的是不同的地区aqi的含量分布
- 第二个子图是aqi分布的雷达图, 描述的是对应地区aqi在12个小时内的变化
- 第3个子图是污染物比例变化图, 描述的对应地区的6种污染物在12个月份的含量比例变化
- 当点击旭日的某一个具体地区时, 旭日会展开到对应地区, 然后另外2个子图的状态也会同步更新, 数据变化到对应的地区

## 图表联动
- 借助 `d3.dispatch` 自定义事件来实现图表间的状态共享
```ts
//定义dispatch
const dispatch = d3.dispatch('update');
//调用事件, 并给事件传送参数
dispatch.call('update', null, { type: type, value: value });
//监听事件, 不同的组件用.加以区分, 执行调用函数
dispatch.on('update.chart', (context) => {
	const { type, value } = context;
  //对事件进行处理
})
```
- 借助 `react` 状态管理实现状态共享
```ts
//日期选择器的状态是用state维护的
const [date, setDate] = useState(dayjs('2018-01-01', 'YYYY-MM-DD'));
//当通过日历图改变时间时,也要改变日期选择器的时间
dispatch.on('update.console', (context) => {
		const { type, value } = context;
		if (type == 'date' && value != date.format('YYYYMMDD')) {
			console.log(value);
			setDate(dayjs(value, 'YYYYMMDD'));//更改组件状态, 实现状态共享
		}
	});
```
## 图表更新
创建一个更新函数, 在状态改变时, 传入相应的数据, 动过`join`机制更新d3图表
```ts
//日历图的更新函数
const update = useCallback(
		(name: string, data?: any) => {
			data = data || datas;
			const svg = d3.select(ref.current);
      //计算当前污染物浓度的最大值
			let max = Math.max(...datas.map((d) => parseFloat(d[stateRef.type])));
      //颜色插值
			const color = d3.interpolateRgb('#30E8BF', '#EB3349');
			svg
				.selectAll('rect')
				.data(datas)//更新数据
				.join('rect')
				.transition()//增加过渡
				.duration(200)
        //应用颜色插值
				.attr('fill', (d, i) => color(parseFloat(d[stateRef.type]) / max));
		},
		[datas]
	);
```
## 数据获取
- nextjs是react的ssr框架, 可以通过ssr在服务端就将数据处理好传送给d3图表, 首屏加载会更快
```ts
//读取数据并并d3处理
const weather = fs
		.readFileSync(path.join(PublicPath, '201801\\2018010100.csv'))
		.toString();
const weatherData = d3.csvParse(weather);
```
- 数据更新时需要从服务端获取数据, 如果是csv的数据, 需要用d3处理一下, 如果是json的数据, 直接用就可以
```ts
//封装数据获取函数, 由于数据是放在根目录下, 并且用日期命名所以可以很好的封装
const getData = async (date: dayjs.Dayjs) => {
	const data = await d3.csv(
		`/${date.format('YYYYMM')}/${date.format('YYYYMMDD00')}.csv`
	);
	return data;
};
```
## 数据处理
- 对于扁平的数据, 使用pandas进行处理
```python
  #利用MySQL的ST_Intersects函数求当前坐标所处的省份和城市, 再插入到dataFrame中, 最后保存到csv中
  cursor = db.cursor()
  sql="SELECT id,deep,name FROM geo WHERE ST_Intersects(polygon, ST_GeomFromText('POINT(%s %s)',0))=1"
  for i in range(len(df)):
    cursor.execute(sql,[float(df.loc[i]["lon"]),float(df.loc[i]["lat"])])
    data=cursor.fetchall()
    df.loc[i,"city"]=data

  #删除列名和数据上多余的空格
  df.columns = df.columns.str.replace(" ", "").str.replace("\(.+\)$", "")
  df.apply(lambda x: x.replace(" ", ""))

  #由于下载的数据是每日在一个文件, 所以计算月份平均的时候需要将数据合并
  files=os.listdir(_dir)
  #将一个目录下的数据合并
  df=pd.DataFrame()
  for file in files:
    if(df.empty):
      df=pd.read_csv(_dir+"\\"+file)
      continue
    ndf=pd.read_csv(_dir+"\\"+file)
    df=pd.merge(df,ndf,how="outer")
  #对数据分组求平均
  df=df.groupby(["province","city"]).mean().round(3).reset_index()
  #保存csv时需要新建一个目录
  try:
    os.makedirs(path)
    print(f"Directory '{path}' created")
  except FileExistsError:
    print(f"Directory '{path}' already exists")
```
- 对于一些pandas不太好处理的结构或者由于前端图表需要而特有的数据结构在pandas上不便处理, 我们可以用js进行处理
```ts
//求一个对象数组中, 有多少个对象的某个属性为特定值, 这是为了对这个属性求平均数
//利用reduce可以很好的完成
const sumOfKey = (arr, key) => {
	return arr.reduce((prev, cur) => {
		if (cur.area === key) {
			return prev + 1;
		} else {
			return prev;
		}
	}, 0);
};

//为了构造如下形式的
/**{
		"area": "南方区域",
		"province": "上海",
		"month": "10",
		"value": 0.4068627450980392
	},
	{
		"area": "南方区域",
		"province": "上海",
		"month": "11",
		"value": 0.7990196078431373
	},
*/
let obj = {};
for (const key in item) {
	if (key !== 'area' && key !== 'province' && key !== 'city') {
			obj['area'] = item.area;
			obj['province'] = item.province;
			obj['city'] = item.city;
			obj['month'] = key;
			obj['value'] = item[key] / sumOfKey(json, item.area);
			newjson.push(obj);
			obj = {};
		}
	}
```
- 在做插值计算或者计算比例的时候可能需要对数据进行归一化, 归一化可以在前端做也可以在后端做
```ts
//这里展示前端的归一化
const getIndex = (value: number, min: string, max: string, len: number) => {
	return Math.floor(
		((value - parseFloat(min.trim())) /
			(parseFloat(max.trim()) - parseFloat(min.trim()))) *
			len
	);
```
