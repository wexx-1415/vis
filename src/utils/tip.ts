const setTip = (
	rect: DOMRect,
	text: string,
	[left, top]: [number, number],
	x?: number,
	y?: number
) => {
	const tip = document.getElementById('tip');

	x = x || 0;
	tip.innerHTML = text;
	tip.style.display = 'block';
	tip.style.zIndex = '1000';
	const tipWidth = tip.getBoundingClientRect().width;
	// console.log(rect, left, top, y);
	tip.style.left = left + 'px';
	tip.style.top = top + 'px';
};

const hiddenTip = () => {
	const tip = document.getElementById('tip');

	tip.style.display = 'none';
};
export { setTip, hiddenTip };
