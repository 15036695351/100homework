from django.shortcuts import render,HttpResponse

from app01 import models
# Create your views here.


def index(request):
    """
    今日练习题
    :param request:
    :return:
    """
    # a.查看所有学位课并打印学位课名称以及授课老师
    # a = models.DegreeCourse.objects.all().values("name", "teachers__name")
    # print(a)


    # b.查看所有学位课并打印学位课名称以及学位课的奖学金
    # b = models.DegreeCourse.objects.all()   # 先查询出所有的学位课
    # for item in b:
    #     print(item.name)   # 查询出所有学位课名称
    #     scholarships = item.scholarship_set.all()       # 查询出学位课
    #     for i in scholarships:
    #         print("-------->", i.time_percent, i.value) # 查询出学位课的奖学金



    # c. 展示所有的专题课
    # c = models.Course.objects.filter(degree_course__isnull=True).all()
    # print(c)


    # d.查看id = 1的学位课对应的所有模块名称
    # d = models.Course.objects.filter(degree_course=1).all()
    # print(d)


    # e. 获取id=1的专题课，并打印：课程名、级别(中文)、why_study、what_to_study_brief、所有recommend_courses
    # e = models.Course.objects.filter(id=1).first()
    # print(e.name,e.get_level_display(),
    #       e.coursedetail.why_study,
    #       e.coursedetail.what_to_study_brief,
    #       e.coursedetail.recommend_courses)


    # f. 获取id=1的专题课，并打印该课程相关的所有常见问题
    # f = models.Course.objects.filter(id=1).values("asked_question__question").all()
    # print(f)


    # g. 获取id=1的专题课，并打印该课程相关的课程大纲
    # g = models.Course.objects.filter(id=1).values("coursedetail__courseoutline__title")
    # print(g)

    # h.获取id = 1的专题课，并打印该课程相关的所有章节
    # h = models.Course.objects.filter(id=1).values("coursechapters__chapter").all()
    # print(h)

    # i.获取id = 1的专题课，并打印该课程相关的所有课时
    i = models.CourseSection.objects.filter(chapter__course_id=1).values("id", "name", "chapter_id", "chapter__name")
    for item in i:
        print(item)

    # j.获取id = 1 的专题课，并打印该课程相关的所有的价格策略
    # j = models.Course.objects.filter(id=1).values("price_policy__valid_period").all()
    # print(j)
    return HttpResponse("ok")


from api.api_serializer.course import CourseSerializer
from rest_framework.viewsets import ModelViewSet


# class CourseView(ModelViewSet):
#     # # 基于django rest framework 写路飞的接口（作业一 + rest framework 序列化）
#     # # - 课程列表API
#     # # - 课程详细API
#     queryset = models.Course.objects.all()
#     serializer_class = api_serializers.CourseSerializer

from api.api_serializer.course import CourseSerializer,CourseModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.versioning import URLPathVersioning
from api.utils.respon import BaseResponse
from rest_framework.pagination import PageNumberPagination


# class CourseView(APIView):
#     def get(self, request, *args, **kwargs):
#         # response = {'code':1000,'data':None,'error':None}
#         # 因为每一个视图对象都要显示response信息，所以把response单独拿出来变成一个类，用的时候直接实例化
#         print("version版本号：", request.version)
#         ret = BaseResponse()    # 使用封装了的BaseResponse类
#         try:
#             # 在URL中将路由分组，并将分组命名为version，那么Django默认这是版本号，可以通过request.version获取版本号
#             queryset = models.Course.objects.all()
#
#             # 分页：如果导出的数据过多，可以用分页器将数据分页
#             page = PageNumberPagination()
#             course_list = page.paginate_queryset(queryset,request,self)
#             # queryset:查询出来需要分页的数据；request：就是request；self:需要处理分页的视图函数
#
#             # 分页之后执行序列化
#             serializer_list = CourseModelSerializer(instance=course_list, many=True)
#             # 分页之后，在URL中可以直接查询相应的页码，例如：http://127.0.0.1:8000/api/v2/course/?page=2
#             ret.data = serializer_list.data     # 执行操作成功修改需要传送的数据
#         except Exception as e:
#             ret.data = 500
#             ret.error = "获取数据失败"
#         return Response(ret.dict)   # 调用ret对象的dict方法将ret以字典的形式 返回
# #
#
# class CourseDetailView(APIView):
#     def get(self, request, pk, *args, **kwargs):
#         # print("version版本号：", request.version)
#         ret = {'code': 1000, 'data': None, 'error': None}  # 使用普通的ret字典
#         try:
#             course = models.Course.objects.filter(id=pk).first()
#             serializer_obj = CourseSerializer(instance=course)
#             ret['data'] = serializer_obj.data
#         except Exception as e:
#             ret['code'] = 500
#             ret['error'] = "获取数据失败"
#         return Response(ret)


"""
作业：写接口
# a.查看所有学位课并打印学位课名称以及授课老师

# b.查看所有学位课并打印学位课名称以及学位课的奖学金

# c.展示所有的专题课

# d. 查看id=1的学位课对应的所有模块名称

# e.获取id = 1的专题课，并打印：课程名、级别(中文)、why_study、what_to_study_brief、所有recommend_courses

# f.获取id = 1的专题课，并打印该课程相关的所有常见问题

# g.获取id = 1的专题课，并打印该课程相关的课程大纲

# h.获取id = 1的专题课，并打印该课程相关的所有章节
"""


from api.api_serializer import course


# 查看所有学位课并打印学位课名称以及授课老师
class DegreeCourseTeacher(APIView):
    def get(self,request,*args,**kwargs):
        ret = BaseResponse()
        try:
            degreecourse_list = models.DegreeCourse.objects.all()
            ret.data = course.DegreeCourseSerializer(instance=degreecourse_list, many=True).data
        except Exception as e:
            ret.code = 500
            ret.error = "未获取到信息"
        return Response(ret.dict)


# b.查看所有学位课并打印学位课名称以及学位课的奖学金
class DegreeCourseScholar(APIView):
    def get(self,request,*args,**kwargs):
        ret = BaseResponse()
        try:
            degreecourse_list = models.DegreeCourse.objects.all()
            ret.data = course.DegreeCourseScholarSerializer(instance=degreecourse_list, many=True).data
        except Exception as e:
            ret.code = 500
            ret.error = "未获取到信息"
        return Response(ret.dict)


# c.展示所有的专题课
class CourseList(APIView):
    def get(self, request, *args, **kwargs):
        ret = BaseResponse()
        try:
            course_list = models.Course.objects.filter(degree_course__isnull=True).all()
            print(course_list)
            ret.data = course.CourseListSerializer(instance=course_list, many=True).data
        except Exception as e:
            ret.code = 500
            ret.error = "未获取到信息"
        return Response(ret.dict)


# d. 查看id=1的学位课对应的所有模块名称
class Degree_Course(APIView):
    def get(self, request, *args, **kwargs):
        ret = BaseResponse()
        try:
            course_list = models.DegreeCourse.objects.filter(id=1).first()
            print(course_list)
            ret.data = course.Degree_CourseSerializer(instance=course_list).data
            print(type(ret.data), ret.data)
        except Exception as e:
            ret.code = 500
            ret.error = "未获取到信息"
        return Response(ret.dict)


# e.获取id = 1的专题课，并打印：课程名、级别(中文)、why_study、what_to_study_brief、所有recommend_courses
class Course_Obj(APIView):
    def get(self, request, *args, **kwargs):
        ret = BaseResponse()
        try:
            course_obj = models.Course.objects.filter(id=1).first() # 我建的表id=1的是学位课，degree_course__isnull字段不填
            print(course_obj)
            ret.data = course.Course_Obj_Serializer(instance=course_obj).data
        except Exception as e:
            ret.code = 500
            ret.error = "未获取到信息"
        return Response(ret.dict)


# f.获取id = 1的专题课，并打印该课程相关的所有常见问题
class Course_Obj_Question(APIView):
    def get(self, request, *args, **kwargs):
        ret = BaseResponse()
        try:
            course_obj = models.Course.objects.filter(id=1).first()
            ret.data = course.Course_Obj_Question_Serializer(instance=course_obj).data
        except Exception as e:
            ret.code = 500
            ret.error = "未获取到信息"
        return Response(ret.dict)


# g.获取id = 1的专题课，并打印该课程相关的课程大纲
class Course_Obj_Outline(APIView):
    def get(self, request, *args, **kwargs):
        ret = BaseResponse()
        try:
            course_obj = models.Course.objects.filter(id=1).first()
            ret.data = course.Course_Obj_Outline_Serializer(instance=course_obj).data
        except Exception as e:
            ret.code = 500
            ret.error = "未获取到信息"
        return Response(ret.dict)


# h.获取id = 1的专题课，并打印该课程相关的所有章节
class Course_Obj_Chapter(APIView):
    def get(self, request, *args, **kwargs):
        ret = BaseResponse()
        try:
            course_obj = models.Course.objects.filter(id=1).first()

            ret.data = course.Course_Obj_Chapter_Serializer(instance=course_obj).data
        except Exception as e:
            ret.code = 500
            ret.error = "未获取到信息"
        return Response(ret.dict)


# ***************************************** 今日内容↓ *************************************************************
from rest_framework.viewsets import ViewSetMixin
from rest_framework.views import APIView


class CourseView(ViewSetMixin, APIView):
    def list(self, request, *args, **kwargs):
        ret = BaseResponse()    # 使用封装了的BaseResponse类
        try:
            queryset = models.Course.objects.all()

            # page = PageNumberPagination()
            # course_list = page.paginate_queryset(queryset,request, self)

            serializer_list = CourseModelSerializer(instance=queryset, many=True)

            ret.data = serializer_list.data     # 执行操作成功修改需要传送的数据
        except Exception as e:
            ret.data = 500
            ret.error = "获取数据失败"
        return Response(ret.dict)   # 调用ret对象的dict方法将ret以字典的形式 返回

    def create(self, request, *args, **kwargs):
        """
        增加
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

    def retrieve(self, request, pk, *args, **kwargs):
        ret = BaseResponse()    # 使用封装了的BaseResponse类
        try:
            queryset = models.Course.objects.filter(id=pk)
            serializer_list = CourseModelSerializer(instance=queryset)

            ret.data = serializer_list.data     # 执行操作成功修改需要传送的数据
        except Exception as e:
            ret.data = 500
            ret.error = "获取数据失败"
        return Response(ret.dict)   # 调用ret对象的dict方法将ret以字典的形式 返回

    def update(self,request, pk, *args, **kwargs):
        """
        修改
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def destroy(self, request, pk, *args, **kwargs):
        """
        删除
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """