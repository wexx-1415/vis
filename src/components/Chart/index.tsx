'use client';
import { getData } from '@/utils/svg';
import * as d3 from 'd3';
import dayjs from 'dayjs';
import { useCallback, useEffect, useRef } from 'react';
interface Props {
	datas: d3.DSVRowArray<string>;
	dispatch: d3.Dispatch<object>;
	width?: number;
	stateRef: {
		type: string;
		date: dayjs.Dayjs;
	};
	height?: number;
}
export default function Home({
	dispatch,
	stateRef,
	datas,
	width,
	height,
}: Props) {
	const ref = useRef(null);
	// const stateRef = useRef({
	width = width || 800;
	height = height || 500;
	const update = useCallback(
		(name: string, data?: any) => {
			data = data || datas;
			data = data.sort((a, b) => b[stateRef.type] - a[stateRef.type]);
			console.log(data);
			const svg = d3.select(ref.current);
			const margin = { top: 20, right: 50, bottom: 30, left: 120 };

			let min = Math.min(...data.map((d) => d[stateRef.type]));
			let max = Math.max(...data.map((d) => d[stateRef.type]));
			console.log(min, max);
			const x = d3.scaleLinear().domain([min, max]).range([0, width]);
			const y = d3
				.scaleBand()
				.domain(data.slice(0, 10).map((d) => d.city))
				.range([0, height])
				.padding(0.1);
			const xAxis = d3.axisBottom(x).ticks(10);
			const yAxis = d3.axisLeft(y);
			svg.selectAll('.x-axis').transition().duration(300).call(xAxis);
			svg.selectAll('.y-axis').transition().duration(300).call(yAxis);

			svg
				.selectAll('rect')
				.data(data.slice(0, 10))
				.join('rect')
				.transition()
				.duration(300)
				.attr('fill', 'url(#gradient)')
				.attr('x', margin.left)
				.attr('y', (d) => y(d.city))
				.attr('width', (d) => x(d[stateRef.type]))
				.attr('height', y.bandwidth());
		},
		[datas]
	);
	useEffect(() => {
		const svg = d3
			.select(ref.current)
			.style('width', width + 60)
			.style('height', height + 80);
		const data = datas
			.sort((a, b) => {
				return parseFloat(b[stateRef.type]) - parseFloat(a[stateRef.type]);
			})
			.slice(0, 11);
		const margin = { top: 20, right: 50, bottom: 30, left: 120 };
		dispatch.on('update.chart', (context) => {
			console.error(context + 'chart');
			const { type, value } = context;
			if (type == stateRef.type) {
				return;
			}
			if (type == 'type') {
				stateRef.type = value;
				getData(stateRef.date)
					.then((data) => {
						update(value, data.slice(0, 11));
					})
					.catch((e) => {
						console.error(e);
					});
			} else if (type == 'date') {
				stateRef.date = dayjs(value);
				getData(dayjs(value))
					.then((data) => {
						update(stateRef.type, data.slice(0, 11));
					})
					.catch((e) => {
						console.error(e);
					});
			}
		});
		const [min, max] = d3.extent(data, (d) => d[stateRef.type]).map(parseFloat);
		const x = d3.scaleLinear().domain([min, max]).range([0, width]);
		const y = d3
			.scaleBand()
			.domain(data.slice(0, 10).map((d) => d.city))
			.range([0, height])
			.padding(0.1);
		const xAxis = d3.axisBottom(x).ticks(10);
		const yAxis = d3.axisLeft(y);
		svg.selectAll('g').remove();
		svg
			.append('g')
			.attr('class', 'x-axis')
			.attr('transform', `translate(${margin.left},${height})`)
			.call(xAxis);
		svg
			.append('g')
			.attr('class', 'y-axis')
			.attr('transform', `translate(${margin.left},0)`)
			.call(yAxis);
		svg.style('overflow', 'visible');
		svg
			.append('text')
			.text('污染物最严重的10个城市')
			.attr('x', 200)
			.attr('y', -10)
			.attr('font-size', 20)
			.attr('fill', 'black');
		svg
			.append('defs')
			.append('linearGradient')
			.attr('id', 'gradient')
			.attr('x1', '0%')
			.attr('y1', '0%')
			.attr('x2', '100%')
			.attr('y2', '0%')
			.selectAll('stop')
			.data([
				{ offset: '0%', color: '#30E8BF' },
				{ offset: '100%', color: '#EB3349' },
			])
			.enter()
			.append('stop')
			.attr('offset', function (d) {
				return d.offset;
			})
			.attr('stop-color', function (d) {
				return d.color;
			});
		svg
			.selectAll('rect')
			.data(data.slice(0, 10))
			.enter()
			.append('rect')
			.attr('fill', 'url(#gradient)')
			.attr('x', margin.left)
			.attr('y', (d) => y(d.city))
			.attr('width', (d) => x(d[stateRef.type]))
			.attr('height', y.bandwidth());
	}, [datas, height, width]);
	return <svg id='abc' ref={ref}></svg>;
}
