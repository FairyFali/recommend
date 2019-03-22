import pandas as pd


def read_ratings_data():
    """
    读取评分文件并保存到csv中
    param path：文件路径
    return DataFrame
    """
    # 为了解决解析的警告，增加参数engine='python'
    f = pd.read_table('data/ratings.dat', sep='::',
                      names=['UserID', 'MovieID', 'Rating', 'Timestamp'],
                      engine='python')
    f.to_csv('data/ratings.csv', index=False)
    print('rating.dat文件->ratings.csv文件')
    # movies.dat,MovieID::Title::Genres
    f = pd.read_table('data/movies.dat', sep='::',
                      names=['MovieID', 'Title', 'Genres'],
                      engine='python')
    f.to_csv('data/movies.csv', index=False)
    print('movies.dat文件->movies.csv文件')
    # users.dat,UserID::Gender::Age::Occupation::Zip-code
    f = pd.read_table('data/users.dat', sep='::',
                      names=['UserID', 'Gender', 'Age',
                             'Occupation', 'Zip-code'],
                      engine='python')
    f.to_csv('data/users.csv', index=False)
    print('users.dat文件->users.csv文件')


read_ratings_data()

