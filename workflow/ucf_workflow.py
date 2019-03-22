import model.ucf as ucf
import time

def run(user_id):
    '''
    调试ucf模型
    :param user_id:
    :return:
    '''
    print('Start..')
    start = time.time()
    item_list = ucf.UserCF().get_top_n_items(user_id)
    print(item_list)
    print('End.')
    print('Cost Time:', time.time()-start)
