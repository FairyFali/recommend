<html>
<?php
$nomessage = "<font size=4 color=red>请输入相关信息!</font>";           //输入错误时的信息
?>
 <head>
  	<meta http-equiv="Content-Type" content="text/html; charset=gb2312">
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>推荐结果</title>
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
 	<div class="well">
 		- Age is chosen from the following ranges:<br/>
		*  1:  "Under 18"<br/>
		* 18:  "18-24"<br/>
		* 25:  "25-34"<br/>
		* 35:  "35-44"<br/>
		* 45:  "45-49"<br/>
		* 50:  "50-55"<br/>
		* 56:  "56+"<br/>
 	</div>

 	<?php 
 		if($_POST[id]=="") echo $nomessage; 
 		else{
 			$params = $_POST[id];
 			$output = shell_exec('/Users/wangfali/miniconda3/bin/python /Library/WebServer/Documents/recommend/get_user_info.py'.' '.$params);
			echo "<br><div class='well'>用户信息：$output</div>";
			echo "<br>";
			$output = shell_exec('/Users/wangfali/miniconda3/bin/python /Library/WebServer/Documents/recommend/get_user_movies.py'.' '.$params);
			echo "<br><div class='well'>用户看过的电影：$output</div>";
			echo "<br>";
			$output = shell_exec('/Users/wangfali/miniconda3/bin/python /Library/WebServer/Documents/recommend/manage.py'.' '.$params.' '.'ucf');
			echo "<br><div class='well'>UCF推荐的电影：$output</div>";
			echo "<br>";
			$output = shell_exec('/Users/wangfali/miniconda3/bin/python /Library/WebServer/Documents/recommend/manage.py'.' '.$params.' '.'lfm');
			echo "<br><div class='well'>LFM推荐的电影：$output</div>";
			echo "<br>";
			$output = shell_exec('/Users/wangfali/miniconda3/bin/python /Library/WebServer/Documents/recommend/manage.py'.' '.$params.' '.'prank');
			echo "<br><div class='well'>PersonRank推荐的电影：$output</div>";
			echo "<br>";
 		}
 	?>
 	</div>
 	<div style="padding-bottom: 80px;"></div>
 	 <footer class="footer navbar-fixed-bottom" style="margin-top: 140px;height: 54px; width: 100%; background-color: #eee; position: fixed; bottom: 0;">
	    <div class="container" style="text-align: right; color: #333; line-height: 44px; font-size: 14px; font-family: 黑体;">
	        中国科学院大学 机器学习小组©2019
	    </div>
	</footer>

 </body>
</html>