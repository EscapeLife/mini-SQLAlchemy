from .. import Filter
from functools import wraps
from webob.exc import HTTPUnauthorized, HTTPForbidden


# 身份认证提供者，用户需要实现principal方法，以及可选的实现has_permissions方法
class AuthenticationProvider:
    def __init__(self, ctx, request):
        self.request = request
        self.ctx = ctx

    @property
    def principal(self):
        raise HTTPUnauthorized()

    def has_permissions(self, permissions=None):
        if self.principal is None:
            raise HTTPUnauthorized()
        if not permissions:
            return True
        if set(getattr(self.principal, 'roles', [])).intersection(permissions):
            return True
        raise HTTPForbidden()


# 用于获取请求信息进行认证，注入实例
class AuthenticationFilter(Filter):
    def __init__(self, cls):
        self.provider_cls = cls

    def before_request(self, ctx, request):
        request.security = self.provider_cls(ctx, request)
        try:
            # 如果认证身份(principal)，通过则继续执行，不通过返回None
            request.principal = request.security.principal
        except HTTPUnauthorized:
            request.principal = None
        return request


# 使用has_permissions进行权限认证
class Require:
    def __init__(self, permissions=None, request=None):
        self.request = request
        self.permissions = permissions

    def __call__(self, fn):
        @wraps(fn)
        def wrap(ctx, request):
            if not getattr(request, 'security'):
                raise HTTPUnauthorized()
            if request.security.has_permissions(self.permissions):
                return fn(ctx, request)
        return wrap

    def __enter__(self):
        if not getattr(self.request, 'security'):
            raise HTTPUnauthorized()
        self.request.security.has_permissions(self.permissions)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
