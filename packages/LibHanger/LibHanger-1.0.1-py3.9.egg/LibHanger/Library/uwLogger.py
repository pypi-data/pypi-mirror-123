import logging
import os
from .uwConfig import cmnConfig as config

def setting(loglevel, config: config):

    """
    ロガー設定

    Parameters
    ----------
    loglevel : Logger.logging
        ログレベル
    config : config.cmnConfig
        共通設定クラス
    """

    # ログ出力先がない場合、作成する
    if os.path.exists(config.LogFolderName) == False:
        os.mkdir(config.LogFolderName)

    # フォーマット定義
    formatter = config.LogFormat

    # ロガー設定
    logging.basicConfig(filename=os.path.join(config.LogFolderName, config.LogFileName),
                        level=loglevel, 
                        format=formatter)

def loggerDecorator(outputString):
    def _loggerDecorator(func):
        """
        関数の開始～終了でコンソールに文字列を出力するデコレーター
        """
        def  wrapper(*args):
            print('(' + outputString + ') ...', end = '')
            try:
                ret = func(*args)
                print('OK')
            except Exception as e:
                print('NG')
                print('=== エラー内容 ===')
                print('type:' + str(type(e)))
                print('args:' + str(e.args))
                print('e自身:' + str(e))
                return
            return ret

        return wrapper

    return _loggerDecorator
