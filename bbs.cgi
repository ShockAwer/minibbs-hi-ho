#! /usr/local/bin/perl


#----------------#
#    �����ݒ�    #
#----------------#


# �f���̖��O --------------------------


$title = '���₵����[��ǁ��͂��ف['; 

# �����F��w�i�Ȃǂ̐ݒ�

# body��

$bgc    = '004040';

$textc  = 'ffffff';

$linkc  = 'eeffee';

$vlinkc = 'dddddd';

$alinkc = 'ff0000';

# �薼�̐F

$subjc  = 'ffffee';

# --- �\������ --------------------------------------------
# �P�y�[�W�ɕ\�����錏���̃f�t�H���g�l
$def =  30;
# �P�y�[�W�ɕ\�����錏���̍ŏ��l
$defmin =  0;
# ���̌����ȏ�Ń����[�h�^�������݂����Ƃ��ɂ͎��͂��̌����ɂ���B
$defmax =300;

# --- �t�q�k ----------------------------------------------
# ���̃X�N���v�g
$cgiurl = 'bbs.cgi';


# �A����
$mailadd = 'goodby@strangers.com';

# ���O�̂t�q�k
$loglog0 = 'log';
$loglog1 = 'http://';

# ---------------------------------------- �������݃`�F�b�N ----------------------------------------
# �Ǘ��l���O�`�F�b�N�E���[���A�h���X�E�p�X���[�h
$namez = '����';
$pass = 'chiba';
# �������ݍő��
$maxlength = 1024*16; 
#���e���e������
$max_v = 8000;      
#���e���e�s���i��̕������Ƃ̌��ˍ������l���āj
$max_line = 120;     

# ��d�������݃`�F�b�N����
$check = 10;
# ��d�������݃`�F�b�N�o�C�g��
$checklength = 10;
# �������݌����̍ő�o�^���̐ݒ�
$max = '300';
 
# ------------------------------------ �f�B���N�g���E�t�@�C���� ------------------------------------
# ���{��R�[�h�ϊ����C�u����jocde.pl�̃p�X
require './jcode.pl';
# ���e���������܂��L�^�t�@�C���̃p�X��ݒ�
$file = './loveyou.dat';
# �ʓr�Ƃ郍�O�̃t�@�C�����擪�����E�g���q�̎w��
$logfile = "./log/";
$logfiledat = ".html";

# -------------------------------------------- �J�E���^ --------------------------------------------
# �J�E���^�v���X�l
$countplus = "";
# �J�E���^�J�n��
$countdate = '99/6/20';
# �J�E���^�t�@�C���̐擪�����E�g���q�̎w��
$countfile = './count/count';
$countfiledat = '.txt';
# �J�E���^���x�i�O�̂Ƃ��͎g�p���Ȃ��j
$countlevel = 3;

# --------------------------------------------- ���̑� ---------------------------------------------
# ����
$tim =0*3600;
# ���͌`���̐ݒ�
$method = 'post';


# ��������
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time + $tim );
$month = ($mon + 1);

# �����̃[���T�v���X
if ($month < 10) { $month = "0$month"; }
if ($mday < 10)  { $mday  = "0$mday";  }
if ($sec < 10)   { $sec   = "0$sec";   }
if ($min < 10)   { $min   = "0$min";   }
if ($hour < 10)  { $hour  = "0$hour";  }

# �j���ϊ�����
$y0="��"; $y1="��"; $y2="��"; $y3="��"; $y4="��"; $y5="��"; $y6="�y";
$youbi = ($y0,$y1,$y2,$y3,$y4,$y5,$y6) [$wday];

# �����t�H�[�}�b�g
$date_now = "$month��$mday��($youbi)$hour��$min��$sec�b";
# ���O�t�@�C�����擾
$filedate = "$logfile$year$month$mday$logfiledat";
# �悭�킩��Ȃ��ϐ�
$gesu = $ENV{'REMOTE_PORT'};
# ���e����action��
$action = "regist";

# �ǉ��΍� -------------------------------

# �O�����e�h�~�R�[�h
$protect_a = 9987;	# 4��
$protect_b = 55;		# 2��
$protect_c = 112;		# 3��

# �ߋ����O�̍ő�t�@�C���T�C�Y
$maxoldlogsize = 3 * 1024 * 1024;		# 3MB

###########################################################################################

# �t�H�[�����͂��ꂽ�f�[�^��$buffer�Ɋi�[����iget��post���ɂ���Ď擾���@���قȂ�j
#if ($ENV{'REQUEST_METHOD'} eq "POST" && $ENV{'CONTENT_LENGTH'} < $maxlength) { read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'}); }
#else { $buffer = $ENV{'QUERY_STRING'}; }
if ($ENV{'REQUEST_METHOD'} eq "POST") { read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'}); } else { $buffer = $ENV{'QUERY_STRING'}; }
if ($ENV{'CONTENT_LENGTH'} > $maxlength) {&error(5);}

# $buffer�Ɋi�[���ꂽFORM�`���̃f�[�^�����o��
@pairs = split(/&/,$buffer);
foreach $pair (@pairs) {
	
	($name, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	
	# �L�^����f�[�^��sjis
	&jcode'convert(*value,'sjis');
	

#���s�A�ł̂������������i�R�s�ȏ㉽���������ɉ��s�݂̂̕����͉��s�����j
#�X�y�[�X�{���s�̘A�ł�����i��L��������邽�߂ɃX�y�[�X������ĉ��s���鈫�Y�̏ꍇ�j
	if ($value =~ /\r\n/) { $value =~ s/\r\n/\r/g; }
	if ($value =~ /\n/) { $value =~ s/\n/\r/g; }

	if ($value =~ / \r \r/) { $value =~ s/ \r \r//g; }
	if ($value =~ /\�@\r\�@\r/) { $value =~ s/\�@\r\�@\r//g; }
	if ($value =~ / \r/) { $value =~ s/ \r/\r/g; }
	if ($value =~ /\�@\r/) { $value =~ s/\�@\r/\r/g; }
	if ($value =~ /\r\r\r\r/) { $value =~ s/\r\r\r\r//g; }


	# �����̓s����̏���
	$value =~ s/\n//g; # ���s�����͏���
	
	if ($name eq 'value') { $value =~ s/&/&amp\;/g; $value =~ s/\,/\0/g; }
	elsif ($name ne 'page' && $name ne 'image') { $value =~ s/\,//g; $value =~ s/\;//g; $value =~ s/\://g; $value =~ s/\=//g; }
	
	else { $value =~ s/\,//g; }
	
	$value =~ s/</&lt\;/g; $value =~ s/>/&gt\;/g;
	
	$FORM{$name} = $value;
}


# �\���y�[�W���̌��� ##################################################
if ($FORM{'def'} ne '') { $def = $FORM{'def'}; }
if ($def < $defmin) { $def = $defmin;}
$defnext = $def;
if ($defnext > $defmax) {$defnext = $defmax;}

# �\���F�̌��� ########################################################
if ($FORM{'bgcolor'} ne '') { $bgc = $FORM{'bgcolor'}; }
$body  = "<body bgcolor=\"#$bgc\" text=\"#$textc\" link=\"#$linkc\" vlink=\"#$vlinkc\" alink=\"#$alinkc\">";

# �|�b�v�A�b�v�E�C���h�E�̌��� ########################################################

#if ($FORM{'image'} eq '') { $checked1='checked'; }
#if ($FORM{'image'} eq '2') { $checked2='checked'; }

#if ($FORM{'himage'} eq '') { $himage=''; }
#if ($FORM{'himage'} eq '2'){ $link='$sec$min'; }


# �S�̗̂�������肷��iaction��pwd�̓t�H�[�����͂��ꂽ�f�[�^���i�[���閼�O�j
########################################################
#    action=regist  --> �L���L�^�������Ēʏ��ʂ�
#    ���̑�  --> �ʏ��ʂ�

if (($FORM{'def'} eq '0') && ($FORM{'value'} ne '')) { &regist; }
if ($FORM{'def'} eq '0') { &read; }

if ($FORM{'action'} eq "$action")  { &regist; }
if ($FORM{'action'} eq 'search1') { &search1; }
if ($FORM{'action'} eq 'search2') { &search2; }
if ($FORM{'action'} eq 'search3') { &search3; }
&html;

# ���C���\���T�u���[�`�� #######################################################
sub html {
	
	# �v���e�N�g�L�[����
	local ( $ptime ) = time + $tim * 60 * 60;
	local ( $pkey ) = ( $ptime + $protect_a ) * $protect_b + $protect_c;
	
	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head>\n";
	print "$body\n";

	
	# �o�i�[�͂���
	
	print "<font size=+1><b>$title</b></font>\n";
	print "<font size=-1>�@<b><a href=\"http://www.geocities.com/Tokyo/Subway/1282/front.html\" target=\"_top\">�����点�y�[�W</a></b></font> \n";
	print " <font size=-1><b><a href=\"http://freehosting1.at.webjump.com/sw/swatty-webjump/\" target=\"_top\">�X���e�B</a></b></font>\n";
#print "<font size=-1><b><a href=\"mailto:$mailadd\">�A����</a></b></font>\n";

	print "<form method=$method action=\"$cgiurl\">\n";
	
	print "<input type=hidden name=\"action\" value=\"$action\">\n";
	print "���e�� <input type=text name=\"name\" size=20 maxlength=40 value=\"$FORM{'name'}\"><br>";
	print "���[�� <input type=text name=\"email\" size=30><br>\n";
	print "�薼�@ <input type=text name=\"subject\" size=30 maxlength=60>  \n";
	print "<input type=submit value=\"���e�^�����[�h\"><input type=reset value=\"����\"><p>���e<i>�i�^�O�͎g���܂���B���e���������ɓ��e�{�^���������ƃ����[�h�ɂȂ�܂��B�j</i><br><textarea name=\"value\" rows=5 cols=70></textarea><input type=hidden name=\"page\" size=70 value=\"http://\"><p>\n";
	print "�\\������\n";
	print "<input type=text name=\"def\" size=8 value=\"$defnext\">\n";
	print "�o�b�N�O���E���h�J���[<input type=text name=\"bgcolor\" size=6 value=\"$bgc\"><input type=hidden name=\"link\" value=\"$FORM{'link'}\">\n";
	print "URL���������N<input type=checkbox name=\"image\" value=\"1\" checked></font> \n";

	print "<input type=hidden name=\"code\" value=\"$sec$min\@$pkey.com\">\n";



	print "<input type=hidden name=\"win_time\" value=\"$month$mday$hour$min$sec\">\n";


	print "<p><font size=-1>�ŋ߂̉ߋ����O��<a href=\"./getlog.cgi\" target=\"_top\">����</a>�B\n";




#�J�E���^�[
	if ( $countlevel > 0 ){
		print "<font size=-1>$countdate���� ";
		&counter; print "$countplus�i�����ɂ������x��$countlevel�j</font>\n";	}

	print "<input type=hidden name=\"win_count\" value=\"$maxcount\">\n";


	# �v���e�N�g�R�[�h�o��
	print "<input type=hidden name=\"protect\" value=\"$pkey\">\n";
	
	
#	print "<br><i>�V�����L������\\�����܂��B�ō�$max���̋L�����L�^����A����𒴂���ƌÂ��L������폜����܂��B<br>\n";
#	print "�P��̕\\����$def�����z����ꍇ�́A���̃{�^�����������ƂŎ��̉�ʂ̋L����\\�����܂��B</i>\n";


			print "<hr><a href=\"http://extra.onlineexpress.net/cgi-bin/strangeworld/bbs.cgi\">�G�N�X�g��</a>�A<a href=\"http://www.kinsan.ne.jp/~miki/strangeworld/bbs.cgi\">���񂳂�</a>�A <a href=\"http://famille.onlineexpress.net/cgi-bin/strangeworld/bbs.cgi\">�ӂ��݁[��</a>�A<a href=\"http://www.bea.hi-ho.ne.jp/cgi-bin/user/strangeworld/bbs.cgi\">�͂��ف[</a> | <a href=\"http://www4.famille.ne.jp/~haruna/remix/bbs.cgi\">REMIX</a>�A<a href=\"http://kakumeigun.onlineexpress.net/cgi-bin/relax/bbs.cgi\">RELAX</a> | <a href=\"http://edoya.neko.to/2/upload.cgi\">���E��Y</a>�A<a href=\"http://saturdaytears.virtualave.net/cgi-bin/upload.cgi\">�p�j����[</a>\n";


#	 �T�[�`�̒��ӏ���
	print "<hr>�ő�\�\\���F$max���@���F�ԐM�@���F���e�Ҍ����@���F�X���b�h�����@\�\\������0���F����\�\\��<hr>���̌f���Ɋւ�邠����s���͑S�Ď����ŐӔC���Ƃ��Ă��������B\n";


#	�����[�h
	print "<p></font></font><input type=submit value=\"���e�^�����[�h\">\n";
	print "</form>\n";
	
	#--- �L�^�L���̏o�� ----------------------------------#
	
	# �L�^�t�@�C����ǂݏo���I�[�v�����āA�z��<@lines>�Ɋi�[����
    open(DB,"$file");
	@lines = <DB>;
	close(DB);
	
	if ($FORM{'page'} eq '') { $page = 0; } else { $page = $FORM{'page'}; }
	
	$accesses = @lines; $accesses--;
	$page_end = $page + $def - 1;
	if ($page_end > $accesses) { $page_end = $accesses; }

	foreach ($page .. $page_end) {
		($date,$name,$email,$value,$subject,$hpage,$himage,$code,$postid) = split(/\,/,$lines[$_]);
		$value =~ s/\0/\,/g; # �k���R�[�h�ɕϊ��L�^�������p�J���}�𕜋A������
		chop($himage) if $himage =~ /\n/;
		chop($hpage) if $hpage =~ /\n/;
		chop($postid) if $postid =~ /\n/;
		&disp;
	}
	
	#--- ���y�[�W���� ------------------------------------#
	
	print "</form><hr><p>\n";
	$page_next = $page_end + 1;
	$i = $page + 1; $j = $page_end + 1;
	if ($page_end ne $accesses) {
		print "<font size=-1><i>�ȏ�́A���ݓo�^����Ă���V����$i�Ԗڂ���$j�Ԗڂ܂ł̋L���ł��B</i></font><p>\n";
		print "<form method=$method action=\"$cgiurl\">\n";
		print "<input type=hidden name=\"page\" value=\"$page_next\">\n";
		print "<input type=hidden name=\"def\" value=\"$def\">\n";
		print "<input type=hidden name=\"bgcolor\" value=\"$bgc\">\n";
		print "<input type=submit value=\"���̃y�[�W\"></form>\n";
	}
	else {
	
		print "<font size=-1><i>�ȏ�́A���ݓo�^����Ă���V����$i�Ԗڂ���$j�Ԗڂ܂ł̋L���ł��B";
		print "����ȉ��̋L���͂���܂���B</i></font>\n";
	}
	
	# ���̃X�N���v�g�̒��쌠�\���i���Ȃ炸�\�����Ă��������j

		print "<form method=$method action=\"$cgiurl\"><input type=hidden name=\"def\" value=\"$def\"><input type=hidden name=\"bgcolor\" value=\"$bgc\"><input type=submit value=\"�@�����[�h�@\"></form>\n";
	print "<h4 align=right><hr size=5><a href=\"http://www.ask.or.jp/~rescue/\">MiniBBS v7.5</a> <a href=\"http://www.bea.hi-ho.ne.jp/strangeworld/recycle/\">REQUIEM 990707��</a> is Free.</h4>\n";
	print "</body></html>\n";
	exit;
}

# �������ݏ����T�u���[�`�� ############################################################
sub regist {
	
	# ���e���X�y�[�X�Ȃ烊���[�h
	if ($FORM{'value'} eq "") { &html; }

 # �ʂ̃y�[�W���炱�̂b�f�h�ւ̓��e��r�����鏈��
	$ref = $ENV{'HTTP_REFERER'};
	$ref_url = $cgiurl; $ref_url =~ s/\~/.*/g;
	if (!($ref =~ /$ref_url/i)) { &error(form); }
	
	# ���͂��ꂽ�f�[�^�̃`�F�b�N ##################################
	if ($FORM{'bgcolor'} eq "") { &error(1); }
	if ($FORM{'def'} eq "") { &error(1); }
	if ($FORM{'win_time'} eq "") { &error(1); }
	if ($FORM{'win_count'} eq "") { &error(1); }
	if ($FORM{'name'} eq "") { $FORM{'name'} = ''; }
	if ($FORM{'email'} =~ /,/) { &error(4); }
          $FORM{'email'}=~ s/\"//g;
	if ($FORM{'email'} ne "") { if (!($FORM{'email'} =~ /(.*)\@(.*)\.(.*)/)) { &error(3); }}
	if ($FORM{'subject'} eq "") { $FORM{'subject'} = '�@'; }
	
	if ($FORM{'page'} eq "" || $FORM{'page'} eq "http://") { $FORM{'page'} = ''; }
	else{
		$FORM{'page'} =~ s/\s//g;$FORM{'page'} =~ s/\"//g;$FORM{'page'} =~ s/\'//g;
		$FORM{'page'} =~ s/http\:\/\/http\:\/\//http\:\/\//g;
	}
	# �s������
if ($max_line) {
		$value_size = ($FORM{'value'} =~ tr/\r/\r/) + 1;     # \r �̐��𐔂���
		if ($value_size > $max_line) { &error(1); }
	}
	# ����������
	if ($max_v) {
		$value_size = length($FORM{'value'});
		if ($value_size > $max_v)  { &error(1); }
	}
	
     # �J�E���^�[����

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


# �v���e�N�g�R�[�h�`�F�b�N
	if ( $FORM{'protect'} ne '' ) {
		local ( $ptime ) = time + $tim * 60 * 60;
		local ( $pcheck ) = ( $FORM{'protect'} - $protect_c ) / $protect_b - $protect_a;
		
		( $csec, $cmin, $chour, $cmday, $cmon, $cyear, $cwday, $cyday, $cisdat )
			= localtime ( $pcheck );
		$cyear += 1900;
		$cmon++;
		local ( $cnowdate ) = sprintf ( "%d/%02d/%02d(%s)%02d��%02d��%02d�b", 
			$cyear, $cmon, $cmday, 
			( '��', '��', '��', '��', '��', '��', '�y' )[$cwday],
			$chour, $cmin, $csec );
		if ( 
		  ( $csec  < 0 ) || ( $csec  > 60 ) ||
		  ( $cmin  < 0 ) || ( $cmin  > 60 ) ||
		  ( $chour < 0 ) || ( $chour > 24 ) ||
		  ( ( $ptime - $pcheck ) > 1 * 60 * 60 ) ) {	# �P����
			&error ( 'xxx' );
		}
	} else {
		&error ( 'xxx' );
	}


	
	# �ߋ����O�̃t�@�C���T�C�Y�`�F�b�N
	if ( ( -s $filedate ) > $maxoldlogsize ) {
		&error (0);
	}


	
	# ���e�Җ��`�F�b�N
	$formname = $FORM{'name'};
#	if ($formname eq "$nameng"){ &error(xx); }
	if ($formname eq "$pass"){$formname = $namez; $FORM{'email'} = $mailadd;}
	else {
		$formname =~ s/$namez/<small>����<\/small>/g;
#		$formname =~ s/����/���́K/g;
	}
	
# �L�^�t�@�C����ǂݏo���I�[�v�����āA�z��<@lines>�Ɋi�[����
	open (DB,"+<$file") || &error (0);
	eval 'flock (DB, 2)';
	@lines = <DB>;


	
	# �ő�ێ��L�^���̏���
	$i = 0;
	foreach $line (@lines) {
		$i++;
		if ($i == $max) { last; }
		push(@new,$line);
	}

	# �A��������e�������݃`�F�b�N
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

	# ID����
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
		

# �ߋ����O�o��
########################
		$FORM{'value'} =~ s/\0/\,/g;
		open(LOG,">>$filedate") || &error(0);
		eval 'flock (LOG, 2)';


if (-z LOG) {
	# �t�@�C������̏ꍇ��HTML�w�b�_��t����
	print LOG "<html>\n<body bgcolor=\"#$bgc\" text=\"#$textc\" link=\"#$linkc\" vlink=\"#$vlinkc\" alink=\"#$alinkc\">\n<hr>";

# �ۑ���T�����߂����ߋ����O�t�@�C���͍폜
	( $oldsec, $oldmin, $oldhour, $oldmday, $oldmonth, $oldyear, $oldwday, $oldyday, $oldisdst )
  = localtime ( time + $tim - 3 * 60 * 60 * 24 );
$oldmonth += 1;
$oldlogfilename = sprintf ( "%s%d%02d%02d%s", $logfile, $oldyear, $oldmonth, $oldmday, $logfiledat );
	unlink $oldlogfilename;
}

		print LOG "<font size=+1 color=\"#$subjc\"><b>$FORM{'subject'}</b></font>";
		# ���[���A�h���X���L�^����Ă���f�[�^�ɂ̓����N��t����
		if ($FORM{'email'} ne '') { print LOG "�@���e�ҁF<b><a href=\"mailto:$FORM{'email'}\">$formname</a></b>\n"; }
		else { print LOG "�@���e�ҁF<font color=\"#$subjc\"><b>$formname</b></font>\n"; }
		print LOG "<font size=-1>�@���e���F$date_now";
	    print LOG "</font><p>\n";
if ($FORM{image} eq '1') {

    $FORM{'value'} =~ s!((https?|ftp|gopher|telnet|whois|news):(=\S+|[\x21-\x7f])+)!<a href="$1" target="$link">$1</a>!ig;
}


		print LOG "<blockquote><pre>$FORM{'value'}</pre><p>\n\n";
		
		# �t�q�k���L�^����Ă���f�[�^�ɂ̓����N��t����
		if ($FORM{'page'} ne '') {
			$page0 = $FORM{'page'};
			$page0 =~ s/$cgiurl\?action=search1\&search=(.*)\&id=\d*/�Q�l�F$1/;
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

	
	# �L�^������A�ēǂݍ��݂���
	if ( $FORM{'def'} eq "0" ) { &read; }
	elsif ( $FORM{'follow'} ne "on" ) { &html; }
	else {
		print "Content-type: text/html\n\n";
		print "<html><head><title>�������݊���</title></head>\n";
		print "$body\n";
		print "<h1>�������݊���</h1>\n";
		exit;
	}
#	print "Location: $cgiurl" . '?' . "\n\n";
#	exit;
}


# �t�H���[���e�T�u���[�`���isearch1�j ############################################
sub search1 {

	#--- ���̓t�H�[����� --------------------------------#

	print "Content-type: text/html\n\n";
	print "<html><head><title>$FORM{search}�ɕԐM</title></head>\n";
	print "$body\n";

	# �o�i�[�͂���

	#--- �L�^�L���̏o�� ----------------------------------#

	# �L�^�t�@�C����ǂݏo���I�[�v�����āA�z��<@lines>�Ɋi�[����
    open(DB,"$file");
	@lines = <DB>;
	close(DB);

	$accesses = @lines;
	$f = 0; $i = 0;

	while (($f == 0) && ($i < $accesses)){

		# �f�[�^���e�ϐ��ɑ������
		($date,$name,$email,$value,$subject,$hpage,$himage,$code,$postid) = split(/\,/,$lines[$i]);
		chop ($postid) if $postid =~ /\n/;
		if ($postid eq $FORM{id}) { $f = 1;}
		$i++;
	}


	if ($f == 1){
		$value =~ s/\0/\,/g; # �k���R�[�h�ɕϊ��L�^�������p�J���}�𕜋A������
		chop($himage) if $himage =~ /\n/;
		chop($hpage) if $hpage =~ /\n/;
		
		&disp;
		print "<hr>\n";
		
		$value =~ s/\r/\r&gt; /g;
  $value =~ s/\r&gt;\s&gt;\s*\r/\r/g;
  $value ="&gt; $value";
#$value =~ s/&gt; &gt; &gt;.*?\r//g; 
		print "<p>\n";



		# �v���e�N�g�L�[����
		local ( $ptime ) = time + $tim * 60 * 60;
		local ( $pkey ) = ( $ptime + $protect_a ) * $protect_b + $protect_c;
		
		print "<form method=$method action=\"$cgiurl\">\n";
		print "<input type=hidden name=\"action\" value=\"$action\">\n";

if ($FORM{'link'} ne '') { $link = $FORM{'link'}; }

	if ($FORM{'link'} ne '_top') { print "<input type=hidden name=\"follow\" value=\"on\">\n"; }
		print "���e�� <input type=text name=\"name\" size=20 maxlength=20><br>";		
		print "���[�� <input type=text name=\"email\" size=30><br>\n";
		print "�薼�@ <input type=text name=\"subject\" size=30 value=\"��$name\">  \n";
		print "<input type=submit value=\"  ���e  \"><input type=reset value=\"����\"><p>\n";	


		print "<input type=hidden name=\"def\" value=\"$defnext\">\n";
		
		# �v���e�N�g�R�[�h�o��
		print "<input type=hidden name=\"protect\" value=\"$pkey\">\n";
		
		print "���e<i>�i�^�O�͎g���܂���B\n";
		print "���e���������ɓ��e�{�^���������ƃ����[�h�ɂȂ�܂��B�j</i><br>\n";
		
		print "<textarea name=\"value\" rows=5 cols=70>$value\r";
		
		print "</textarea><p>\n";



		if ($himage ne '1') { 	print "URL���������N<input type=checkbox name=\"image\" value=\"1\"></font> \n";}
else{
	print "URL���������N<input type=checkbox name=\"image\" value=\"1\" checked></font> \n";}

#�J�E���^�[
	if ( $countlevel > 0 ){
		print "<font size=-1 color=$bgc>$countdate���� ";
		&counter; print "$countplus�i�����ɂ������x��$countlevel�j</font>\n";	}

	print "<input type=hidden name=\"win_count\" value=\"$maxcount\">\n";

	print "<input type=hidden name=\"win_time\" value=\"$month$mday$hour$min$sec\">\n";

		print "<input type=hidden name=\"code\" value=\"$code\">\n";
		print "<input type=hidden name=\"page\" size=70 value=\"$cgiurl\?action\=search1\&search\=$date\&id=$postid\">\n";
		print "<input type=hidden name=\"bgcolor\" value=\"$bgc\"></form><p>\n";	
}

	else { print "�݂���܂���<br>";}

	
	print "<hr></body></html>\n";
	exit;
}


# ���e�Җ��T�[�`�p�T�u���[�`���isearch2�j ############################################
sub search2 {

	print "Content-type: text/html\n\n";
	print "<html><head><title>$FORM{search}�̓��e�ꗗ</title></head>\n";
	print "$body\n";

	# �o�i�[�͂���

	#--- �L�^�L���̏o�� ----------------------------------#

	# �L�^�t�@�C����ǂݏo���I�[�v�����āA�z��<@lines>�Ɋi�[����
    open(DB,"$file");
	@lines = <DB>;
	close(DB);

	$accesses = @lines;
	$f = 0;
	foreach ( @lines ){
		# �f�[�^���e�ϐ��ɑ������
		($date,$name,$email,$value,$subject,$hpage,$himage,$code,$postid) = split(/\,/,$_);
		if ( $name eq $FORM{search} ) {
			$f = 1;
			$value =~ s/\0/\,/g; # �k���R�[�h�ɕϊ��L�^�������p�J���}�𕜋A������
			chop($himage) if $himage =~ /\n/;
			chop($hpage) if $hpage =~ /\n/;
			&disp;
		}
	}

	if ($f == 0){ print "�݂���܂���<br>";}

	print "<hr></body></html>\n";
	exit;
}

# �g�s�b�N�T�[�`�p�T�u���[�`���isearch3�j ############################################
sub search3 {


	print "Content-type: text/html\n\n";
	print "<html><head><title>�X���b�h�ꗗ</title></head>\n";
	print "$body\n";

	#--- �L�^�L���̏o�� ----------------------------------#

	# �L�^�t�@�C����ǂݏo���I�[�v�����āA�z��<@lines>�Ɋi�[����
open(DB,"$file");

	@lines = <DB>;
	close(DB);

	$accesses = @lines;
	$f = 0;
	foreach ( @lines ){
		# �f�[�^���e�ϐ��ɑ������
		($date,$name,$email,$value,$subject,$hpage,$himage,$code,$postid) = split(/\,/,$_);

		if ( $code eq $FORM{search} ) {
			$f = 1;
			$value =~ s/\0/\,/g; # �k���R�[�h�ɕϊ��L�^�������p�J���}�𕜋A������
			chop($himage) if $himage =~ /\n/;
			chop($hpage) if $hpage =~ /\n/;
			&disp;
		}
	}

	if ($f == 0){ print "�݂���܂���<br>";}

	print "<hr></body></html>\n";
	exit;
}

# ���O�ǂݕ\���T�u���[�`�� #######################################################
sub  read {
	
	# �v���e�N�g�L�[����
	local ( $ptime ) = time + $tim * 60 * 60;
	local ( $pkey ) = ( $ptime + $protect_a ) * $protect_b + $protect_c;
	
	print "Content-type: text/html\n\n";
	print "<html><head><title>$title</title></head>\n";
	print "$body\n";

	
	# �o�i�[�͂���
	
	print "<font size=+1><b>$title</b></font>�@\n";
	print "<font size=-1><b><a href=\"http://www.geocities.com/Tokyo/Subway/1282/front.html\" target=\"_top\">�����点�y�[�W</a></b></font> \n";
	print " <font size=-1><b><a href=\"http://freehosting1.at.webjump.com/sw/swatty-webjump/\" target=\"_top\">�X���e�B</a></b></font>\n";
#print "<font size=-1><b><a href=\"mailto:$mailadd\">�A����</a></b></font>\n";

	print "<form method=$method action=\"$cgiurl\">\n";
	
	print "<input type=hidden name=\"action\" value=\"$action\">\n";
	print "���e�� <input type=text name=\"name\" size=20 maxlength=40 value=\"$FORM{'name'}\"><br>";
	print "���[�� <input type=text name=\"email\" size=30><br>\n";
	print "�薼�@ <input type=text name=\"subject\" size=30 maxlength=60>  \n";
	print "<input type=submit value=\"���e�^�����[�h\"><input type=reset value=\"����\"><p>���e<i>�i�^�O�͎g���܂���B���e���������ɓ��e�{�^���������ƃ����[�h�ɂȂ�܂��B�j</i><br><textarea name=\"value\" rows=5 cols=70></textarea><input type=hidden name=\"page\" size=70 value=\"http://\"><p>\n";
	print "�\\������\n";
	print "<input type=text name=\"def\" size=8 value=\"$defnext\">\n";
	print "�o�b�N�O���E���h�J���[<input type=text name=\"bgcolor\" size=6 value=\"$bgc\"><input type=hidden name=\"link\" value=\"$FORM{'link'}\">\n";


 #$month��$mday��($youbi)$hour��$min��$sec�b

	print "<input type=hidden name=\"win_time\" value=\"$month$mday$hour$min$sec\">\n";


	print "URL���������N<input type=checkbox name=\"image\" value=\"1\" checked></font> \n";

	print "<input type=hidden name=\"code\" value=\"$sec$min\@$pkey.com\">\n";

	print "<p><font size=-1>�ŋ߂̉ߋ����O��<a href=\"./getlog.cgi\" target=\"_top\">����</a>�B\n";

#�J�E���^�[
	if ( $countlevel > 0 ){
		print "<font size=-1>$countdate���� ";
		&counter; print "$countplus�i�����ɂ������x��$countlevel�j</font>\n";	}

	print "<input type=hidden name=\"win_count\" value=\"$maxcount\">\n";

	# �v���e�N�g�R�[�h�o��
	print "<input type=hidden name=\"protect\" value=\"$pkey\">\n";
	
	
#	print "<br><i>�V�����L������\\�����܂��B�ō�$max���̋L�����L�^����A����𒴂���ƌÂ��L������폜����܂��B<br>\n";
#	print "�P��̕\\����$def�����z����ꍇ�́A���̃{�^�����������ƂŎ��̉�ʂ̋L����\\�����܂��B</i>\n";

			print "<hr><a href=\"http://extra.onlineexpress.net/cgi-bin/strangeworld/bbs.cgi\">�G�N�X�g��</a>�A<a href=\"http://www.kinsan.ne.jp/~miki/strangeworld/bbs.cgi\">���񂳂�</a>�A <a href=\"http://famille.onlineexpress.net/cgi-bin/strangeworld/bbs.cgi\">�ӂ��݁[��</a>�A<a href=\"http://www.bea.hi-ho.ne.jp/cgi-bin/user/strangeworld/bbs.cgi\">�͂��ف[</a> | <a href=\"http://www4.famille.ne.jp/~haruna/remix/bbs.cgi\">REMIX</a>�A<a href=\"http://kakumeigun.onlineexpress.net/cgi-bin/relax/bbs.cgi\">RELAX</a> | <a href=\"http://edoya.neko.to/2/upload.cgi\">���E��Y</a>�A<a href=\"http://saturdaytears.virtualave.net/cgi-bin/upload.cgi\">�p�j����[</a>\n";

#	 �T�[�`�̒��ӏ���
	print "<hr>�ő�\�\\���F$max���@���F�ԐM�@���F���e�Ҍ����@���F�X���b�h�����@\�\\������0���F���ǃ��b�Z�[�W<hr>���e�̍폜�͂��Ȃ��̂ŁA���̌f���Ɋւ�邠����s���͎����ŐӔC���Ƃ��Ă��������B\n";

#	�����[�h
	print "<p></font></font><input type=submit value=\"���e�^�����[�h\">\n";


	print "</form>\n";


	
	#--- �L�^�L���̏o�� ----------------------------------#
	
# $date=#$month��$mday��($youbi)$hour��$min��$sec�b
#

	# �L�^�t�@�C����ǂݏo���I�[�v�����āA�z��<@lines>�Ɋi�[����
open(DB,"$file");
	@lines = <DB>;
	close(DB);

#$FORM{'win_time'}=~ s/0//o;

	$accesses = @lines;
	$f = 0;
	foreach ( @lines ){
		# �f�[�^���e�ϐ��ɑ������
		($date,$name,$email,$value,$subject,$hpage,$himage,$code,$postid) = split(/\,/,$_);

$date_s = $date;
$date=~ s/��|��|\(|\)|��|��|�b|��|��|��|��|�y//g;
#$date=~ s/0//o;

		if ( $FORM{'win_time'} <= $date ) {
			$f = $f + 1;
			$value =~ s/\0/\,/g; # �k���R�[�h�ɕϊ��L�^�������p�J���}�𕜋A������
			chop($himage) if $himage =~ /\n/;
			chop($hpage) if $hpage =~ /\n/;

            $date = $date_s;
			&disp;
		}
else { last; }

}

$g = $f;

		if ( $f eq 0 ) {print "<hr><p><font size=-1><i>���ǃ��b�Z�[�W�͂���܂���B</i></font><p>";}

else {print "<hr><p><font size=-1><i>$g���̃��b�Z�[�W������܂��B</i></font><p>";}


	
	# ���̃X�N���v�g�̒��쌠�\���i���Ȃ炸�\�����Ă��������j

		print "<form method=$method action=\"$cgiurl\"><input type=hidden name=\"def\" value=\"$def\"><input type=hidden name=\"bgcolor\" value=\"$bgc\"><input type=hidden name=\"win_time\" value=\"$month$mday$hour$min$sec\"><input type=submit value=\"�@�����[�h�@\"></form>\n";
	print "<h4 align=right><hr size=5><a href=\"http://www.ask.or.jp/~rescue/\">MiniBBS v7.5</a> <a href=\"http://www.bea.hi-ho.ne.jp/strangeworld/recycle/\">REQUIEM 990707��</a> is Free.</h4>\n";
	print "</body></html>\n";
	exit;




}


# �e���e�\���p�T�u���[�`�� #############################################################
sub disp {

	$hpage0 =$hpage;
	$hpage0 =~ s/$cgiurl\?action=search1\&search=(.*)\&id=\d*/�Q�l�F$1/;
	print "<hr>";
	print "<font size=+1 color=\"#$subjc\"><b>$subject</b></font>�@";
	

	if ($email ne '') { print "���e�ҁF<b><a href=\"mailto:$email\">$name</a></b>\n"; }
	else { print "���e�ҁF<b>$name</b></font>\n"; }

		print "<font size=-1>�@���e���F$date";

	print "�@<a href=\"$cgiurl\?bgcolor\=$bgc\&action\=search1\&search\=$date\&id=$postid\" target=\"link\">��</a>";
	print "�@<a href=\"$cgiurl\?bgcolor\=$bgc\&action\=search2\&search\=$name\" target=\"link\">��</a>";
	if ($hpage ne'' ) { print "�@<a href=\"$cgiurl\?bgcolor\=$bgc\&action\=search3\&search\=$code\" target=\"link\">��</a>\n"; }
	print "</font><p>\n";

if (($FORM{search}  eq '') && ($himage eq '1') ){
$value =~ s!((https?|ftp|gopher|telnet|whois|news):(=\S+|[\x21-\x7f])+)!<a href=\"$1\" target=\"link\">$1</a>!ig;

}


	print "<blockquote><pre>$value</pre><p>\n\n";
	
	if ($hpage ne '') { print "<a href=\"$hpage\" target=\"link\">$hpage0</a><p>\n"; }
	
	print "</blockquote>\n";
}

# �G���[�����T�u���[�`�� ############################################################
sub error {
	
	#  &error(xx); �ŌĂяo���ꂽ���[�`���́A()���̐����� $error �ɑ�������B
	
	$error = $_[0];
	
	if    ($error eq "0") { $error_msg = '�L�^�t�@�C���̓��o�͂ɃG���[���������܂����B'; }
	elsif ($error eq "2") {	$error_msg = '���e��������Ă��܂���B�܂��͋L�^�֎~�̃^�O��������Ă��܂��B'; }
	elsif ($error eq "3") {	$error_msg = '���[���A�h���X�����������͂���Ă��܂���B'; }
	elsif ($error eq "4") {	$error_msg = '���[���A�h���X�͕����w��ł��܂���B'; }
	elsif ($error eq "5") {	$error_msg = '���e���e���傫�����܂��B'; }

	elsif ($error eq "6") {	$error_msg = '�A�N�Z�X�����ݍ����Ă邽�߁A�������݂ł��܂���ł����B������x�A���e�{�^���������Ă��������B'; }
	elsif ($error eq "form") { $error_msg = "���e��ʂ̂t�q�k��<br>$cgiurl<br>" . '�ȊO����̓��e�͂ł��܂���B'; }
	elsif ($error eq "x") {	$error_msg = "�ȉ��̏�񂪋L�^����܂����B����"; }
	elsif ($error eq "xx") { $error_msg = "���킢����"; }
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

# �J�E���^�[�����T�u���[�`�� #########################################################
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
