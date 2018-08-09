# 重写中间件，必须要继承MiddlewareMixin类。还要再setting配置文件中导入该类名
# 因为接口很多，所以我们不能每一个接口的响应头都去手动增加：['Access-Control-Allow-Origin'] = 'http://localhost:8080'。
#   因此跨域问题需要在中间件进行全局配置,在中间件走到process_response时，重写process_response方法
#   又因为请求分为简单请求和复杂请求，所以：简单的在响应头增加'Access-Control-Allow-Origin'是不可行的，因此还要进行
# 简单的请求：
#     在请求头设置一个允许访问的域名和端口
# 复杂请求
# options请求做预检，允许设置的特殊的请求方式和请求头 +  允许访问的域名和端口
#     真正请求就可以发送过来进行处理  +  允许域名访问

from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class CorsMiddleware(MiddlewareMixin):

    def process_response(self,request,response):
        response['Access-Control-Allow-Origin'] = 'http://localhost:8080'
        if request.method == "OPTIONS":
            response["Access-Control-Allow-Methods"] = "PUT,DELETE"
            response["Access-Control-Allow-Headers"] = "Content-Type,xxxxx"
            # response["Access-Control-Allow-Methods"] = settings.CORS_METHODS
            # response["Access-Control-Allow-Headers"] = settings.CORS_HEADERS
        return response
