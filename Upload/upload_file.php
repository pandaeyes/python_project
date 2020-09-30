<?php
echo "testsss";
// 获取上传文件对应的字典（对象
$fileInfo = $_FILES["myfile"];
$name = $fileInfo["name"];
echo("name===:".$name);

$exType = $_POST['mod'];
echo($exType);

$fp = fopen($fileInfo['tmp_name'], 'rb');
$tmpname = $fileInfo['tmp_name'];
if(move_uploaded_file($tmpname, "D:/data/".$name)) {
    echo("succ");
} else {
    echo("Failed");
}


// $_FILES["file"]["name"] - 被上传文件的名称
// $_FILES["file"]["type"] - 被上传文件的类型
// $_FILES["file"]["size"] - 被上传文件的大小，以字节计
// $_FILES["file"]["tmp_name"] - 存储在服务器的文件的临时副本的名称
// $_FILES["file"]["error"] - 由文件上传导致的错误代码

