from flask import Blueprint, request, render_template, url_for, redirect
from models import House
import math


list_page = Blueprint('list_page', __name__)

"""
实现搜索列表页的功能
1. 定义一个路由为 /query的视图函数
2. 使用request 获取到请求字段 具体的查询信息
3. 使用sqlalchemy 在字段中 查询具体的信息 获取满足这个条件的房源
4. 使用publish_time字段，进行降序排序
5. 使用render_template进行渲染
"""


@list_page.route('/query/<int:page>')
def search_txt_info(page):
    addr = request.args.get('addr')
    rooms_info = request.args.get('rooms')

    if addr:
        house_num = House.query.filter(House.address.like(f'%{addr}%')).count()  
        total_num = math.ceil(house_num / 10)
        result = House.query.filter(House.address.like(f'%{addr}%')).order_by(House.publish_time.desc()).paginate(page=page, per_page=10)
        return render_template('search_list.html', house_list=result.items, page_num=result.page, total_num=total_num, addr=addr)

    if rooms_info:
        house_num = House.query.filter(House.rooms == rooms_info).count()
        total_num = math.ceil(house_num / 10)
        result = House.query.filter(House.rooms == rooms_info).order_by(House.publish_time.desc()).paginate(page=page, per_page=10)
        return render_template('search_list.html', house_list=result.items, page_num=result.page, total_num=total_num, rooms_info=rooms_info)

    return redirect(url_for('index_page.index'))



"""
1. 去定义一个视图函数 /list/pattern/<int:page>  method=get
2. 获取全部的房源数据，再根据房源的发布时间 publish_time 字段进行降序排序
3. 实现分页功能 借助分页插件 和 paginate函数来完成
4. 使用render_template进行渲染
"""

@list_page.route('/list/pattern/<int:page>')
def return_new_list(page):
    
    house_num = House.query.count()
    
    total_num = math.ceil(house_num / 10)
    result = House.query.order_by(House.publish_time.desc()).paginate(page=page, per_page=10)
    return render_template('list.html', house_list=result.items, page_num=result.page, total_num=total_num)



@list_page.route('/list/hot_house/<int:page>')
def return_hot_list(page):
    
    house_num = House.query.count()
    
    total_num = math.ceil(house_num / 10)
    result = House.query.order_by(
        House.page_views.desc()).paginate(page=page, per_page=10)
    return render_template('list.html', house_list=result.items, page_num=result.page, total_num=total_num)


def deal_title_over(word):
    if len(word) > 15:
        return word[:15] + '...'  
    else:
        return word


def deal_direction(word):
    if len(word) == 0 or word is None:  
        return '暂无信息！'
    else:
        return word


list_page.add_app_template_filter(deal_title_over, 'dealover')
list_page.add_app_template_filter(deal_direction, 'dealdirection')
