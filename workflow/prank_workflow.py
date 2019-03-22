import model.prank as prank
import os
import time

def run(user_id):
    '''
    调试PersonRank算法
    :param user_id:
    :return:
    '''
    assert os.path.exists('data/ratings.csv'), \
        'File not exists in path, run preprocess.py before this.'
    print('Start..')
    start = time.time()
    if(os.path.exists('data/prank_{}.model'.format(user_id))):
        print(prank.PersonalRank().predict(user_id))
    else:
        pr = prank.PersonalRank()
        pr.train(user_id)
        print(pr.predict(user_id))
    print('End.')
    print('Cost Time:', time.time() - start)


