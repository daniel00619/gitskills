from flask import Flask, session, g
from exts import db
from flask_migrate import Migrate
import config
from blueprints.customer import bp as customer_bp
from blueprints.manage import bp as manage_bp
from models import *
from flasgger import Swagger


app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)
# db与app文件进行绑定
db.init_app(app)
# mail与app文件进行绑定
# mail.init_app(app)

# 导入和更新数据库
migrate = Migrate(app, db)

# blueprints 用来做模块化
# 举例：
# 豆瓣：电影，音乐，读书等
# 绑定蓝图
app.register_blueprint(customer_bp)
app.register_blueprint(manage_bp)

# 关联swagger
Swagger(app)

# hook
# 每次request请求前执行
@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)

# 上下文处理器
# 返回一个在所有模板(.html)中可见的字典
@app.context_processor
def my_context_processor():
    return {'user': g.user}

if __name__ == '__main__':
    app.run()
