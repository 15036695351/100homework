from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser
from api.utils.respon import BaseResponse
from app01 import models
import redis
from django.conf import settings
import json

CONN = redis.Redis(host='192.168.11.175', port=6379)
USER_ID = 1


class ShoppingCarView(ViewSetMixin, APIView):
    # parser_classes = [JSONParser,FormParser]  # 默认的解析器类可以设置多个，但我们应该和前端约定好使用一种数据格式
    # parser_classes = [JSONParser]     # 由于解析器每次都要使用，所以应该在settings文件中配置
    def list(self, request, *args, **kwargs):
        ret = BaseResponse()
        try:
            shopping_car_course_list = []
            pattern = settings.LUFFY_SHOPPING_CAR % (USER_ID, "*")  # 找到购物车所有的商品
            keys_list = CONN.keys(pattern)  # 获取每一个商品的key
            # print(keys_list)
            for key in keys_list:
                print(6666)
                temp = {
                    'id': CONN.hget(key, 'id').decode('utf-8'),
                    'name': CONN.hget(key, 'name').decode('utf-8'),
                    'course_img': CONN.hget(key, 'course_img').decode('utf-8'),
                    'default_price_policy_id': CONN.hget(key, 'default_price_policy_id').decode('utf-8'),
                    'price_policy_dict': json.loads(CONN.hget(key, 'price_policy_dict').decode('utf-8'))
                }
                print(77777777)
                shopping_car_course_list.append(temp)
            ret.data = shopping_car_course_list
            print(ret.data)
        except Exception as e:
            ret.code = 10002
            ret.error = "获取购物车数据失败"
        return Response(ret.dict)

    def create(self, request, *args, **kwargs):
        """
        1. 接受用户选中的课程ID和价格策略ID
        2. 判断合法性
            - 课程是否存在？
            - 价格策略是否合法？
        3. 把商品和价格策略信息放入购物车 SHOPPING_CAR

        注意：用户ID=1
        """

        # 1.接收用户选中的课程id和价格策略id
        ret = BaseResponse()
        course_id = request.data.get("course_id")
        price_policy_id = request.data.get("price_policy_id")
        # 2.判断数据的合法性
        # 2. 判断合法性
        #   - 课程是否存在？
        #   - 价格策略是否合法？

        # 2.1 课程是否存在？
        course = models.Course.objects.filter(id=course_id).first()
        print(course.id)
        if not course:
            ret.code = 10001,
            ret.error = "课程不存在"
            return Response(ret.dict)

        # 2.2 价格策略是否合法
        price_policy_queryset = course.price_policy.all()  # 将该课程对应的所有的价格策略找出来
        price_policy_dict = {}
        for item in price_policy_queryset:
            temp = {
                "id": item.id,
                "price": item.price,
                "valid_period": item.valid_period,
                "valid_period_display": item.get_valid_period_display()
            }
            price_policy_dict[item.id] = temp
        if price_policy_id not in price_policy_dict:
            ret.code = 10002,
            ret.error = "价格策略不要修改"
            return Response(ret.dict)

        # 3. 把商品和价格策略信息放入购物车 SHOPPING_CAR
        # ******************** 判断购物车的商品是否过多  ***************
        pattern = settings.LUFFY_SHOPPING_CAR % (USER_ID, "*")
        keys = CONN.keys(pattern)
        if keys and len(keys) >= 1000:
            ret.code = 10003
            ret.data = "购物车已爆满，请先结算"
            return Response(ret.dict)

        # 将每一个商品的信息放到redis里面。
        key = settings.LUFFY_SHOPPING_CAR % (USER_ID, course_id,)
        CONN.hset(key, 'id', course_id)
        CONN.hset(key, 'name', course.name)
        CONN.hset(key, 'course_img', course.course_img)
        CONN.hset(key, 'default_price_policy_id', price_policy_id)
        CONN.hset(key, 'price_policy_dict', json.dumps(price_policy_dict))  # redis 字典里面如果再嵌套字典的话不能解析，所以只能手动解析

        CONN.expire(key, 20 * 60)  # expire：设置数据存在的时间，定时器

        ret.code = 10000
        ret.data = "购买成功"

        return Response(ret.dict)

    def destroy(self, request, *args, **kwargs):
        ret = BaseResponse()
        try:
            course_id = request.data.get("course_id")    # get
            key = settings.LUFFY_SHOPPING_CAR % (USER_ID, course_id,)

            CONN.delete(key)            # delete(key)==》删除redis中的某一个
            # CONN.hdel(key,'id')       # hdel()==》删除redis中某一个中的id

            ret.data = "删除成功"
        except Exception as e:
            ret.code = 10000
            ret.data = "删除数据失败"

        return Response(ret.dict)

    def update(self, request, *args, **kwargs):
        # 修改课程，只允许修改课程的价格策略
        ret = BaseResponse()
        try:
            course_id = request.data.get("course_id")  # get

            # 收到修改的价格策略的id
            price_policy_id = str(request.data.get("default_price_policy_id"))if request.data.get("default_price_policy_id") else None
            key = settings.LUFFY_SHOPPING_CAR % (USER_ID, course_id,)   # 找到需要修改的商品

            if not CONN.exists(key):    # 先判断课程
                ret.code = 10007
                ret.error = "课程不存在"
                return Response(ret.dict)

            # 再判断课程对应的价格策略的信息
            price_policy_dict = json.loads(CONN.hget(key, 'price_policy_dict').decode("utf-8"))  # 获取课程的价格策略
            if price_policy_id not in price_policy_dict:
                ret.code = 10008
                ret.error = "价格策略不存在"
                return Response(ret.dict)

            # 修改默认的价格策略id
            CONN.hset(key, 'default_price_policy_id', price_policy_id).decode("utf-8")
            CONN.expire(key, 20*6)
            ret.code = 10009
            ret.error = "价格策略修改成功"
            return Response(ret.dict)

        except Exception as e:
            ret.code = 10010
            ret.data = "修改价格策略失败"

        return Response(ret.dict)
