import pandas as pd

def dfAppend(df:pd.DataFrame, counter:int, row:int):

    """ 
    dataframeに行を追加(appendの代替)
    """

    # 追加用のディクショナリを宣言
    dict_tmp = {}

    # ディクショナリに行をセット
    dict_tmp[counter] = row

    # キー値を加算
    counter += 1

    # 戻り値を返す
    return df.from_dict(dict_tmp, orient="index"), counter