import * as d3 from 'd3';
import fs from 'fs';
import path from 'path';
import Index from './index';
export default function Home() {
	const dir = 'D:\\学习\\可视化\\实验\\final\\src\\data';
	const paths = path.join(dir, 'gdppercapita_us_inflation_adjusted.csv');
	const PublicPath = 'D:\\学习\\可视化\\实验\\final\\public';
	const csv = fs.readFileSync(paths).toString();
	const datas = d3.csvParse(csv);
	const geojson = fs.readFileSync(path.join(dir, 'country.json')).toString();
	const geo = JSON.parse(geojson);
	const weather = fs
		.readFileSync(path.join(PublicPath, '201812\\2018120100.csv'))
		.toString();
	const weatherData = d3.csvParse(weather);
	const city = fs
		.readFileSync(path.join(PublicPath, '\\year\\2018-上海.csv'))
		.toString();

	// console.log(weatherData.columns);
	return (
		<>
			{/* <Chart datas={datas}></Chart> */}
			{/* <Geo dispatch={dispatch} datas={geo} weather={weatherData}></Geo> */}
			
			<Index
				columns={weatherData.columns.slice(2, weatherData.columns.length - 2)}
				datas={geo}
				city={d3.csvParse(city)}
				weather={weatherData}
			></Index>
		</>
	);
}
