import datetime

class uwGetter:

    @staticmethod
    def getNow():

        """ 
        現在日時取得
        
        Parameters
        ----------
        none
        """

        # 日本時刻取得
        return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))) 

    @staticmethod
    def addDays(targetDate, addDays):
        
        """ 
        対象日付の日数を加算する
        
        Parameters
        ----------
        targetDate :
            加算対象日付
        addDays :
            加算する日数
        """

        # 戻り値を返す
        return targetDate + datetime.timedelta(days=addDays)
