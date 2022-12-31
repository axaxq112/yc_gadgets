<?php
//获得三者中间字段的方法
function GetBetween($content,$start,$end){
    $r = explode($start, $content);
    if (isset($r[1])){
        $r = explode($end, $r[1]);
        return $r[0];
    }
    return '';
}


//判断是不是微信UA
function isweixin() {
    if (strpos($_SERVER['HTTP_USER_AGENT'], 'MicroMessenger') !== false) {
      return true;
    } else {
      return false;
    }
}