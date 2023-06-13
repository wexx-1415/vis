import { DatePicker } from 'antd';
import type { RangePickerProps } from 'antd/es/date-picker';
import dayjs from 'dayjs';
import customParseFormat from 'dayjs/plugin/customParseFormat';
import React from 'react';
dayjs.extend(customParseFormat);

// eslint-disable-next-line arrow-body-style
const disabledDate: RangePickerProps['disabledDate'] = (current) => {
	// Can not select days before today and today
	const start = dayjs('2018-12-01', 'YYYY-MM-DD');
	const end = dayjs('2018-12-31', 'YYYY-MM-DD');
	return (
		(current && current > end.endOf('day')) || current < start.startOf('day')
	);
};

const App: React.FC = () => (
	<DatePicker
		format='YYYY-MM-DD'
		disabledDate={disabledDate}
		defaultValue={dayjs('2018-12-01', 'YYYY-MM-DD')}
	/>
);

export default App;
