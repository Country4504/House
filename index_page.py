from flask import Blueprint, render_template, request, jsonify
from models import House
from sqlalchemy import func

# 创建蓝图，蓝图的名称为包的名称index_page
index_page = Blueprint('index_page', __name__)


@index_page.route('/')
def index():
    # 获取房源总数量
    house_total_num = House.query.count()
    # 获取最新房源TOP6
    house_new_list = House.query.order_by(House.publish_time.desc()).limit(6).all()
    # 获取最热房源TOP4
    house_hot_list = House.query.order_by(House.page_views.desc()).limit(4).all()
    return render_template('index.html', num=house_total_num,
                           house_new_list=house_new_list,
                           house_hot_list=house_hot_list)


# 完成查询关键字的功能
# 1. 获取前端传递过来的查询参数 {"kw": keyWord, "info": info} kw：查询关键字 info：查询字段  使用request提取参数信息
# 2. 根据查询参数  过滤房源信息 address 包含三里屯的房源
# 3. 使用group_by 对address字段进行分组
# 4. 使用count来统计 相同地址下的房源数量
# 5. 使用order_by 根据房源的数量进行排序 并把它换成降序排序
# 6. 使用limit 获取数据的前9行
# 7. 组装数据 完成前后端的交互
@index_page.route('/search/keyword/', methods=['POST'])
def search_kw():
    kw = request.form['kw']  # 获取搜索关键字
    info = request.form['info']  # 获取用户选择的搜索选项
    if info == '地区搜索':
        # 获取查询的结果
        house_data = House.query.with_entities(
            House.address, func.count()).filter(House.address.contains(kw))
        # 对查询的结果进行分组、排序，并获取数量最多的前9条房源信息
        result = house_data.group_by('address').order_by(
            func.count().desc()).limit(9).all()
        if len(result):  # 有查询结果
            data = []
            for i in result:
                # 将查询的房源数据添加到data列表中
                data.append({'t_name': i[0], 'num': i[1]})
            return jsonify({'code': 1, 'info': data})
        else:  # 没有查询结果
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
