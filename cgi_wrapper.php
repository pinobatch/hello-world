<?php
// Shim to run a CGI script from within PHP
// for when your web host won't let you mix MediaWiki and a
// web app written in a language other than PHP on one domain
//
// Copyright 2021 Damian Yerrick
// Copying and distribution of this file, with or without
// modification, are permitted in any medium without royalty,
// provided the copyright notice and this notice are preserved.
// This file is offered as-is, without any warranty.
$envnames_to_reflect = [
  'HTTP_HOST', 'REQUEST_URI', 'REQUEST_METHOD', 'QUERY_STRING'
];
foreach ($envnames_to_reflect as $name) {
  putenv("$name=".@$_SERVER[$name]);
}

chdir("..");
$stdout = shell_exec('python3 nameofscript.py');
$topbottom = explode("\r\n\r\n", $stdout, 2);
$headers = explode("\n", $topbottom[0]);
foreach ($headers as $h) header($h);
echo $topbottom[1];
