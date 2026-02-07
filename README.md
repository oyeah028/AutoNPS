# AutoNPS

帮助你在云服务器上快速实现内网穿透。（MC联机，网页测试……）

## 使用教程

首先，你要知道你的使用场景及其对应的端口。
- ssh: 22
- udp远程桌面: 3389
- mc房间: 以游戏中提示的端口为准
- mc服务器(java): 25565

在云服务商处购买一个云服务器 [阿里云八折优惠](https://www.aliyun.com/minisite/goods?userCode=49csqam7)。

建议使用以下配置。（记得在安全组中开放对应端口并设置定时释放，钱包空空不负责）

![](https://github.com/oyeah028/image/blob/main/%E5%BE%AE%E4%BF%A1%E5%9B%BE%E7%89%87_20260207145418_20_41.png?raw=true)

从 Releases 中下载对应版本的 AutoNPS.zip 并解压。打开 config.json 文件并编辑为你的配置。

```json
{
    "host": "Your Server IP", // 云服务器的公网IP
    "username": "root", // 云服务器的用户名
    "password": "Your Password", // 云服务器的密码
    "port": [11451]
}
```

双击 AutoNPS.exe 即可启动内网穿透。

### 其他

本项目基于 [NPS](https://github.com/ehang-io/nps) 实现。考虑国内网络环境很差，所以直接将 NPS 编译好的二进制文件打包到了 AutoNPS 中。如有侵权，请联系我删除。
