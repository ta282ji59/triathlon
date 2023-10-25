!/usr/local/bin/perl

#��������������������������������������������������������������������
#�� LOG IN : check.cgi - 2013/01/01
#�� Copyright (c) KentWeb
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

# ���W���[���錾
use strict;
use CGI::Carp qw(fatalsToBrowser);

# �O���t�@�C����荞��
require './init.cgi';
my %cf = &init;

print <<EOM;
Content-type: text/html; charset=shift_jis

<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=shift_jis">
<title>Check Mode</title>
</head>
<body>
<b>Check Mode: [ $cf{version} ]</b>
<ul>
EOM

# �B���t�@�C��
if ($cf{secfile} !~ /^https?\:\/\//) {
	if (-f $cf{secfile}) {
		print "<li>�B���t�@�C���p�X : OK\n";
	} else {
		print "<li>�B���t�@�C���p�X : NG\n";
	}
}

# �e���v���[�g
my @tmpl = qw|enter error|;
foreach (@tmpl) {
	if (-f "$cf{tmpldir}/$_.html") {
		print "<li>�e���v���[�g( $_.html ) : OK\n";
	} else {
		print "<li>�e���v���[�g( $_.html ) : NG\n";
	}
}

print <<EOM;
</ul>
</body>
</html>
EOM
exit;

