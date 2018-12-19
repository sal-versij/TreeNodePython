<# self.header(inherit="./master.pml", title="Home Page") #/>
<link href="/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="/dist/css/flow-text.css" rel="stylesheet">
<# self.container(id="Head") #/>
<style>
    .card {
        width: 250px;
        position: absolute;
        top: 10%;
        left: 10%;
    }

    .card .card-body {
        padding: 0;
        display: block;
        position: relative;
    }

    .card .card-body .gates {
        padding-left: 0;
        padding-right: 0;
    }

    .card .card-body .content {
        padding-left: 5px;
        padding-right: 5px;
    }

    .gates li {
    }

    .gates li:hover {
        opacity: 0.5;
    }

    .gates.output li {
        text-align: right;
    }

    .color {
        color: white;
    }

    .color.class.green {
        border: 0.1rem solid green;
    }

    .color.class.red {
        border: 0.1rem solid red;
    }

    .color.class.blue {
        border: 0.1rem solid blue;
    }

    .color.class.black {
        border: 0.1rem solid black;
    }
</style>
<# self.container(id="Body") #/>
<div id="main">
    <div class="card">
        <div class="card-header text-center">
            <span>Titolo</span>
        </div>
        <div class="card-body my-2">
            <div class="container-fluid">
                <div class="row">
                    <div class="col-md-1 gates input">
                        <ul class="list-unstyled">
                            <li><span class="color class green"></span></li>
                        </ul>
                    </div>
                    <div class="col-md-10 content">
                        <div class="form-inline">
                            <div class="input-group-prepend">
                                <div class="input-group-text">@</div>
                            </div>
                            <input style="width:70%;" type="text" class="form-control" name="miao" id="miao"
                                   placeholder="sdf">
                        </div>
                    </div>
                    <div class="col-md-1 gates output">
                        <ul class="list-unstyled">
                            <li><span class="color class green"></span></li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
<# self.container(id="Scripts") #/>