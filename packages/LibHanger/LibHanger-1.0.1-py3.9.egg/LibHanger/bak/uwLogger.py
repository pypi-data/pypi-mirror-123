import logging
import os
import uwConfig as config

class uwLogger:

    @staticmethod
    def setting(loglevel, config: config.cmnConfig):

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
