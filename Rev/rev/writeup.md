程序用IDA打开很复杂

一开始用`boost::tokenizer`切割字符串

输入形如`aaaa-bbbbb-cccccc`，中间的特殊符号会被认为是分隔符，然后获得这三个`std::string`，分别check



第一个，res[0]，要求长度是10，然后经过

`boost::trim_left_copy_if(res[0], boost::is_any_of("1"))`

这句话是把这个字符串左边的`1`全部去掉

进入一个循环，要求每个字符异或0xab后和数组相同，长度要求是5，也就是说一开始被去掉了五个`1`

于是输入的第一段是`11111suctf`





第二个，res[1]，

`((res[1].length() == 4) &&`

`(boost::all(res[1],boost::is_from_range('a','g')`

`|| boost::is_from_range('A', 'G')))) `

长度是4，每个字符都是[A-Ga-g]

经过`boost::to_upper`要求和原string相同，这表明输入的4个字符都是大写字母

限制范围在[A-G]了

要求4个字符的数值递增，步长为2,

那么只能ACEG

也就是第二个的输入



第三个，res[2]

通过`boost::all(res[2],boost::is_digit())`判断要求都是数字，小于10位，转成int，记作sum

要求`(sum % 2 == 0) && (func(sum) == -1412590079) && (func2(sum) == 305392417)`

如果不加第一个%2==0的条件，会有三个结果31415925 31415926 31415927

这样下来只有一个结果31415926

int范围内只有这一个符合要求

也就是第三个输入



那么输入就形如`11111suctf-ACEG-31415926`

输出为  suctf{ACEG31415926}
You win!