#! /usr/local/bin/perl


#はじあや＠ふぁみーるのパソヲタさん、本当にありがとう


#--------------------

$body = '<body bgcolor="#004040" text="#ffffff" link="#eeffee" vlink="#dddddd" alink="#ff0000">';
$bbstitle ="あやしいわーるど";

#$logdir = 'http://www2u.biglobe.ne.jp/~rebirth/strange/log/';

$cgiurl = 'getlog.cgi';
$action ='getlog';

$bbsurl = './bbs.cgi';
$logurl = './log/990720.html';

# 日本語コード変換ライブラリjocde.plのパス
require './jcode.pl';

# キーワードの最大文字数（半角）
$keylength = 64;

# 時差 サーバの時計がずれてる時や日本時間以外にしたい時に使う
$tim = 0;

# 時刻処理
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time + $tim );

$month = ($mon + 1);
$month= "0$month";


$filedate3 = "./log/$year$month$mday.html";
$m2day =$mday-1;
$filedate2 = "./log/$year$month$m2day.html";
$m1day =$mday-2;
$filedate1 = "./log/$year$month$m1day.html";
#--------------------

$buffer = $ENV{'QUERY_STRING'};


@argv = split(/&/,$buffer);
foreach (@argv) {
	($name, $value) = split(/=/);
	$value =~ tr/+/ /;

	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	&jcode'convert(*value,'sjis');

	$COMMAND{$name} = $value;
}

&error(2) if (length($COMMAND{'keyword'}) > $keylength);
&viewlog if ($COMMAND{'action'} eq "$action");


&list;


# リストの出力
########################
sub list {

#&error(0) if(!opendir(DIR, $logdir));

opendir(DIR, $logdir);


	@files=readdir(DIR);
	closedir(DIR);

               @files = sort by_number @files;
               $end = @files;
               $end--; 


	print "Content-type: text/html\n\n";
	print "<html><head><title>$bbstitle 過去ログ</title></head>\n";
	print "<form method=get action=\"$cgiurl\">";
	print "$body\n";
	print "<center><font size=+1><b>$bbstitle 過去ログ一覧</b></font><br>\n";
	print "<input type=hidden name=\"action\" value=\"$action\">";
	print "<table>";
	print "<tr><td></td><td>ファイル名</td><td align=right>サイズ</td><td align=center></td></tr>";


($dev,$ino,$mode,$nlink,$uid,$gid,$rdev,$size,$atime,$mtime,$ctime,$blksize,$blocks) = stat $filedate1;



			print "<tr><td><input type=\"radio\" name=\"logfile\" value=\"$filedate1\"></td>";
			print "<td><a href=\"$filedate1\">$year$month$m1day.html</a></td>";
			print "<td align=right>$size byte</td><td align=center></td></tr>";

#########
($dev,$ino,$mode,$nlink,$uid,$gid,$rdev,$size,$atime,$mtime,$ctime,$blksize,$blocks) = stat $logurl;


			print "<tr><td><input type=\"radio\" name=\"logfile\" value=\"$filedate2\"></td>";
			print "<td><a href=\"$filedate2\">$year$month$m2day.html</a></td>";
			print "<td align=right>$size byte</td><td align=center></td></tr>";

#######
($dev,$ino,$mode,$nlink,$uid,$gid,$rdev,$size,$atime,$mtime,$ctime,$blksize,$blocks) = stat $filedate3;


			print "<tr><td><input type=\"radio\" name=\"logfile\" value=\"$filedate3\" checked></td>";
			print "<td><a href=\"$filedate3\">$year$month$mday.html</a></td>";
			print "<td align=right>$size byte</td><td align=center></td></tr>";



	print "<tr><td></td></tr><tr><td colspan=4>
※ラジオボタンでファイル名を指定してください。</td></tr><tr><td></td></tr>\n";
	print "<tr><td colspan=4><select name=\"hour1\">";
	print "<option value=\"00\">0";
	print "<option value=\"01\">1";
	print "<option value=\"02\">2";
	print "<option value=\"03\">3";
	print "<option value=\"04\">4";
	print "<option value=\"05\">5";
	print "<option value=\"06\">6";
	print "<option value=\"07\">7";
	print "<option value=\"08\">8";
	print "<option value=\"09\">9";
	print "<option value=\"10\">10";
	print "<option value=\"11\">11";
	print "<option value=\"12\">12";
	print "<option value=\"13\">13";
	print "<option value=\"14\">14";
	print "<option value=\"15\">15";
	print "<option value=\"16\">16";
	print "<option value=\"17\">17";
	print "<option value=\"18\">18";
	print "<option value=\"19\">19";
	print "<option value=\"20\">20";
	print "<option value=\"21\">21";
	print "<option value=\"22\">22";
	print "<option value=\"23\">23";
	print "</select>時";
	print"<select name=\"min1\">";
	print "<option value=\"00\">00";
	print "<option value=\"05\">05";
	print "<option value=\"10\">10";
	print "<option value=\"15\">15";
	print "<option value=\"20\">20";
	print "<option value=\"25\">25";
	print "<option value=\"30\">30";
	print "<option value=\"35\">35";
	print "<option value=\"40\">40";
	print "<option value=\"45\">45";
	print "<option value=\"50\">50";
	print "<option value=\"55\">55";
	print "</select>分から";

	print "<select name=\"hour2\">";
	print "<option value=\"24\">24";
	print "<option value=\"00\">0";
	print "<option value=\"01\">1";
	print "<option value=\"02\">2";
	print "<option value=\"03\">3";
	print "<option value=\"04\">4";
	print "<option value=\"05\">5";
	print "<option value=\"06\">6";
	print "<option value=\"07\">7";
	print "<option value=\"08\">8";
	print "<option value=\"09\">9";
	print "<option value=\"10\">10";
	print "<option value=\"11\">11";
	print "<option value=\"12\">12";
	print "<option value=\"13\">13";
	print "<option value=\"14\">14";
	print "<option value=\"15\">15";
	print "<option value=\"16\">16";
	print "<option value=\"17\">17";
	print "<option value=\"18\">18";
	print "<option value=\"19\">19";
	print "<option value=\"20\">20";
	print "<option value=\"21\">21";
	print "<option value=\"22\">22";
	print "<option value=\"23\">23";
	print "</select>時";
	print"<select name=\"min2\">";
	print "<option value=\"00\">00";
	print "<option value=\"05\">05";
	print "<option value=\"10\">10";
	print "<option value=\"15\">15";
	print "<option value=\"20\">20";
	print "<option value=\"25\">25";
	print "<option value=\"30\">30";
	print "<option value=\"35\">35";
	print "<option value=\"40\">40";
	print "<option value=\"45\">45";
	print "<option value=\"50\">50";
	print "<option value=\"55\">55";
	print "</select>分まで";

	print "</td></tr><br>";
	print " <tr><td colspan=4>検索：";
	print "<select name=\"searchmode\">";
	print "<option value=\"keyword\">全文";
	print "<option value=\"name\">投稿者名";
	print "<option value=\"subject\">題名\n</select>";
	print "<input type=text name=\"keyword\" size=\"24\" maxlength=$keylength></td></tr><tr><td colspan=4 align=center>";
	print "<input type=submit value=\"Get / Search\"></form></td></tr>";
	print "</table>";
	print "<hr>";
#print "現在ベータテスト中です。バグを見つけたら掲示板に書いてね";
	print "<p align=center><a href=\"$bbsurl\">掲示板へ</a></p>";
	print "<h4 align=right><a href=\"http://logshonin.virtualave.net/\">Getlog Ver0.3b4</a></h4>";
	print "</body></html>";

}



sub viewlog {

#if (!open(DB,"./log/$COMMAND{'logfile'}")) { &error(1); }

 open(DB,$COMMAND{'logfile'});

	@lines = <DB>;
	close(DB);
#----------------------------
	$COMMAND{'last'} = $COMMAND{'first'} + 1 if ($COMMAND{'first'} >= $COMMAND{'last'});
	$first = "$COMMAND{'hour1'}時$COMMAND{'min1'}分";
	$last = "$COMMAND{'hour2'}時$COMMAND{'min2'}分";
	
	if ($COMMAND{'searchmode'} eq 'name') { $keyword = "投稿者：.*>${COMMAND{'keyword'}}<"; }
	elsif ($COMMAND{'searchmode'} eq 'subject') { $keyword = "color=\"#ffffee\"><b>${COMMAND{'keyword'}}</b></font>"; }
	else { $keyword = $COMMAND{'keyword'}; }
	if ($keyword ne '') {
		$keyword =~ s/\\/\\\\/;
		$keyword =~ s/\[/\\[/;
	}

#----------------------------



	print "Content-type: text/html\n\n";
	print "<html><head><title>$bbstitle 過去ログ $COMMAND{'logfile'}</title></head>";
	print "$body";
	print "<font size=+1><b>$COMMAND{'logfile'} $first～$last</b></font>";

############################

	$end = @lines;
	$end--;
	foreach (0 .. $end) {
#		MiniBBS7.5あやしいわーるど仕様
		if ($lines[$_] =~ /<font size=-1>　投稿日：/) {
			$hour = substr( $lines[$_], 36, 8 );

			
			last if ($hour ge "$first");
		}
		$skip++;
	}
	$skip--;

#print"<hr>";
	foreach ($skip .. $end) {
#	MiniBBS7.5あやしいわーるど仕様
		if ($lines[$_] =~ /<font size=-1>　投稿日：/) {
		$hour = substr( $lines[$_], 36, 8 );

			last if ($hour ge "$last");
		}
		

		if ($keyword ne '') {
			if ($lines[$_] =~ /$keyword/) {
				$flag = 1;
				$hit++; 
			}

			push( @article, $lines[$_] );
			if ($lines[$_] =~ /<\/blockquote>/) {
				print @article if ($flag > 0);  
				splice( @article, 0 );
				$flag = 0;
			}
		}

		else { print $lines[$_]; }
}

	if ($COMMAND{'keyword'} ne '') {
		print "<hr>";
		if ( $hit > 0 ) { print "<h3>「$COMMAND{'keyword'}」は $hit件見つかりました。</h3>"; }
		else { print "<h3>「$COMMAND{'keyword'}」は見つかりませんでした。</h3>"; }
	}


	print "</body></html>";

	exit;

}

####################





sub error {

	$error = $_[0];
	if ($error == 0) { $errmsg = 'ディレクトリが開けませんでした。'; }
	if ($error == 1) { $errmsg = 'ファイルが開けませんでした。'; }
	if ($error == 2) { $errmsg = 'キーワードが長すぎます。'; }

	print "Content-type: text/html\n";
	print "<html><head><title>エラー</title></head>";
	print "$body";
	print "<h1>$errmsg</h1>";
	print "</body></html>";
	exit;
}
