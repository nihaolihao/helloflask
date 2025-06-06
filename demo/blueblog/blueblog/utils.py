try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for, current_app


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target) and target != '/auth/logout':
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def allowed_file(filename):
    # 检查文件扩展名是否存在 and 提取并验证扩展名
    # rsplit('.', 1) 从右侧分隔文件名，仅分隔一次（如“image.jpg”->["image","jpg"]
    # [1] 获取扩展名部分（“jpg”）
    # lower() 转换为小写，确保大小写敏感性
    # in 
    #current_app.config['BLUELOG_ALLOWED_IMAGE_EXTENSIONS']：
    # 检查扩展名是否在Flask应用的配置项 BLUELOG_ALLOWED_IMAGE_EXTENSIONS 中（通常是一个列表，如 ['jpg', 'png', 'gif']）。
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['BLUELOG_ALLOWED_IMAGE_EXTENSIONS']