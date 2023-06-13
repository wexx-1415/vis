'use client';
import { getData, getIndex } from '@/utils/svg';
import { hiddenTip, setTip } from '@/utils/tip';
import * as d3 from 'd3';
import dayjs from 'dayjs';
import { useCallback, useEffect, useRef } from 'react';
export type Props = {
	datas: any;
	dispatch: d3.Dispatch<object>;
	weather?: any;
	width?: number;
	height?: number;
	stateRef: {
		type: string;
		date: dayjs.Dayjs;
	};
};

export default function Home({
	datas,
	weather,
	stateRef,
	width,
	height,
	dispatch,
}: Props) {
	const ref = useRef(null);

	width = width || 600;
	height = height || 600;
	const update = useCallback(
		(name: string, data?: any) => {
			data = data || weather;
			console.log(name);
			const color = d3.interpolateRgb('white', 'red');
			let [min, max] = d3.extent(data, (d) => d[name]);
			const colors = d3.schemeCategory10;
			d3.select(ref.current)
				.selectAll('circle')
				.transition()
				.duration(200)
				.attr('fill', (d) => {
					const value = d[name];
					return color(
						getIndex(value, min, max, colors.length) / colors.length
					);
				});
			d3.select(ref.current)
				.selectAll('path')
				.transition()
				.duration(200)
				.attr('fill', (d) => {
					//@ts-ignore
					const province = weather.find(
						(w) => w.province === d.properties.name
					);
					const value = parseFloat(province ? province[name].trim() : 100);
					return color(
						getIndex(value, min, max, colors.length) / colors.length
					);
				});
		},
		[weather]
	);
	useEffect(() => {
		let [min, max] = d3.extent(weather, (d) => d['PM2.5']);
		const color = d3.interpolateRgb('white', 'red');
		const svg = d3
			.select(ref.current)
			.style('width', width + 60)
			.style('overflow', 'hidden')
			.style('height', height + 80);
		const aProjection = d3.geoMercator().fitExtent(
			[
				[0, 0],
				[width, height],
			],
			datas
		);
		// .center([107, 31]) //地图中心位置,107是经度，31是纬度
		// .scale(920) //设置缩放量
		// .translate([width / 2, height / 2 + 200]); // 设置平移量
		// 指定投影
		const path = d3.geoPath(aProjection);
		const colors = d3.schemeCategory10;
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
						update(value, data);
					})
					.catch((e) => {
						console.error(e);
					});
			} else if (type == 'date') {
				stateRef.date = dayjs(value);
				getData(dayjs(value))
					.then((data) => {
						update(stateRef.type, data);
					})
					.catch((e) => {
						console.error(e);
					});
			}
		});
		const zoomed = ({ transform }: { transform: d3.ZoomTransform }) => {
			svg.attr('transform', transform.toString());
		};
		svg.call(
			d3
				.zoom()
				.extent([
					[0, 0],
					[648, 480],
				])
				.scaleExtent([1, 3])
				.on('zoom', zoomed)
		);
		svg
			.append('text')
			.text('全国污染物分布图')
			.attr('x', 250)
			.attr('y', 40)
			.attr('font-size', 20)
			.attr('fill', 'black');
		svg
			.append('g')
			.selectAll('path')
			.data(datas.features)
			.join('path')
			.attr('stroke', 'black')
			.attr('fill', (d) => {
				//@ts-ignore
				const province = weather.find((w) => w.province === d.properties.name);
				const value = parseFloat(province ? province['PM2.5'].trim() : 100);
				return color(getIndex(value, min, max, colors.length) / colors.length);
			})
			.attr('d', path)
			.on('mouseover', function (e, d) {
				//@ts-ignore
				const province = weather.find((w) => w.province === d.properties.name);
				//@ts-ignore
				const rect = this.getBoundingClientRect();
				//@ts-ignore
				setTip(
					rect,
					d.properties.name,
					path.centroid(d),
					0,
					svg.node().getBoundingClientRect().top
				);
			})
			.on('mouseout', function (e, d) {
				hiddenTip();
			});
	}, [datas, dispatch, height, update, weather, width]);
	return <svg id='geo' ref={ref}></svg>;
}
