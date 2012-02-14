<%inherit file="../base.mako"/>

		<div class="hero-unit">
			<h1>Pyramid &amp; Velruse Demo</h1>
			<p>The purpose of this demo application is to show how once can easily configure
			Pyramid and Velruse to do social authentication. You will need to change the
			consume and secrets in the ini file to match yours. You will also need to ensure
			that your end_point is a valid for your system, even if that means adding an entry
			to your /etc/hosts file.
			</p>
		</div>
		<div class="row">
			<div class="span-one-third">
				<h2>Features</h2>
				<ul>
					<li>Easily allow social signups</li>
					<li>Mix social with normal signups</li>
					<li>Uses the latest approach for Pyramid integration.</li>
				</ul>
			</div>
			<div class="span-one-third">
				<h2>Links</h2>
				<ul>
					<li>Piece of Py <a href="http://pieceofpy.com">link</a></li>
				</ul>
			</div>
			<div class="span-one-third">
			%if request.user:
				<h2>Get Started!</h2>
				<ul>
					<li><a href="${request.route_url('user.profile', username=request.user.username)}">Update profile</a></li>
				</ul>
			%else:
				<h2>Sign Up</h2>
				<p>Signing up is easy, just fill out a small form you your free account will be
				created instantly for you.</p>
			<form action="${request.route_url('signup')}" method="GET">
			<input type="submit" class="btn primary" value="Sign Up" />
			</form>
			
			%endif

 			</div>
		</div>
