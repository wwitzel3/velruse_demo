<%inherit file="../base.mako"/>

		<div class="hero-unit">
			<h1>Login or Signup!</h1>
			<p>Here is where you can signup using social integration or just a standard
			form. Your account is created in the same tables and even if you choose social
			integration, once you are logged in, you can create a password, add an email
			and change your user name to allow you to sign in with either method.
			</p>
		</div>
		<div class="row">
			<div class="span8">
				${signup_form|n}
			</div>
			<div class="span8">
				${login_form|n}
			</div>
		</div>
