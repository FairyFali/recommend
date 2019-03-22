# -*- coding: utf-8 -*-
import os
import time
from model.lfm import LFM,Corpus


def run(user_id):
    '''
    调试lfm模型
    :param user_id:
    :return:
    '''
    assert os.path.exists('data/ratings.csv'), \
        'File not exists in path, run preprocess.py before this.'
    print('Start..')
    start = time.time()
    if not os.path.exists('data/lfm_items.dict'):
        Corpus.pre_process()
    if not os.path.exists('data/lfm.model'):
        LFM().train()
    movies = LFM().predict(user_id)
    movies_list = list(map(lambda x:x[0], movies))
    print(movies_list)
    print('End.')
    print('Cost Time:', time.time()-start)





