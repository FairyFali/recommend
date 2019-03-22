import pandas as pd
import sys 

params = sys.argv[1]

def get_user_info(user_id):
    frame = pd.read_csv('data/users.csv')
    result = frame[frame['UserID']==user_id]
    gender = 'Male'
    if str(result['Gender'].values[0]) == 'F':
    	gender = 'Female'
    return "Gender:" + gender + ',' + 'Age:' + str(result['Age'].values[0])

params = int(params)
print(get_user_info(params))


