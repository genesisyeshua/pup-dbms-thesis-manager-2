<?php

define('EMAIL_FOR_REPORTS', '');
define('RECAPTCHA_PRIVATE_KEY', '@privatekey@');
define('FINISH_URI', 'http://');
define('FINISH_ACTION', 'message');
define('FINISH_MESSAGE', 'You have successfully created a thesis entry!');
define('UPLOAD_ALLOWED_FILE_TYPES', 'doc, docx, xls, csv, txt, rtf, html, zip, jpg, jpeg, png, gif');

define('_DIR_', str_replace('\\', '/', dirname(__FILE__)) . '/');
require_once _DIR_ . '/handler.php';

?>

<?php if (frmd_message()): ?>
<link rel="stylesheet" href="<?php echo dirname($form_path); ?>/formoid-solid-dark.css" type="text/css" />
<span class="alert alert-success"><?php echo FINISH_MESSAGE; ?></span>
<?php else: ?>
<!-- Start Formoid form-->
<link rel="stylesheet" href="<?php echo dirname($form_path); ?>/formoid-solid-dark.css" type="text/css" />
<script type="text/javascript" src="<?php echo dirname($form_path); ?>/jquery.min.js"></script>
<form class="formoid-solid-dark" style="background-color:#014355;font-size:13px;font-family:'Roboto',Arial,Helvetica,sans-serif;color:#000000;max-width:480px;min-width:150px" method="post"><div class="title"><h2>New Thesis Entry</h2></div>
	<div class="element-select<?php frmd_add_class("select"); ?>" title="Academic Year"><label class="title"></label><div class="item-cont"><div class="medium"><span><select name="select" >

		<option value="Academic Year">Academic Year</option>
		<option value="2011">2011</option>
		<option value="2012">2012</option>
		<option value="2013">2013</option>
		<option value="2014">2014</option>
		<option value="2015">2015</option></select><i></i><span class="icon-place"></span></span></div></div></div>
	<div class="element-input<?php frmd_add_class("input"); ?>" title="Thesis Title"><label class="title"></label><div class="item-cont"><input class="large" type="text" name="input" placeholder="Thesis Title"/><span class="icon-place"></span></div></div>
	<div class="element-input<?php frmd_add_class("input1"); ?>" title="Subtitle"><label class="title"></label><div class="item-cont"><input class="large" type="text" name="input1" placeholder="Subtitle"/><span class="icon-place"></span></div></div>
	<div class="element-textarea<?php frmd_add_class("textarea"); ?>" title="Thesis Abstract"><label class="title"></label><div class="item-cont"><textarea class="medium" name="textarea" cols="20" rows="5" placeholder="Thesis Abstract"></textarea><span class="icon-place"></span></div></div>
	<div class="element-input<?php frmd_add_class("input2"); ?>" title="Thesis Adviser"><label class="title"></label><div class="item-cont"><input class="large" type="text" name="input2" placeholder="Thesis Adviser"/><span class="icon-place"></span></div></div>
	<div class="element-input<?php frmd_add_class("input3"); ?>" title="Proponent 1"><label class="title"></label><div class="item-cont"><input class="large" type="text" name="input3" placeholder="Proponent 1"/><span class="icon-place"></span></div></div>
	<div class="element-input<?php frmd_add_class("input4"); ?>" title="Proponent 2"><label class="title"></label><div class="item-cont"><input class="large" type="text" name="input4" placeholder="Proponent 2"/><span class="icon-place"></span></div></div>
	<div class="element-input<?php frmd_add_class("input5"); ?>" title="Proponent 3"><label class="title"></label><div class="item-cont"><input class="large" type="text" name="input5" placeholder="Proponent 3"/><span class="icon-place"></span></div></div>
	<div class="element-input<?php frmd_add_class("input6"); ?>" title="Proponent 4"><label class="title"></label><div class="item-cont"><input class="large" type="text" name="input6" placeholder="Proponent 4"/><span class="icon-place"></span></div></div>
	<div class="element-select<?php frmd_add_class("select1"); ?>" title="Section"><label class="title"></label><div class="item-cont"><div class="small"><span><select name="select1" >

		<option value="Section">Section</option>
		<option value="1">1</option>
		<option value="2">2</option>
		<option value="3">3</option>
		<option value="4">4</option>
		<option value="5">5</option></select><i></i><span class="icon-place"></span></span></div></div></div>
	<div class="element-input<?php frmd_add_class("input7"); ?>" title="Comma-separated"><label class="title"></label><div class="item-cont"><input class="large" type="text" name="input7" placeholder="Tags"/><span class="icon-place"></span></div></div>
<div class="submit"><input type="submit" value="Create"/></div></form><script type="text/javascript" src="<?php echo dirname($form_path); ?>/formoid-solid-dark.js"></script>

<!-- Stop Formoid form-->
<?php endif; ?>

<?php frmd_end_form(); ?>