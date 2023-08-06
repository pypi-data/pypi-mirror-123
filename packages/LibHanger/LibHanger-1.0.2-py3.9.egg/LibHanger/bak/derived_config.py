from cmnConfig import cmnConfig

class dconfig(cmnConfig):

    """
    共通設定クラスを継承した派生設定クラス
    """ 
    def __init__(self):
        cmnConfig.__init__(self)
        self.ADD_MEMBER = 'add Member'
        
    def getConfig(self, scriptPath):

        """ 
        設定ファイルを読み込む 
        
        Args:
            self (:cmnConfig:`属性の型`):
        """
        
        config_ini = cmnConfig.getConfig(self, scriptPath)
        self.ADD_MEMBER = config_ini['DEFAULT']['ADD_MEMBER']