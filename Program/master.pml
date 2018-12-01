<# self.header() #>
<# self.create_container(id="Head") #>
<# self.create_container(id="Body") #>
<# self.create_container(id="Scripts") #>

<html>
<head>
    <# self.println(title=lambda _: _["title"]) #>
    <title>{title}</title>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"
          integrity="sha256-OweaP/Ic6rsV+lysfyS4h+LM6sRwuO3euTYfr6M124g=" crossorigin="anonymous"/>
    <# self.set_container_point(id="Head") #>
</head>
<body>
<header></header>

<section>
    <# self.set_container_point(id="Body") #>
</section>

<footer></footer>

<section>
    <script src="https://code.jquery.com/jquery-3.3.1.min.js"
            integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"
            integrity="sha256-U/cHDMTIHCeMcvehBv1xQ052bPSbJtbuiw4QA9cTKz0=" crossorigin="anonymous"></script>
    <# self.set_container_point(id="Scripts") #>
</section>
</body>
</html>