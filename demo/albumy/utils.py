from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
import os
import random
from PIL import Image

dirname = os.path.dirname(__file__)


def r(): return random.randint(128, 255)


img = Image.new('RGB', (800, 800), color=(r(), r(), r()))
img.save(os.path.join(dirname, 'output_image.jpg'))


def generate_token(user, operation, expire_in=None, **kwargs):
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)
    data = {'id': user.id, 'operation': operation}
    data.update(**kwargs)
    return s.dumps(data)


def validate_token(user, token, operation,new_password=None):
    s = Serializer(current_app.config['SECRET_KEY'])

    try:
        data = s.loads(token)
    except (SingnatureExpired, BadSignature):
        return False

    if operation != data.get('operation') or user.id != data.get('id'):
        return False

    if operation == operation.CONFIRM:
        user.confirmed = True
    elif operation == operation.RESET_PASSWORD:
        user.set_password(new_password)  # 重置密码
    else:
        return False

    db.session.commit()
    return True
