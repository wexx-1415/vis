import dayjs from "dayjs";
import * as d3 from "d3";
const getData = async (date: dayjs.Dayjs) => {
	const data = await d3.csv(
		`/${date.format('YYYYMM')}/${date.format('YYYYMMDD00')}.csv`
	);
	return data;
};
const getIndex = (value: number, min: string, max: string, len: number) => {
	return Math.floor(
		((value - parseFloat(min.trim())) /
			(parseFloat(max.trim()) - parseFloat(min.trim()))) *
			len
	);
};
export  {getData, getIndex};