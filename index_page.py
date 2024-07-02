from flask import Blueprint, render_template, request, jsonify
from models import House
from sqlalchemy import func


index_page = Blueprint('index_page', __name__)


@index_page.route('/')
def index():
    
    house_total_num = House.query.count()
    
    house_new_list = House.query.order_by(House.publish_time.desc()).limit(6).all()
    
    house_hot_list = House.query.order_by(House.page_views.desc()).limit(4).all()
    return render_template('index.html', num=house_total_num,
                           house_new_list=house_new_list,
                           house_hot_list=house_hot_list)










@index_page.route('/search/keyword/', methods=['POST'])
def search_kw():
    kw = request.form['kw']  
    info = request.form['info']  
    if info == '地区搜索':
        
        house_data = House.query.with_entities(
            House.address, func.count()).filter(House.address.contains(kw))
        
        result = house_data.group_by('address').order_by(
            func.count().desc()).limit(9).all()
        if len(result):  
            data = []
            for i in result:
                
                data.append({'t_name': i[0], 'num': i[1]})
            return jsonify({'code': 1, 'info': data})
        else:  
            return jsonify({'code': 0, 'info': []})
    if info == '户型搜索':
        house_data = House.query.with_entities(
            House.rooms, func.count()).filter(House.rooms.contains(kw))
        result = house_data.group_by('rooms').order_by(
            func.count().desc()).limit(9).all()
        if len(result):
            data = []
            for i in result:
                data.append({'t_name': i[0], 'num': i[1]})
            return jsonify({'code': 1, 'info': data})
        else:
            return jsonify({'code': 0, 'info': []})
