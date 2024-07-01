from utils.con_to_db import query_data
from math import sqrt

# 获取推荐表中所有的用户id
"""
1. 创建一个函数
2. 获取推荐表中的所有用户浏览的信息， 根据用户ID进行分类 ，获取所有的用户的ID
3. 对获取到的结果进行变形
"""


def get_total_u_id():
    # 用来获取推荐表中 所有的用户ID
    sql = 'select user_id from house_recommend group by user_id'
    result = query_data(sql)
    # 将所有的用户ID放入到一个列表中
    total_u_id = list([i[0] for i in result])
    return total_u_id


# 获取每个用户的浏览记录
"""
1. 创建一个函数
2. 通过user_id这个字段过滤出当前用户的所有的浏览历史，从当前的这组数据中 获取house_id  和 score
3. 对获取到的数据进行组装，即{1: {123:4, 234:2} }==>{u_id: {house_id: score, house_id:score.....}}
"""
def get_user_info(user_id):
    # 使用SQL语句完成数据库的查询
    sql = 'select user_id, house_id, score from house_recommend where user_id = "{}"'.format(user_id)
    result = query_data(sql)
    data = {}
    for info in result:
        if info[0] not in data.keys():
            data[info[0]] = {info[1]: info[2]}
        else:
            data[info[0]][info[1]] = info[2]
    return data

# 获取两个用户的相似度
"""
1. 创建一个函数
2. 获取两个用户的 各自的浏览记录
3. 后去两个用户共同的浏览过的房源
4. 使用皮尔逊相关系数的公式获取两个用户的相似度
"""


def pearson_sim(user1, sim_user):
    # 获取两个用户的 各自的浏览记录
    user1_data = get_user_info(user1)[int(user1)]
    user2_data = get_user_info(sim_user)[int(sim_user)]
    # 定义空列表，用于保存两个用户共同的浏览过的房源
    common = []
    for key in user1_data.keys():
        if key in user2_data.keys():
            common.append(key)
    # 如果没有共同评论过的房源就返回0
    if len(common) == 0:
        return 0
    # 统计相同房源的数量
    n = len(common)
    # 计算评分和Ex和Ey
    user1_sum = sum([user1_data[hid] for hid in common])
    user2_sum = sum([user2_data[hid] for hid in common])
    # 计算评分的平方和 E(x)^2 E(y)^2
    pow_sum1 = sum([pow(user1_data[hid], 2) for hid in common])
    pow_sum2 = sum([pow(user2_data[hid], 2) for hid in common])

    # 计算乘积的和
    PSum = sum([float(user1_data[hid] * float(user2_data[hid])) for hid in common])

    # 组装成分子
    molecule = PSum - (user1_sum * user2_sum / n)
    # 组装成分母
    denominator = sqrt(pow_sum1 - pow(user1_sum, 2) / n) * (pow_sum2 - pow(user2_sum, 2) / n)

    if denominator == 0:
        return 0
    result = molecule / denominator

    return result


# 获取相似度在前十名的用户
"""
1. 创建一个函数
2. 获取推荐表中的全部的用户的ID
3. 遍历全部用户的ID获取除自己之外的所有用户的相似度
4. 使用sort()函数来进行降序排序 获取前十名的用户ID
"""
def top10_similar(UserID):
    #  获取推荐表中的全部的用户的ID
    total_u_id = get_total_u_id()

    # 计算当前用户与其他用户的相似度
    res = []
    for u_id in total_u_id:
        if int(UserID) != u_id:
            similar = pearson_sim(int(UserID), int(u_id))
            if similar > 0:
                res.append((u_id, similar))
    # 将所有用户ID降序排列
    res.sort(key=lambda val: val[1], reverse=True)
    return res[:10]

# 获取推荐的房源
"""
1. 创建一个函数
2. 获取相似度最高的用户 通过这个用户 获取他完整的 浏览记录
3. 获取当前这个用户的 完整浏览记录
4. 判断 当前用户中没有  但是在 相似用户中 评价最高的房源
5. 按照 评分 使用sort来进行排序 降序排序 获取前6个
"""


def recommend(user):

    # 判断是否有相似度高的用户，若没有返回None
    if len(top10_similar(user)) == 0:
        return None

    # 获取相似度最高的用户ID
    top_sim_user = top10_similar(user)[0][0]

    # 获取相似度最高的用户 的完整浏览记录
    items = get_user_info(top_sim_user)[int(top_sim_user)]  # {1: {123:4, 234:2}}

    # 获取相似度最高的用户的完整浏览记录
    user_data = get_user_info(user)[int(user)]

    # 获取当前用户的浏览记录
    recommendata = []

    for item in items.keys():
        if item not in user_data.keys():
            recommendata.append((item, items[item]))
    recommendata.sort(key=lambda val: val[1], reverse=True)
    # 返回评分最高的房源
    if len(recommendata) > 6:
        return recommendata[:6]
    else:
        return recommendata


if __name__ == '__main__':
    recommend(1)