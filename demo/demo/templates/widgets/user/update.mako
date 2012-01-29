<form id="user.profile" method="POST" action="">
<div class="clearfix">
<label for="username">Username</label>
<div class="input">
<input class="xlarge" id="username" name="username" size="30" type="text" value="${user.username}" />
<span class="help-block"> This is your username. It is how people will find you on the site.</span>
</div>

<label for="email">Email</label>
<div class="input">
<input class="xlarge" id="email" name="email" size="30" type="text" value="${user.email}" />
</div>

<div class="actions">
<input type="submit" class="btn primary" value="Save changes">&nbsp;<button type="reset" class="btn">Cancel</button>
</div>

</form>
