'use client';
import Chart from '@/components/Chart';
import DemoSunburst from '@/components/Chart/Sunset';
import Calendar from '@/components/Chart/calendar';
import Echart from '@/components/Chart/echart';
import { Props as GProps } from '@/components/Geo';
import Emap from '@/components/Geo/eMap';
import { Button, DatePicker, Select } from 'antd';
import type { RangePickerProps } from 'antd/es/date-picker';
import * as d3 from 'd3';
import dayjs from 'dayjs';
import customParseFormat from 'dayjs/plugin/customParseFormat';
import { useRef, useState } from 'react';
type Props = Omit<GProps, 'dispatch' | 'stateRef'> & {
	columns: string[];
	city: any;
};
dayjs.extend(customParseFormat);

// eslint-disable-next-line arrow-body-style
const disabledDate: RangePickerProps['disabledDate'] = (current) => {
	// Can not select days before today and today
	const start = dayjs('2018-01-01', 'YYYY-MM-DD');
	const end = dayjs('2018-12-31', 'YYYY-MM-DD');
	return (
		(current && current > end.endOf('day')) || current < start.startOf('day')
	);
};

const Index = ({ datas, weather, city, columns }: Props) => {
	const dispatch = d3.dispatch('update');
	const [date, setDate] = useState(dayjs('2018-01-01', 'YYYY-MM-DD'));
	const handleChange = (value: any, type: 'date' | 'type') => {
		stateRef.current[type] = value;
		if (type == 'date') setDate(value);
		console.log(`selected ${value}`);
		dispatch.call('update', null, { type: type, value: value });
	};
	dispatch.on('update.console', (context) => {
		const { type, value } = context;
		if (type == 'date' && value != date.format('YYYYMMDD')) {
			console.log(value);
			setDate(dayjs(value, 'YYYYMMDD'));
		}
	});
	let time = useRef<any>();
	const handlePlay = () => {
		if (text == '播放') {
			time.current = setInterval(() => {
				const date = stateRef.current.date.add(1, 'day');
				stateRef.current.date = date;
				setDate(date);
				if (date.isAfter('2018-12-31')) {
					clearInterval(time.current);
					setText('播放');
					return;
				}
				dispatch.call('update', null, { type: 'date', value: date });
			}, 1000);
		} else {
			console.log('clear');
			clearInterval(time.current);
		}
		setText(text == '播放' ? '暂停' : '播放');
	};
	const [text, setText] = useState('播放');
	const stateRef = useRef({
		type: columns[0],
		date: dayjs('2018-01-01', 'YYYY-MM-DD'),
	});
	const [area, setArea] = useState('');
	return (
		<>
			<div>
				<Select
					defaultValue={columns[0]}
					style={{ width: 120 }}
					onChange={(v) => handleChange(v, 'type')}
					options={columns.map((d) => ({ value: d, label: d }))}
				/>
				<DatePicker
					format='YYYY-MM-DD'
					value={date}
					onChange={(v) => handleChange(v, 'date')}
					disabledDate={disabledDate}
					defaultValue={dayjs('2018-01-01', 'YYYY-MM-DD')}
				/>
				<Button onClick={handlePlay}>{text}</Button>
			</div>
			<Emap
				stateRef={stateRef.current}
				dispatch={dispatch}
				datas={datas}
				weather={weather}
			></Emap>
			<Chart
				stateRef={stateRef.current}
				datas={weather}
				dispatch={dispatch}
			></Chart>
			<Calendar
				dispatch={dispatch}
				datas={city}
				stateRef={stateRef.current}
			></Calendar>
			<DemoSunburst setArea={setArea}></DemoSunburst>
			<Echart area={area}></Echart>
		</>
	);
};
export default Index;
