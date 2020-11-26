# dlib_face_API
[dlib官网](http://dlib.net/compile.html)
## 环境配置
### windows 系统
下载安装[cmake](https://cmake.org/download/)   
pip安装 `pip install dlib`
## 快速启动
本工程ubuntu下能够自动下载模型参数并解压。   
由于bz2在windows上不便脚本解压，因此windows系统请先去[dlib下载目录](http://dlib.net/files/)下载模型文件并放置在modules/face_server/params文件夹中。   
需要注册的人脸图片放置在register_img文件夹中。图片文件名即为注册名。注意图片中有且仅有一张脸，否则报注册无效。
### 带摄像头的笔记本
`main.py` 中使用`face_register_batch('register_img')`进行注册，使用 `show_in_video()`函数打开笔记本摄像头实时监测识别。
### 没有摄像头的电脑
`main.py` 中使用`result = search_identity(path='test.jpg')`获取返回的json结果。'test.jpg'替换为你的测试图片路径。
