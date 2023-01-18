#! /usr/local/bin/perl


#----------------#
#    初期設定    #
#----------------#


# 掲示板の名前 --------------------------


$title = 'あやしいわーるど＠はいほー'; 

# 文字色や背景などの設定

# body部

$bgc    = '004040';

$textc  = 'ffffff';

$linkc  = 'eeffee';

$vlinkc = 'dddddd';

$alinkc = 'ff0000';

# 題名の色

$subjc  = 'ffffee';

# --- 表示件数 --------------------------------------------
# １ページに表示する件数のデフォルト値
$def =  30;
# １ページに表示する件数の最小値
$defmin =  0;
# この件数以上でリロード／書き込みしたときには次はこの件数にする。
$defmax =300;

# --- ＵＲＬ ----------------------------------------------
# このスクリプト
$cgiurl = 'bbs.cgi';


# 連絡先
$mailadd = 'goodby@strangers.com';

# ログのＵＲＬ
$loglog0 = 'log';
$loglog1 = 'http://';

# ---------------------------------------- 書き込みチェック ----------------------------------------
# 管理人名前チェック・メールアドレス・パスワード
$namez = 'しば';
$pass = 'chiba';
# 書き込み最大量
$maxlength = 1024*16; 
#投稿内容文字数
$max_v = 8000;      
#投稿内容行数（上の文字数との兼ね合いを考えて）
$max_line = 120;     

# 二重書き込みチェック件数
$check = 10;
# 二重書き込みチェックバイト数
$checklength = 10;
# 書き込み件数の最大登録数の設定
$max = '300';
 
# ------------------------------------ ディレクトリ・ファイル名 ------------------------------------
# 日本語コード変換ライブラリjocde.plのパス
require './jcode.pl';
# 内容が書き込まれる記録ファイルのパスを設定
$file = './loveyou.dat';
# 別途とるログのファイル名先頭文字・拡張子の指定
$logfile = "./log/";
$logfiledat = ".html";

# -------------------------------------------- カウンタ --------------------------------------------
# カウンタプラス値
$countplus = "";
# カウンタ開始日
$countdate = '99/6/20';
# カウンタファイルの先頭文字・拡張子の指定
$countfile = './count/count';
$countfiledat = '.txt';
# カウンタ強度（０のときは使用しない）
$countlevel = 3;

# --------------------------------------------- その他 ---------------------------------------------
# 時差
$tim =0*3600;
# 入力形式の設定
$method = 'post';


# 時刻処理
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time + $tim );
$month = ($mon + 1);

# 時刻のゼロサプレス
if ($month < 10) { $month = "0$month"; }
if ($mday < 10)  { $mday  = "0$mday";  }
if ($sec < 10)   { $sec   = "0$sec";   }
if ($min < 10)   { $min   = "0$min";   }
if ($hour < 10)  { $hour  = "0$hour";  }

# 曜日変換処理
$y0="日"; $y1="月"; $y2="火"; $y3="水"; $y4="木"; $y5="金"; $y6="土";
$youbi = ($y0,$y1,$y2,$y3,$y4,$y5,$y6) [$wday];

# 時刻フォーマット
$date_now = "$month月$mday日($youbi)$hour時$min分$sec秒";
# ログファイル名取得
$filedate = "$logfile$year$month$mday$logfiledat";
# よくわからない変数
$gesu = $ENV{'REMOTE_PORT'};
# 投稿時のaction名
$action = "regist";

# 追加対策 -------------------------------

# 外部投稿防止コード
$protect_a = 9987;	# 4桁
$protect_b = 55;		# 2桁
$protect_c = 112;		# 3桁

# 過去ログの最大ファイルサイズ
$maxoldlogsize = 3 * 1024 * 1024;		# 3MB

###########################################################################################

# フォーム入力されたデータを$bufferに格納する（getかpostかによって取得方法が異なる）
#if ($ENV{'REQUEST_METHOD'} eq "POST" && $ENV{'CONTENT_LENGTH'} < $maxlength) { read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'}); }
#else { $buffer = $ENV{'QUERY_STRING'}; }
if ($ENV{'REQUEST_METHOD'} eq "POST") { read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'}); } else { $buffer = $ENV{'QUERY_STRING'}; }
if ($ENV{'CONTENT_LENGTH'} > $maxlength) {&error(5);}

# $bufferに格納されたFORM形式のデータを取り出す
@pairs = split(/&/,$buffer);
foreach $pair (@pairs) {
	
	($name, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	
	# 記録するデータはsjis
	&jcode'convert(*value,'sjis');
	

#改行連打のいたずらを回避（３行以上何も書かずに改行のみの部分は改行無視）
#スペース＋改行の連打を回避（上記を回避するためにスペースをいれて改行する悪戯の場合）
	if ($value =~ /\r\n/) { $value =~ s/\r\n/\r/g; }
	if ($value =~ /\n/) { $value =~ s/\n/\r/g; }

	if ($value =~ / \r \r/) { $value =~ s/ \r \r//g; }
	if ($value =~ /\　\r\　\r/) { $value =~ s/\　\r\　\r//g; }
	if ($value =~ / \r/) { $value =~ s/ \r/\r/g; }
	if ($value =~ /\　\r/) { $value =~ s/\　\r/\r/g; }
	if ($value =~ /\r\r\r\r/) { $value =~ s/\r\r\r\r//g; }


	# 処理の都合上の処理
	$value =~ s/\n//g; # 改行文字は消去
	
	if ($name eq 'value') { $value =~ s/&/&amp\;/g; $value =~ s/\,/\0/g; }
	elsif ($name ne 'page' && $name ne 'image') { $value =~ s/\,//g; $value =~ s/\;//g; $value =~ s/\://g; $value =~ s/\=//g; }
	
	else { $value =~ s/\,//g; }
	
	$value =~ s/</&lt\;/g; $value =~ s/>/&gt\;/g;
	
	$FORM{$name} = $value;
}


# 表示ページ数の決定 ##################################################
if ($FORM{'def'} ne '') { $def = $FORM{'def'}; }
if ($def < $defmin) { $def = $defmin;}
$defnext = $def;
if ($defnext > $defmax) {$defnext = $defmax;}

# 表示色の決定 ########################################################
if ($FORM{'bgcolor'} ne '') { $bgc = $FORM{'bgcolor'}; }
$body  = "<body bgcolor=\"#$bgc\" text=\"#$textc\" link=\"#$linkc\" vlink=\"#$vlinkc\" alink=\"#$alinkc\">";

# ポップアップウインドウの決定 ########################################################

#if ($FORM{'image'} eq '') { $checked1='checked'; }
#if ($FORM{'image'} eq '2') { $checked2='checked'; }

#if ($FORM{'himage'} eq '') { $himage=''; }
#if ($FORM{'himage'} eq '2'){ $link='$sec$min'; }


# 全体の流れを決定する（actionやpwdはフォーム入力されたデータを格納する名前）
########################################################
#    action=regist  --> 記事記録処理して通常画面へ
#    その他  --> 通常画面へ

if (($FORM{'def'} eq '0') && ($FORM{'value'} ne '')) { &regist; }
if ($FORM{'def'} eq '0') { &read; }

if ($FORM{'action'} eq "$action")  { &regist; }
if ($FORM{'action'} eq 'search1') { &search1; }
if ($FORM{'action'} eq 'search2') { &search2; }
if ($FORM{'action'} eq 'search3') { &search3; }
&html;

# メイン表示サブルーチン #######################################################
sub html {
	
	# プロテクトキー生成
	local ( $ptime ) = time + $tim * 60 * 60;
	local ( $pkey ) = ( $ptime + $protect_a ) * $protect_b + $protect_c;
	
	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head>\n";
	print "$body\n";

	
	# バナーはここ
	
	print "<font size=+1><b>$title</b></font>\n";
	print "<font size=-1>　<b><a href=\"http://www.geocities.com/Tokyo/Subway/1282/front.html\" target=\"_top\">おしらせページ</a></b></font> \n";
	print " <font size=-1><b><a href=\"http://freehosting1.at.webjump.com/sw/swatty-webjump/\" target=\"_top\">スワティ</a></b></font>\n";
#print "<font size=-1><b><a href=\"mailto:$mailadd\">連絡先</a></b></font>\n";

	print "<form method=$method action=\"$cgiurl\">\n";
	
	print "<input type=hidden name=\"action\" value=\"$action\">\n";
	print "投稿者 <input type=text name=\"name\" size=20 maxlength=40 value=\"$FORM{'name'}\"><br>";
	print "メール <input type=text name=\"email\" size=30><br>\n";
	print "題名　 <input type=text name=\"subject\" size=30 maxlength=60>  \n";
	print "<input type=submit value=\"投稿／リロード\"><input type=reset value=\"消す\"><p>内容<i>（タグは使えません。内容を書かずに投稿ボタンを押すとリロードになります。）</i><br><textarea name=\"value\" rows=5 cols=70></textarea><input type=hidden name=\"page\" size=70 value=\"http://\"><p>\n";
	print "表\示件数\n";
	print "<input type=text name=\"def\" size=8 value=\"$defnext\">\n";
	print "バックグラウンドカラー<input type=text name=\"bgcolor\" size=6 value=\"$bgc\"><input type=hidden name=\"link\" value=\"$FORM{'link'}\">\n";
	print "URL自動リンク<input type=checkbox name=\"image\" value=\"1\" checked></font> \n";

	print "<input type=hidden name=\"code\" value=\"$sec$min\@$pkey.com\">\n";



	print "<input type=hidden name=\"win_time\" value=\"$month$mday$hour$min$sec\">\n";


	print "<p><font size=-1>最近の過去ログは<a href=\"./getlog.cgi\" target=\"_top\">ここ</a>。\n";




#カウンター
	if ( $countlevel > 0 ){
		print "<font size=-1>$countdateから ";
		&counter; print "$countplus（こわれにくさレベル$countlevel）</font>\n";	}

	print "<input type=hidden name=\"win_count\" value=\"$maxcount\">\n";


	# プロテクトコード出力
	print "<input type=hidden name=\"protect\" value=\"$pkey\">\n";
	
	
#	print "<br><i>新しい記事から表\示します。最高$max件の記事が記録され、それを超えると古い記事から削除されます。<br>\n";
#	print "１回の表\示で$def件を越える場合は、下のボタンを押すことで次の画面の記事を表\示します。</i>\n";


			print "<hr><a href=\"http://extra.onlineexpress.net/cgi-bin/strangeworld/bbs.cgi\">エクストラ</a>、<a href=\"http://www.kinsan.ne.jp/~miki/strangeworld/bbs.cgi\">きんさん</a>、 <a href=\"http://famille.onlineexpress.net/cgi-bin/strangeworld/bbs.cgi\">ふぁみーる</a>、<a href=\"http://www.bea.hi-ho.ne.jp/cgi-bin/user/strangeworld/bbs.cgi\">はいほー</a> | <a href=\"http://www4.famille.ne.jp/~haruna/remix/bbs.cgi\">REMIX</a>、<a href=\"http://kakumeigun.onlineexpress.net/cgi-bin/relax/bbs.cgi\">RELAX</a> | <a href=\"http://edoya.neko.to/2/upload.cgi\">ぁ界遺産</a>、<a href=\"http://saturdaytears.virtualave.net/cgi-bin/upload.cgi\">徘徊する骸</a>\n";


#	 サーチの注意書き
	print "<hr>最大\表\示：$max件　■：返信　★：投稿者検索　◆：スレッド検索　\表\示件数0件：未読\表\示<hr>この掲示板に関わるあらゆる行動は全て自分で責任をとってください。\n";


#	リロード
	print "<p></font></font><input type=submit value=\"投稿／リロード\">\n";
	print "</form>\n";
	
	#--- 記録記事の出力 ----------------------------------#
	
	# 記録ファイルを読み出しオープンして、配列<@lines>に格納する
    open(DB,"$file");
	@lines = <DB>;
	close(DB);
	
	if ($FORM{'page'} eq '') { $page = 0; } else { $page = $FORM{'page'}; }
	
	$accesses = @lines; $accesses--;
	$page_end = $page + $def - 1;
	if ($page_end > $accesses) { $page_end = $accesses; }

	foreach ($page .. $page_end) {
		($date,$name,$email,$value,$subject,$hpage,$himage,$code,$postid) = split(/\,/,$lines[$_]);
		$value =~ s/\0/\,/g; # ヌルコードに変換記録した半角カンマを復帰させる
		chop($himage) if $himage =~ /\n/;
		chop($hpage) if $hpage =~ /\n/;
		chop($postid) if $postid =~ /\n/;
		&disp;
	}
	
	#--- 改ページ処理 ------------------------------------#
	
	print "</form><hr><p>\n";
	$page_next = $page_end + 1;
	$i = $page + 1; $j = $page_end + 1;
	if ($page_end ne $accesses) {
		print "<font size=-1><i>以上は、現在登録されている新着順$i番目から$j番目までの記事です。</i></font><p>\n";
		print "<form method=$method action=\"$cgiurl\">\n";
		print "<input type=hidden name=\"page\" value=\"$page_next\">\n";
		print "<input type=hidden name=\"def\" value=\"$def\">\n";
		print "<input type=hidden name=\"bgcolor\" value=\"$bgc\">\n";
		print "<input type=submit value=\"次のページ\"></form>\n";
	}
	else {
	
		print "<font size=-1><i>以上は、現在登録されている新着順$i番目から$j番目までの記事です。";
		print "これ以下の記事はありません。</i></font>\n";
	}
	
	# このスクリプトの著作権表示（かならず表示してください）

		print "<form method=$method action=\"$cgiurl\"><input type=hidden name=\"def\" value=\"$def\"><input type=hidden name=\"bgcolor\" value=\"$bgc\"><input type=submit value=\"　リロード　\"></form>\n";
	print "<h4 align=right><hr size=5><a href=\"http://www.ask.or.jp/~rescue/\">MiniBBS v7.5</a> <a href=\"http://www.bea.hi-ho.ne.jp/strangeworld/recycle/\">REQUIEM 990707γ</a> is Free.</h4>\n";
	print "</body></html>\n";
	exit;
}

# 書き込み処理サブルーチン ############################################################
sub regist {
	
	# 内容がスペースならリロード
	if ($FORM{'value'} eq "") { &html; }

 # 別のページからこのＣＧＩへの投稿を排除する処理
	$ref = $ENV{'HTTP_REFERER'};
	$ref_url = $cgiurl; $ref_url =~ s/\~/.*/g;
	if (!($ref =~ /$ref_url/i)) { &error(form); }
	
	# 入力されたデータのチェック ##################################
	if ($FORM{'bgcolor'} eq "") { &error(1); }
	if ($FORM{'def'} eq "") { &error(1); }
	if ($FORM{'win_time'} eq "") { &error(1); }
	if ($FORM{'win_count'} eq "") { &error(1); }
	if ($FORM{'name'} eq "") { $FORM{'name'} = ''; }
	if ($FORM{'email'} =~ /,/) { &error(4); }
          $FORM{'email'}=~ s/\"//g;
	if ($FORM{'email'} ne "") { if (!($FORM{'email'} =~ /(.*)\@(.*)\.(.*)/)) { &error(3); }}
	if ($FORM{'subject'} eq "") { $FORM{'subject'} = '　'; }
	
	if ($FORM{'page'} eq "" || $FORM{'page'} eq "http://") { $FORM{'page'} = ''; }
	else{
		$FORM{'page'} =~ s/\s//g;$FORM{'page'} =~ s/\"//g;$FORM{'page'} =~ s/\'//g;
		$FORM{'page'} =~ s/http\:\/\/http\:\/\//http\:\/\//g;
	}
	# 行数制限
if ($max_line) {
		$value_size = ($FORM{'value'} =~ tr/\r/\r/) + 1;     # \r の数を数える
		if ($value_size > $max_line) { &error(1); }
	}
	# 文字数制限
	if ($max_v) {
		$value_size = length($FORM{'value'});
		if ($value_size > $max_v)  { &error(1); }
	}
	
     # カウンター制限

	for( $i=0 ; $i < $countlevel ; $i++){
		open(IN,"$countfile$i$countfiledat");
		$count[$i] = <IN>;
		$filenumber[$count[$i]] = $i;
		close(IN);
	}
	@sortedcount = sort by_number @count;
	$maxcount = $sortedcount[$countlevel-1];
	$mincount = $sortedcount[0];

if ( $FORM{'win_count'} > $maxcount ) { &repeat; }


# プロテクトコードチェック
	if ( $FORM{'protect'} ne '' ) {
		local ( $ptime ) = time + $tim * 60 * 60;
		local ( $pcheck ) = ( $FORM{'protect'} - $protect_c ) / $protect_b - $protect_a;
		
		( $csec, $cmin, $chour, $cmday, $cmon, $cyear, $cwday, $cyday, $cisdat )
			= localtime ( $pcheck );
		$cyear += 1900;
		$cmon++;
		local ( $cnowdate ) = sprintf ( "%d/%02d/%02d(%s)%02d時%02d分%02d秒", 
			$cyear, $cmon, $cmday, 
			( '日', '月', '火', '水', '木', '金', '土' )[$cwday],
			$chour, $cmin, $csec );
		if ( 
		  ( $csec  < 0 ) || ( $csec  > 60 ) ||
		  ( $cmin  < 0 ) || ( $cmin  > 60 ) ||
		  ( $chour < 0 ) || ( $chour > 24 ) ||
		  ( ( $ptime - $pcheck ) > 1 * 60 * 60 ) ) {	# １時間
			&error ( 'xxx' );
		}
	} else {
		&error ( 'xxx' );
	}


	
	# 過去ログのファイルサイズチェック
	if ( ( -s $filedate ) > $maxoldlogsize ) {
		&error (0);
	}


	
	# 投稿者名チェック
	$formname = $FORM{'name'};
#	if ($formname eq "$nameng"){ &error(xx); }
	if ($formname eq "$pass"){$formname = $namez; $FORM{'email'} = $mailadd;}
	else {
		$formname =~ s/$namez/<small>しば<\/small>/g;
#		$formname =~ s/しぱ/しは゜/g;
	}
	
# 記録ファイルを読み出しオープンして、配列<@lines>に格納する
	open (DB,"+<$file") || &error (0);
	eval 'flock (DB, 2)';
	@lines = <DB>;


	
	# 最大保持記録数の処理
	$i = 0;
	foreach $line (@lines) {
		$i++;
		if ($i == $max) { last; }
		push(@new,$line);
	}

	# 連続同一内容書き込みチェック
	$i = 0; $j = 0;
	while ( ( $i < $check ) && ($j == 0) ) {
		($date0,$name0,$email0,$value0,$subject0,$hpage0,$himage0,$code0,$postid0,$win_time0,$win_count0) = split(/\,/,$lines[$i]);

    if ( $FORM{'value'} eq $value0 ) { $j = 2;}
#	if ( $FORM{'win_count'} eq $win_count0 ) { $j = 1; }
#    if (( $FORM{'win_count'} > $win_count0 ) &&($FORM{'win_time'} < $win_time0 )){  $j = 1;}
 #   if (( $FORM{'win_count'} < $win_count0 ) && ($FORM{'win_time'} > $win_time0)){  $j = 1;}

#		if (substr($FORM{'value'},0,$checklength) eq substr($value0,0,$checklength)){ $j = 1; }
#    	if (substr($FORM{'value'},1-$checklength,$checklength) eq substr($value0,1-$checklength,$checklength)) { $j = 1; }
		$i++;
	}

	# ID生成
	if ( $lines[0] =~ /^.*,.*,.*,.*,.*,.*,.*,.*,(.*),.*,.*\n/ ) {
		$postid = $1 + 1;
	} else {
		$postid = 1;
	}

		if ( $j == 1) { &repeat; }


	if ( $j == 0 ) {
		$value = "$date_now\,$formname\,$FORM{'email'}\,$FORM{'value'}\,$FORM{'subject'}\,$FORM{'page'}\,$FORM{'image'},$FORM{'code'},$postid,$FORM{'win_time'},$FORM{'win_count'}\n";
		unshift(@new,$value);
		
		seek (DB, 0, 0);
		print DB @new;
		eval 'flock (DB, 8)';
		close (DB);
		

# 過去ログ出力
########################
		$FORM{'value'} =~ s/\0/\,/g;
		open(LOG,">>$filedate") || &error(0);
		eval 'flock (LOG, 2)';


if (-z LOG) {
	# ファイルが空の場合はHTMLヘッダを付ける
	print LOG "<html>\n<body bgcolor=\"#$bgc\" text=\"#$textc\" link=\"#$linkc\" vlink=\"#$vlinkc\" alink=\"#$alinkc\">\n<hr>";

# 保存後５日を過ぎた過去ログファイルは削除
	( $oldsec, $oldmin, $oldhour, $oldmday, $oldmonth, $oldyear, $oldwday, $oldyday, $oldisdst )
  = localtime ( time + $tim - 3 * 60 * 60 * 24 );
$oldmonth += 1;
$oldlogfilename = sprintf ( "%s%d%02d%02d%s", $logfile, $oldyear, $oldmonth, $oldmday, $logfiledat );
	unlink $oldlogfilename;
}

		print LOG "<font size=+1 color=\"#$subjc\"><b>$FORM{'subject'}</b></font>";
		# メールアドレスが記録されているデータにはリンクを付ける
		if ($FORM{'email'} ne '') { print LOG "　投稿者：<b><a href=\"mailto:$FORM{'email'}\">$formname</a></b>\n"; }
		else { print LOG "　投稿者：<font color=\"#$subjc\"><b>$formname</b></font>\n"; }
		print LOG "<font size=-1>　投稿日：$date_now";
	    print LOG "</font><p>\n";
if ($FORM{image} eq '1') {

    $FORM{'value'} =~ s!((https?|ftp|gopher|telnet|whois|news):(=\S+|[\x21-\x7f])+)!<a href="$1" target="$link">$1</a>!ig;
}


		print LOG "<blockquote><pre>$FORM{'value'}</pre><p>\n\n";
		
		# ＵＲＬが記録されているデータにはリンクを付ける
		if ($FORM{'page'} ne '') {
			$page0 = $FORM{'page'};
			$page0 =~ s/$cgiurl\?action=search1\&search=(.*)\&id=\d*/参考：$1/;
			if ( $FORM{'page'} eq $page0 ) {
				print LOG "<a href=\"$FORM{'page'}\" target=\"jump\">$page0</a><p>\n";
			} else {
				print LOG "<font color=\"#$linkc\"><u>$page0</u></font><p>\n";
			}
		}
		print LOG "</blockquote>\n<hr>";
		
		eval 'flock (LOG, 8)';
		close(LOG);
		
#		if (!open(BD,">>./0000.txt")) {error(0); }
#		print BD "$date_now\,$FORM{'subject'}\,$host\n";
#		while ( ($a,$b) = each %ENV) {print BD "$a=$b\,";}
#		print BD "\n";
#		close(BD);
	
	} else {
		eval 'flock (LOG, 8)';
		close(LOG);
	}

	
	# 記録処理後、再読み込みする
	if ( $FORM{'def'} eq "0" ) { &read; }
	elsif ( $FORM{'follow'} ne "on" ) { &html; }
	else {
		print "Content-type: text/html\n\n";
		print "<html><head><title>かきこみ完了</title></head>\n";
		print "$body\n";
		print "<h1>かきこみ完了</h1>\n";
		exit;
	}
#	print "Location: $cgiurl" . '?' . "\n\n";
#	exit;
}


# フォロー投稿サブルーチン（search1） ############################################
sub search1 {

	#--- 入力フォーム画面 --------------------------------#

	print "Content-type: text/html\n\n";
	print "<html><head><title>$FORM{search}に返信</title></head>\n";
	print "$body\n";

	# バナーはここ

	#--- 記録記事の出力 ----------------------------------#

	# 記録ファイルを読み出しオープンして、配列<@lines>に格納する
    open(DB,"$file");
	@lines = <DB>;
	close(DB);

	$accesses = @lines;
	$f = 0; $i = 0;

	while (($f == 0) && ($i < $accesses)){

		# データを各変数に代入する
		($date,$name,$email,$value,$subject,$hpage,$himage,$code,$postid) = split(/\,/,$lines[$i]);
		chop ($postid) if $postid =~ /\n/;
		if ($postid eq $FORM{id}) { $f = 1;}
		$i++;
	}


	if ($f == 1){
		$value =~ s/\0/\,/g; # ヌルコードに変換記録した半角カンマを復帰させる
		chop($himage) if $himage =~ /\n/;
		chop($hpage) if $hpage =~ /\n/;
		
		&disp;
		print "<hr>\n";
		
		$value =~ s/\r/\r&gt; /g;
  $value =~ s/\r&gt;\s&gt;\s*\r/\r/g;
  $value ="&gt; $value";
#$value =~ s/&gt; &gt; &gt;.*?\r//g; 
		print "<p>\n";



		# プロテクトキー生成
		local ( $ptime ) = time + $tim * 60 * 60;
		local ( $pkey ) = ( $ptime + $protect_a ) * $protect_b + $protect_c;
		
		print "<form method=$method action=\"$cgiurl\">\n";
		print "<input type=hidden name=\"action\" value=\"$action\">\n";

if ($FORM{'link'} ne '') { $link = $FORM{'link'}; }

	if ($FORM{'link'} ne '_top') { print "<input type=hidden name=\"follow\" value=\"on\">\n"; }
		print "投稿者 <input type=text name=\"name\" size=20 maxlength=20><br>";		
		print "メール <input type=text name=\"email\" size=30><br>\n";
		print "題名　 <input type=text name=\"subject\" size=30 value=\"＞$name\">  \n";
		print "<input type=submit value=\"  投稿  \"><input type=reset value=\"消す\"><p>\n";	


		print "<input type=hidden name=\"def\" value=\"$defnext\">\n";
		
		# プロテクトコード出力
		print "<input type=hidden name=\"protect\" value=\"$pkey\">\n";
		
		print "内容<i>（タグは使えません。\n";
		print "内容を書かずに投稿ボタンを押すとリロードになります。）</i><br>\n";
		
		print "<textarea name=\"value\" rows=5 cols=70>$value\r";
		
		print "</textarea><p>\n";



		if ($himage ne '1') { 	print "URL自動リンク<input type=checkbox name=\"image\" value=\"1\"></font> \n";}
else{
	print "URL自動リンク<input type=checkbox name=\"image\" value=\"1\" checked></font> \n";}

#カウンター
	if ( $countlevel > 0 ){
		print "<font size=-1 color=$bgc>$countdateから ";
		&counter; print "$countplus（こわれにくさレベル$countlevel）</font>\n";	}

	print "<input type=hidden name=\"win_count\" value=\"$maxcount\">\n";

	print "<input type=hidden name=\"win_time\" value=\"$month$mday$hour$min$sec\">\n";

		print "<input type=hidden name=\"code\" value=\"$code\">\n";
		print "<input type=hidden name=\"page\" size=70 value=\"$cgiurl\?action\=search1\&search\=$date\&id=$postid\">\n";
		print "<input type=hidden name=\"bgcolor\" value=\"$bgc\"></form><p>\n";	
}

	else { print "みつかりません<br>";}

	
	print "<hr></body></html>\n";
	exit;
}


# 投稿者名サーチ用サブルーチン（search2） ############################################
sub search2 {

	print "Content-type: text/html\n\n";
	print "<html><head><title>$FORM{search}の投稿一覧</title></head>\n";
	print "$body\n";

	# バナーはここ

	#--- 記録記事の出力 ----------------------------------#

	# 記録ファイルを読み出しオープンして、配列<@lines>に格納する
    open(DB,"$file");
	@lines = <DB>;
	close(DB);

	$accesses = @lines;
	$f = 0;
	foreach ( @lines ){
		# データを各変数に代入する
		($date,$name,$email,$value,$subject,$hpage,$himage,$code,$postid) = split(/\,/,$_);
		if ( $name eq $FORM{search} ) {
			$f = 1;
			$value =~ s/\0/\,/g; # ヌルコードに変換記録した半角カンマを復帰させる
			chop($himage) if $himage =~ /\n/;
			chop($hpage) if $hpage =~ /\n/;
			&disp;
		}
	}

	if ($f == 0){ print "みつかりません<br>";}

	print "<hr></body></html>\n";
	exit;
}

# トピックサーチ用サブルーチン（search3） ############################################
sub search3 {


	print "Content-type: text/html\n\n";
	print "<html><head><title>スレッド一覧</title></head>\n";
	print "$body\n";

	#--- 記録記事の出力 ----------------------------------#

	# 記録ファイルを読み出しオープンして、配列<@lines>に格納する
open(DB,"$file");

	@lines = <DB>;
	close(DB);

	$accesses = @lines;
	$f = 0;
	foreach ( @lines ){
		# データを各変数に代入する
		($date,$name,$email,$value,$subject,$hpage,$himage,$code,$postid) = split(/\,/,$_);

		if ( $code eq $FORM{search} ) {
			$f = 1;
			$value =~ s/\0/\,/g; # ヌルコードに変換記録した半角カンマを復帰させる
			chop($himage) if $himage =~ /\n/;
			chop($hpage) if $hpage =~ /\n/;
			&disp;
		}
	}

	if ($f == 0){ print "みつかりません<br>";}

	print "<hr></body></html>\n";
	exit;
}

# ログ読み表示サブルーチン #######################################################
sub  read {
	
	# プロテクトキー生成
	local ( $ptime ) = time + $tim * 60 * 60;
	local ( $pkey ) = ( $ptime + $protect_a ) * $protect_b + $protect_c;
	
	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head>\n";
	print "$body\n";

	
	# バナーはここ
	
	print "<font size=+1><b>$title</b></font>　\n";
	print "<font size=-1><b><a href=\"http://www.geocities.com/Tokyo/Subway/1282/front.html\" target=\"_top\">おしらせページ</a></b></font> \n";
	print " <font size=-1><b><a href=\"http://freehosting1.at.webjump.com/sw/swatty-webjump/\" target=\"_top\">スワティ</a></b></font>\n";
#print "<font size=-1><b><a href=\"mailto:$mailadd\">連絡先</a></b></font>\n";

	print "<form method=$method action=\"$cgiurl\">\n";
	
	print "<input type=hidden name=\"action\" value=\"$action\">\n";
	print "投稿者 <input type=text name=\"name\" size=20 maxlength=40 value=\"$FORM{'name'}\"><br>";
	print "メール <input type=text name=\"email\" size=30><br>\n";
	print "題名　 <input type=text name=\"subject\" size=30 maxlength=60>  \n";
	print "<input type=submit value=\"投稿／リロード\"><input type=reset value=\"消す\"><p>内容<i>（タグは使えません。内容を書かずに投稿ボタンを押すとリロードになります。）</i><br><textarea name=\"value\" rows=5 cols=70></textarea><input type=hidden name=\"page\" size=70 value=\"http://\"><p>\n";
	print "表\示件数\n";
	print "<input type=text name=\"def\" size=8 value=\"$defnext\">\n";
	print "バックグラウンドカラー<input type=text name=\"bgcolor\" size=6 value=\"$bgc\"><input type=hidden name=\"link\" value=\"$FORM{'link'}\">\n";


 #$month月$mday日($youbi)$hour時$min分$sec秒

	print "<input type=hidden name=\"win_time\" value=\"$month$mday$hour$min$sec\">\n";


	print "URL自動リンク<input type=checkbox name=\"image\" value=\"1\" checked></font> \n";

	print "<input type=hidden name=\"code\" value=\"$sec$min\@$pkey.com\">\n";

	print "<p><font size=-1>最近の過去ログは<a href=\"./getlog.cgi\" target=\"_top\">ここ</a>。\n";

#カウンター
	if ( $countlevel > 0 ){
		print "<font size=-1>$countdateから ";
		&counter; print "$countplus（こわれにくさレベル$countlevel）</font>\n";	}

	print "<input type=hidden name=\"win_count\" value=\"$maxcount\">\n";

	# プロテクトコード出力
	print "<input type=hidden name=\"protect\" value=\"$pkey\">\n";
	
	
#	print "<br><i>新しい記事から表\示します。最高$max件の記事が記録され、それを超えると古い記事から削除されます。<br>\n";
#	print "１回の表\示で$def件を越える場合は、下のボタンを押すことで次の画面の記事を表\示します。</i>\n";

			print "<hr><a href=\"http://extra.onlineexpress.net/cgi-bin/strangeworld/bbs.cgi\">エクストラ</a>、<a href=\"http://www.kinsan.ne.jp/~miki/strangeworld/bbs.cgi\">きんさん</a>、 <a href=\"http://famille.onlineexpress.net/cgi-bin/strangeworld/bbs.cgi\">ふぁみーる</a>、<a href=\"http://www.bea.hi-ho.ne.jp/cgi-bin/user/strangeworld/bbs.cgi\">はいほー</a> | <a href=\"http://www4.famille.ne.jp/~haruna/remix/bbs.cgi\">REMIX</a>、<a href=\"http://kakumeigun.onlineexpress.net/cgi-bin/relax/bbs.cgi\">RELAX</a> | <a href=\"http://edoya.neko.to/2/upload.cgi\">ぁ界遺産</a>、<a href=\"http://saturdaytears.virtualave.net/cgi-bin/upload.cgi\">徘徊する骸</a>\n";

#	 サーチの注意書き
	print "<hr>最大\表\示：$max件　■：返信　★：投稿者検索　◆：スレッド検索　\表\示件数0件：未読メッセージ<hr>投稿の削除はしないので、この掲示板に関わるあらゆる行動は自分で責任をとってください。\n";

#	リロード
	print "<p></font></font><input type=submit value=\"投稿／リロード\">\n";


	print "</form>\n";


	
	#--- 記録記事の出力 ----------------------------------#
	
# $date=#$month月$mday日($youbi)$hour時$min分$sec秒
#

	# 記録ファイルを読み出しオープンして、配列<@lines>に格納する
open(DB,"$file");
	@lines = <DB>;
	close(DB);

#$FORM{'win_time'}=~ s/0//o;

	$accesses = @lines;
	$f = 0;
	foreach ( @lines ){
		# データを各変数に代入する
		($date,$name,$email,$value,$subject,$hpage,$himage,$code,$postid) = split(/\,/,$_);

$date_s = $date;
$date=~ s/月|日|\(|\)|時|分|秒|火|水|木|金|土//g;
#$date=~ s/0//o;

		if ( $FORM{'win_time'} <= $date ) {
			$f = $f + 1;
			$value =~ s/\0/\,/g; # ヌルコードに変換記録した半角カンマを復帰させる
			chop($himage) if $himage =~ /\n/;
			chop($hpage) if $hpage =~ /\n/;

            $date = $date_s;
			&disp;
		}
else { last; }

}

$g = $f;

		if ( $f eq 0 ) {print "<hr><p><font size=-1><i>未読メッセージはありません。</i></font><p>";}

else {print "<hr><p><font size=-1><i>$g件のメッセージがあります。</i></font><p>";}


	
	# このスクリプトの著作権表示（かならず表示してください）

		print "<form method=$method action=\"$cgiurl\"><input type=hidden name=\"def\" value=\"$def\"><input type=hidden name=\"bgcolor\" value=\"$bgc\"><input type=hidden name=\"win_time\" value=\"$month$mday$hour$min$sec\"><input type=submit value=\"　リロード　\"></form>\n";
	print "<h4 align=right><hr size=5><a href=\"http://www.ask.or.jp/~rescue/\">MiniBBS v7.5</a> <a href=\"http://www.bea.hi-ho.ne.jp/strangeworld/recycle/\">REQUIEM 990707γ</a> is Free.</h4>\n";
	print "</body></html>\n";
	exit;




}


# 各投稿表示用サブルーチン #############################################################
sub disp {

	$hpage0 =$hpage;
	$hpage0 =~ s/$cgiurl\?action=search1\&search=(.*)\&id=\d*/参考：$1/;
	print "<hr>";
	print "<font size=+1 color=\"#$subjc\"><b>$subject</b></font>　";
	

	if ($email ne '') { print "投稿者：<b><a href=\"mailto:$email\">$name</a></b>\n"; }
	else { print "投稿者：<b>$name</b></font>\n"; }

		print "<font size=-1>　投稿日：$date";

	print "　<a href=\"$cgiurl\?bgcolor\=$bgc\&action\=search1\&search\=$date\&id=$postid\" target=\"link\">■</a>";
	print "　<a href=\"$cgiurl\?bgcolor\=$bgc\&action\=search2\&search\=$name\" target=\"link\">★</a>";
	if ($hpage ne'' ) { print "　<a href=\"$cgiurl\?bgcolor\=$bgc\&action\=search3\&search\=$code\" target=\"link\">◆</a>\n"; }
	print "</font><p>\n";

if (($FORM{search}  eq '') && ($himage eq '1') ){
$value =~ s!((https?|ftp|gopher|telnet|whois|news):(=\S+|[\x21-\x7f])+)!<a href=\"$1\" target=\"link\">$1</a>!ig;

}


	print "<blockquote><pre>$value</pre><p>\n\n";
	
	if ($hpage ne '') { print "<a href=\"$hpage\" target=\"link\">$hpage0</a><p>\n"; }
	
	print "</blockquote>\n";
}

# エラー処理サブルーチン ############################################################
sub error {
	
	#  &error(xx); で呼び出されたルーチンは、()内の数字が $error に代入される。
	
	$error = $_[0];
	
	if    ($error eq "0") { $error_msg = '記録ファイルの入出力にエラーが発生しました。'; }
	elsif ($error eq "2") {	$error_msg = '内容が書かれていません。または記録禁止のタグが書かれています。'; }
	elsif ($error eq "3") {	$error_msg = 'メールアドレスが正しく入力されていません。'; }
	elsif ($error eq "4") {	$error_msg = 'メールアドレスは複数指定できません。'; }
	elsif ($error eq "5") {	$error_msg = '投稿内容が大きすぎます。'; }

	elsif ($error eq "6") {	$error_msg = 'アクセスが混み合ってるため、書き込みできませんでした。もう一度、投稿ボタンを押してください。'; }
	elsif ($error eq "form") { $error_msg = "投稿画面のＵＲＬが<br>$cgiurl<br>" . '以外からの投稿はできません。'; }
	elsif ($error eq "x") {	$error_msg = "以下の情報が記録されました。けけ"; }
	elsif ($error eq "xx") { $error_msg = "かわいそう"; }
	elsif ($error eq 'xxx') { $error_msg = ' '; }
	
	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head>\n";
	print "$body\n";
	print "<h3>$error_msg</h3>\n";

	
	
	if ($error eq "x") {
		while ( ($a,$b) = each %ENV) {
			print "$a=$b<br><br>\n";
		}
	}
	
	if ($error eq "xx") {
		print "<table>\n";
	}

	print "</body></html>\n";
	exit;
}

# カウンター処理サブルーチン #########################################################
sub counter {

	for( $i=0 ; $i < $countlevel ; $i++){
		open(IN,"$countfile$i$countfiledat");
		$count[$i] = <IN>;
		$filenumber[$count[$i]] = $i;
		close(IN);
	}
	@sortedcount = sort by_number @count;
	$maxcount = $sortedcount[$countlevel-1];
	$mincount = $sortedcount[0];

	$maxcount++;
	print $maxcount;

	open(OUT,">$countfile$filenumber[$mincount]$countfiledat");
	print OUT $maxcount;
	close(OUT);
}

sub by_number {
	$a <=> $b;
}

#end_of_script
