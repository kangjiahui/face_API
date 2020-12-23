# dlib_face_API
[dlib官网](http://dlib.net/compile.html)
## 环境配置
### windows 系统
下载安装[cmake](https://cmake.org/download/)   
pip安装   `pip install dlib`  
### ubuntu系统
命令安装cmake   `sudo apt install cmake`  
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

### flask 服务负责数据库增删改查功能
#### 人脸信息注册  
@app.route('/uploadInfo', methods=["POST"])  
输入输出详见 api.py 文档中的 face_register 方法  
#### 人脸更新（有图片更新）  
@app.route('/updateInfo', methods=["POST"])  
输入输出详见 api.py 文档中的 face_update 方法  
#### 人脸更新（无图片）  
@app.route('/updateInfo2', methods=["POST"])  
输入输出详见 api.py 文档中的 face_update 方法  
#### 人脸删除  
@app.route('/deleteInfo', methods=["POST"])  
输入输出详见 api.py 文档中的 face_delete 方法  
#### 人脸信息获取  
@app.route('/getAllInfo', methods=["POST"])  
输入输出详见 api.py 文档中的 face_get_info 方法  

### websocket负责图像帧实时传输
start_server = websockets.serve(time, "10.20.50.163", 5678)   

输入输出详见 api.py 文档中的 search_identity 方法

### api.py 文档
Help on module modules.utils.api in modules.utils:

NAME

    modules.utils.api

DESCRIPTION

    File Name：     faceRecognition.py
    Description :  Instantiate FaceRecognition from faceRecognition.py. Give a clear API for user.
    Author :       KangJiaHui
    date：         2020/11/26

FUNCTIONS

    face_delete(user_id)
        Delete an exact face_info by user_id
        :param user_id: string e.x. "10098440"
        :return: None, the face_info will be deleted from database.
    
    face_get_info(page_num=1, max_rows=100)
        Fetch face_info page by page. You can only fetch one page at once.
        :param page_num: int, page index
        :param max_rows: int, how many registered faces in one page
        :return: dict, e.x. {"result": 0, "message": "SUCCESS",
                            "user_data": [{"userID": "10098440", "userGroup": "staff", "userGender": "女", "userName": "康佳慧",
                                            "latest_modify_time": "2020-12-15 15:15:41", "userIMG": base64_image}, ]}
    
    face_register(input_dict)
        Registers only one picture.
        :param input_dict:
            e.x. {"user_id": "10098440", "group_id": "staff", "gender": "女", "user_info": "康佳慧", "user_image": base64_image}
        :return: None, results will be written into database.
    
    face_update(input_dict)
        Update exist face_info.
        :param input_dict: e.x. {"user_id": "10098440", "group_id": "staff", "user_info": "康佳慧", "user_image": base64_image}
        :return: None, results will be written into data_path.
    
    new_database()
        Initial a new database. Only execute once before use.
        :return: None. Database and table will be established.
    
    search_identity(image=None, path=None, thresh=0.4)
        Serch all faces in one image in the register of n faces' features.
        If path and image coexist, then path will cover image.
        :param image: numpy.ndarray
        :param path: str, indicates an image
        :param thresh: distance between face and matched face should be smaller than thresh
        :return:dict, in format of
                {"result": 0, "message": "SUCCESS", "image": encoded_base64_img,
                "faces":[{"user_id": "10098440", "group_id": "staff", "gender": "女", "user_info": "康佳慧",
                        "box": [216, 118, 439, 341], "distance": 0.35670, "image": base64_image}, ]}

DATA

    face = <modules.face_server.faceRecognition.FaceRecognition object>

FILE

    e:\deeplearning\kang\face_api\modules\utils\api.py
