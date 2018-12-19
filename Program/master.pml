<# self.header() #/>
<# self.create_container(id="Head") #/>
<# self.create_container(id="Body") #/>
<# self.create_container(id="Scripts") #/>

<html lang="en">
<head>
    <# self.println(title=lambda _: _["title"]) #/>
    <title>{title}</title>
    <meta charset="UTF-8">
    <meta content="width=device-width, initial-scale=1, shrink-to-fit=no" name="viewport">
    <link href="/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="/dist/css/flow-text.css" rel="stylesheet">
    <# self.set_container_point(id="Head") #/>
</head>
<body>
<header class="navbar-fixed">
    <nav class="navbar navbar-dark bg-dark">
        <a class="navbar-brand" href="/">Python Tree Node Editor</a>
        <button aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation" class="navbar-toggler"
                data-target="#navbarNav" data-toggle="collapse" type="button">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item active"><a class="nav-link" href="#">Home</a></li>
            </ul>
        </div>
    </nav>
</header>

<section style="height:100%;">
    <# self.set_container_point(id="Body") #/>
</section>

<footer>
    <div class="container-fluid text-white bg-dark p-100">

    </div>
</footer>

<section>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="/dist/js/bootstrap.bundle.min.js"></script>
    <script src="/dist/js/holder.min.js"></script>
    <script src="https://use.fontawesome.com/releases/v5.5.0/js/all.js"></script>

    <script src="https://cdn.jsdelivr.net/gh/sal-versij/TurtleFrameWork@master/Utils.js"></script>
    <# self.set_container_point(id="Scripts") #/>
</section>
</body>
</html>