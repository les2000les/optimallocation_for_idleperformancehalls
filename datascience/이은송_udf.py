#### Type Your Code ####
# 자유롭게 UDF를 만들어보세요.
# Argument로 원하는 파일을 불러오고, 원하는 전처리를 수행하고, 원하는 파일명으로 저장하는 기능을 넣을 것!
########################
import pandas as pd
import numpy as np

def udf_code(inputname, filetype, outputname):
    ## 파일 불러오기
    # global df
    if filetype == 'txt':
        df = pd.read_table(inputname)
        #input = pd.read_csv(address, delimiter = '\t')
    elif filetype == 'csv':
        df = pd.read_csv(inputname)
    else: #filetype == 'excel'
        df = pd.read_excel(inputname)

    ## 전처리
    #인덱스 초기화
    df.reset_index(inplace = True)
    #이상치 처리 (수치형)
    for column in df.columns:
        if df[column].dtype != object:

            quartile_1 = np.percentile(df[column].values, 25)
            quartile_3 = np.percentile(df[column].values, 75)

            IQR = quartile_3 - quartile_1
            IQR_weight = IQR *1.5
            lower_bound = quartile_1 - IQR_weight
            upper_bound = quartile_3 + IQR_weight

            #이상치 식별
            outliers = (df[column] < lower_bound) | (df[column] > upper_bound)

            # 이상치를 중앙값으로 대체
            median = np.median(df[column].values)
            df.loc[outliers, column] = median
    #결측치 처리
    df = df.fillna(0)

    #output 저장
    df.to_csv(outputname + '.csv', index=False)

#udf 실행
udf_code("train.csv", "csv", "final")