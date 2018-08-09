from django.conf.urls import url
from api.views import course,auth,shoppingcar
urlpatterns = [
    # url(r'degreecourseteacher/$', course.DegreeCourseTeacher.as_view()),
    # url(r'degreecoursescholar/$', course.DegreeCourseScholar.as_view()),
    # url(r'courselist/$', course.CourseList.as_view()),
    # url(r'degree_course/$', course.Degree_Course.as_view()),
    # url(r'course_obj/$', course.Course_Obj.as_view()),
    # url(r'course_obj_question/$', course.Course_Obj_Question.as_view()),
    # url(r'course_obj_outline/$', course.Course_Obj_Outline.as_view()),
    # url(r'course_obj_chapter/$', course.Course_Obj_Chapter.as_view()),
    # url(r'index/$', course.index),
    url(r'shoppingcar/$', shoppingcar.ShoppingCarView.as_view({'post': 'create', 'get': 'list','put':'update','delete':'destroy'})),
    url(r'auth/$', auth.AuthView.as_view(
        {'post': 'login'}
    )),
    url(r'course/$', course.CourseView.as_view(
        {'get': 'list', 'post': 'create'}
    )),

    url(r'course/(?P<pk>\d+)/$', course.CourseView.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}
    )),


]

# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register(r'course', course.CourseView)
# urlpatterns += router.urls