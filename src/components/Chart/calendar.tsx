'use client';
import { hiddenTip, setTip } from '@/utils/tip';
import * as d3 from 'd3';
import dayjs from 'dayjs';
import { useCallback, useEffect, useRef } from 'react';
dayjs.locale('zh-cn');
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
export default function Calendar({
	dispatch,
	stateRef,
	datas,
	width,
	height,
}: Props) {
	const ref = useRef(null);
	// const stateRef = useRef({
	width = width || 1500;
	height = height || 500;
	const update = useCallback(
		(name: string, data?: any) => {
			data = data || datas;
			const svg = d3.select(ref.current);
			let max = Math.max(...datas.map((d) => parseFloat(d[stateRef.type])));
			const color = d3.interpolateRgb('#30E8BF', '#EB3349');
			svg
				.selectAll('rect')
				.data(datas)
				.join('rect')
				.transition()
				.duration(200)
				.attr('fill', (d, i) => color(parseFloat(d[stateRef.type]) / max));
		},
		[datas]
	);
	useEffect(() => {
		const svg = d3
			.select(ref.current)
			.style('width', width + 60)
			.style('height', height + 80);
		let max = Math.max(...datas.map((d) => parseFloat(d[stateRef.type])));
		const color = d3.interpolateRgb('#30E8BF', '#EB3349');
		dispatch.on('update.calendar', (context) => {
			const { type, value } = context;
			if (type == 'type') {
				stateRef.type = value;
				update(value);
			}
		});
		svg
			.selectAll('rect')
			.data(datas)
			.join('rect')
			.attr('fill', (d, i) => color(parseFloat(d[stateRef.type]) / max))
			.attr('x', (d, i) => Math.floor(i / 7) * 30)
			.attr('y', (d, i) => (i % 7) * 30)
			.attr('width', 25)
			.attr('height', 25)
			.attr('transform', 'translate(100, 30)')
			.attr('rx', 2)
			.attr('ry', 2)
			.on('mouseover', function (e, d) {
				console.log(d);
				setTip(
					this.getBoundingClientRect(),
					dayjs(d.date, 'YYYYMMDD').format('YYYY[年]-MM[月]-DD[日: ]') +
						d[stateRef.type],
					[this.getBoundingClientRect().left, e.clientY]
				);
				0, this.getBoundingClientRect().top;
			})
			.on('mouseout', () => {
				hiddenTip();
			})
			.on('click', (e, d) => {
				console.log(d.date);
				dispatch.call('update', null, { type: 'date', value: d.date });
			});
		svg.style('overflow', 'visible');
		svg
			.append('text')
			.text('全国污染物浓度日历图')
			.attr('x', 200)
			.attr('y', -10)
			.attr('font-size', 20)
			.attr('fill', 'black');
	}, [datas, height, width]);
	return <svg id='calendar' ref={ref}></svg>;
}
