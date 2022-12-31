<?php
error_reporting(0);

if(!isset($_GET['type']) or $_GET['type'] == ""){
    exit("type有误,请正确请求");
}

date_default_timezone_set('PRC');
DEFINE ('DB_USER', 'root');
DEFINE ('DB_PASSWORD', 'root');
DEFINE ('DB_HOST', '127.0.0.1');
DEFINE ('DB_NAME', 'bilibiliSpider');

$db = @mysqli_connect (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME) OR die ('Could not connect to
MySQL: ' . mysqli_connect_error());
mysqli_set_charset($db, 'utf8mb4'); #设置字符集
$db->query('SET NAMES utf8mb4');  #设置字符集
$db->query("SET CHARACTER SET utf8mb4"); #设置字符集
$db->query("SET character_set_connection=utf8mb4"); #设置字符集


function getLine($file, $line, $length = 4096){
    $returnTxt = null;
    $i = 1; //行数
    $handle = @fopen($file, "r");
    if ($handle) {
        while (!feof($handle)) {
            $buffer = fgets($handle, $length);
            if($line == $i) $returnTxt = $buffer;
            $i++;
        }
        fclose($handle);
    }
    return $returnTxt;
}

$type = $_GET['type'];

if($type == "1"){
    $latestAid_FileDir = "/Users/susie/PythonProjects/bilibiliSpider/latestAid.txt";
    $timeStr = date('Y-m-d H:i:s');
    $aidStr = getLine($latestAid_FileDir,1);

    while($aidStr == ""){
        sleep(0.2); //等待然后重试
        $aidStr = getLine($latestAid_FileDir,1);
    }

    exit($aidStr . "|" . $timeStr); //返回由"|"分割的内容

}elseif($type =="2"){ //请求当前最新爬取时间
    $sql = "SELECT * FROM `bilibiliSpider`.`videoContents` ORDER BY `id` DESC LIMIT 0,3";
    $result = mysqli_fetch_assoc($db->query($sql));
    $retStr = $result['video_pubYear']."年".$result['video_pubMonth']."月".$result['video_pubDay']."日";
    $retStr = $retStr . " ".$result['video_pubHour']."时".$result['video_pubMinute']."分".$result['video_pubSecond']."秒";

    $sql2 = "SELECT COUNT(id) from videoContents";
    $result2 = mysqli_fetch_assoc($db->query($sql2));
    $countAll = $result2["COUNT(id)"];
    $retStr = $retStr ."  现存记录:".$countAll . "条";

    $sql3 = "SELECT id,aid,video_title,ownerName FROM videoContents ORDER BY aid DESC LIMIT 0,3";
    $result3 = mysqli_fetch_assoc($db->query($sql3));
    $retStr = $retStr . "  现存最大aid(倒序):".$result3['aid']."  <br>当前视频标题:".$result3['video_title'] ."    作者:".$result3['ownerName'];

    exit($retStr);
}else{
    exit("未知的type类型:" + $type);
}
?>