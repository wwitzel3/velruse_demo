<div class="row">
<div class="span8">
<form name="facebook" action="/auth/facebook/login" method="get">
</form>
<a class="fb-button" href="javascript:document.facebook.submit();">&nbsp;</a>
</div>
<div class="span8">
<form name="twitter" action="/auth/twitter/login" method="get">
</form>
<a class="twitter-button" href="javascript:document.twitter.submit();">&nbsp;</a>
</div>
</div>

<div class="row">
<div class="span16">
<form name='login' action='${request.route_url('login')}' class='form-stacked' method='post'>
<fieldset>
<legend>Already have an account?</legend>
<div class="clearfix">
<label for="xlInput">Login or Email</label>
<div class="input">
<input class="xlarge" name="login" size="30" type="text">
</div>
</div>

<div class="clearfix">
<label for="xlInput">Password</label>
<div class="input">
<input class="xlarge" name="password" size="30" type="text">
</div>
</div>

<div class="actions">
<button name="form.login" type="submit" class="btn primary">Log In</button>
</div>
</fieldset>
</form>
</div>
</div>

