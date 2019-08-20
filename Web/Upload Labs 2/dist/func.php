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
        <a href="index.php">去看看你自己到底要做了个啥！！！</a>
    </div>

    <div>-------------我是华丽的分割线----------------</div>
    <form action="func.php" method="post" enctype="multipart/form-data">
        <label for="file">文件名：</label>
        <input type="text" name="url" id="url"><br>
        <input type="submit" name="submit" value="提交">
    </form>
</body>

</html>

<?php
include 'class.php';

if (isset($_POST["submit"]) && isset($_POST["url"])) {
    if(preg_match('/^(ftp|zlib|data|glob|phar|ssh2|compress.bzip2|compress.zlib|rar|ogg|expect)(.|\\s)*|(.|\\s)*(file|data|\.\.)(.|\\s)*/i',$_POST['url'])){
        die("Go away!");
    }else{
        $file_path = $_POST['url'];
        $file = new File($file_path);
        $file->getMIME();
        echo "<p>Your file type is '$file' </p>";
    }
}


?>