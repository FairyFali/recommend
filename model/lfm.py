import pandas as pd
import pickle
import numpy as np
import math
import random

class Corpus:
    # 数据字典位置
    items_dict_path = 'data/lfm_items.dict'

    @classmethod
    def pre_process(cls):
        '''
        预处理数据，需要存在ratings.csv文件
        获得所有的用户id
        获得所有的商品id
        获得所有的商品字典{userid1:{itemid1:1,itemid2:0},...}
        :return:
        '''
        print('Process 语料生成')
        file_path = 'data/ratings.csv'
        cls.frame = pd.read_csv(file_path)
        cls.user_ids = set(cls.frame['UserID'])
        cls.item_ids = set(cls.frame['MovieID'])
        cls.items_dict = {user_id: cls._get_pos_neg_item(user_id)
                          for user_id in list(cls.user_ids)}
        cls.save()
        print('Process 语料生成完毕->', cls.items_dict_path)

    @classmethod
    def save(cls):
        '''
        保存items_dict到文件
        :return:
        '''
        f = open(cls.items_dict_path, 'wb')
        pickle.dump(cls.items_dict, f)
        f.close()

    @classmethod
    def load(cls):
        '''
        加载items_dict
        :return:
        '''
        f = open(cls.items_dict_path, 'rb')
        items_dict = pickle.load(f)
        f.close()
        return items_dict


    @classmethod
    def _get_pos_neg_item(cls, user_id):
        '''
        获得等量的用户喜欢的商品和不喜欢的商品
        :param user_id:
        :return:
        '''
        pos_items_ids = set(cls.frame[cls.frame['UserID']
                                     == user_id]['MovieID'])
        neg_items_ids = cls.item_ids ^ pos_items_ids
        neg_items_ids = list(neg_items_ids)[:len(pos_items_ids)]
        item_dict = {}
        for i in pos_items_ids:
            item_dict[i]=1
        for i in neg_items_ids:
            item_dict[i]=0

        return item_dict


class LFM:

    model_path = 'data/lfm.model'

    def __init__(self):
        # 隐类数量
        self.class_count = 5
        # 迭代次数
        self.iter_count = 5
        # 学习率
        self.lr = 0.02
        # 正则项
        self.lam = 0.01
        # 初始化模型
        self._init_model()

    def _init_model(self):
        '''
        获得语料，初始化隐类矩阵
        :return:
        '''
        file_path = 'data/ratings.csv'
        self.frame = pd.read_csv(file_path)
        self.user_ids = set(self.frame['UserID'])
        self.item_ids = set(self.frame['MovieID'])
        self.items_dict = Corpus.load()

        # 生成正态分布带随机矩阵
        array_p = np.random.randn(len(self.user_ids), self.class_count)
        array_q = np.random.randn(len(self.item_ids), self.class_count)

        # 带索引的隐类矩阵，行是user_id和item_id
        self.p = pd.DataFrame(array_p, columns=range(self.class_count),
                              index=list(self.user_ids))
        self.q = pd.DataFrame(array_q, columns=range(self.class_count),
                              index=list(self.item_ids))

    def save(self):
        '''
        保存模型参数
        :return:
        '''
        f = open(self.model_path, 'wb')
        pickle.dump(self.p, self.q, f)
        f.close()


    def load(self):
        '''
        加载模型参数
        :return:
        '''
        f = open(self.model_path, 'rb')
        self.p, self.q = pickle.load(f)
        f.close()

    def _predict(self, user_id, item_id):
        '''
        计算用户对商品的兴趣
        :param user_id:
        :param item_id:
        :return:
        '''
        p = np.mat(self.p.loc[user_id].values)
        q = np.mat(self.q.loc[item_id].values).T
        r = sum(p*q)
        logit = 1/(1+math.exp(-r))
        return logit


    def predict(self, user_id, top_n=10):
        '''
        给用户推荐
        :param user_id:
        :param top_n:
        :return:
        '''
        self.load()
        # print(self.p)
        # print(self.q)
        pos_items_ids = set(self.frame[self.frame['UserID']
                                      == user_id]['MovieID'])
        neg_items_ids = self.item_ids ^ pos_items_ids
        interest_list = []
        for i in neg_items_ids:
            interest_list.append(self._predict(user_id, i))
        candidates = sorted(zip(list(neg_items_ids), interest_list),
                            key=lambda x: x[1], reverse=True)
        return candidates[:top_n]

    def _loss(self, user_id, item_id, y, step):
        '''
        实际的损失值
        :param user_id:
        :param item_id:
        :param y: 实际的喜好
        :param step: 迭代到第几步
        :return:
        '''
        e = y - self._predict(user_id, item_id)
        print('setp', step, 'user_id', user_id, 'item_id', item_id,
              '实际值', y, 'loss', e)
        return e

    def _optimize(self, user_id, item_id, e):
        '''
        使用梯度下降的方法对模型进行优化
        已知用户对商品的偏差值，调整模型
        方法如下,调整第p行和第q行：
        E = 1/2 * (y - predict)^2, predict = matrix_p * matrix_q
        derivation(E, p) = -matrix_q*(y - predict),
        derivation(E, q) = -matrix_p*(y - predict),
        derivation（l2_square，p) = lam * p,
        derivation（l2_square, q) = lam * q
        delta_p = lr * (derivation(E, p) + derivation（l2_square，p))
        delta_q = lr * (derivation(E, q) + derivation（l2_square, q))
        :param user_id:
        :param item_id:
        :param e:
        :return:
        '''
        gradient_p = -e * self.q.loc[item_id].values
        gradient_q = -e * self.p.loc[user_id].values

        l2_p = self.lam*self.q.loc[item_id].values
        l2_q = self.lam*self.p.loc[user_id].values

        delta_p = self.lr*(gradient_p + l2_p)
        delta_q = self.lr*(gradient_q + l2_q)

        self.p -= delta_p
        self.q -= delta_q

    def train(self):
        '''
        训练模型，定期完成
        :return:
        '''
        for step in range(0, self.iter_count):
            for user_id, item_dict in self.items_dict.items():
                item_ids = list(item_dict.keys())
                random.shuffle(item_ids)
                for item_id in item_ids:
                    e = self._loss(user_id, item_id,
                                   item_dict[item_id], step)
                    self._optimize(user_id, item_id, e)
            # 逐渐降低学习率，避免震荡
            self.lr *= 0.9
        self.save()


