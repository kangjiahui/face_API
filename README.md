# dlib_face_API
[dlib官网](http://dlib.net/compile.html)
## 环境配置
### windows 系统
下载安装[cmake](https://cmake.org/download/)   
pip安装   `pip install dlib`  
### ubuntu系统
命令安装cmake  `sudo apt install cmake`  
pip安装   `pip install dlib`  
## 快速启动
本工程ubuntu下能够自动下载模型参数并解压。   
由于bz2在windows上不便脚本解压，因此windows系统请先去[dlib下载目录](http://dlib.net/files/)下载模型文件并放置在modules/face_server/params文件夹中。   
运行之前需要调用新建数据库的api，详见`modules/utils/api.py`中的`new_database()`方法  
注意人脸注册图片中有且仅有一张脸，否则视为无效注册，数据库不做更新。  
### 需要开启http和websocket两个服务
运行`app.py`   
`websocket_serve.py`中`start_server = websockets.serve(time, "10.20.50.163", 5678)`ip地址更换为客户端地址  
运行`websocket_serve.py`  
### 本服务端已具备人脸注册、信息删除或修改、已注册人脸信息查询等功能。前端调用对应接口即可

