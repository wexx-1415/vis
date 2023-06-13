'use client';
import dayjs from 'dayjs';
import * as echarts from 'echarts';
import { useEffect, useRef } from 'react';
import { getData } from '../../utils/svg';
import './china.js';
import { Props } from './index.jsx';
const getProvinces = (datas: any, key: string) => {
	const provinces = [];
	datas.forEach((d: any) => {
		let it = provinces.find((p: any) => p.province === d.province);
		if (!it) {
			it = { name: d.province, value: d[key] };
			provinces.push(it);
		} else {
			it.value += d[key];
		}
	});
	return provinces;
};
const getRank = (datas: any, key: string) => {
	datas = datas.sort((a: any, b: any) => b[key] - a[key]).slice(0, 10);
	datas.forEach((e) => {
		e.name = e.province;
		e.value = [e.lon, e.lat];
	});
	console.log(datas);
	return datas;
};
const getOption = (
	datas: any,
	stateRef: {
		type: string;
		date: dayjs.Dayjs;
	}
) => {
	const provinces = getProvinces(datas, stateRef.type);
	const rank = getRank(datas, stateRef.type);
	const option = {
		tooltip: {
			// 数据格式化
			formatter: function (params, callback) {
				return stateRef.type + '<br />' + params.name + '：' + params.value;
			},
			// trigger:"none"
		},
		title: {
			text: '全国污染物分布图',
			textAlign: 'auto',
			left: 'center',
		},
		visualMap: {
			min: 0,
			max: 1000,
			left: 'left',
			top: 'bottom',
			text: ['高', '低'], //取值范围的文字
			inRange: {
				color: ['#30E8BF', '#EB3349'], //取值范围的颜色
			},
			show: true, //图注
		},
		geo: {
			map: 'china',
			roam: false, //不开启缩放和平移
			zoom: 1.23, //视角缩放比例
			label: {
				normal: {
					show: true,
					fontSize: '10',
					color: 'rgba(0,0,0,0.7)',
				},
			},
			itemStyle: {
				normal: {
					borderColor: 'rgba(0, 0, 0, 0.2)',
				},
				emphasis: {
					areaColor: '#FC5C7D', //鼠标选择区域颜色
					shadowOffsetX: 0,
					shadowOffsetY: 0,
					shadowBlur: 20,
					borderWidth: 0,
					shadowColor: 'rgba(0, 0, 0, 0.5)',
				},
			},
		},
		series: [
			{
				name: '省份',
				type: 'map',
				geoIndex: 0,
				data: provinces,
			},
			{
				name: '在地图中显示散点图',
				type: 'scatter',
				coordinateSystem: 'geo', //设置坐标系为 geo
				data: rank,
				itemStyle: {
					color: '#6A82FB',
				},
			},
		],
	};
	return option;
};
const Emap = ({ weather, datas, stateRef, dispatch }: Props) => {
	console.log(weather, datas, stateRef);
	console.log(getProvinces(weather, stateRef.type));
	const option = getOption(weather, stateRef);

	const ref = useRef(null);
	useEffect(() => {
		const chart = echarts.init(ref.current);
		chart.setOption(option);
		dispatch.on('update.geo', (context) => {
			console.error(context + 'update');
			const { type, value } = context;
			if (type == stateRef.type) {
				return;
			}
			if (type == 'type') {
				stateRef.type = value;
				getData(stateRef.date)
					.then((data) => {
						const option = getOption(data, stateRef);
						chart.setOption(option);
					})
					.catch((e) => {
						console.error(e);
					});
			} else if (type == 'date') {
				stateRef.date = dayjs(value);
				getData(dayjs(value))
					.then((data) => {
						const option = getOption(data, stateRef);
						chart.setOption(option);
					})
					.catch((e) => {
						console.error(e);
					});
			}
		});
	}, [stateRef]);
	return (
		<div
			id='main'
			ref={ref}
			style={{ width: '600px', height: 600, display: 'inline-block' }}
		></div>
	);
};
export default Emap;
