import re
import pandas as pd
import numpy as np


def main():
    df = pd.read_json('newhouse.json', orient='values', encoding='utf-8')
    print(df.info())
    df2 = data_cleaning(df)
    print(df2.info())
    write_to_file(df2)


def write_to_file(df2):
    # 添加北京的数据
    df2.loc[('直辖市', '北京'), :] = [54599]
    df3 = df2.sort_values('price_without_unit')
    df3 = df3.dropna()
    # print(df3.count())
    pd4 = df3[0:20]
    pd4['date'] = 1
    for i in range(1, int(df3.count()) - 20 + 1):
        pd5 = df3[i:i + 20]
        pd5['date'] = i + 1
        pd4 = pd.concat([pd4, pd5])
    print(pd4)
    pd4.to_csv('my777.csv')
    print('数据写入完毕')


def data_cleaning(df):
    ps = []
    for price in df['price']:
        res = re.search(r'^.*?(\d+)元/㎡$', price)
        if not res:
            p = np.nan
        else:
            p = res.group(1)
        ps.append(p)
    df['price_without_unit'] = ps
    df['price_without_unit'] = df['price_without_unit'].astype('float')
    # 按城市分组
    city_groups = df['price_without_unit'].groupby(by=[df['province'], df['city']]).median()
    return pd.DataFrame(city_groups)


if __name__ == '__main__':
    main()
