from flasgger import swag_from
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from exts import mail
from flask_mail import Message
import random
import string
from exts import db
from .forms import *
from models import UserModel, GPUModel
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('customer', __name__, url_prefix='/customer')

@bp.route('/login/', methods=['POST', 'GET'])
# @swag_from('../swagger_yaml/login.yaml')
def login():
    if request.method == 'GET':
        data = {
            'status': 200,
            'msg': 'get ok',
        }
        return jsonify(data)
        # return render_template('login.html')
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            user = UserModel.query.filter_by(email=email).first()
            if user:
                password = form.password.data
                if check_password_hash(user.password, password):
                    session['user_id'] = user.id  # 得到全局变量user
                    # return redirect(url_for('qa.index'))  # 这种使用方式url_for()里面的是方法名
                    data = {
                        'status': 200,
                        'msg': '登录成功',
                    }
                    return jsonify(data)
                    # return redirect('/')  # 两种都可以跳转到主页面
                else:
                    print("邮箱或密码错误")
                    data = {
                        'status': 400,
                        'msg': '邮箱或密码错误',
                    }
                    return jsonify(data)
                    # return redirect(url_for('customer.login'))
            else:
                print("邮箱不存在")
                data = {
                    'status': 400,
                    'msg': '邮箱不存在',
                }
                return jsonify(data)
                # return redirect(url_for('customer.login'))
        else:
            print(form.errors)
            data = {
                'status': 401,
                'msg': form.errors,
            }
            return jsonify(data)
            # return redirect(url_for('customer.login'))

# GET: 从服务器上获取数据
# POST: 将客户端的数据提交给服务器
@bp.route('/register/', methods=['POST', 'GET'])
# @swag_from('../swagger_yaml/register.yaml')
def register():
    if request.method == 'GET':
        data = {
            'status': 200,
            'msg': 'get ok',
        }
        return jsonify(data)
        # return render_template('register.html')
    else:
        # 验证用户提交的表单是否正确
        # 表单验证 flask-wtf: wtforms
        form = RegisterForm(request.form)
        if form.validate():
            email =form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            data = {
                'status': 200,
                'msg': '注册成功',
            }
            return jsonify(data)
            # return redirect(url_for("customer.login"))
        else:
            print(form.errors)
            data = {
                'status': 401,
                'msg': form.errors,
            }
            return jsonify(data)
            # return redirect(url_for("customer.register"))



# bp.route: 如果没有指定methods参数，默认就是GET请求
@bp.route("/captcha/email/<int:id>", methods=['POST', 'GET'])
@swag_from('../swagger_yaml/captcha_email.yaml')
def get_email_captcha(id):
    # url传参数
    # /captcha/emial?email=xxx@qq.com
    # form = SendEmailForm(request.form)
    # id = request.args.get('id')
    gpu = GPUModel.query.get(id)
    if gpu.user:
        email = gpu.user.email
    else:
        return jsonify({'code': 201, "message": "GPU空闲", "data": None})
    # print(email)
    # # 6位，数字和字母的组成
    # source = string.digits*6
    # captcha = random.sample(source, 6)
    # # 列表变成字符串
    # captcha = "".join(captcha)
    # print(captcha)

    # I/O 操作
    message = Message(subject="gpu使用情况提示", recipients=[email], body="同学，这块GPU你还在使用吗")
    mail.send(message)

    # 存储到数据库中
    # email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    # db.session.add(email_captcha)
    # db.session.commit()

    # RESTful API
    # {code: 200/400/500, message: "", data: {}}
    return jsonify({'code': 200, "message": "邮件发送成功", "data": None})


@bp.route('/logout/')
@swag_from('../swagger_yaml/logout.yaml')
def logout():
    session.clear()
    data = {
        'status': 200,
        'msg': '退出成功',
    }
    return jsonify(data)
    # return redirect(url_for('customer.login'))