from app01 import models
from rest_framework import serializers


class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class CourseModelSerializer(serializers.ModelSerializer):
    level_name = serializers.CharField(source='get_level_display')
    hours = serializers.CharField(source='coursedetail.hours')
    course_slogan = serializers.CharField(source='coursedetail.course_slogan')
    # recommend_courses = serializers.CharField(source='coursedetail.recommend_courses.all')  # 多对多的字段不能用source来解决，只能用SerializerMethodField() 并找到对应的方法

    recommend_courses = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = ['id','name','level_name','hours','course_slogan','recommend_courses']

    def get_recommend_courses(self,row):
        recommend_list = row.coursedetail.recommend_courses.all()
        return [{'id':item.id,'name':item.name} for item in recommend_list]


# 查看所有学位课并打印学位课名称以及授课老师
class DegreeCourseSerializer(serializers.ModelSerializer):
    teachers_list = serializers.SerializerMethodField()

    class Meta:
        model = models.DegreeCourse
        fields = ["id", "name", "teachers_list"]

    def get_teachers_list(self, row):
        abc_list = row.teachers.all()
        return [{"teachers_name": item.name} for item in abc_list]


# b.查看所有学位课并打印学位课名称以及学位课的奖学金
class DegreeCourseScholarSerializer(serializers.ModelSerializer):
    scholarship = serializers.SerializerMethodField()

    class Meta:
        model = models.DegreeCourse
        fields = ["id", "name", "scholarship"]

    def get_scholarship(self, row):
        abc_list = row.scholarship_set.all()
        return [{"scholarship": item.value}for item in abc_list]



# c. 展示所有的专题课
class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ["id", "name"]


# d. 查看id=1的学位课对应的所有模块名称
class Degree_CourseSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = ["course_name"]

    def get_course_name(self,row):
        abc_list = row.course_set.all()
        return [{"course_name": item.name}for item in abc_list]


# e.获取id = 1的专题课，并打印：课程名、级别(中文)、why_study、what_to_study_brief、所有recommend_courses
class Course_Obj_Serializer(serializers.ModelSerializer):
    level = serializers.CharField(source="get_level_display")
    why_study = serializers.CharField(source="coursedetail.why_study")
    what_to_study_brief = serializers.CharField(source="coursedetail.what_to_study_brief")
    recommend_courses = serializers.SerializerMethodField()

    def get_recommend_courses(self,row):
        abc_list = row.coursedetail.recommend_courses.all()
        return [{"course_name": item.name}for item in abc_list]

    class Meta:
        model = models.Course
        fields = ["name", "level", "why_study", "what_to_study_brief", "recommend_courses"]


# f.获取id = 1的专题课，并打印该课程相关的所有常见问题
class Course_Obj_Question_Serializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    def get_questions(self,row):
        abc_list = row.asked_question.all()
        return [{"questions": item.question }for item in abc_list]

    class Meta:
        model = models.Course
        fields = ["name", "questions" ]


# g.获取id = 1的专题课，并打印该课程相关的课程大纲
class Course_Obj_Outline_Serializer(serializers.ModelSerializer):
    outline = serializers.SerializerMethodField()

    def get_outline(self,row):
        abc_list = row.coursedetail.courseoutline_set.all()
        return [{"outline": item.title, "content":item.content }for item in abc_list]

    class Meta:
        model = models.Course
        fields = ["name", "outline" ]


# h.获取id = 1的专题课，并打印该课程相关的所有章节
class Course_Obj_Chapter_Serializer(serializers.ModelSerializer):
    chapters = serializers.SerializerMethodField()

    def get_chapters(self,row):
        print(6666666)
        abc_list = row.coursechapters.all() # 该字段被起了别名，别名为：coursechapters
        return [{"chapters": item.name, "summary": item.summary }for item in abc_list]

    class Meta:
        model = models.Course
        fields = ["name", "chapters"]











