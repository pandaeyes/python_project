<?php
// 获取上传文件对应的字典（对象
$fileInfo = $_FILES["myfile"];
$name = $fileInfo["name"];
echo("name:".$name."\r\n");

$exType = $_POST['alias'];
echo("alias:".$exType."\r\n");

$fp = fopen($fileInfo['tmp_name'], 'rb');
$tmpname = $fileInfo['tmp_name'];


$fdir = "/data/ysc_log/log/".date("Ymd",time())."/";
if(!is_dir($fdir)) {
    mkdir($fdir); 
}

if(move_uploaded_file($tmpname, $fdir.$name)) {
    echo("succ");
} else {
    echo("Failed");
}


