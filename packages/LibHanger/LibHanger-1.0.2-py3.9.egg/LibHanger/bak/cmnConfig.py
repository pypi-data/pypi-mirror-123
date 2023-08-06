import configparser
import os
import pathlib

class cmnConfig:

    """
    共通設定クラス
    """ 

    def __init__(self):

        """
        コンストラクタ
        """ 

        """ ログファイル名 """
        self.LogFileName = 'default.log'

    def printLogFileName(self):

        """
        ログファイル名出力
        """ 

        print(self.LogFileName)

    def getConfig(self, scriptPath):

        """ 
        設定ファイルを読み込む 
        
        Args:
            self (:cmnConfig:`属性の型`):
        """
        
        # configparser宣言
        config_ini = configparser.ConfigParser()

        # iniファイル読み込み
        #iniDirPath = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
        iniDirPath = pathlib.Path(os.path.abspath(os.path.dirname(scriptPath)))
        iniFilePath = os.path.join(iniDirPath,'config.ini')
        print(iniFilePath)
        config_ini.read(iniFilePath, encoding='utf-8')

        # 読込内容をconfigに格納
        self.LogFileName = config_ini['DEFAULT']['LOGFILE_NAME']

        return config_ini

