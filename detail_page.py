from flask import Blueprint, render_template, jsonify, request
from models import House, User, Recommend
from sqlalchemy import func
from utils.regression_data import linear_model_main
from settings import db
from utils.pearson_recommend import recommend
from datetime import datetime, timedelta

detail_page = Blueprint('detail_page', __name__)


# 实现房源数据展示
@detail_page.route('/house/<int:hid>')
def detail(hid):
    # 从数据库查询房源ID为hid的房源对象
    house = House.query.get(hid)
    # 获取房源对象的配套设施，比如床-宽带-洗衣机-空调-热水器-暖气
    facilities_str = house.facilities
    # 将分隔后的每个设施名称保存到列表中
    facilities_list = facilities_str.split('-')
    # 判断用户是否处于登录状态下
    name = request.cookies.get('name')
    # 定义一个用于存放推荐房源的列表容器
    recommend_li = []
    # 在登录状态下
    if name:
        # 获取用户对象
        user = User.query.filter(User.name == name).first()
        # 获取用户对象的浏览记录，格式为'123，234，345'或者null
        seen_id_str = user.seen_id
        # 存在浏览记录
        if seen_id_str:
            # 将浏览记录中保存的字符串转换成列表，比如'123，234，345'==>['123','234','345']
            seen_id_list = seen_id_str.split(',')
            # 借助set()函数去重
            set_id = set([int(i) for i in seen_id_list])
            # 判断hid是否在浏览记录中
            if hid not in set_id:
                new_seen_id_str = seen_id_str + ',' + str(hid)
                user.seen_id = new_seen_id_str
                db.session.commit()
        else:
            # 直接将当前的hid插入到浏览记录中
            user.seen_id = str(hid)
            db.session.commit()
        # 查询house_recommend表中是否有当前用户对此房源的浏览记录
        info = Recommend.query.filter(Recommend.user_id == user.id, Recommend.house_id == house.id).first()
        # 第一种情况，该用户已经浏览过此房源，就对推荐表中score进行+1操作
        if info:
            new_score = info.score + 1
            info.score = new_score
            db.session.commit()
        # 第二种情况，该用户没有浏览过此房源，直接插入一条新的数据
        else:
            new_info = Recommend(user_id=user.id, house_id=house.id, title=house.title, address=house.address,
                                 block=house.block, score=1)
            db.session.add(new_info)
            db.session.commit()
        result = recommend(user.id)
        # 有推荐房源，此时返回推荐房源给用户
        if result:
            for recommend_hid, recommend_num in result:
                recommend_house = House.query.get(int(recommend_hid))
                recommend_li.append(recommend_house)
        # 推荐房源列表为空，此时返回同小区的房源给用户
        else:
            ordinary_recommend = House.query.filter(House.address == house.address).order_by(
                House.page_views.desc()).all()

            if len(ordinary_recommend) > 6:
                recommend_li = ordinary_recommend[:6]
            else:
                recommend_li = ordinary_recommend
    # 未登陆状态下
    else:
        ordinary_recommend = House.query.filter(House.address == house.address).order_by(House.page_views.desc()).all()

        if len(ordinary_recommend) > 6:
            recommend_li = ordinary_recommend[:6]
        else:
            recommend_li = ordinary_recommend

    return render_template('detail_page.html', house=house, facilities=facilities_list, recommend_li=recommend_li)


# 实现户型占比功能
@detail_page.route('/get/piedata/<block>')
def return_pie_data(block):
    result = House.query.with_entities(House.rooms, func.count()).filter(House.block == block).group_by(
        House.rooms).order_by(func.count().desc()).all()
    data = []
    for one_house in result:
        data.append({'name': one_house[0], 'value': one_house[1]})
    return jsonify({'data': data})


# 实现房价预测功能
@detail_page.route('/get/scatterdata/<block>')
def return_scatter_data(block):
    # 获取时间序列
    result = House.query.with_entities(func.avg(House.price / House.area)).filter(House.block == block).group_by(
        House.publish_time).order_by(House.publish_time).all()
    time_stamp = House.query.filter(House.block == block).with_entities(House.publish_time).all()
    time_stamp.sort(reverse=True)
    date_li = []
    for i in range(1, 30):
        latest_release = datetime.fromtimestamp(int(time_stamp[0][0]))
        day = latest_release + timedelta(days=-i)
        date_li.append(day.strftime("%m-%d"))
    date_li.reverse()
    # 获取平均价格
    data = []
    x = []
    y = []
    for index, i in enumerate(result):
        x.append([index])
        y.append(round(i[0], 2))
        data.append([index, round(i[0], 2)])
    # 对未来一天的价格进行预测
    predict_value = len(data)
    predict_outcome = linear_model_main(x, y, predict_value)
    p_outcome = round(predict_outcome[0], 2)
    # 将预测的数据添加入data中
    data.append([predict_value, p_outcome])
    return jsonify({'data': {'data-predict': data, 'date_li': date_li}})


# 自定义过滤器，用于处理交通条件有无数据的情况
def deal_traffic_txt(word):
    if len(word) == 0 or word is None:
        return '暂无信息！'
    else:
        return word


detail_page.add_app_template_filter(deal_traffic_txt, 'dealNone')
