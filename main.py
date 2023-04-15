import os
import sys
from io import BytesIO

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication

from ai_module import ali_nls
from core import wsa_server
from gui import flask_server
from gui.window import MainWindow
from utils import config_util
from scheduler.thread_manager import MyThread


#开启项目之前清空采集的声音样本
def __clear_samples():
    if not os.path.exists("./samples"):
        os.mkdir("./samples")
    for file_name in os.listdir('./samples'):
        if file_name.startswith('sample-') and file_name.endswith('.mp3'):
            os.remove('./samples/' + file_name)


def __clear_songs():
    if not os.path.exists("./songs"):
        os.mkdir("./songs")
    for file_name in os.listdir('./songs'):
        if file_name.endswith('.mp3'):
            os.remove('./songs/' + file_name)



#不能被引用，直接作为脚本运行
if __name__ == '__main__':
    #先清空样本采集
    __clear_samples()
    __clear_songs()
    #加载配置文件
    config_util.load_config()
    
    #创建两个服务，一个数字人客户端服务，并开启服务
    ws_server = wsa_server.new_instance(port=10002)
    ws_server.start_server()
    #一个控制器客户端服务，并开启服务
    web_ws_server = wsa_server.new_web_instance(port=10003)
    web_ws_server.start_server()
    
    #开启阿里云，语音转文字技术
    ali_nls.start()
    #开启flask浏览器web
    flask_server.start()
    #实例一个桌面应用程序app
    app = QApplication(sys.argv)
    #设置app的icon
    app.setWindowIcon(QtGui.QIcon('icon.png'))
    #创建一个窗口，展示
    win = MainWindow()
    win.show()
    app.exit(app.exec_())

    
