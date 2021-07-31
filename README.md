# p2p即时通信软件-UDP-SOCKET实现
## 什么人需要？
* 当你需要完成一个质量不高的国密中SM2,SM4的密钥生成，保存，文件加解密等等功能的同学（直接自己看crp.py部分代码）
* 当你需要完成一个p2p即时通讯，文件传输功能（p2p代码）
* 当你需要python实现的音频录制播放保存加密功能（crp.py部分）
* 包含以上所有的部分的同学
> 这是一个小学期的作品，因为开发时间极短可能有一些问题。需要的可以在这个基础上做自己想做的一切改进。
> 只面向小白去借鉴如何完成p2p即时通信过程中的基本功能。大佬勿喷！该小产物借鉴了很多很多别人的代码，主要是非对称密钥生成，lsb隐写部分。
> 是可以改的精细一点，但感觉对自己没什么意义。所以有什么问题报错可以在这个项目内问我，我看到会回复的：QQ:2792338056
## 功能描述
* **p2p端的即时通信，该通信完全依靠p2p，没有c/s服务来获取**ip，pubkey，name**等数据信息不用管ip_message以及ip_sm4这个是自动生成的**
> 也因此需要读者自行将ip_pubkey，ip_name改换为合适的内容。其实就是将上述文件里面的ip换成内网ip，如果是要测试一台主机上的相互通信，要记得把两个机子中9999端口号改为接受和发送不同的端口。

同时读者可以自己开发**webAPI**接口实现ip_name和ip_pubkey的自动获取，添加一定的注册登录功能，当然也可以通过一个新的**socket**实现服务端的交互，但不要占用p2p通信端口以及文件传输端口。
* **该p2p通信包含密钥协商（就是用公私钥加密后的sm4对称密钥加密之后每次的通信内容，包括音频通信）**
* **该p2p通信包含可进行隐写的图像传输功能。**
* **包含录制5s音频后进行对称加密传输并在对端解密播放功能**
## 文件说明：
* p2ppy：主要实现p2p交互部分所有逻辑，主要调用了crp.py文件lsbtq.py文件。
* crppy：主要实现了国密加密标准中的对称密钥以及非对称密钥从密钥生成，保存，加密，解密，签名，验证以及对文件的相应操作等功能。此外还具有播放录制音频的功能（这里需要安装两个相应的包，建议多找几个pip源去安装，可能会有一定问题。）
* p2pfrontpy：主要实现了前端页面,也是所有功能的入口函数
* lsbtqpy：主要实现了图像隐写以及提取功能
* ip_系列：其中pubkey,name需要你自己填写。_message,_sm4是会自动生成的，可以将文件内内容删除掉，但记得不要直接删除文件，不确定是否做了文件是否存在的验证，因为这不是该项目最后一版代码-最后一版有c/s但需要数据库配套服务，放那个代码可能你根本没法用。就加加油在这个基础上改吧。
* temkey：这个文件是在你录制和接受音频后产生的。该文件就是你录制音频经过sm4加密后产生的。
## 使用说明：
相信很多拿到别人代码的人都想先跑一下，以下部分就是介绍如何快速跑其这个代码的说明：
**环境要求**：python3 pip 一个没有隔离的内网环境
### 步骤一

在你的终端中运行如下命令**以安装相关包**并不是说运行了就不需要安装其他包了，可能你的python没有一些基础包还得你自己手动下载。
	
```pip install -r requirements.txt```
> 当然有一部分同学可能不太会配置pip相关环境，尤其在你有python2的情况下。这时候你可以运行你的pycharm打开这个项目文件。而后右键点击文件目录部分-打开于-终端。而后在里面键入如下命令。一切的前提是你在pycharm里面配置好了你需要的一切。如果没有请百度一下！
> 
当然你也可以一个个安装相应的包，应该不会因为包版本问题造成什么异常。如果有你也可以卸载了包后照着requirements文件重新安装。注意用豆瓣或者阿里的安装源。
### 步骤二
**设置好您的ip_name以及ip_pubkey文件**。记住你的密钥协商都是基于这个ip_pubkey以及你文件夹下的sm2_prikey（crp代码生成）实现的。我这边建议第一次运行可以让两个p端有一样的非对称密钥免得出什么问题。但之后在这基础上做变化时候一定要注意这个prikey和pubkey对应的问题。
关于设置**ip_name和ip_pubkey直接将你看到的ip部分放置为你的内网ip**即可（wifi-属性-ipv4地址）有的学校可能有内网隔离导致你无法正常通讯。可以试试用自己手机热点。
### 步骤三
两个p端都运行p2p_front代码。而后点击你刚刚设置好的ip_name中的对应角色即可。看到命令行输出密钥协商，以及在对端看到收到密钥协商成功并返回一段随机字符串说明成功。可以随便发送一些文字，图片信息试试
### 其他
如果你想在自己电脑单机尝试，要在上述步骤二之后复制一份代码在出来。并在p2p代码中全局搜索9999端口（有两处，一处改为999）

并在复制出的那个代码中（将上述改动的另外一处改为999）
