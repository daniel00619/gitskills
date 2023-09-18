from flask import Blueprint, render_template, request, g, redirect, url_for, jsonify
from sqlalchemy import and_
from .forms import *
from models import *
from decorators import login_required
from flasgger import swag_from

bp = Blueprint('gpu', __name__, url_prefix='/')

@bp.route('/')
def jump():
    return redirect(url_for("gpu.index"))

@bp.route('/gpu/list/')
@swag_from('../swagger_yaml/list.yaml')
def index():
    gpus = GPUModel.query.all()
    gpu_list = []
    for gpu in gpus:
        gpu_list.append(gpu.to_dict())
    data = {
        'status': 200,
        'msg': 'get ok',
        'gpu_list': gpu_list
    }
    return jsonify(data)
    # return jsonify([gpu.to_dict() for gpu in gpus])


@bp.route('/gpu/record/')
@swag_from('../swagger_yaml/record.yaml')
def record():
    records = LeaseholdModel.query.all()
    record_list = []
    for record in records:
        record_list.append(record.to_dict())
    data = {
        'status': 200,
        'msg': 'get ok',
        'gpu_list': record_list
    }
    return jsonify(data)

@bp.route('/gpu/detail/<int:id>', methods=['POST', 'GET'])
@swag_from('../swagger_yaml/detail.yaml')
def detail(id):
        gpu = GPUModel.query.get(id)
        gpu_dict = gpu.to_dict()
        data = {
            'status': 200,
            'msg': 'get ok',
            'gpu': gpu_dict
        }
        return jsonify(data)

@bp.post('/gpu/lend/')
@login_required
@swag_from('../swagger_yaml/lend.yaml')
def lend_gpu():
    form = LendForm(request.form)
    if form.validate():
        gpu_id = form.gpu_id.data
        gpu = GPUModel.query.get(gpu_id)
        if gpu.is_used:
            print("gpu已被占用!")
            data = {
                'status': 400,
                'msg': 'gpu已被占用!',
            }
            return jsonify(data)
            # return redirect('/')
        else:
            days = form.days.data
            gpu.is_used = True
            gpu.start_time = datetime.now()
            gpu.user_id = g.user.id
            gpu.days = days
            leasehold = LeaseholdModel(gpu_id=gpu_id, user_id=g.user.id, start_time=datetime.now())
            reverse = ReserveModel.query.filter(and_(ReserveModel.gpu_id == gpu_id, ReserveModel.user_id == g.user.id)).first()
            if reverse:
                db.session.delete(reverse) 
            db.session.add_all([leasehold, gpu])
            db.session.commit()
            data = {
                'status': 200,
                'msg': '借用成功',
            }
            return jsonify(data)
            # return redirect(url_for("gpu.my_lend"))
    else:
        print(form.errors)
        data = {
            'status': 401,
            'msg': form.errors,
            'id': request.form.get("gpu_id")
        }
        return jsonify(data)
        # return redirect(url_for("gpu.detail", id=request.form.get("gpu_id")))

@bp.post('/gpu/return/')
@login_required
@swag_from('../swagger_yaml/return.yaml')
def return_gpu():
    form = ReturnForm(request.form)
    if form.validate():
        gpu_id = form.gpu_id.data
        gpu = GPUModel.query.get(gpu_id)
        user_id = gpu.user_id
        if user_id != g.user.id:
            # print("哥，别测试了，不然还得改！")
            data = {
                'status': 400,
                'msg': '归还失败',
                'id': request.form.get("gpu_id")
            }
            return jsonify(data)
            # return redirect(url_for("gpu.detail", id=request.form.get("gpu_id")))
        else:
            leasehold = LeaseholdModel.query.filter(and_(LeaseholdModel.gpu_id == gpu_id, LeaseholdModel.start_time == gpu.start_time)).first()
            gpu.is_used = False
            gpu.start_time = None
            gpu.days = None
            gpu.user_id = None
            leasehold.end_time = datetime.now()
            db.session.add_all([gpu, leasehold])
            db.session.commit()
            data = {
                'status': 200,
                'msg': '归还成功',
            }
            return jsonify(data)
            # return redirect(url_for('gpu.my_lend'))


@bp.route('/gpu/my_lend/')
@login_required
@swag_from('../swagger_yaml/my_lend.yaml')
def my_lend():
    gpus = g.user.user_gpus
    gpu_list = []
    for gpu in gpus:
        gpu_list.append(gpu.to_dict())
    data = {
        'status': 200,
        'msg': 'get ok',
        'gpu_list': gpu_list
    }
    return jsonify(data)

@bp.post('/gpu/reserve/')
@login_required
@swag_from('../swagger_yaml/reserve.yaml')
def reserve():
    form = ReserveForm(request.form)
    if form.validate():
        gpu_id = form.gpu_id.data
        reverse_data = ReserveModel(gpu_id=gpu_id, user_id=g.user.id, user_name=g.user.username, reserve_time=datetime.now())
        db.session.add(reverse_data)
        db.session.commit()
        data = {
            'status': 200,
            'msg': '预约成功',
            'id': gpu_id
        }
        return jsonify(data)
        # return redirect(url_for('gpu.detail', id=gpu_id))
    else:
        print(form.errors)
        data = {
            'status': 401,
            'msg': form.errors,
            'id': request.form.get("gpu_id")
        }
        return jsonify(data)
        # return redirect(url_for('gpu.detail', id=request.form.get("gpu_id")))

@bp.post('/gpu/reserve_cancel/')
@login_required
@swag_from('../swagger_yaml/reserve_cancel.yaml')
def reserve_cancel():
    form = ReserveCancelForm(request.form)
    if form.validate():
        gpu_id = form.gpu_id.data
        user_id = form.user_id.data
        if user_id != g.user.id:
            print('点错了 亲！这不是你的预约')
            data = {
                'status': 400,
                'msg': '这不是你的预约',
                'id': gpu_id
            }
            return jsonify(data)
            # return redirect(url_for('gpu.detail', id=gpu_id))
        else:
            reserve = ReserveModel.query.filter(and_(ReserveModel.gpu_id == gpu_id, ReserveModel.user_id == user_id)).first()
            db.session.delete(reserve)
            db.session.commit()
            data = {
                'status': 200,
                'msg': '预约取消成功',
                'id': gpu_id
            }
            return jsonify(data)
            # return redirect(url_for('gpu.detail', id=gpu_id))
    else:
        print(form.errors)
        data = {
            'status': 401,
            'msg': form.errors,
            'id': request.form.get("gpu_id")
        }
        return jsonify(data)
        # return redirect(url_for('gpu.detail', id=request.form.get("gpu_id")))

@bp.route('/gpu/search/')
@swag_from('../swagger_yaml/search.yaml')
def search():
    q = request.args.get('q')
    gpus = GPUModel.query.filter(GPUModel.is_used.contains(q)).all()
    gpu_list = []
    for gpu in gpus:
        gpu_list.append(gpu.to_dict())
    data = {
        'status': 200,
        'msg': 'get ok',
        'gpu_list': gpu_list
    }
    return jsonify(data)

