!/usr/local/bin/perl

#┌─────────────────────────────────
#│ LOG IN : login.cgi - 2013/01/01
#│ Copyright (c) KentWeb
#│ http://www.kent-web.com/
#└─────────────────────────────────

# モジュール宣言
use strict;
use CGI::Carp qw(fatalsToBrowser);

# 設定ファイル
require './init.cgi';
my %cf = &init;

# データ受け取り
my %in = &parse_form;

# 処理分岐
if ($in{mode} eq 'logout') { &logout; }
if ($in{login}) { &login; }
&enter_form;

#-----------------------------------------------------------
#  ログイン認証
#-----------------------------------------------------------
sub login {
	# 認証エラー
	if ($in{pw} ne $cf{password}) { &error("認証できません"); }

	# ファイル指定がURLであれば Locaionヘッダでジャンプ
	if ($cf{secfile} =~ /^https?\:\/\//) {

		# 移動
		&location($cf{secfile});

	# HTMLの場合
	} else {

		# チェック
		if (! -f $cf{secfile}) { &error("隠しファイルが存在しません"); }

		# 読み込み
		open(IN,"$cf{secfile}") or &error("open err: $cf{secfile}");
		print "Content-type: text/html\n\n";
		print <IN>;
		close(IN);

		exit;
	}
}

#-----------------------------------------------------------
#  認証画面
#-----------------------------------------------------------
sub enter_form {
	# テンプレート読み込み
	open(IN,"$cf{tmpldir}/enter.html") or &error("open err: enter.html");
	my $tmpl = join('', <IN>);
	close(IN);

	# 置き換え
	$tmpl =~ s/!login_cgi!/$cf{login_cgi}/;

	# 表示
	print "Content-type: text/html; charset=shift_jis\n\n";
	&footer($tmpl);
}

#-----------------------------------------------------------
#  エラー処理
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
#  フッター
#-----------------------------------------------------------
sub footer {
	my $foot = shift;

	# 著作権表記（削除厳禁）
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
#  フォームデコード
#-----------------------------------------------------------
sub parse_form {
	my ($buf,%in);
	if ($ENV{REQUEST_METHOD} eq "POST") {
		&error('受理できません') if ($ENV{CONTENT_LENGTH} > $cf{maxdata});
		read(STDIN, $buf, $ENV{CONTENT_LENGTH});
	} else {
		$buf = $ENV{QUERY_STRING};
	}
	foreach ( split(/&/, $buf) ) {
		my ($key,$val) = split(/=/);
		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;

		# 不要コード
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
#  ログアウト
#-----------------------------------------------------------
sub logout {
	# 移動
	&location($cf{logout_url});
}

#-----------------------------------------------------------
#  URL移動
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

