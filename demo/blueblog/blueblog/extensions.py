from flask_bootstrap import Bootstrap4
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
 
bootstrap = Bootstrap4()
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
ckeditor = CKEditor()
mail = Mail()
moment = Moment()
toolbar = DebugToolbarExtension()
migrate = Migrate()
 
# 定义用户加载器函数，用于从数据库中加载用户对象
@login_manager.user_loader
def load_user(user_id):
    from blueblog.models import Admin
    user = Admin.query.get(int(user_id))
    return user
 
# 设置登录视图，用于处理用户登录
login_manager.login_view = 'auth.login'
# login_manager.login_message = 'Your custom message'
# 设置登录消息类别为警告
login_manager.login_message_category = 'warning'