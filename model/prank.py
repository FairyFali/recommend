import pickle
import pandas as pd

class Graph:

    graph_path = 'data/prank.graph'
    frame = pd.read_csv('data/ratings.csv')

    @classmethod
    def gen_user_graph(cls, user_id):
        '''
        获得用户的相连的节点
        :param user_id:
        :return:
        '''
        # 获得目标用户的电影列表
        item_list = list(set(cls.frame[cls.frame['UserID']== user_id]['MovieID']))
        # 该用户节点的链表
        graph_dict = {'i'+str(i):1 for i in item_list}
        return graph_dict

    @classmethod
    def gen_item_graph(cls, item_id):
        '''
        获得商品的相连的节点
        :param item_id:
        :return:
        '''
        # 目标节点的用户
        user_list = list(set(cls.frame[cls.frame['MovieID']== item_id]['UserID']))
        # 该商品节点的链表
        graph_dict = {'u'+str(i):1 for i in user_list}
        return graph_dict

    @classmethod
    def gen_graph(cls):
        '''
        获得图，图中每个节点都是用户或者商品，每一条边代表用户和商品有评分，权重设为1
        :return:
        '''
        # 所有的用户id和商品id
        user_ids = list(set(cls.frame['UserID']))
        item_ids = list(set(cls.frame['MovieID']))
        # 获得图的邻接链表，以字典的形式存储
        G = {'u'+str(i):cls.gen_user_graph(i) for i in user_ids}
        for i in item_ids:
            G['i'+str(i)] = cls.gen_item_graph(i)
        return G

    @classmethod
    def save(cls):
        '''
        保存图到本地文件
        :return:
        '''
        f = open(cls.graph_path, 'wb')
        pickle.dump(cls.gen_graph(), f)
        f.close()

    @classmethod
    def load(cls):
        '''
        加载图信息
        :return:
        '''
        f = open(cls.graph_path, 'rb')
        G = pickle.load(f)
        f.close()
        return G

class PersonalRank:

    def __init__(self):
        self.prank_path = 'data/prank_{}.model'
        self.frame = pd.read_csv('data/ratings.csv')
        # 随机游走概率
        self.alpha = 0.6
        # 迭代次数
        self.iter_count = 20
        # 图信息
        self.graph = Graph.load()
        # 存储节点的游走概率
        self.params = {i:0 for i in self.graph.keys()}

    def train(self, user_id):
        '''
        对于目标用户，每一轮将从该节点开始，意味着prob将为1。
        节点将按如下公式更新：
        对于每个节点，如果节点j的边缘在i之间：
            prob_i_j=alpha*prob_j/edge_num_out_of_node_j
            prob_i+=prob_i_j
        alpha表示随机游走的问题。
        :return:
        '''
        # 起点的概率为1
        self.params['u'+str(user_id)] = 1
        # 迭代iter_count次
        for i in range(self.iter_count):
            # tmp存储本次迭代后游走概率的值
            tmp = {key : 0 for key in self.graph.keys()}
            # 遍历图的节点和对应的边
            for node, edges in self.graph.items():
                for next,_ in edges.items():
                    # 对应于边，每个边对应的节点都增加相应的概率根据上次的params
                    tmp[next] += self.alpha*self.params[node]/len(edges)
            # 起点值
            tmp['u'+str(user_id)] += 1 - self.alpha
            # 把当前的概率值赋给params
            self.params = tmp
        # 排序
        self.params = sorted(self.params.items(), key=lambda x:x[1],
                             reverse=True)
        # 保存到本地
        self.save(user_id)

    def save(self, user_id):
        path = self.prank_path.format(user_id)
        f = open(path, 'wb')
        pickle.dump(self.params, f)
        f.close()

    def load(self, user_id):
        path = self.prank_path.format(user_id)
        f = open(path, 'rb')
        self.params = pickle.load(f)
        f.close()

    def predict(self, user_id, top_n=10):
        '''
        预测用户的商品
        :param user_id:
        :param top_n:
        :return:
        '''
        self.load(user_id)
        item_list = list(set(self.frame[self.frame['UserID']
                                        ==user_id]['MovieID']))
        item_list = ['i'+str(i) for i in item_list]
        candicate_list = []
        for key,value in self.params:
            if key not in item_list and 'u' not in key:
                candicate_list.append((key, value))
        return candicate_list[:top_n]


