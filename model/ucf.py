import pandas as pd
import math

class UserCF:

    def __init__(self):
        self.file_path = 'data/ratings.csv'
        self.frame = pd.read_csv(self.file_path)
        self.item_ids = set(self.frame['MovieID'])
        self.user_ids = set(self.frame['UserID'])


    def cos_sim(self, target_items, items):
        '''
        计算用户1和用户2的余弦相似度
        e.g: x = [1 0 1 1 0], y = [0 1 1 0 1]
        cosine = (x1*y1+x2*y2+...)
            / [sqrt(x1^2+x2^2+...)+sqrt(y1^2+y2^2+...)]
        that means union_len(movies1, movies2)
            / sqrt(len(movies1)*len(movies2))
        :param target_items:
        :param items:
        :return:
        '''
        # 交集
        union_len = len(set(target_items) & set(items))
        if union_len==0 : return 0
        len1 = len(target_items)
        len2 = len(items)
        # 分母
        product = len1*len2
        return union_len/math.sqrt(product)


    def get_top_n_user(self, target_user_id, top_n=10):
        '''
        获取和目标用户最相似的top_n个用户
        :param target_user_id:
        :param top_n:
        :return:
        '''
        # 所有的用户id
        all_user_ids = set(self.frame['UserID'])
        # 其他的用户id，(set对象的^相当于取差集)
        other_user_ids = all_user_ids ^ {target_user_id}
        # 获取其他所有用户评分过的电影
        other_user_items = []
        for i in other_user_ids:
            other_user_items.append(set(self.frame[self.frame['UserID'] == i]['MovieID'].values))
        # 目标用户评分过的电影
        target_user_items = set(self.frame[self.frame['UserID']==target_user_id]['MovieID'].values)
        # 相似度列表，计算目标用户和所有用户的相似度
        sim_list = []
        for items in other_user_items:
            sim_list.append(self.cos_sim(target_user_items, items))
        # 排序（sorted函数将序列排序，zip将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表。）
        sim_list = sorted(zip(other_user_ids, sim_list),
                          key=lambda x:x[1], reverse=True)
        # 返回前top_n个用户的id和相似度值
        return sim_list[:top_n]

    def get_top_n_items(self, target_user_id, top_n=10):
        '''
        获得前top_n个相似的商品
        :param target_user_id:
        :param top_n:
        :return:
        '''
        # 获得相似度用户列表
        sim_list = self.get_top_n_user(target_user_id)
        # 计算所有的相似度总和，做归一化使用（不做也可以，主要是比较大小）
        total_sim = sum([i[1] for i in sim_list])
        # 相似用户的数据信息，里面存储的相似用户对应的所有的电影的评分集合
        sim_user_data = []
        for user in sim_list:
            sim_user_data.append(
                self.frame[self.frame['UserID'] == user[0]])
        # 目标用户评分过的电影
        target_item_ids = set(self.frame[self.frame['UserID']==
                                      target_user_id]['MovieID'])
        # 候选推荐商品，目标用户看过的电影和相似用户看过的电影做差集
        candidates_item_ids = self.item_ids ^ target_item_ids
        # 对候选列表的电影进行预测得分
        interest_list = []
        for item_id in candidates_item_ids:
            # 所有相似用户对item_id的得分
            tmp = []
            for user_data in sim_user_data:
                if item_id in user_data['MovieID'].values:
                    tmp.append(user_data[user_data['MovieID']
                                     ==item_id]['Rating'].values[0])
                else:
                    # 没看过的算0分
                    tmp.append(0)
            interest = sum([tmp[i]*sim_list[i][1]/total_sim
                            for i in range(0, len(sim_list))])
            interest_list.append([item_id, interest])
        # 排序
        interest_list = sorted(interest_list, key=lambda x:x[1],
                               reverse=True)
        # 返回top_n得分高的电影
        return interest_list[:top_n]



# print(UserCF().get_top_n_items(1))
