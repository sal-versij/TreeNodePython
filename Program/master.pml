<# self.header() #/>
<# self.create_container(id="Head") #/>
<# self.create_container(id="Body") #/>
<# self.create_container(id="Scripts") #/>

<html lang="en">
<head>
	<# self.println(title=lambda _: _["title"]) #/>
	<title>{title}</title>
	<meta charset="UTF-8">
	<link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"
	      rel="stylesheet">
	<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
	<# self.set_container_point(id="Head") #/>
</head>
<body>
<header class="navbar-fixed">
	<nav class="nav-extended blue darken-3">
		<div class="nav-wrapper">
			<a class="brand-logo center hide-on-med-and-down" href="/">Logo</a>
			<ul class="left" id="nav-mobile">
				<li><a href="/">Home</a></li>
			</ul>
		</div>
		<div class="nav-content">
			<ul class="tabs tabs-transparent">
				<li class="tab"><a class="active" href="#tab1">asd</a></li>
			</ul>
		</div>
	</nav>
</header>

<section style="height:100%;">
	<# self.set_container_point(id="Body") #/>
</section>

<footer class="page-footer blue-grey darken-4">
	<div class="container">
		<div class="row">
			<div class="col l6 s12">
				<h5 class="white-text">Footer Content</h5>
				<p class="grey-text text-lighten-4">You can use rows and columns here to organize your
				                                    footer
				                                    content.</p>
			</div>
			<div class="col l4 offset-l2 s12">
				<h5 class="white-text">Links</h5>
				<ul>
					<li><a class="grey-text text-lighten-3" href="#">Link 1</a></li>
				</ul>
			</div>
		</div>
	</div>
	<div class="footer-copyright">
		<div class="container">
			<a class="grey-text text-lighten-4 right" href="#">More Links</a>
		</div>
	</div>
</footer>

<section>
	<script crossorigin="anonymous"
	        integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8="
	        src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
	<script src="https://cdn.jsdelivr.net/gh/sal-versij/TurtleFrameWork@master/Utils.js"></script>
	<# self.set_container_point(id="Scripts") #/>
	<script type="text/javascript">
		$(document).ready(function () {
			$('.sidenav').sidenav();
			$('.dropdown-trigger').dropdown();
		});
	
	</script>
</section>
</body>
</html>
