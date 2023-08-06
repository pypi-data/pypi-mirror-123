import cmnConfig
import configparser
import os
import pathlib

def getConfig():

    """ 
    設定ファイル読み込み 
    
    Parameters
    ----------
    none
    """

    # 共通設定クラス生成
    config = cmnConfig.cmnConfig()

    # configparser宣言
    config_ini = configparser.ConfigParser()

    # iniファイル読み込み
    iniDirPath = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
    iniFilePath = os.path.join(iniDirPath.parents[0],'config.ini')
    config_ini.read(iniFilePath, encoding='utf-8')

    # 読込内容をconfigに格納
    config.LogFileName = config_ini['DEFAULT']['LOGFILE_NAME']
    
    # 戻り値を返す
    return config