<?php
include 'config.php';

class File{

    public $file_name;
    public $type;
    public $func = "Check";

    function __construct($file_name){
        $this->file_name = $file_name;
    }

    function __wakeup(){
        $class = new ReflectionClass($this->func);
        $a = $class->newInstanceArgs($this->file_name);
        $a->check();
    }
    
    function getMIME(){
        $finfo = finfo_open(FILEINFO_MIME_TYPE);
        $this->type = finfo_file($finfo, $this->file_name);
        finfo_close($finfo);
    }

    function __toString(){
        return $this->type;
    }

}

class Check{

    public $file_name;

    function __construct($file_name){
        $this->file_name = $file_name;
    }

    function check(){
        $data = file_get_contents($this->file_name);
        if (mb_strpos($data, "<?") !== FALSE) {
            die("&lt;? in contents!");
        }
    }
}