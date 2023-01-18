#! /usr/bin/perl


#---------------------------------#
#    Setup (Modify these pl0x)    #
#---------------------------------#


# Bulletin Board Name  --------------------------


$title = 'Dubious World@hi-ho'; 
# Associated links
$link = '<a href=\"http://extra.onlineexpress.net/cgi-bin/strangeworld/bbs.cgi\">エクストラ</a>、<a href=\"http://www.kinsan.ne.jp/~miki/strangeworld/bbs.cgi\">きんさん</a>、 <a href=\"http://famille.onlineexpress.net/cgi-bin/strangeworld/bbs.cgi\">ふぁみーる</a>、<a href=\"http://www.bea.hi-ho.ne.jp/cgi-bin/user/strangeworld/bbs.cgi\">はいほー</a> | <a href=\"http://www4.famille.ne.jp/~haruna/remix/bbs.cgi\">REMIX</a>、<a href=\"http://kakumeigun.onlineexpress.net/cgi-bin/relax/bbs.cgi\">RELAX</a> | <a href=\"http://edoya.neko.to/2/upload.cgi\">ぁ界遺産</a>、<a href=\"http://saturdaytears.virtualave.net/cgi-bin/upload.cgi\">徘徊する骸</a>';

# Set text color, background, etc.

# Body

$bgc    = '004040';

$textc  = 'ffffff';

$linkc  = 'eeffee';

$vlinkc = 'dddddd';

$alinkc = 'ff0000';

# Subject

$subjc  = 'ffffee';

# --- Number of posts -------------------------------------
# Default number of posts to display on one page
$def =  30;
# Default number of posts to display on one page
$defmin =  0;
# Maximum total posts (?)
$defmax =300;

# --- ＵＲＬ ----------------------------------------------
# Script filename
$cgiurl = 'bbs.cgi';


# Contact
$mailadd = 'goodby@strangers.com';

# Log URL
$loglog0 = 'log';
$loglog1 = 'http://';

# ---------------------------------------- Write-check ----------------------------------------
# Manager access information (CHANGE THIS)
$namez = 'しば';
$pass = 'chiba';
# maximum write capacity
$maxlength = 1024*16; 
# Number of characters of the submitted content
$max_v = 8000;      
#Number of lines of content to be submitted (to be combined with the number of characters above)
$max_line = 120;     

# Number of double write checks
$check = 10;
# Double write check bytes
$checklength = 10;
# Set the maximum number of writings to be registered
$max = '300';
 
# ------------------------------------ directory and file name ------------------------------------
# Path of the Japanese code conversion library jocde.pl
require '/jcode.pl';
# Set the path to the recording file whose contents will be written
$file = 'loveyou.dat';
# Specify the name and extension of the log file name to be taken separately
$logfile = "/log/log";
$logfiledat = ".html";

# -------------------------------------------- カウンタ --------------------------------------------
# counter plus value
$countplus = "";
# Counter start date
$countdate = '99/6/20';
# Specify the name and extension of the counter file
$countfile = '/count/count';
$countfiledat = '.txt';
# Counter strength (not used when 0)
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
$y0="Sunday"; $y1="Monday"; $y2="Tuesday"; $y3="Thursday"; $y4="Wednesday"; $y5="Friday"; $y6="Saturday";
$youbi = ($y0,$y1,$y2,$y3,$y4,$y5,$y6) [$wday];

# 時刻フォーマット
$date_now = "$monthMonth$mdayDay($youbi)$hourHour$minMinute$secSecond";
# Log file name acquisition
$filedate = "$logfile$year$month$mday$logfiledat";
# Unfamiliar Variables
$gesu = $ENV{'REMOTE_PORT'};
# Action name at time of submission
$action = "regist";

# additional measures -------------------------------

# External Posting Prevention Code
$protect_a = 9987;	# four-digit number
$protect_b = 55;		# two-digit number
$protect_c = 112;		# three-digit number

# Maximum file size of logs
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
#print "<font size=-1><b><a href=\"mailto:$mailadd\">Contact</a></b></font>\n";

	print "<form method=$method action=\"$cgiurl\">\n";
	
	print "<input type=hidden name=\"action\" value=\"$action\">\n";
	print "Poster <input type=text name=\"name\" size=20 maxlength=40 value=\"$FORM{'name'}\"><br>";
	print "E-mail <input type=text name=\"email\" size=30><br>\n";
	print "Title　 <input type=text name=\"subject\" size=30 maxlength=60>  \n";
	print "<input type=submit value=\"Post／Reload\"><input type=reset value=\"Reset\"><p>Contents<i>（HTML tags are not allowed. If you do not post something it will reload.）</i><br><textarea name=\"value\" rows=5 cols=70></textarea><input type=hidden name=\"page\" size=70 value=\"http://\"><p>\n";
	print "Total of posts shown\n";
	print "<input type=text name=\"def\" size=8 value=\"$defnext\">\n";
	print "Background color<input type=text name=\"bgcolor\" size=6 value=\"$bgc\"><input type=hidden name=\"link\" value=\"$FORM{'link'}\">\n";
	print "URL auto-linking <input type=checkbox name=\"image\" value=\"1\" checked></font> \n";

	print "<input type=hidden name=\"code\" value=\"$sec$min\@$pkey.com\">\n";



	print "<input type=hidden name=\"win_time\" value=\"$month$mday$hour$min$sec\">\n";


	print "<p><font size=-1>The recent logs are <a href=\"./getlog.cgi\" target=\"_top\">here</a>.\n";




#カウンター
	if ( $countlevel > 0 ){
		print "<font size=-1>from $countdate";
		&counter; print "$countplus（Crack resistance level$countlevel）</font>\n";	}

	print "<input type=hidden name=\"win_count\" value=\"$maxcount\">\n";


	# プロテクトコード出力
	print "<input type=hidden name=\"protect\" value=\"$pkey\">\n";
	
	
#	print "<br><i>Table is shown starting with the newest posts. Old posts will be pruned after $max posts have been submitted.<br>\n";
#	print "If the number of posts exceeds $def in one page, you can press the button below to display the posts on the next page.</i>\n";


			print "<hr>$link\n";


#	 サーチの注意書き
	print "max\table:display:$max ■：Replies ★：Posters Search ◆：Thread Search \table:display:0件：Unread\table:display<hr>You are responsible for any and all actions related to this forum. \n";


#	リロード
	print "<p></font></font><input type=submit value=\"Post/Reload">\n";
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
		print "<font size=-1><i>These are the $ith to $jth newest posts currently registered.</i></font><p>\n";
		print "<form method=$method action=\"$cgiurl\">\n";
		print "<input type=hidden name=\"page\" value=\"$page_next\">\n";
		print "<input type=hidden name=\"def\" value=\"$def\">\n";
		print "<input type=hidden name=\"bgcolor\" value=\"$bgc\">\n";
		print "<input type=submit value=\"Next page\"></form>\n";
	}
	else {
	
		print "<font size=-1><i>The above is... Currently registered posts from $ith to $jth in order of newest to oldest.";
		print "No further posts are available.</i></font>\n";
	}
	
	# このスクリプトの著作権表示（かならず表示してください）

		print "<form method=$method action=\"$cgiurl\"><input type=hidden name=\"def\" value=\"$def\"><input type=hidden name=\"bgcolor\" value=\"$bgc\"><input type=submit value=\"　リロード　\"></form>\n";
	print "<h4 align=right><hr size=5><a href=\"https://www.rescue.ne.jp/cgi/minibbs1/\">MiniBBS v7.5</a> <a href=\"https://github.com/ShockAwer/minibbs-hi-ho/\">REQUIEM 990707γ</a> is Free.</h4>\n";
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
			( 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday' )[$cwday],
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
		$formname =~ s/$namez/<small>(Dead horse)<\/small>/g;
#		$formname =~ s/Branch゜/g;
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
	# HTML header if the file is empty
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
		if ($FORM{'email'} ne '') { print LOG "　Name：<b><a href=\"mailto:$FORM{'email'}\">$formname</a></b>\n"; }
		else { print LOG "　Name：<font color=\"#$subjc\"><b>$formname</b></font>\n"; }
		print LOG "<font size=-1>　Date：$date_now";
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
		print "<html><head><title>Entry completed</title></head>\n";
		print "$body\n";
		print "<h1>Complete post</h1>\n";
		exit;
	}
#	print "Location: $cgiurl" . '?' . "\n\n";
#	exit;
}


# フォロー投稿サブルーチン（search1） ############################################
sub search1 {

	#--- 入力フォーム画面 --------------------------------#

	print "Content-type: text/html\n\n";
	print "<html><head><title>$FORM{search}Reply</title></head>\n";
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
		print "Poster <input type=text name=\"name\" size=20 maxlength=20><br>";		
		print "E-mail <input type=text name=\"email\" size=30><br>\n";
		print "Title　 <input type=text name=\"subject\" size=30 value=\"＞$name\">  \n";
		print "<input type=submit value=\"  Post  \"><input type=reset value=\"Reset\"><p>\n";	


		print "<input type=hidden name=\"def\" value=\"$defnext\">\n";
		
		# プロテクトコード出力
		print "<input type=hidden name=\"protect\" value=\"$pkey\">\n";
		
		print "Content <i>(HTML tags are not allowed.) \n";
		print "(If you press the submit button without writing the content, it will reload.）</i><br>\n";
		
		print "<textarea name=\"value\" rows=5 cols=70>$value\r";
		
		print "</textarea><p>\n";



		if ($himage ne '1') { 	print "URL auto-linking<input type=checkbox name=\"image\" value=\"1\"></font> \n";}
else{
	print "URL auto-linking<input type=checkbox name=\"image\" value=\"1\" checked></font> \n";}

#カウンター
	if ( $countlevel > 0 ){
		print "<font size=-1 color=$bgc>$countdateから ";
		&counter; print "$countplus（Crack resistance level$countlevel）</font>\n";	}

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
	print "<html><head><title>$FORM{search}List of posts by</title></head>\n";
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
