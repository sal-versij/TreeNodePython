<# self.header(inherit="./master.pml", title="Home Page") #/>
<# self.container(id="Head") #/>
<# self.container(id="Body") #/>
<div id="main"></div>
<# self.container(id="Scripts") #/>
<script>
	draw = SVG('main').size('100%', '100%').panZoom();

	const background = draw.pattern(20, 20, function (add) {
		add.rect(20, 20).fill('#bbb');
		add.rect(19, 19).radius(3);
	});

	const card = draw.group();
	card.add(draw.rect(60, 90).fill('#333').radius(10));
	card.add(draw.rect(59, 89).fill('#000').radius(10));

	let rect = draw.rect('1000%', '1000%').fill(background);
	let r = [card.];
</script>