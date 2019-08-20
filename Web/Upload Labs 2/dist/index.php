<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Upload Labs 2</title>
</head>

<body>
    <h2>Upload Labs 2</h2>
    <div>
        <p>假装有一个很酷很酷的前端，有一个很漂亮很漂亮的前端妹子</p> 
        <a href="func.php">去看看你自己到底传了个啥！！！</a>
    </div>

    <div>-------------我是华丽的分割线----------------</div>
    <form action="index.php" method="post" enctype="multipart/form-data">
        <label for="file">文件名：</label>
        <input type="file" name="file" id="file"><br>
        <input type="submit" name="upload" value="提交">
    </form>
</body>

</html>

<?php
include 'class.php';

$userdir = "upload/" . md5($_SERVER["REMOTE_ADDR"]);
if (!file_exists($userdir)) {
    mkdir($userdir, 0777, true);
}
if (isset($_POST["upload"])) {
    // 允许上传的图片后缀
    $allowedExts = array("gif", "jpeg", "jpg", "png");
    $tmp_name = $_FILES["file"]["tmp_name"];
    $file_name = $_FILES["file"]["name"];
    $temp = explode(".", $file_name);
    $extension = end($temp);
    if ((($_FILES["file"]["type"] == "image/gif")
            || ($_FILES["file"]["type"] == "image/jpeg")
            || ($_FILES["file"]["type"] == "image/png"))
        && ($_FILES["file"]["size"] < 204800)   // 小于 200 kb
        && in_array($extension, $allowedExts)
    ) {
        $c = new Check($tmp_name);
        $c->check();
        if ($_FILES["file"]["error"] > 0) {
            echo "错误：: " . $_FILES["file"]["error"] . "<br>";
            die();
        } else {
            move_uploaded_file($tmp_name, $userdir . "/" . md5($file_name) . "." . $extension);
            echo "文件存储在: " . $userdir . "/" . md5($file_name) . "." . $extension;
        }
    } else {
        echo "非法的文件格式";
    }
    
}
