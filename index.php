<html>
 <head>
  	<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>推荐系统</title>

    <link rel="stylesheet" href="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css">
	<script src="https://cdn.staticfile.org/jquery/2.1.1/jquery.min.js"></script>
	<script src="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
 </head>
 <body>
 	<nav class="navbar navbar-default" role="navigation">
	    <div class="container-fluid">
	    <div class="navbar-header">
	        <a class="navbar-brand" href="#">推荐系统主页</a>
	    </div>
	    <div>
	        <ul class="nav navbar-nav">
	            <li class="active"><a href="#">Ready</a></li>
	            <li><a href="#">Ready</a></li>
	            <li class="dropdown">
	                <a href="#" class="dropdown-toggle" data-toggle="dropdown">
	                    Ready
	                    <b class="caret"></b>
	                </a>
	                <ul class="dropdown-menu">
	                    <li><a href="#">jmeter</a></li>
	                    <li><a href="#">EJB</a></li>
	                    <li><a href="#">Jasper Report</a></li>
	                    <li class="divider"></li>
	                    <li><a href="#">分离的链接</a></li>
	                    <li class="divider"></li>
	                    <li><a href="#">另一个分离的链接</a></li>
	                </ul>
	            </li>
	        </ul>
	    </div>
	    </div>
	</nav>
	<div class="container">
		<div class="col-sm-2"></div>
		<form action="result.php" method="post" target="_blank"  class="form-inline col-sm-8" role="form">
			根据用户ID进行推荐: <input type="text" name="id" class="form-control" style="width: 300px;">
			<input type="submit" value="提交"  class="btn btn-default">
		</form>	
	</div>
 	
 	<?php 
 		
 	?>
 	<div class="container">
 		<div class="col-sm-2"></div>
 		<img src="img/recommend.jpeg" class="col-sm-8" width="200%">
 	</div>
 	<footer class="footer navbar-fixed-bottom" style="margin-top: 140px;height: 54px; width: 100%; background-color: #eee; position: fixed; bottom: 0;">
	    <div class="container" style="text-align: right; color: #333; line-height: 44px; font-size: 14px; font-family: 黑体;">
	        中国科学院大学 机器学习小组©2019
	    </div>
	</footer>

 </body>
</html>