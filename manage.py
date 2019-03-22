from workflow.lfm_workflow import run as lfm
from workflow.ucf_workflow import run as ucf
from workflow.prank_workflow import run as prank

import sys

params = sys.argv[1]
params = int(params)
params2 = sys.argv[2]

if __name__=='__main__':
    if params2 != '':
        arg = params2
    # lfm模型给用户推荐的商品列表
    if arg == 'lfm':
        lfm(params)
    elif arg == 'ucf':
        ucf(params)
    elif arg == 'prank':
        prank(params)
    else:
        print('对不起，请重新输入模型参数')



