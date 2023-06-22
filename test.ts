const fs = require('fs');

let json = JSON.parse(
	fs.readFileSync(
		'D:\\学习\\可视化\\实验\\final\\public\\year\\2018-month.json'
	)
);
let newjson = [];
let tjson = [];
const sumOfKey = (arr, key) => {
	return arr.reduce((prev, cur) => {
		if (cur.area === key) {
			return prev + 1;
		} else {
			return prev;
		}
	}, 0);
};
// json = json.filter((item) => item.area === '北方区域');
json.forEach((e) => {
	const index = tjson.findIndex(
		(item) => item.province === e.province && item.month === e.month
	);
	if (index === -1) {
		delete e['city'];
		tjson.push(e);
	} else {
		delete e['city'];
		for (let key in e) {
			if (key !== 'area' && key !== 'month' && key !== 'province') {
				tjson[index][key] += e[key];
			}
		}
	}
});
tjson.forEach((item) => {
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
});
console.log(sumOfKey(newjson, '北方区域'));
fs.writeFileSync('./test1.json', JSON.stringify(newjson));
// console.log(newjson);
