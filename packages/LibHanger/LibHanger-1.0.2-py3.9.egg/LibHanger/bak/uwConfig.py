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

        """ ログ出力先フォルダ名 """    
        self.LogFolderName = 'log'

        """ ログフォーマット定義 """    
        self.LogFormat = '%(levelname)s : %(asctime)s : %(message)s'

    def returnMe(self):
        return self

    def printLogFileName(self):

        """
        ログファイル名出力
        """ 

        print(self.LogFileName)

    def getConfig(self, scriptPath):

        """ 
        設定ファイルを読み込む 
        
        Parameters
        ----------
        self : LibHanger.cmnConfig
            共通設定クラス
        scriptPath : string
            スクリプトファイルパス

        """
        
        # configparser宣言
        config_ini = configparser.ConfigParser()

        # iniファイル読み込み
        iniDirPath = pathlib.Path(os.path.abspath(os.path.dirname(scriptPath)))
        iniFilePath = os.path.join(iniDirPath,'config.ini')
        print(iniFilePath)
        config_ini.read(iniFilePath, encoding='utf-8')

        # 読込内容をconfigに格納
        self.LogFileName = config_ini['DEFAULT']['LOGFILE_NAME']
        self.LogFolderName = config_ini['DEFAULT']['LOGFOLDER_NAME']
        self.LogFormat = config_ini['DEFAULT']['LOGFORMAT']
        
        # 設定内容を返す
        return config_ini

