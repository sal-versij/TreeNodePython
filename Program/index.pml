<# self.header(inherit="./master.pml", title="Home Page") #/>
<# self.container(id="Head") #/>
<# self.container(id="Body") #/>
<div id="main"></div>
<# self.container(id="Scripts") #/>
<script>
	draw = SVG('main').size('100%', '100%').panZoom();

	const card = draw.group();
	card.add(draw.rect(60, 90).fill('#aaa').radius(10));
	card.draggy();

</script>