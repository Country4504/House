from utils.con_to_db import query_data
from math import sqrt


"""
1. 创建一个函数
2. 获取推荐表中的所有用户浏览的信息， 根据用户ID进行分类 ，获取所有的用户的ID
3. 对获取到的结果进行变形
"""


def get_total_u_id():
    
    sql = 'select user_id from house_recommend group by user_id'
    result = query_data(sql)
    
    total_u_id = list([i[0] for i in result])
    return total_u_id


def get_user_info(user_id):
    
    sql = 'select user_id, house_id, score from house_recommend where user_id = "{}"'.format(user_id)
    result = query_data(sql)
    data = {}
    for info in result:
        if info[0] not in data.keys():
            data[info[0]] = {info[1]: info[2]}
        else:
            data[info[0]][info[1]] = info[2]
    return data




def pearson_sim(user1, sim_user):
    
    user1_data = get_user_info(user1)[int(user1)]
    user2_data = get_user_info(sim_user)[int(sim_user)]
    
    common = []
    for key in user1_data.keys():
        if key in user2_data.keys():
            common.append(key)
    
    if len(common) == 0:
        return 0
    
    n = len(common)
    
    user1_sum = sum([user1_data[hid] for hid in common])
    user2_sum = sum([user2_data[hid] for hid in common])
    
    pow_sum1 = sum([pow(user1_data[hid], 2) for hid in common])
    pow_sum2 = sum([pow(user2_data[hid], 2) for hid in common])

    
    PSum = sum([float(user1_data[hid] * float(user2_data[hid])) for hid in common])

    
    molecule = PSum - (user1_sum * user2_sum / n)
    
    denominator = sqrt(pow_sum1 - pow(user1_sum, 2) / n) * (pow_sum2 - pow(user2_sum, 2) / n)

    if denominator == 0:
        return 0
    result = molecule / denominator

    return result


def top10_similar(UserID):
    
    total_u_id = get_total_u_id()

    
    res = []
    for u_id in total_u_id:
        if int(UserID) != u_id:
            similar = pearson_sim(int(UserID), int(u_id))
            if similar > 0:
                res.append((u_id, similar))
    
    res.sort(key=lambda val: val[1], reverse=True)
    return res[:10]




def recommend(user):

    
    if len(top10_similar(user)) == 0:
        return None

    
    top_sim_user = top10_similar(user)[0][0]

    
    items = get_user_info(top_sim_user)[int(top_sim_user)]  

    
    user_data = get_user_info(user)[int(user)]

    
    recommendata = []

    for item in items.keys():
        if item not in user_data.keys():
            recommendata.append((item, items[item]))
    recommendata.sort(key=lambda val: val[1], reverse=True)
    
    if len(recommendata) > 6:
        return recommendata[:6]
    else:
        return recommendata


if __name__ == '__main__':
    recommend(1)