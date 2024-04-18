from django.contrib import admin
from django.urls import path

# from .views.coursemanagementviews import (# )
# from .views.courseviews import (# )

from .views.superadmindashboardviews import (
    ActiveRegisteredCustomerCountView,
    CountOfActiveRegistrationPerCoure, 
    CourseCountView,
    GraphOfProgressPerCourseView, 
)

from .views.registercourseviews import (
    CourseCustomerRegistrationView,
    LMSCustomerListView,
    ManageCourseRegistrationRecordStatusView
)
from .views.coursesviews import (
    CourseView,
    ManageCourseView,
    FirstVersionActiveCourseListView,
    DerivedVersionActiveCourseListView,
)
from .views.coursecontentviews import (
    CourseStructureView,
    ReadingMaterialView,
    QuizView,

)
from .views.quizcontentviews import (
    ChoicesView,
    QuestionView,
    QuizTake,
    dummy_quiz_index,
)
from .views.clientadmindashboard import(
    ProgressCountView,
    RegisteredCourseCountView, 
    ActiveEnrolledUserCountPerCustomerView,
    
) 

urlpatterns = [
    #courseview.py  views url
    
    #coursemanagementviews.py views url

    
    #registercourseviews.py views url
    path('lms-customer/', LMSCustomerListView.as_view(), name='lms-customer-list'),
    path('course-register-record/', CourseCustomerRegistrationView.as_view(), name='course-register-record'),
    path('manage-status/register-records/', ManageCourseRegistrationRecordStatusView.as_view(), name='manage-register-records'), 
        
    #superadmindashboardviews.py views url
    path('dashboard/sa/registration/count/', ActiveRegisteredCustomerCountView.as_view(), name='active-registration-count'),
    path('dashboard/sa/active_registration-per-course/count/', CountOfActiveRegistrationPerCoure.as_view(), name='active_registration-per-course-count'),
    path('dashboard/sa/progress-per-course/count/', GraphOfProgressPerCourseView.as_view(), name='not_started-per-course-count'),
    path('dashboard/sa/course/count/', CourseCountView.as_view(), name='course-count'),

    # coursesviews.py view urls
    path('courses/', CourseView.as_view(), name='courses'), #*
    path('manage/course/', ManageCourseView.as_view(), name='manage-course'), #*
    path('courses/active/v1/', FirstVersionActiveCourseListView.as_view(), name='active-first-version-courses-list'),
    path('courses/derived-active/<int:course_id>/', DerivedVersionActiveCourseListView.as_view(), name='active-derived-version-course-list'),
    
    # coursecontentviews.py view urls
    path('course/<int:course_id>/structure/', CourseStructureView.as_view(), name='course-structure'), #*
    path('course/<int:course_id>/reading-material/', ReadingMaterialView.as_view(), name='reading-material'), #*
    path('course/<int:course_id>/quiz/', QuizView.as_view(), name='quiz'), #*

    # quizcontentviews.py views urls
    path('quiz/<int:quiz_id>/question/', QuestionView.as_view(), name='reading-material'), #*
    path('question/<int:question_id>/choices/', ChoicesView.as_view(), name='question-choice'),
    path("<int:pk>/<slug:quiz_slug>/take/", QuizTake.as_view(), name="quiz_take"), #href="{% url 'quiz_take' pk=course.pk slug=quiz.slug %}
    #extra
    path('quiz/redirect/<int:course_id>/', view=dummy_quiz_index, name='quiz_index'),
    path('count-registered-courses/', RegisteredCourseCountView.as_view(), name='count_registered_courses'),
    path('active-enrolled-user-count/', ActiveEnrolledUserCountPerCustomerView.as_view(), name='active_enrolled_user_count'),
    path('progress-count/', ProgressCountView.as_view(), name='progress_count'),
    
]