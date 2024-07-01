from flask import Blueprint, request, Response, jsonify, render_template, redirect, make_response
from models import User, House
from settings import db
import json

user_page = Blueprint('user_page', __name__)


@user_page.route('/register', methods=["POST"])
def register():
    # 获取用户的注册信息，包括用户名、密码、邮箱
    name = request.form['username']
    password = request.form['password']
    email = request.form['email']
    # 查询数据库中
    result = User.query.filter(User.name == name).all()
    # 判断用户是否已经注册，如果没有注册在返回的结果中设置Cookie
    if len(result) == 0:
        user = User(name=name, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        json_str = json.dumps({'valid': '1', 'msg': user.name})
        res = Response(json_str)  # 实例化的过程中需要给他传入响应内容
        res.set_cookie('name', user.name, 3600 * 2)
        return res
    # 用户名已经被注册过
    else:
        return jsonify({'valid': '0', 'msg': '用户已注册！'})


@user_page.route('/user/<name>')
def user(name):
    # 查询数据库中用户名为name的User类对象
    user = User.query.filter(User.name == name).first()
    # 判断用户是否存在
    if user:   # 该用户存在
        collect_id_str = user.collect_id    # 获取当前用户收藏的房源ID
        if collect_id_str:                  # 若不为空
            collect_id_list = collect_id_str.split(',')
            collect_house_list = []
            # 根据房源ID获取对应的房源对象
            for hid in collect_id_list:
                house = House.query.get(int(hid))
                # 将房源对象添加到列表中
                collect_house_list.append(house)
        else:                     # 若为空
            collect_house_list = []

        seen_id_str = user.seen_id       # 获取当前用户的浏览记录
        if seen_id_str:
            seen_id_list = seen_id_str.split(',')
            seen_house_list = []
            # 根据房源ID获取对应的房源对象
            for hid in seen_id_list:
                house = House.query.get(int(hid))
                seen_house_list.append(house)
        else:
            seen_house_list = []
        return render_template('user_page.html', user=user,
                               collect_house_list=collect_house_list,
                               seen_house_list=seen_house_list)
    else:
        # 重定向到首页
        return redirect('/')


@user_page.route('/login', methods=['POST'])
def login():
    # 首先需要获取用户提交的信息用户的名字和密码
    name = request.form['username']
    password = request.form['password']
    # 根据用户名进行校验  
    user = User.query.filter(User.name == name).first()
    # 用户名存在的时候
    if user:
        # 判断用户输入的密码是否正确
        if user.password == password:
            # 将响应信息变化成JSON字符串
            result = {'valid': '1', 'msg': user.name}
            result_json = json.dumps(result)
            # 构建返回数据
            res = Response(result_json)
            # 设置Cookie的过期时间
            res.set_cookie('name', user.name, 3600 * 2)
            return res
        else:
            return jsonify({'valid': '0', 'msg': '密码不正确！'})
    # 用户不存在的时候
    else:
        return jsonify({'valid': '0', 'msg': '用户名不正确！'})


@user_page.route('/logout')
def logout():
    # 在Cookie中获取用户信息
    name = request.cookies.get('name')
    # 用户处于登录状态下
    if name:
        result = {'valid': '1', 'msg': '退出登录成功！'}
        json_str = json.dumps(result)
        res = Response(json_str)
        # 删除用户的Cookie
        res.delete_cookie('name')
        return res
    # 用户处于未登录状态下
    else:
        return jsonify({'valid': '0', 'msg': '未登录！'})


@user_page.route('/modify/userinfo/<option>', methods=['POST'])
def modify_info(option):
    if option == 'name':
        y_name = request.form['y_name']  # 获取旧的用户名
        name = request.form['name']  # 获取新的用户名
        # 查询用户是否存在
        user = User.query.filter(User.name == y_name).first()
        # 用户存在
        if user:
            # 更新昵称
            user.name = name
            db.session.commit()
            result = {'ok': '1'}
            json_str = json.dumps(result)
            # 创建响应对象
            res = Response(json_str)
            res.set_cookie('name', user.name, 3600 * 2)
            return res
        # 用户不存在
        else:
            return jsonify({'ok': '0'})
    elif option == 'addr':
        # 获取用户名
        y_name = request.form['y_name']
        # 获取新的住址
        addr = request.form['addr']
        # 查询用户是否存在
        user = User.query.filter(User.name == y_name).first()
        # 用户存在
        if user:
            # 更新住址
            user.addr = addr
            db.session.commit()
            # 返回JSON字符串
            return jsonify({'ok': '1'})
        # 用户不存在
        else:
            return jsonify({'ok': '0'})
    elif option == 'password':
        # 获取用户名
        y_name = request.form['y_name']
        # 获取新的密码
        password = request.form['password']
        # 查询用户是否存在
        user = User.query.filter(User.name == y_name).first()
        # 用户存在
        if user:
            # 更新密码
            user.password = password
            db.session.commit()
            return jsonify({'ok': '1'})
        # 用户不存在
        else:
            return jsonify({'ok': '0'})
    elif option == 'email':
        # 获取用户名
        y_name = request.form['y_name']
        # 获取新的邮箱
        email = request.form['email']
        # 查询用户是否存在
        user = User.query.filter(User.name == y_name).first()
        # 用户存在
        if user:
            # 更新邮箱
            user.email = email
            db.session.commit()
            return jsonify({'ok': '1'})
        # 用户不存在
        else:
            return jsonify({'ok': '0'})
    return 'ok'


@user_page.route('/add/collection/<int:hid>')
def add_collection_id(hid):
    name = request.cookies.get('name')  # 从Cookie中获取用户名
    if name:
        user = User.query.filter(User.name == name).first()  # 获取user对象
        collect_id_str = user.collect_id  # 通过user对象获取用户收藏房源数据
        # 判断当前用户是否有收藏房源数据
        if collect_id_str:
            collect_id_list = collect_id_str.split(',')
            set_id = set([int(i) for i in collect_id_list])
            if hid in set_id:
                return jsonify({'valid': '1', 'msg': '已经收藏过了!'})
            else:
                new_collect_id_str = collect_id_str + ',' + str(hid)
                user.collect_id = new_collect_id_str
                db.session.commit()
                return jsonify({'valid': '1', 'msg': '收藏完成!'})
        else:
            user.collect_id = str(hid)
            db.session.commit()
            return jsonify({'valid': '1', 'msg': '收藏完成!'})
    else:
        return jsonify({'valid': '0', 'msg': '需要登录后才能使用收藏功能'})


@user_page.route('/collect_off', methods=['POST'])
def collect_off():
    name = request.form['user_name']  # 获取用户名
    hid = request.form['house_id']  # 获取房源ID
    user = User.query.filter(User.name == name).first()  # 获取用户对象
    collect_id_str = user.collect_id  # 获取用户的收藏房源列表
    collect_id_list = collect_id_str.split(',')
    if hid in collect_id_list:  # 判断要删除的房源ID是否在收藏房源列表中
        collect_id_list.remove(hid)
        new_collect_id_str = ','.join(collect_id_list)  # 重新拼接收藏房源ID
        user.collect_id = new_collect_id_str
        db.session.commit()  # 更新数据库
        result = {'valid': '1', 'msg': '删除成功！'}
        return jsonify(result)
    else:
        result = {'valid': '0', 'msg': '删除失败！'}
        return jsonify(result)


@user_page.route('/del_record', methods=['POST'])
def del_record():
    # 获取前端传递过来的用户名
    name = request.form['user_name']
    # 获取用户对象
    user = User.query.filter(User.name == name).first()
    # 获取用户对象的浏览记录
    seen_id_str = user.seen_id
    # 浏览记录存在
    if seen_id_str:
        user.seen_id = ''
        db.session.commit()
        return jsonify({'valid':'1', 'msg':'删除成功!'})
    # 浏览记录不存在
    else:
        return jsonify({'valid': '0', 'msg': '暂无信息可以删除!'})
