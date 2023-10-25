!/usr/local/bin/perl

#��������������������������������������������������������������������
#�� LOG IN : login.cgi - 2013/01/01
#�� Copyright (c) KentWeb
#�� http://www.kent-web.com/
#��������������������������������������������������������������������

# ���W���[���錾
use strict;
use CGI::Carp qw(fatalsToBrowser);

# �ݒ�t�@�C��
require './init.cgi';
my %cf = &init;

# �f�[�^�󂯎��
my %in = &parse_form;

# ��������
if ($in{mode} eq 'logout') { &logout; }
if ($in{login}) { &login; }
&enter_form;

#-----------------------------------------------------------
#  ���O�C���F��
#-----------------------------------------------------------
sub login {
	# �F�؃G���[
	if ($in{pw} ne $cf{password}) { &error("�F�؂ł��܂���"); }

	# �t�@�C���w�肪URL�ł���� Locaion�w�b�_�ŃW�����v
	if ($cf{secfile} =~ /^https?\:\/\//) {

		# �ړ�
		&location($cf{secfile});

	# HTML�̏ꍇ
	} else {

		# �`�F�b�N
		if (! -f $cf{secfile}) { &error("�B���t�@�C�������݂��܂���"); }

		# �ǂݍ���
		open(IN,"$cf{secfile}") or &error("open err: $cf{secfile}");
		print "Content-type: text/html\n\n";
		print <IN>;
		close(IN);

		exit;
	}
}

#-----------------------------------------------------------
#  �F�؉��
#-----------------------------------------------------------
sub enter_form {
	# �e���v���[�g�ǂݍ���
	open(IN,"$cf{tmpldir}/enter.html") or &error("open err: enter.html");
	my $tmpl = join('', <IN>);
	close(IN);

	# �u������
	$tmpl =~ s/!login_cgi!/$cf{login_cgi}/;

	# �\��
	print "Content-type: text/html; charset=shift_jis\n\n";
	&footer($tmpl);
}

#-----------------------------------------------------------
#  �G���[����
#-----------------------------------------------------------
sub error {
	my $err = shift;

	open(IN,"$cf{tmpldir}/error.html") or die;
	my $tmpl = join('', <IN>);
	close(IN);

	$tmpl =~ s/!error!/$err/g;

	print "Content-type: text/html; charset=shift_jis\n\n";
	print $tmpl;
	exit;
}

#-----------------------------------------------------------
#  �t�b�^�[
#-----------------------------------------------------------
sub footer {
	my $foot = shift;

	# ���쌠�\�L�i�폜���ցj
	my $copy = <<EOM;
<p align="center" style="margin-top:3em;font-size:10px;font-family:verdana,helvetica,arial,osaka;">
- <a href="http://www.kent-web.com/" target="_top">Log in</a> -
</p>
EOM

	if ($foot =~ /(.+)(<\/body[^>]*>.*)/si) {
		print "$1$copy$2\n";
	} else {
		print "$foot$copy\n";
		print "</body></html>\n";
	}
	exit;
}

#-----------------------------------------------------------
#  �t�H�[���f�R�[�h
#-----------------------------------------------------------
sub parse_form {
	my ($buf,%in);
	if ($ENV{REQUEST_METHOD} eq "POST") {
		&error('�󗝂ł��܂���') if ($ENV{CONTENT_LENGTH} > $cf{maxdata});
		read(STDIN, $buf, $ENV{CONTENT_LENGTH});
	} else {
		$buf = $ENV{QUERY_STRING};
	}
	foreach ( split(/&/, $buf) ) {
		my ($key,$val) = split(/=/);
		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;

		# �s�v�R�[�h
		$val =~ s/&/&amp;/g;
		$val =~ s/</&lt;/g;
		$val =~ s/>/&gt;/g;
		$val =~ s/"/&quot;/g;
		$val =~ s/'/&#39;/g;
		$val =~ s/[\r\n]//g;

		$in{$key} .= "\0" if (defined($in{$key}));
		$in{$key} .= $val;
	}
	return %in;
}

#-----------------------------------------------------------
#  ���O�A�E�g
#-----------------------------------------------------------
sub logout {
	# �ړ�
	&location($cf{logout_url});
}

#-----------------------------------------------------------
#  URL�ړ�
#-----------------------------------------------------------
sub location {
	my $url = shift;

	if ($ENV{PERLXS} eq "PerlIS") {
		print "HTTP/1.0 302 Temporary Redirection\r\n";
		print "Content-type: text/html\n";
	}
	print "Location: $url\n\n";
	exit;
}

