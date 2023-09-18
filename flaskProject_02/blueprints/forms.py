import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired

from exts import db
from models import UserModel

# 用来验证前端提交的数据是否符合要求
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    # captcha = wtforms.StringField(validators=[Length(min=6, max=6, message="验证码格式错误！")])
    username = wtforms.StringField(validators=[Length(min=1, max=20, message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致")])

    # 自定义验证
    # 1、邮箱是否被注册
    # 2、验证码是否正确
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册！")
"""
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message='邮箱或验证码错误！')
        # else:
        #     # todo: 可以删除captcha_model
        #     db.session.delete(captcha_model)
        #     db.session.commit()
"""

class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])


class LendForm(wtforms.Form):
    gpu_id = wtforms.IntegerField(validators=[InputRequired(message='必须要传入gpu_id')])
    days = wtforms.DateField(validators=[InputRequired(message='必须要传入预计归还时间')])


class ReturnForm(wtforms.Form):
    gpu_id = wtforms.IntegerField(validators=[InputRequired(message='必须要传入gpu_id')])

class ReserveForm(wtforms.Form):
    gpu_id = wtforms.IntegerField(validators=[InputRequired(message='必须要传入gpu_id')])

class ReserveCancelForm(wtforms.Form):
    gpu_id = wtforms.IntegerField(validators=[InputRequired(message='必须要传入gpu_id')])
    user_id = wtforms.IntegerField(validators=[InputRequired(message='必须要传入user_id')])

# class SendEmailForm(wtforms.Form):
#     gpu_id = wtforms.IntegerField(validators=[InputRequired(message='必须要传入gpu_id')])