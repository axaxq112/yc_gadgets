<?php
date_default_timezone_set("PRC");
// MySQL Config
$MySQL_Host = "127.0.0.1";
$MySQL_Port = 3306;
$MySQL_User = "root";
$MySQL_Pass = "root";
$MySQL_Db = "bsh";
$innerUrl = "http://192.168.101.30"; //【应于exportToZipConfig.yaml中地址一样】
$outerUrl = "http://axaxq.natapp1.cc";
$reqPass = "bsh1230"; //接口鉴权秘钥【应于exportToZipConfig.yaml中一样】

try{
    $MySQli = new mysqli($MySQL_Host,$MySQL_User,$MySQL_Pass,$MySQL_Db,$MySQL_Port);
}catch (Exception $e){
    exit("MySQL链接失败，原因:".$e->getMessage());
}


if(isset($_GET['token'])){
    if($_GET['token'] != ""){
        $token = $_GET['token'];
        $querySql = "SELECT * FROM exportLinks WHERE token = ?";
        $query = $MySQli->prepare($querySql);
        $query->bind_param("s",$token);
        $query->store_result();
        $query->bind_result($db_id,$db_type,$db_ver,$db_absPath,$db_insertTs,$db_expireTs,$db_token);
        $query->execute();

        while($query->fetch()){
            if($token == $db_token){
                if(!file_exists($db_absPath)){
                    exit("源文件不存在");
                }

                $tsNow = time();
                if ($tsNow <= $db_expireTs){
                    ob_end_clean();
                    ob_start();
                    $fileSize = filesize($db_absPath);
                    $handler = fopen($db_absPath,"r+b");
                    header("Content-type: application/octet-stream");
                    header("Accept-Ranges: bytes");
                    header("Content-Disposition: attachment;filename=".basename($db_absPath));
                    echo fread($handler,$fileSize);
                    fclose($handler);
                    ob_end_flush();
                }else{
                    exit("分享文件已过期");
                }
                exit();
            }
        }

        exit();
    }else{
        exit("token不能为空");
    }
}




if (!isset($_GET["type"]) or !isset($_GET['reqPass']) or !isset($_GET['ver']) or !isset($_GET['absPath']) ){
    exit("参数不全");
}else if ($_GET["type"] != "inner" and $_GET["type"] != "outer"){
    exit("type参数有误");
}else if ($_GET['reqPass'] == ""){
    exit("本接口需要鉴权秘钥");
}else if ($_GET['reqPass'] !== $reqPass){
    exit("鉴权秘钥有误");
}


$type = $_GET['type'];
$ver = $_GET['ver'];
$absPath = $_GET['absPath'];

if(!file_exists($absPath)){
    exit("目录不存在该文件");
}

$insertTs = time();
$expireOuterTs = $insertTs + 86400 * 3; //外网分享(有效期3天)
$expireInnerTs = $insertTs + 86400 * 30; //内网分享(有效期30天）

if ($type == "inner") {
    $expireTs = $expireInnerTs;
}else if ($type == "outer"){
    $expireTs = $expireOuterTs;
}
 
function uuid(){
    $chars = md5(uniqid(mt_rand(), true));
    $uuid = substr ( $chars, 0, 8 ) . '-'
            . substr ( $chars, 8, 4 ) . '-'
            . substr ( $chars, 12, 4 ) . '-'
            . substr ( $chars, 16, 4 ) . '-'
            . substr ( $chars, 20, 12 );
    return $uuid ;
}

$token = uuid();

$insertSql = "INSERT INTO `exportLinks` (`type`, `ver`, `absPath`, `insertTs`, `expireTs`, `token`) VALUES (?,?,?,?,?,?)";
$query = $MySQli->prepare($insertSql);
$query->bind_param("ssssss",$type,$ver,$absPath,$insertTs,$expireTs,$token);

if($query->execute()){
    if ($type == "inner") {
        $innerDownloadUrl = $innerUrl . "/bsh/getExportLink.php?token=".$token;
        exit($innerDownloadUrl);
    }else if ($type == "outer"){
        $outerDownloadUrl = $outerUrl . "/bsh/getExportLink.php?token=".$token;
        exit($outerDownloadUrl);
    }
}else {
    exit("添加失败");
}