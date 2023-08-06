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
        
        """ iniファイル読込内容 """
        self.config_ini = None

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
        config_ini.read(iniFilePath, encoding='utf-8')

        # 各設定値をメンバ変数にセット
        self.LogFileName = config_ini['DEFAULT']['LOGFILE_NAME']
        self.LogFolderName = config_ini['DEFAULT']['LOGFOLDER_NAME']
        self.LogFormat = config_ini['DEFAULT']['LOGFORMAT']
        
        # 読込内容をメンバ変数に設定する
        self.config_ini = config_ini
