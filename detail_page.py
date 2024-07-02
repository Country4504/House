from flask import Blueprint, render_template, jsonify, request
from models import House, User, Recommend
from sqlalchemy import func
from utils.regression_data import linear_model_main
from settings import db
from utils.pearson_recommend import recommend
from datetime import datetime, timedelta

detail_page = Blueprint('detail_page', __name__)



@detail_page.route('/house/<int:hid>')
def detail(hid):
    
    house = House.query.get(hid)
    
    facilities_str = house.facilities
    
    facilities_list = facilities_str.split('-')
    
    name = request.cookies.get('name')
    
    recommend_li = []
    
    if name:
        
        user = User.query.filter(User.name == name).first()
        
        seen_id_str = user.seen_id
        
        if seen_id_str:
            
            seen_id_list = seen_id_str.split(',')
            
            set_id = set([int(i) for i in seen_id_list])
            
            if hid not in set_id:
                new_seen_id_str = seen_id_str + ',' + str(hid)
                user.seen_id = new_seen_id_str
                db.session.commit()
        else:
            
            user.seen_id = str(hid)
            db.session.commit()
        
        info = Recommend.query.filter(Recommend.user_id == user.id, Recommend.house_id == house.id).first()
        
        if info:
            new_score = info.score + 1
            info.score = new_score
            db.session.commit()
        
        else:
            new_info = Recommend(user_id=user.id, house_id=house.id, title=house.title, address=house.address,
                                 block=house.block, score=1)
            db.session.add(new_info)
            db.session.commit()
        result = recommend(user.id)
        
        if result:
            for recommend_hid, recommend_num in result:
                recommend_house = House.query.get(int(recommend_hid))
                recommend_li.append(recommend_house)
        
        else:
            ordinary_recommend = House.query.filter(House.address == house.address).order_by(
                House.page_views.desc()).all()

            if len(ordinary_recommend) > 6:
                recommend_li = ordinary_recommend[:6]
            else:
                recommend_li = ordinary_recommend
    
    else:
        ordinary_recommend = House.query.filter(House.address == house.address).order_by(House.page_views.desc()).all()

        if len(ordinary_recommend) > 6:
            recommend_li = ordinary_recommend[:6]
        else:
            recommend_li = ordinary_recommend

    return render_template('detail_page.html', house=house, facilities=facilities_list, recommend_li=recommend_li)



@detail_page.route('/get/piedata/<block>')
def return_pie_data(block):
    result = House.query.with_entities(House.rooms, func.count()).filter(House.block == block).group_by(
        House.rooms).order_by(func.count().desc()).all()
    data = []
    for one_house in result:
        data.append({'name': one_house[0], 'value': one_house[1]})
    return jsonify({'data': data})






@detail_page.route('/get/scatterdata/<block>')
def return_scatter_data(block):
    
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
    
    data = []
    x = []
    y = []
    for index, i in enumerate(result):
        x.append([index])
        y.append(round(i[0], 2))
        data.append([index, round(i[0], 2)])
    
    predict_value = len(data)
    predict_outcome = linear_model_main(x, y, predict_value)
    p_outcome = round(predict_outcome[0], 2)
    
    data.append([predict_value, p_outcome])
    return jsonify({'data': {'data-predict': data, 'date_li': date_li}})






def deal_traffic_txt(word):
    if len(word) == 0 or word is None:
        return '暂无信息！'
    else:
        return word


detail_page.add_app_template_filter(deal_traffic_txt, 'dealNone')
