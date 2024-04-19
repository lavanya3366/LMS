from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from backend.models.coremodels import Customer, User
from core.custom_mixins import ClientAdminMixin
from core.custom_permissions import ClientAdminPermission
from rest_framework import serializers
from backend.serializers.clientadmindashboard import ActiveEnrolledUserCountSerializer, ProgressDataSerializer, RegisteredCourseCountSerializer  # Import your serializer

from backend.models.coremodels import Customer, User
from core.custom_mixins import ClientAdminMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models.allmodels import (
    Course,
    CourseCompletionStatusPerUser,
    CourseRegisterRecord,
)
from rest_framework.exceptions import NotFound, ValidationError
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator

# to be taken from anuj and lavanya
# =================================================================
# employee dashboard
# =================================================================

class CreateCourseCompletionStatusPerUserView(APIView):
    """
        allowed for client admin
        POST request
        triggered after course enrollment records creation , similar to that one.
                in request body :
                        list of course_id =[..., ..., ..., ...]
                        list of user_id =[..., ..., ..., ...]
                        each course in list will be mapped for all users in list
        while creating instance :
            enrolled_user = request body
            course = request body
            completion_status = (default=False)
            in_progress_status = (default=False)
            created_at = (auto_now_add=True)
    """
    pass

class CreateQuizScoreView(APIView):
    """
        allowed for client admin
        POST request
        triggered after course enrollment records creation , similar to that one.
                in request body :
                        list of course_id =[..., ..., ..., ...]
                        list of user_id =[..., ..., ..., ...]
                        each course in list will be mapped for all users in list
        while creating instance :
            enrolled_user = request body
            course = request body
            total_quizzes_per_course = calculate in view for course by counting active quizzes in it
            completed_quiz_count = by default 0
            total_score_per_course = (default=0)
    """
    pass

class UpdateCompleteQuizCountView(APIView):
    """
        POST request
        triggered when quiz attempt history for that course, that user have completed =true , if set of quiz, course, user doesn't already have completed = true in table
        while updating instance :
            completed_quiz_count = increment by 1
    """
    pass

class UpdateTotalScorePerCourseView(APIView):
    """
        POST request
        triggered when quiz attempt history for that course, that user have completed =true 
        while updating instance :
            total_score_per_course -> calculate for it 
    """
    pass

class UpdateCourseCompletionStatusPerUserView(APIView):
    """
        POST request
        triggers when 
        total_quizzes_per_course = completed_quiz_count in quiz score for that user in request
        if total_quizzes_per_course == completed_quiz_count:
            completion_status=True and in_progress_status =False
        if total_quizzes_per_course > completed_quiz_count:
            completion_status=False and in_progress_status =True
    """
    pass

class DisplayClientCourseProgressView(APIView):
    """
        GET request
        for user in request, if he have data in course enrollment table
        
        display if user in request have active enrollment for the course
        display:
            completed_quiz_count
    """
    pass

class DisplayClientCourseCompletionStatusView(APIView):
    """
        GET request
        for user in request, if he have data in course enrollment table(active)
        display:
            completion_status or in_progress_status = Based on which is true for the user for thi course
    """
    pass

class CountOfAssignedCoursesView(APIView):
    """
    GET request
    for user in request , count the number of active enrollments he have in course enrollment table
    """
    pass

class CountClientCompletedCourseView(APIView):
    """
        GET request
        for the user filter the CourseCompletionStatusPerUser table
        and count courses for which completion_status= True and in_progress_status = False as completed courses
        and count courses for which completion_status= False and in_progress_status = True as completed courses
    """
    pass

# =================================================================
# employer dashboard
# =================================================================
 # Import your User model
class ActiveEnrolledUserCountPerCustomerView(APIView):
    """
    Get API for counting active enrolled users per customer ID.
    """
    permission_classes = [ClientAdminPermission]
    def get(self, request):
        try:

            serializer = ActiveEnrolledUserCountSerializer(data=request.query_params)
            serializer.is_valid(raise_exception=True)
            customer_id = serializer.validated_data.get('customer_id')
            # Retrieve the customer ID from the request query parameters
            user_count = User.objects.filter(customer_id=customer_id, status='active').count()
            # Return the count in the response
            return Response({"user_count": user_count}, status=status.HTTP_200_OK)
        except (serializers.ValidationError, Exception) as e:
            error_message = e.detail if isinstance(e, serializers.ValidationError) else str(e)
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)



class RegisteredCourseCountView(APIView):
    """
    Get API for client admin to count registered active courses per customer ID.
    """
    permission_classes = [ClientAdminPermission]
    def get(self, request):
        try:
            serializer = RegisteredCourseCountSerializer(data=request.query_params)
            serializer.is_valid(raise_exception=True)
            # Extract customer ID from request query parameters
            customer_id = serializer.validated_data.get('customer_id')
            registered_course_counts = CourseRegisterRecord.objects.filter(
                customer_id=customer_id, 
                active=True,  # Only active registrations
                course__active=True  # Only active courses
            ).values('course').distinct().count()
            # Your existing logic to count registered active courses per customer ID
            response_data = {
                'active_course_count': registered_course_counts
            }
            return Response(response_data)

        except Exception as e:
            if isinstance(e, ValidationError):
                return Response({'error': e.detail}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#---------
# graph : (per course)(for a customer) [employeer (client admin) dashboard]




class ProgressCountView(APIView):

    """
    API endpoint to get the count of users in different progress states for each registered course.
    """
    permission_classes = [ClientAdminPermission]
    def get(self, request):
        try:
            user= request.data.get('user')
            # Fetch all active courses
            active_course_ids = CourseCompletionStatusPerUser.objects.filter(
                enrolled_user__customer__id=user['customer'], active=True
            ).values_list('course_id', flat=True).distinct()
            # Fetch details of active courses
            active_courses = Course.objects.filter(id__in=active_course_ids)
            progress_data = []
            # # Iterate over each active course
            for course in active_courses:
                # Fetch course title
                course_title = course.title
                status_record = CourseCompletionStatusPerUser.objects.filter(course=course, active=True, enrolled_user__customer__id=user['customer'])
                
                # Check if the course is active in CourseCompletionStatusPerUser
                if status_record is None:
                    # Skip counting progress for this course if status is inactive
                    return Response({'error':'no course completion status found'},status=status.HTTP_404_NOT_FOUND)
                # Count the number of users in different progress states for each course
                completion_count = CourseCompletionStatusPerUser.objects.filter(
                    course=course, status="completed", active=True, enrolled_user__customer__id=user['customer']
                ).count()
                in_progress_count = CourseCompletionStatusPerUser.objects.filter(
                    course=course, status="in_progress", active=True, enrolled_user__customer__id=user['customer']
                ).count()
                not_started_count = CourseCompletionStatusPerUser.objects.filter(
                    course=course, status="not_started", active=True, enrolled_user__customer__id=user['customer']
                ).count()
                # Append course progress data to the progress_data list
                progress_data.append({
                    'course_title': course_title,
                    'completion_count': completion_count,
                    'in_progress_count': in_progress_count,
                    'not_started_count': not_started_count,
                })
                serializer = ProgressDataSerializer(progress_data, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#---------

