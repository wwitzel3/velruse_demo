<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" xmlns:tal="http://xml.zope.org/namespaces/tal">
<head>
  <title>Pyramid &amp; Velruse Demo</title>
  <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
  <meta name="keywords" content="python web application" />
  <meta name="description" content="pyramid web application" />

  <link rel="stylesheet/less" href="${request.static_url('demo:static/lib/bootstrap.less')}">
  <link rel="shortcut icon" href="${request.static_url('demo:static/favicon.ico')}" />
  <link rel="stylesheet/less" href="${request.static_url('demo:static/style.less')}" media="screen" charset="utf-8" />


  <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
  <script src="${request.static_url('demo:static/less-1.1.5.min.js')}"></script>
  <script type="text/javascript" src="${request.static_url('demo:static/script.js')}"></script>

</head>
<body>
	<div class="topbar">
		<div class="fill">
			<div class="container">
				<a class="brand" href="${request.route_url('index')}">Demo</a>
				<ul class="nav">
					<li class="active"><a href="${request.route_url('index')}">Home</a></li>
					<li><a href="#about">About</a></li>
					% if request.user:
					<li><a href="${request.route_url('logout')}">Logout</a></li>
					% else:
					<li><a href="${request.route_url('signup')}">Login</a></li>
					% endif
				</ul>
			</div>
		</div>
	</div>

	<div class="container">
		${next.body()}
	</div>
</body>
</html>
