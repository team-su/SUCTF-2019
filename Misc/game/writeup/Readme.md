###game
在1分15秒内完成游戏后得到假flag，suctf{hAHaha_Fak3_F1ag}
![1.png-42.8kB][2]

   [2]: http://static.zybuluo.com/Disp41r/f8kcccboy0rpkzbyn3wowb4d/1.png
在three.min.js中找到secret为一张图片
 ![2.png-556.7kB][11]

 [11]: http://static.zybuluo.com/Disp41r/2ithyv9owckptc957o2df4h7/2.png

打开图片，发现lsb存在密文，密文是3des加密的，密钥为之前的假flag，解密得到flag
![3.png-14.9kB][12]
  
  [12]: http://static.zybuluo.com/Disp41r/0etn7vlsiepf8uri8zrk008d/3.png